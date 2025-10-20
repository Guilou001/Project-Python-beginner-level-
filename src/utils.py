"""
Utility Functions Module
=========================

This module provides helper functions for the ML trading strategy.

Functions:
---------
- set_random_seed: Set random seeds for reproducibility
- save_results: Save backtest results to disk
- load_results: Load backtest results from disk
- save_metrics: Save performance metrics to JSON
- load_metrics: Load performance metrics from JSON
- print_metrics_summary: Print formatted metrics summary
- calculate_correlation_matrix: Calculate feature correlation matrix
- detect_outliers: Detect outliers in data
"""

import numpy as np
import pandas as pd
import json
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def set_random_seed(seed=42):
    """
    Set random seeds for reproducibility.

    Parameters:
    -----------
    seed : int
        Random seed
    """
    np.random.seed(seed)
    import random
    random.seed(seed)

    try:
        import tensorflow as tf
        tf.random.set_seed(seed)
    except ImportError:
        pass

    logger.info(f"Random seed set to {seed}")


def save_results(results_df, filepath):
    """
    Save backtest results to CSV.

    Parameters:
    -----------
    results_df : pd.DataFrame
        Results DataFrame
    filepath : str
        Path to save file
    """
    results_df.to_csv(filepath, index=False)
    logger.info(f"Results saved to {filepath}")


def load_results(filepath):
    """
    Load backtest results from CSV.

    Parameters:
    -----------
    filepath : str
        Path to file

    Returns:
    --------
    pd.DataFrame
        Results DataFrame
    """
    if not os.path.exists(filepath):
        logger.error(f"File not found: {filepath}")
        return None

    results_df = pd.read_csv(filepath)
    results_df['date'] = pd.to_datetime(results_df['date'])
    logger.info(f"Results loaded from {filepath}")

    return results_df


def save_metrics(metrics_dict, filepath):
    """
    Save performance metrics to JSON.

    Parameters:
    -----------
    metrics_dict : dict
        Metrics dictionary
    filepath : str
        Path to save file
    """
    # Convert numpy types to Python types for JSON serialization
    def convert_to_serializable(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.Series):
            return obj.to_dict()
        elif isinstance(obj, pd.DataFrame):
            return obj.to_dict()
        else:
            return obj

    serializable_metrics = {k: convert_to_serializable(v) for k, v in metrics_dict.items()}

    with open(filepath, 'w') as f:
        json.dump(serializable_metrics, f, indent=4)

    logger.info(f"Metrics saved to {filepath}")


def load_metrics(filepath):
    """
    Load performance metrics from JSON.

    Parameters:
    -----------
    filepath : str
        Path to file

    Returns:
    --------
    dict
        Metrics dictionary
    """
    if not os.path.exists(filepath):
        logger.error(f"File not found: {filepath}")
        return None

    with open(filepath, 'r') as f:
        metrics = json.load(f)

    logger.info(f"Metrics loaded from {filepath}")

    return metrics


def print_metrics_summary(metrics):
    """
    Print formatted metrics summary.

    Parameters:
    -----------
    metrics : dict
        Metrics dictionary
    """
    print("\n" + "="*70)
    print("PERFORMANCE METRICS SUMMARY".center(70))
    print("="*70)

    # Returns
    print("\nRETURNS:")
    print(f"  Total Return:           {metrics.get('total_return', 0):.2%}")
    print(f"  Annualized Return:      {metrics.get('annualized_return', 0):.2%}")

    # Risk
    print("\nRISK:")
    print(f"  Annualized Volatility:  {metrics.get('annualized_volatility', 0):.2%}")
    print(f"  Maximum Drawdown:       {metrics.get('max_drawdown', 0):.2%}")

    # Risk-adjusted returns
    print("\nRISK-ADJUSTED RETURNS:")
    print(f"  Sharpe Ratio:           {metrics.get('sharpe_ratio', 0):.4f}")
    print(f"  Sortino Ratio:          {metrics.get('sortino_ratio', 0):.4f}")
    print(f"  Calmar Ratio:           {metrics.get('calmar_ratio', 0):.4f}")

    # Trading statistics
    print("\nTRADING STATISTICS:")
    print(f"  Win Rate:               {metrics.get('win_rate', 0):.2%}")
    print(f"  Profit Factor:          {metrics.get('profit_factor', 0):.4f}")
    print(f"  Average Win:            {metrics.get('avg_win', 0):.4%}")
    print(f"  Average Loss:           {metrics.get('avg_loss', 0):.4%}")

    # Benchmark comparison (if available)
    if 'benchmark_annual_return' in metrics:
        print("\nBENCHMARK COMPARISON:")
        print(f"  Benchmark Return:       {metrics.get('benchmark_annual_return', 0):.2%}")
        print(f"  Excess Return:          {metrics.get('excess_return', 0):.2%}")
        print(f"  Benchmark Sharpe:       {metrics.get('benchmark_sharpe', 0):.4f}")

    # Model performance (if available)
    if 'accuracy' in metrics:
        print("\nMODEL PERFORMANCE:")
        print(f"  Accuracy:               {metrics.get('accuracy', 0):.2%}")
        print(f"  Precision:              {metrics.get('precision', 0):.2%}")
        print(f"  Recall:                 {metrics.get('recall', 0):.2%}")
        print(f"  F1 Score:               {metrics.get('f1_score', 0):.2%}")
        print(f"  AUC:                    {metrics.get('auc', 0):.4f}")

    print("\n" + "="*70 + "\n")


def calculate_correlation_matrix(features_df, method='pearson'):
    """
    Calculate correlation matrix for features.

    Parameters:
    -----------
    features_df : pd.DataFrame
        Features DataFrame
    method : str
        Correlation method ('pearson', 'spearman', 'kendall')

    Returns:
    --------
    pd.DataFrame
        Correlation matrix
    """
    logger.info(f"Calculating {method} correlation matrix...")
    corr_matrix = features_df.corr(method=method)

    return corr_matrix


def detect_outliers(data, column, method='iqr', threshold=1.5):
    """
    Detect outliers in data.

    Parameters:
    -----------
    data : pd.DataFrame
        Data
    column : str
        Column name
    method : str
        Method for outlier detection ('iqr', 'zscore')
    threshold : float
        Threshold for outlier detection

    Returns:
    --------
    pd.DataFrame
        Outliers
    """
    if method == 'iqr':
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR

        outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]

    elif method == 'zscore':
        from scipy import stats
        z_scores = np.abs(stats.zscore(data[column]))
        outliers = data[z_scores > threshold]

    else:
        logger.error(f"Unknown outlier detection method: {method}")
        return None

    logger.info(f"Detected {len(outliers)} outliers in {column} using {method} method")

    return outliers


def create_date_features(df, date_column='date'):
    """
    Create date-based features.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with date column
    date_column : str
        Name of date column

    Returns:
    --------
    pd.DataFrame
        DataFrame with additional date features
    """
    df = df.copy()

    # Ensure date column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column])

    # Extract features
    df['year'] = df[date_column].dt.year
    df['month'] = df[date_column].dt.month
    df['day'] = df[date_column].dt.day
    df['day_of_week'] = df[date_column].dt.dayofweek
    df['quarter'] = df[date_column].dt.quarter
    df['week_of_year'] = df[date_column].dt.isocalendar().week

    return df


def align_dataframes(*dfs, join='inner'):
    """
    Align multiple DataFrames by index.

    Parameters:
    -----------
    *dfs : pd.DataFrame
        DataFrames to align
    join : str
        Join type ('inner', 'outer', 'left', 'right')

    Returns:
    --------
    list
        List of aligned DataFrames
    """
    if len(dfs) == 0:
        return []

    # Find common index
    if join == 'inner':
        common_index = dfs[0].index
        for df in dfs[1:]:
            common_index = common_index.intersection(df.index)
    elif join == 'outer':
        common_index = dfs[0].index
        for df in dfs[1:]:
            common_index = common_index.union(df.index)
    else:
        logger.error(f"Unsupported join type: {join}")
        return dfs

    # Align DataFrames
    aligned_dfs = [df.loc[common_index.intersection(df.index)] for df in dfs]

    logger.info(f"Aligned {len(dfs)} DataFrames with {len(common_index)} common dates")

    return aligned_dfs


def get_project_summary():
    """
    Get project summary information.

    Returns:
    --------
    str
        Formatted project summary
    """
    summary = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║         ML TRADING STRATEGY FOR S&P 500 PREDICTION           ║
    ╚═══════════════════════════════════════════════════════════════╝

    PROJECT OVERVIEW:
    -----------------
    This project implements a state-of-the-art machine learning trading
    strategy using LSTM neural networks to predict S&P 500 direction and
    optimize portfolio allocation across sector ETFs.

    KEY FEATURES:
    ------------
    • LSTM-based directional prediction
    • GARCH volatility modeling
    • Technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands, ATR)
    • Portfolio optimization (Markowitz, Min Variance, Risk Parity)
    • Comprehensive backtesting with transaction costs
    • Risk management and drawdown analysis
    • Interactive visualizations

    METHODOLOGY:
    -----------
    1. Data Collection: Historical S&P 500, VIX, and sector ETF data
    2. Feature Engineering: Technical indicators + GARCH volatility
    3. Model Training: Bidirectional LSTM with dropout regularization
    4. Portfolio Optimization: Mean-variance optimization
    5. Backtesting: Walk-forward validation with strict out-of-sample test
    6. Performance Analysis: Sharpe, Sortino, Calmar, Max Drawdown

    """
    return summary


if __name__ == "__main__":
    print(get_project_summary())
