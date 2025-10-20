"""
Main Execution Script
=====================

This script orchestrates the entire ML trading strategy pipeline:
1. Download and prepare data
2. Engineer features
3. Train LSTM model
4. Run backtest
5. Generate visualizations
6. Save results

Usage:
------
python main.py [--skip-download] [--skip-training] [--skip-backtest]

Flags:
------
--skip-download : Skip data download (use existing data)
--skip-training : Skip model training (use existing model)
--skip-backtest : Skip backtesting (only train model)
"""

import os
import sys
import argparse
import logging
import pandas as pd
import numpy as np
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import project modules
import config
from src.data_sourcing import DataDownloader, merge_market_data
from src.feature_engineering import FeatureEngineer
from src.model import LSTMModel
from src.portfolio_optimization import PortfolioOptimizer
from src.backtesting import Backtester
from src.plotting import StrategyVisualizer
from src.utils import (
    set_random_seed, save_results, save_metrics,
    print_metrics_summary, get_project_summary
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_strategy.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='ML Trading Strategy for S&P 500')

    parser.add_argument('--skip-download', action='store_true',
                       help='Skip data download (use existing data)')
    parser.add_argument('--skip-training', action='store_true',
                       help='Skip model training (use existing model)')
    parser.add_argument('--skip-backtest', action='store_true',
                       help='Skip backtesting (only train model)')

    return parser.parse_args()


def step_1_download_data(downloader):
    """Step 1: Download market data."""
    logger.info("\n" + "="*70)
    logger.info("STEP 1: DOWNLOADING MARKET DATA")
    logger.info("="*70 + "\n")

    # Download all data
    data = downloader.download_all(
        sp500_ticker=config.SP500_TICKER,
        vix_ticker=config.VIX_TICKER,
        sector_tickers=config.SECTOR_TICKERS
    )

    # Merge S&P 500 and VIX
    if data['sp500'] is not None and data['vix'] is not None:
        merged_data = merge_market_data(data['sp500'], data['vix'])
        downloader.save_data(merged_data, "market_data.parquet")
    else:
        logger.error("Failed to download required data")
        sys.exit(1)

    logger.info("Step 1 completed successfully!\n")
    return data


def step_2_engineer_features(downloader):
    """Step 2: Engineer features."""
    logger.info("\n" + "="*70)
    logger.info("STEP 2: FEATURE ENGINEERING")
    logger.info("="*70 + "\n")

    # Load market data
    market_data = downloader.load_data("market_data.parquet")

    if market_data is None:
        logger.error("Market data not found. Please run with data download first.")
        sys.exit(1)

    # Create features
    fe = FeatureEngineer(market_data)
    features_df = fe.create_all_features(config)

    # Save features
    downloader.save_data(features_df, "features.parquet")

    logger.info("Step 2 completed successfully!\n")
    return features_df, fe.get_feature_names()


def step_3_train_model(features_df, feature_names):
    """Step 3: Train LSTM model."""
    logger.info("\n" + "="*70)
    logger.info("STEP 3: TRAINING LSTM MODEL")
    logger.info("="*70 + "\n")

    # Initialize model
    lstm_model = LSTMModel(config)

    # Prepare data
    data = lstm_model.prepare_data(features_df, feature_names)

    # Build and train model
    logger.info("Building model architecture...")
    lstm_model.build_model(input_shape=(config.SEQUENCE_LENGTH, len(feature_names)))

    logger.info("Training model...")
    history = lstm_model.train(data)

    # Evaluate on test set
    logger.info("Evaluating model...")
    metrics = lstm_model.evaluate(data['X_test'], data['y_test'])

    # Save model
    lstm_model.save_model()

    logger.info("Step 3 completed successfully!\n")
    return lstm_model, data, metrics, history


def step_4_run_backtest(lstm_model, features_df, feature_names, downloader):
    """Step 4: Run backtest."""
    logger.info("\n" + "="*70)
    logger.info("STEP 4: RUNNING BACKTEST")
    logger.info("="*70 + "\n")

    # Prepare data for prediction
    data = lstm_model.prepare_data(features_df, feature_names)

    # Get test data
    X_test = data['X_test']
    y_test = data['y_test']

    # Make predictions on test set
    y_pred, y_proba = lstm_model.predict(X_test)

    # Calculate test start index (accounting for sequence length)
    test_start_idx = int(len(features_df) * (config.TRAIN_RATIO + config.VALIDATION_RATIO)) + config.SEQUENCE_LENGTH

    # Create predictions DataFrame
    test_dates = features_df.index[test_start_idx:test_start_idx + len(y_test)]

    predictions_df = pd.DataFrame({
        'date': test_dates,
        'actual': y_test,
        'prediction': y_pred,
        'probability': y_proba
    })

    # Load sector ETF data
    sector_data = downloader.load_data("sectors_raw.parquet")

    if sector_data is None:
        logger.error("Sector data not found")
        sys.exit(1)

    # Align sector data with test period
    sector_data_aligned = sector_data.loc[test_dates[0]:test_dates[-1]]

    # Initialize portfolio optimizer and backtester
    portfolio_optimizer = PortfolioOptimizer(config)
    backtester = Backtester(config)

    # Run backtest
    results_df = backtester.run_backtest(
        predictions_df,
        sector_data_aligned,
        portfolio_optimizer
    )

    # Calculate benchmark returns (S&P 500 buy and hold)
    sp500_data = downloader.load_data("market_data.parquet")
    sp500_test = sp500_data.loc[test_dates[0]:test_dates[-1], 'close']
    benchmark_returns = sp500_test.pct_change().dropna()

    # Align strategy returns with benchmark
    strategy_returns = pd.Series(
        results_df['daily_return'].values[1:],
        index=results_df['date'].values[1:]
    )

    # Calculate metrics
    backtest_metrics = backtester.calculate_metrics(
        results_df=results_df,
        benchmark_returns=benchmark_returns
    )

    # Save results
    save_results(results_df, config.RESULTS_CSV_PATH)

    # Combine model and backtest metrics
    all_metrics = {**backtest_metrics}

    save_metrics(all_metrics, config.METRICS_JSON_PATH)

    logger.info("Step 4 completed successfully!\n")
    return results_df, predictions_df, all_metrics, backtester.weights_history, benchmark_returns


def step_5_generate_visualizations(results_df, predictions_df, weights_history,
                                   benchmark_returns, history):
    """Step 5: Generate visualizations."""
    logger.info("\n" + "="*70)
    logger.info("STEP 5: GENERATING VISUALIZATIONS")
    logger.info("="*70 + "\n")

    visualizer = StrategyVisualizer(config)

    # 1. Cumulative returns
    strategy_returns = pd.Series(
        results_df['daily_return'].values,
        index=results_df['date'].values
    )

    visualizer.plot_cumulative_returns(
        strategy_returns,
        benchmark_returns,
        save_path=config.CUMULATIVE_RETURNS_PLOT
    )

    # 2. Predictions vs actual
    visualizer.plot_predictions(
        predictions_df['date'].values,
        predictions_df['actual'].values,
        predictions_df['prediction'].values,
        predictions_df['probability'].values,
        save_path=config.PREDICTIONS_PLOT
    )

    # 3. Portfolio allocation
    visualizer.plot_portfolio_allocation(
        weights_history,
        save_path=config.ALLOCATION_PLOT
    )

    # 4. Confusion matrix
    visualizer.plot_confusion_matrix(
        predictions_df['actual'].values,
        predictions_df['prediction'].values,
        save_path=config.CONFUSION_MATRIX_PLOT
    )

    # 5. Drawdown chart
    visualizer.plot_drawdown(
        strategy_returns,
        save_path=config.DRAWDOWN_PLOT
    )

    # 6. Training history
    visualizer.plot_training_history(
        history,
        save_path=os.path.join(config.RESULTS_DIR, "training_history.png")
    )

    # 7. Interactive dashboard
    visualizer.create_interactive_dashboard(
        results_df,
        save_path=os.path.join(config.RESULTS_DIR, "dashboard.html")
    )

    logger.info("Step 5 completed successfully!\n")


def main():
    """Main execution function."""
    # Print project summary
    print(get_project_summary())

    # Parse arguments
    args = parse_arguments()

    # Set random seed for reproducibility
    set_random_seed(config.RANDOM_SEED)

    # Initialize data downloader
    downloader = DataDownloader(config.START_DATE, config.END_DATE, config.DATA_DIR)

    try:
        # Step 1: Download data
        if not args.skip_download:
            step_1_download_data(downloader)
        else:
            logger.info("Skipping data download (using existing data)")

        # Step 2: Feature engineering
        features_df, feature_names = step_2_engineer_features(downloader)

        # Step 3: Train model
        if not args.skip_training:
            lstm_model, model_data, model_metrics, history = step_3_train_model(
                features_df, feature_names
            )
        else:
            logger.info("Skipping model training (loading existing model)")
            lstm_model = LSTMModel(config)
            lstm_model.load_model()

            # Still need to get feature names
            if not feature_names:
                import joblib
                feature_names = joblib.load(config.FEATURE_NAMES_PATH)

            history = None

        # Step 4: Run backtest
        if not args.skip_backtest:
            results_df, predictions_df, metrics, weights_history, benchmark_returns = step_4_run_backtest(
                lstm_model, features_df, feature_names, downloader
            )

            # Step 5: Generate visualizations
            step_5_generate_visualizations(
                results_df, predictions_df, weights_history,
                benchmark_returns, history
            )

            # Print final summary
            print_metrics_summary(metrics)

        # Final message
        logger.info("\n" + "="*70)
        logger.info("PIPELINE COMPLETED SUCCESSFULLY!")
        logger.info("="*70)
        logger.info(f"\nResults saved to: {config.RESULTS_DIR}")
        logger.info(f"Model saved to: {config.MODELS_DIR}")
        logger.info(f"Data saved to: {config.DATA_DIR}\n")

    except Exception as e:
        logger.error(f"\n{'='*70}")
        logger.error(f"ERROR: {str(e)}")
        logger.error(f"{'='*70}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
