"""
Configuration file for the ML Trading Strategy project.
Contains all hyperparameters, paths, and settings.
"""

import os
from datetime import datetime

# ================== PATHS ==================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# ================== DATA SOURCING ==================
# Tickers to download
SP500_TICKER = "^GSPC"
VIX_TICKER = "^VIX"
RISK_FREE_RATE_TICKER = "^IRX"  # 13-week Treasury Bill

# Date range for historical data
START_DATE = "2014-01-01"
END_DATE = datetime.now().strftime("%Y-%m-%d")

# Additional tickers for portfolio optimization (S&P 500 sectors)
SECTOR_TICKERS = [
    "XLK",  # Technology
    "XLF",  # Financials
    "XLV",  # Healthcare
    "XLE",  # Energy
    "XLI",  # Industrials
    "XLY",  # Consumer Discretionary
    "XLP",  # Consumer Staples
    "XLU",  # Utilities
    "XLRE", # Real Estate
    "XLB",  # Materials
    "XLC",  # Communication Services
]

# ================== FEATURE ENGINEERING ==================
# Technical indicators parameters
SMA_PERIODS = [5, 10, 20, 50, 200]
EMA_PERIODS = [12, 26, 50]
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BBANDS_PERIOD = 20
BBANDS_STD = 2
ATR_PERIOD = 14

# GARCH model parameters
GARCH_P = 1  # Order of GARCH component
GARCH_Q = 1  # Order of ARCH component
GARCH_FORECAST_HORIZON = 1  # Days ahead

# Feature lags
RETURN_LAGS = [1, 2, 3, 5, 10, 20]
VOLUME_LAGS = [1, 5, 10]

# ================== MODEL ARCHITECTURE ==================
# LSTM hyperparameters
SEQUENCE_LENGTH = 60  # Number of time steps to look back
LSTM_UNITS_1 = 128
LSTM_UNITS_2 = 64
DROPOUT_RATE = 0.3
LEARNING_RATE = 0.001
BATCH_SIZE = 32
EPOCHS = 100
EARLY_STOPPING_PATIENCE = 15
VALIDATION_SPLIT = 0.15

# Model architecture
USE_BIDIRECTIONAL = True
ACTIVATION = "tanh"
OPTIMIZER = "adam"
LOSS = "binary_crossentropy"
METRICS = ["accuracy", "Precision", "Recall", "AUC"]

# ================== DATA SPLIT ==================
# Train/Validation/Test split (chronological)
TRAIN_RATIO = 0.70
VALIDATION_RATIO = 0.15
TEST_RATIO = 0.15  # Out-of-sample

# ================== PORTFOLIO OPTIMIZATION ==================
# Optimization method
OPTIMIZATION_METHOD = "mean_variance"  # Options: "mean_variance", "min_variance", "hrp"

# Constraints for portfolio optimization
MIN_WEIGHT = 0.0  # Minimum weight per asset (0 = no shorting)
MAX_WEIGHT = 0.30  # Maximum weight per asset (prevent over-concentration)
RISK_FREE_RATE = 0.02  # Annual risk-free rate (2%)

# Portfolio rebalancing
REBALANCING_FREQUENCY = 20  # Rebalance every N trading days (monthly ~20 days)

# Expected return estimation method
RETURN_ESTIMATION_WINDOW = 252  # Days for historical return estimation (1 year)
COVARIANCE_ESTIMATION_WINDOW = 252  # Days for covariance matrix estimation

# ================== BACKTESTING ==================
# Initial capital
INITIAL_CAPITAL = 100000.0

# Transaction costs
TRANSACTION_COST = 0.001  # 0.1% per trade

# Position sizing
CASH_ALLOCATION_WHEN_BEARISH = 1.0  # 100% cash when prediction is down
MAX_POSITION_SIZE = 0.95  # Maximum % of capital to invest

# ================== PERFORMANCE METRICS ==================
# Risk-free rate for Sharpe/Sortino calculation
ANNUAL_RISK_FREE_RATE = 0.02

# Trading days per year
TRADING_DAYS_PER_YEAR = 252

# ================== PLOTTING ==================
# Plot settings
PLOT_STYLE = "seaborn-v0_8-darkgrid"
FIGURE_SIZE = (14, 8)
DPI = 100
COLOR_PALETTE = "husl"

# Save formats
SAVE_PLOTS = True
PLOT_FORMAT = "png"  # Options: "png", "jpg", "svg", "pdf"

# ================== RANDOM SEED ==================
# For reproducibility
RANDOM_SEED = 42

# ================== VERBOSE ==================
# Logging and output verbosity
VERBOSE = 1  # 0: Silent, 1: Progress bars, 2: Detailed output

# TensorFlow logging
TF_LOG_LEVEL = "2"  # 0: All, 1: INFO, 2: WARNING, 3: ERROR

# ================== MODEL SAVING ==================
MODEL_NAME = "lstm_sp500_predictor"
MODEL_PATH = os.path.join(MODELS_DIR, f"{MODEL_NAME}.keras")
SCALER_PATH = os.path.join(MODELS_DIR, "feature_scaler.pkl")
FEATURE_NAMES_PATH = os.path.join(MODELS_DIR, "feature_names.pkl")

# ================== RESULTS SAVING ==================
RESULTS_CSV_PATH = os.path.join(RESULTS_DIR, "backtest_results.csv")
METRICS_JSON_PATH = os.path.join(RESULTS_DIR, "performance_metrics.json")
PREDICTIONS_CSV_PATH = os.path.join(RESULTS_DIR, "predictions.csv")

# Plot paths
CUMULATIVE_RETURNS_PLOT = os.path.join(RESULTS_DIR, "cumulative_returns.png")
PREDICTIONS_PLOT = os.path.join(RESULTS_DIR, "predictions_vs_actual.png")
ALLOCATION_PLOT = os.path.join(RESULTS_DIR, "portfolio_allocation.png")
CONFUSION_MATRIX_PLOT = os.path.join(RESULTS_DIR, "confusion_matrix.png")
DRAWDOWN_PLOT = os.path.join(RESULTS_DIR, "drawdown_chart.png")
FEATURE_IMPORTANCE_PLOT = os.path.join(RESULTS_DIR, "feature_importance.png")
