"""
Backtesting Module
==================

This module implements a backtesting engine for the ML trading strategy.

Strategy:
--------
1. Use LSTM model to predict S&P 500 direction (up/down)
2. If prediction = UP: Allocate capital to optimized portfolio of sector ETFs
3. If prediction = DOWN: Hold cash

Metrics:
--------
- Total return
- Annualized return
- Annualized volatility
- Sharpe ratio
- Sortino ratio
- Maximum drawdown
- Calmar ratio
- Win rate

Functions:
---------
- run_backtest: Execute backtest
- calculate_metrics: Calculate performance metrics
- generate_trades: Generate trade signals
"""

import numpy as np
import pandas as pd
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Backtester:
    """
    Backtesting engine for ML trading strategy.
    """

    def __init__(self, config):
        """
        Initialize Backtester.

        Parameters:
        -----------
        config : module
            Configuration module
        """
        self.config = config
        self.initial_capital = config.INITIAL_CAPITAL
        self.transaction_cost = config.TRANSACTION_COST
        self.results = None

    def calculate_returns(self, prices_df):
        """
        Calculate returns from prices.

        Parameters:
        -----------
        prices_df : pd.DataFrame
            Price data

        Returns:
        --------
        pd.DataFrame
            Returns
        """
        return prices_df.pct_change()

    def calculate_portfolio_return(self, returns_df, weights, date):
        """
        Calculate portfolio return for a given date and weights.

        Parameters:
        -----------
        returns_df : pd.DataFrame
            Returns data
        weights : pd.Series
            Portfolio weights
        date : datetime
            Date for return calculation

        Returns:
        --------
        float
            Portfolio return
        """
        if date not in returns_df.index:
            return 0.0

        # Get returns for the date
        daily_returns = returns_df.loc[date]

        # Calculate weighted return
        portfolio_return = np.dot(weights.values, daily_returns.values)

        return portfolio_return

    def calculate_transaction_costs(self, old_weights, new_weights, portfolio_value):
        """
        Calculate transaction costs from portfolio rebalancing.

        Parameters:
        -----------
        old_weights : pd.Series
            Old portfolio weights
        new_weights : pd.Series
            New portfolio weights
        portfolio_value : float
            Current portfolio value

        Returns:
        --------
        float
            Transaction cost
        """
        # Calculate turnover (sum of absolute weight changes)
        turnover = np.sum(np.abs(new_weights.values - old_weights.values))

        # Transaction cost = turnover * cost_rate * portfolio_value
        cost = turnover * self.transaction_cost * portfolio_value

        return cost

    def run_backtest(self, predictions_df, sector_prices_df, portfolio_optimizer):
        """
        Run backtest with ML predictions and portfolio optimization.

        Parameters:
        -----------
        predictions_df : pd.DataFrame
            DataFrame with columns: ['date', 'prediction', 'probability']
        sector_prices_df : pd.DataFrame
            Sector ETF prices
        portfolio_optimizer : PortfolioOptimizer
            Portfolio optimizer instance

        Returns:
        --------
        pd.DataFrame
            Backtest results
        """
        logger.info("Running backtest...")
        logger.info(f"Initial capital: ${self.initial_capital:,.2f}")
        logger.info(f"Transaction cost: {self.transaction_cost:.2%}")

        # Calculate returns
        sector_returns = self.calculate_returns(sector_prices_df)

        # Initialize results tracking
        dates = predictions_df['date'].values
        portfolio_values = [self.initial_capital]
        cash_positions = []
        positions = []
        daily_returns = []
        weights_history = []

        # Initial state
        current_value = self.initial_capital
        current_weights = pd.Series(0, index=sector_prices_df.columns)
        in_market = False

        # Rebalancing counter
        days_since_rebalance = 0

        for i, date in enumerate(dates[:-1]):  # Exclude last date (no next day)
            # Get prediction for today
            prediction = predictions_df.loc[predictions_df['date'] == date, 'prediction'].values[0]

            # Determine if we should be in market
            should_be_in_market = (prediction == 1)

            # Check if we need to rebalance
            need_rebalance = (
                days_since_rebalance >= self.config.REBALANCING_FREQUENCY or
                (should_be_in_market != in_market)
            )

            if need_rebalance:
                # Get new weights
                if should_be_in_market:
                    # Optimize portfolio
                    # Use historical data up to current date
                    historical_returns = sector_returns.loc[:date].iloc[-self.config.COVARIANCE_ESTIMATION_WINDOW:]

                    try:
                        opt_result = portfolio_optimizer.optimize_portfolio(
                            historical_returns,
                            method=self.config.OPTIMIZATION_METHOD
                        )
                        new_weights = opt_result['weights']
                    except Exception as e:
                        logger.warning(f"Portfolio optimization failed on {date}: {str(e)}. Using equal weights.")
                        new_weights = pd.Series(
                            1.0 / len(sector_prices_df.columns),
                            index=sector_prices_df.columns
                        )

                    # Apply max position size constraint
                    new_weights = new_weights * self.config.MAX_POSITION_SIZE
                else:
                    # Go to cash
                    new_weights = pd.Series(0, index=sector_prices_df.columns)

                # Calculate transaction costs
                transaction_cost = self.calculate_transaction_costs(
                    current_weights, new_weights, current_value
                )

                # Deduct transaction costs
                current_value -= transaction_cost

                # Update weights
                current_weights = new_weights
                in_market = should_be_in_market
                days_since_rebalance = 0
            else:
                days_since_rebalance += 1

            # Calculate next day's return
            next_date = dates[i + 1]

            if in_market:
                # Calculate portfolio return
                port_return = self.calculate_portfolio_return(
                    sector_returns, current_weights, next_date
                )
            else:
                # Cash return (assuming 0% for simplicity)
                port_return = 0.0

            # Update portfolio value
            current_value = current_value * (1 + port_return)

            # Record results
            portfolio_values.append(current_value)
            cash_positions.append(0 if in_market else 1)
            positions.append(1 if in_market else 0)
            daily_returns.append(port_return)
            weights_history.append(current_weights.copy())

        # Create results DataFrame
        results_df = pd.DataFrame({
            'date': dates,
            'portfolio_value': portfolio_values,
            'in_market': positions + [positions[-1]],  # Pad last value
            'cash_position': cash_positions + [cash_positions[-1]],
            'daily_return': [0] + daily_returns
        })

        results_df['cumulative_return'] = (results_df['portfolio_value'] / self.initial_capital - 1)

        # Store weights history
        weights_df = pd.DataFrame(weights_history, index=dates[:-1])
        weights_df['date'] = dates[:-1]

        self.results = results_df
        self.weights_history = weights_df

        logger.info(f"Backtest completed. Final portfolio value: ${current_value:,.2f}")

        return results_df

    def calculate_metrics(self, results_df=None, benchmark_returns=None):
        """
        Calculate performance metrics.

        Parameters:
        -----------
        results_df : pd.DataFrame
            Backtest results (uses self.results if None)
        benchmark_returns : pd.Series
            Benchmark returns for comparison

        Returns:
        --------
        dict
            Performance metrics
        """
        if results_df is None:
            results_df = self.results

        if results_df is None:
            logger.error("No backtest results available")
            return {}

        logger.info("Calculating performance metrics...")

        # Extract returns
        returns = results_df['daily_return'].values

        # Remove first return (always 0)
        returns = returns[1:]

        # Total return
        total_return = results_df['cumulative_return'].iloc[-1]

        # Number of trading days
        n_days = len(returns)
        n_years = n_days / self.config.TRADING_DAYS_PER_YEAR

        # Annualized return
        annualized_return = (1 + total_return) ** (1 / n_years) - 1

        # Annualized volatility
        annualized_volatility = np.std(returns) * np.sqrt(self.config.TRADING_DAYS_PER_YEAR)

        # Sharpe ratio
        excess_returns = returns - (self.config.ANNUAL_RISK_FREE_RATE / self.config.TRADING_DAYS_PER_YEAR)
        sharpe_ratio = np.mean(excess_returns) / np.std(returns) * np.sqrt(self.config.TRADING_DAYS_PER_YEAR)

        # Sortino ratio (using downside deviation)
        downside_returns = returns[returns < 0]
        downside_std = np.std(downside_returns) if len(downside_returns) > 0 else 0.0
        sortino_ratio = np.mean(excess_returns) / downside_std * np.sqrt(self.config.TRADING_DAYS_PER_YEAR) if downside_std > 0 else 0.0

        # Maximum drawdown
        cumulative = (1 + results_df['daily_return']).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()

        # Calmar ratio
        calmar_ratio = annualized_return / abs(max_drawdown) if max_drawdown != 0 else 0.0

        # Win rate
        winning_days = np.sum(returns > 0)
        win_rate = winning_days / len(returns)

        # Average win/loss
        avg_win = np.mean(returns[returns > 0]) if np.sum(returns > 0) > 0 else 0.0
        avg_loss = np.mean(returns[returns < 0]) if np.sum(returns < 0) > 0 else 0.0

        # Profit factor
        total_wins = np.sum(returns[returns > 0])
        total_losses = abs(np.sum(returns[returns < 0]))
        profit_factor = total_wins / total_losses if total_losses > 0 else 0.0

        metrics = {
            'total_return': total_return,
            'annualized_return': annualized_return,
            'annualized_volatility': annualized_volatility,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'max_drawdown': max_drawdown,
            'calmar_ratio': calmar_ratio,
            'win_rate': win_rate,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'total_trades': len(returns),
            'n_years': n_years
        }

        # Benchmark comparison
        if benchmark_returns is not None:
            benchmark_total_return = (1 + benchmark_returns).prod() - 1
            benchmark_annual_return = (1 + benchmark_total_return) ** (1 / n_years) - 1
            benchmark_volatility = benchmark_returns.std() * np.sqrt(self.config.TRADING_DAYS_PER_YEAR)
            benchmark_sharpe = (benchmark_annual_return - self.config.ANNUAL_RISK_FREE_RATE) / benchmark_volatility

            metrics['benchmark_total_return'] = benchmark_total_return
            metrics['benchmark_annual_return'] = benchmark_annual_return
            metrics['benchmark_volatility'] = benchmark_volatility
            metrics['benchmark_sharpe'] = benchmark_sharpe
            metrics['excess_return'] = annualized_return - benchmark_annual_return

        # Log metrics
        logger.info("\n" + "="*60)
        logger.info("PERFORMANCE METRICS")
        logger.info("="*60)
        logger.info(f"Total Return: {total_return:.2%}")
        logger.info(f"Annualized Return: {annualized_return:.2%}")
        logger.info(f"Annualized Volatility: {annualized_volatility:.2%}")
        logger.info(f"Sharpe Ratio: {sharpe_ratio:.4f}")
        logger.info(f"Sortino Ratio: {sortino_ratio:.4f}")
        logger.info(f"Maximum Drawdown: {max_drawdown:.2%}")
        logger.info(f"Calmar Ratio: {calmar_ratio:.4f}")
        logger.info(f"Win Rate: {win_rate:.2%}")
        logger.info(f"Profit Factor: {profit_factor:.4f}")

        if benchmark_returns is not None:
            logger.info("\n" + "-"*60)
            logger.info("BENCHMARK COMPARISON")
            logger.info("-"*60)
            logger.info(f"Benchmark Total Return: {metrics['benchmark_total_return']:.2%}")
            logger.info(f"Benchmark Annual Return: {metrics['benchmark_annual_return']:.2%}")
            logger.info(f"Excess Return: {metrics['excess_return']:.2%}")
            logger.info(f"Benchmark Sharpe: {metrics['benchmark_sharpe']:.4f}")

        logger.info("="*60 + "\n")

        return metrics


if __name__ == "__main__":
    # Example usage
    import sys
    sys.path.append('..')
    import config
    from src.portfolio_optimization import PortfolioOptimizer

    logger.info("Backtesting module loaded successfully")
