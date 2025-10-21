"""
Portfolio Optimization Module
==============================

This module implements portfolio optimization strategies for allocating capital
across S&P 500 sector ETFs.

Strategies:
----------
- Mean-Variance Optimization (Markowitz)
- Minimum Variance Portfolio
- Equal Weighting
- Risk Parity

Functions:
---------
- calculate_expected_returns: Estimate expected returns
- calculate_covariance_matrix: Estimate covariance matrix
- optimize_mean_variance: Mean-variance optimization
- optimize_min_variance: Minimum variance optimization
- equal_weight_portfolio: Equal weight allocation
- risk_parity_portfolio: Risk parity allocation
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PortfolioOptimizer:
    """
    Portfolio optimization class implementing various allocation strategies.
    """

    def __init__(self, config):
        """
        Initialize PortfolioOptimizer.

        Parameters:
        -----------
        config : module
            Configuration module
        """
        self.config = config
        self.min_weight = config.MIN_WEIGHT
        self.max_weight = config.MAX_WEIGHT
        self.risk_free_rate = config.RISK_FREE_RATE

    def calculate_expected_returns(self, returns_df, method='mean', window=None):
        """
        Calculate expected returns.

        Parameters:
        -----------
        returns_df : pd.DataFrame
            Historical returns
        method : str
            Method for calculating expected returns ('mean', 'ewma')
        window : int
            Window for return estimation (None = use all data)

        Returns:
        --------
        pd.Series
            Expected returns for each asset
        """
        if window is not None:
            returns_df = returns_df.iloc[-window:]

        if method == 'mean':
            expected_returns = returns_df.mean()
        elif method == 'ewma':
            expected_returns = returns_df.ewm(span=window if window else 60).mean().iloc[-1]
        else:
            expected_returns = returns_df.mean()

        # Annualize returns (assuming daily returns)
        expected_returns = expected_returns * self.config.TRADING_DAYS_PER_YEAR

        return expected_returns

    def calculate_covariance_matrix(self, returns_df, window=None):
        """
        Calculate covariance matrix.

        Parameters:
        -----------
        returns_df : pd.DataFrame
            Historical returns
        window : int
            Window for covariance estimation (None = use all data)

        Returns:
        --------
        pd.DataFrame
            Covariance matrix
        """
        if window is not None:
            returns_df = returns_df.iloc[-window:]

        # Calculate covariance matrix
        cov_matrix = returns_df.cov()

        # Annualize covariance (assuming daily returns)
        cov_matrix = cov_matrix * self.config.TRADING_DAYS_PER_YEAR

        return cov_matrix

    def portfolio_performance(self, weights, expected_returns, cov_matrix):
        """
        Calculate portfolio expected return, volatility, and Sharpe ratio.

        Parameters:
        -----------
        weights : np.array
            Portfolio weights
        expected_returns : pd.Series or np.array
            Expected returns
        cov_matrix : pd.DataFrame or np.array
            Covariance matrix

        Returns:
        --------
        tuple
            (expected_return, volatility, sharpe_ratio)
        """
        # Portfolio return
        portfolio_return = np.dot(weights, expected_returns)

        # Portfolio volatility
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

        # Sharpe ratio
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility

        return portfolio_return, portfolio_volatility, sharpe_ratio

    def optimize_mean_variance(self, expected_returns, cov_matrix, target_return=None):
        """
        Mean-Variance Optimization (Markowitz).

        Parameters:
        -----------
        expected_returns : pd.Series
            Expected returns
        cov_matrix : pd.DataFrame
            Covariance matrix
        target_return : float
            Target return (None = maximize Sharpe ratio)

        Returns:
        --------
        np.array
            Optimal portfolio weights
        """
        n_assets = len(expected_returns)

        # Objective function
        if target_return is None:
            # Maximize Sharpe ratio = minimize negative Sharpe ratio
            def objective(weights):
                _, _, sharpe = self.portfolio_performance(weights, expected_returns, cov_matrix)
                return -sharpe
        else:
            # Minimize variance for a target return
            def objective(weights):
                _, volatility, _ = self.portfolio_performance(weights, expected_returns, cov_matrix)
                return volatility

        # Constraints
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # Weights sum to 1
        ]

        if target_return is not None:
            constraints.append({
                'type': 'eq',
                'fun': lambda x: np.dot(x, expected_returns) - target_return
            })

        # Bounds for weights
        bounds = tuple((self.min_weight, self.max_weight) for _ in range(n_assets))

        # Initial guess (equal weights)
        initial_weights = np.array([1.0 / n_assets] * n_assets)

        # Optimize
        result = minimize(
            objective,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints,
            options={'maxiter': 1000}
        )

        if not result.success:
            logger.warning(f"Optimization did not converge: {result.message}")
            # Return equal weights as fallback
            return initial_weights

        # Normalize weights to sum to 1 (due to numerical precision)
        optimal_weights = result.x / np.sum(result.x)

        return optimal_weights

    def optimize_min_variance(self, cov_matrix):
        """
        Minimum Variance Portfolio optimization.

        Parameters:
        -----------
        cov_matrix : pd.DataFrame
            Covariance matrix

        Returns:
        --------
        np.array
            Optimal portfolio weights
        """
        n_assets = cov_matrix.shape[0]

        # Objective function: minimize portfolio variance
        def objective(weights):
            return np.dot(weights.T, np.dot(cov_matrix, weights))

        # Constraints: weights sum to 1
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        ]

        # Bounds for weights
        bounds = tuple((self.min_weight, self.max_weight) for _ in range(n_assets))

        # Initial guess (equal weights)
        initial_weights = np.array([1.0 / n_assets] * n_assets)

        # Optimize
        result = minimize(
            objective,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints,
            options={'maxiter': 1000}
        )

        if not result.success:
            logger.warning(f"Min variance optimization did not converge: {result.message}")
            return initial_weights

        # Normalize weights
        optimal_weights = result.x / np.sum(result.x)

        return optimal_weights

    def equal_weight_portfolio(self, n_assets):
        """
        Equal weight portfolio (1/N).

        Parameters:
        -----------
        n_assets : int
            Number of assets

        Returns:
        --------
        np.array
            Portfolio weights
        """
        return np.array([1.0 / n_assets] * n_assets)

    def risk_parity_portfolio(self, cov_matrix):
        """
        Risk Parity portfolio optimization.
        Each asset contributes equally to portfolio risk.

        Parameters:
        -----------
        cov_matrix : pd.DataFrame
            Covariance matrix

        Returns:
        --------
        np.array
            Optimal portfolio weights
        """
        n_assets = cov_matrix.shape[0]

        # Objective function: minimize difference in risk contributions
        def objective(weights):
            portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

            # Marginal contribution to risk
            marginal_contrib = np.dot(cov_matrix, weights) / portfolio_vol

            # Risk contribution
            risk_contrib = weights * marginal_contrib

            # Target risk contribution (equal for all assets)
            target_risk = portfolio_vol / n_assets

            # Sum of squared differences from target
            return np.sum((risk_contrib - target_risk) ** 2)

        # Constraints: weights sum to 1
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        ]

        # Bounds for weights
        bounds = tuple((self.min_weight, self.max_weight) for _ in range(n_assets))

        # Initial guess (equal weights)
        initial_weights = np.array([1.0 / n_assets] * n_assets)

        # Optimize
        result = minimize(
            objective,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints,
            options={'maxiter': 1000}
        )

        if not result.success:
            logger.warning(f"Risk parity optimization did not converge: {result.message}")
            return initial_weights

        # Normalize weights
        optimal_weights = result.x / np.sum(result.x)

        return optimal_weights

    def optimize_portfolio(self, returns_df, method='mean_variance', **kwargs):
        """
        Optimize portfolio using specified method.

        Parameters:
        -----------
        returns_df : pd.DataFrame
            Historical returns
        method : str
            Optimization method ('mean_variance', 'min_variance', 'equal_weight', 'risk_parity')
        **kwargs : dict
            Additional parameters for optimization

        Returns:
        --------
        dict
            Dictionary with weights and portfolio metrics
        """
        # Calculate expected returns and covariance
        window = kwargs.get('window', self.config.COVARIANCE_ESTIMATION_WINDOW)
        expected_returns = self.calculate_expected_returns(returns_df, window=window)
        cov_matrix = self.calculate_covariance_matrix(returns_df, window=window)

        # Optimize based on method
        if method == 'mean_variance':
            weights = self.optimize_mean_variance(expected_returns, cov_matrix)
        elif method == 'min_variance':
            weights = self.optimize_min_variance(cov_matrix)
        elif method == 'equal_weight':
            weights = self.equal_weight_portfolio(len(returns_df.columns))
        elif method == 'risk_parity':
            weights = self.risk_parity_portfolio(cov_matrix)
        else:
            logger.error(f"Unknown optimization method: {method}")
            weights = self.equal_weight_portfolio(len(returns_df.columns))

        # Calculate portfolio metrics
        port_return, port_vol, sharpe = self.portfolio_performance(
            weights, expected_returns, cov_matrix
        )

        # Create weights series with asset names
        weights_series = pd.Series(weights, index=returns_df.columns)

        logger.info(f"Portfolio Optimization ({method}):")
        logger.info(f"Expected Return: {port_return:.2%}")
        logger.info(f"Volatility: {port_vol:.2%}")
        logger.info(f"Sharpe Ratio: {sharpe:.4f}")
        logger.info(f"Weights:\n{weights_series}")

        return {
            'weights': weights_series,
            'expected_return': port_return,
            'volatility': port_vol,
            'sharpe_ratio': sharpe
        }


if __name__ == "__main__":
    # Example usage
    import sys
    sys.path.append('..')
    import config
    from src.data_sourcing import DataDownloader

    # Load sector ETF data
    downloader = DataDownloader(config.START_DATE, config.END_DATE, config.DATA_DIR)
    sector_data = downloader.load_data("sectors_raw.parquet")

    if sector_data is not None:
        # Calculate returns
        returns = sector_data.pct_change().dropna()

        # Initialize optimizer
        optimizer = PortfolioOptimizer(config)

        # Test different optimization methods
        methods = ['mean_variance', 'min_variance', 'equal_weight', 'risk_parity']

        for method in methods:
            print(f"\n{'='*60}")
            print(f"Method: {method.upper()}")
            print('='*60)

            result = optimizer.optimize_portfolio(returns, method=method)

            print(f"\nTop 5 Holdings:")
            print(result['weights'].nlargest(5))
