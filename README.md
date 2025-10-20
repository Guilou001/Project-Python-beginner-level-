# Machine Learning Trading Strategy for S&P 500 Prediction

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow 2.13+](https://img.shields.io/badge/TensorFlow-2.13+-orange.svg)](https://www.tensorflow.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive, state-of-the-art machine learning project that uses LSTM neural networks to predict S&P 500 market direction and optimize portfolio allocation across sector ETFs. The strategy combines deep learning, volatility modeling (GARCH), and modern portfolio theory to achieve superior risk-adjusted returns.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Project Architecture](#project-architecture)
- [Methodology](#methodology)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

## Overview

This project implements an end-to-end quantitative trading system that:

1. **Predicts** the direction of the S&P 500 index (up/down) using a bidirectional LSTM neural network
2. **Optimizes** portfolio allocation across S&P 500 sector ETFs using mean-variance optimization
3. **Manages risk** by switching to cash when market conditions are predicted to be bearish
4. **Evaluates** performance using comprehensive backtesting with realistic transaction costs

The project is designed to be:
- **Reproducible**: Fixed random seeds and detailed documentation
- **Modular**: Clean separation of concerns with reusable components
- **Educational**: Extensively commented code and clear methodology
- **Production-ready**: Robust error handling and logging

## Key Features

### Machine Learning
- **LSTM Architecture**: Bidirectional LSTM with dropout regularization to prevent overfitting
- **Advanced Features**: 60+ engineered features including:
  - Technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands, ATR)
  - GARCH(1,1) conditional volatility forecasts
  - VIX (fear index) and its derivatives
  - Temporal features with cyclical encoding
  - Lagged returns and volume features

### Portfolio Optimization
- **Mean-Variance Optimization** (Markowitz): Maximize Sharpe ratio
- **Minimum Variance Portfolio**: Minimize portfolio volatility
- **Risk Parity**: Equal risk contribution from each asset
- **Equal Weighting**: Baseline 1/N strategy

### Risk Management
- **Dynamic Allocation**: Adjust exposure based on ML predictions
- **Transaction Costs**: Realistic 0.1% cost per trade
- **Position Limits**: Maximum 30% per asset, 95% maximum equity exposure
- **Rebalancing**: Monthly portfolio rebalancing

### Backtesting & Evaluation
- **Walk-Forward Validation**: Strict chronological train/validation/test split (70/15/15)
- **Out-of-Sample Testing**: No data leakage, true predictive performance
- **Comprehensive Metrics**:
  - Returns: Total, annualized, cumulative
  - Risk: Volatility, maximum drawdown
  - Risk-adjusted: Sharpe, Sortino, Calmar ratios
  - Trading: Win rate, profit factor, average win/loss

### Visualizations
- Cumulative returns vs. buy-and-hold benchmark
- Prediction accuracy and confusion matrix
- Portfolio allocation over time
- Drawdown analysis
- Training history and model diagnostics
- Interactive Plotly dashboard

## Project Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA SOURCING                            │
│  (Yahoo Finance: S&P 500, VIX, Sector ETFs, 2014-2024)    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                 FEATURE ENGINEERING                         │
│  • Technical Indicators (SMA, EMA, RSI, MACD, BB, ATR)    │
│  • GARCH Volatility Modeling                               │
│  • Temporal Features (Day, Month, Cyclical Encoding)      │
│  • Lagged Features (Returns, Volume)                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   LSTM MODEL                                │
│  • Architecture: Bidirectional LSTM (128, 64 units)       │
│  • Input: 60-day sequences of 60+ features                │
│  • Output: Binary classification (Up/Down)                 │
│  • Training: Adam optimizer, early stopping                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              PORTFOLIO OPTIMIZATION                         │
│  • Mean-Variance Optimization (Markowitz)                  │
│  • Constraints: Long-only, max 30% per asset              │
│  • Rebalancing: Monthly or on signal change               │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKTESTING                              │
│  • Walk-forward validation                                 │
│  • Transaction costs (0.1% per trade)                     │
│  • Performance metrics calculation                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                 RESULTS & VISUALIZATION                     │
│  • Performance plots                                        │
│  • Interactive dashboards                                   │
│  • Metrics export (JSON, CSV)                             │
└─────────────────────────────────────────────────────────────┘
```

## Methodology

### 1. Data Collection

Historical data from **2014-2024** (10 years):
- **S&P 500 Index** (`^GSPC`): Main target for direction prediction
- **VIX** (`^VIX`): Volatility index for fear/greed sentiment
- **Sector ETFs**: 11 S&P 500 sector ETFs for portfolio diversification
  - Technology (XLK), Financials (XLF), Healthcare (XLV), Energy (XLE)
  - Industrials (XLI), Consumer Discretionary (XLY), Consumer Staples (XLP)
  - Utilities (XLU), Real Estate (XLRE), Materials (XLB), Communication (XLC)

### 2. Feature Engineering

**Technical Indicators:**
- Simple Moving Averages (5, 10, 20, 50, 200 days)
- Exponential Moving Averages (12, 26, 50 days)
- Relative Strength Index (RSI-14)
- MACD (12, 26, 9)
- Bollinger Bands (20-day, 2σ)
- Average True Range (ATR-14)

**Volatility Features:**
- Historical volatility (5, 10, 20, 60 days)
- GARCH(1,1) conditional volatility forecast
- VIX and its moving averages

**Temporal Features:**
- Day of week (cyclical encoding)
- Month (cyclical encoding)
- Quarter, year

**Lagged Features:**
- Returns with lags [1, 2, 3, 5, 10, 20] days
- Volume changes with lags [1, 5, 10] days

**Target Variable:**
- Binary: 1 if next day's S&P 500 return > 0, else 0

### 3. Model Architecture

**LSTM Neural Network:**
```
Input: (60 time steps, 60+ features)
    ↓
Bidirectional LSTM (128 units) + Dropout (30%)
    ↓
Bidirectional LSTM (64 units) + Dropout (30%)
    ↓
Dense (32 units, ReLU) + Dropout (20%)
    ↓
Dense (1 unit, Sigmoid) → Probability of up move
```

**Training Configuration:**
- Optimizer: Adam (learning rate = 0.001)
- Loss: Binary cross-entropy
- Metrics: Accuracy, Precision, Recall, AUC
- Early stopping: Patience = 15 epochs
- Batch size: 32
- Max epochs: 100

### 4. Portfolio Optimization

When the model predicts **UP** (bullish):
- Optimize portfolio allocation across 11 sector ETFs
- Method: Mean-Variance Optimization (maximize Sharpe ratio)
- Constraints:
  - Long-only (no shorting): weights ≥ 0
  - Diversification: max 30% per asset
  - Max exposure: 95% of capital

When the model predicts **DOWN** (bearish):
- Move to 100% cash
- Preserve capital during predicted downturns

### 5. Backtesting

**Data Split:**
- Training: 70% (2014-2020)
- Validation: 15% (2020-2022)
- Test (Out-of-Sample): 15% (2022-2024)

**Execution:**
- Start with $100,000 initial capital
- Transaction cost: 0.1% per trade
- Rebalance portfolio every 20 trading days (~monthly)
- Calculate daily returns and portfolio value

**Benchmark:**
- Buy-and-hold S&P 500 index for comparison

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) Virtual environment

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ml-sp500-trading-strategy.git
cd ml-sp500-trading-strategy
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python -c "import tensorflow as tf; print(f'TensorFlow version: {tf.__version__}')"
python -c "import yfinance; print('yfinance installed successfully')"
```

## Usage

### Quick Start

Run the complete pipeline with default settings:

```bash
python main.py
```

This will:
1. Download historical data (2014-2024)
2. Engineer 60+ features
3. Train the LSTM model
4. Run backtest on out-of-sample data
5. Generate visualizations and save results

### Command-Line Options

```bash
# Skip data download (use existing data)
python main.py --skip-download

# Skip model training (use existing model)
python main.py --skip-training

# Only train model, skip backtesting
python main.py --skip-backtest
```

### Running Individual Modules

**Data Download:**
```bash
python -m src.data_sourcing
```

**Feature Engineering:**
```bash
python -m src.feature_engineering
```

**Model Training:**
```bash
python -m src.model
```

**Portfolio Optimization:**
```bash
python -m src.portfolio_optimization
```

### Jupyter Notebooks

Explore the data and results interactively:

```bash
jupyter notebook notebooks/01_data_exploration.ipynb
```

## Results

### Performance Metrics (Example)

**Strategy Performance:**
- **Total Return**: 45.2%
- **Annualized Return**: 18.5%
- **Annualized Volatility**: 12.3%
- **Sharpe Ratio**: 1.42
- **Sortino Ratio**: 2.15
- **Maximum Drawdown**: -8.7%
- **Calmar Ratio**: 2.13
- **Win Rate**: 56.8%

**Benchmark (Buy & Hold S&P 500):**
- **Total Return**: 32.1%
- **Annualized Return**: 14.2%
- **Sharpe Ratio**: 0.98
- **Maximum Drawdown**: -15.3%

**Excess Returns**: +4.3% annualized

**Model Performance:**
- **Accuracy**: 58.3%
- **Precision**: 61.2%
- **Recall**: 55.7%
- **AUC**: 0.64

### Visualizations

All plots are automatically saved to the `results/` directory:

- `cumulative_returns.png`: Strategy vs. benchmark performance
- `predictions_vs_actual.png`: Model predictions visualization
- `portfolio_allocation.png`: Asset allocation over time
- `confusion_matrix.png`: Classification performance
- `drawdown_chart.png`: Drawdown analysis
- `training_history.png`: Model training metrics
- `dashboard.html`: Interactive Plotly dashboard

## Project Structure

```
ml-sp500-trading-strategy/
│
├── config.py                 # Configuration and hyperparameters
├── main.py                   # Main execution script
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .gitignore               # Git ignore file
│
├── src/                      # Source code modules
│   ├── __init__.py
│   ├── data_sourcing.py     # Data download and preparation
│   ├── feature_engineering.py # Feature creation and GARCH
│   ├── model.py             # LSTM model architecture
│   ├── portfolio_optimization.py # Portfolio allocation
│   ├── backtesting.py       # Backtesting engine
│   ├── plotting.py          # Visualization functions
│   └── utils.py             # Helper utilities
│
├── notebooks/               # Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   └── 02_model_evaluation.ipynb
│
├── data/                    # Data storage (gitignored)
│   ├── market_data.parquet
│   ├── features.parquet
│   └── sectors_raw.parquet
│
├── models/                  # Trained models (gitignored)
│   ├── lstm_sp500_predictor.keras
│   ├── feature_scaler.pkl
│   └── feature_names.pkl
│
└── results/                 # Output files (gitignored)
    ├── backtest_results.csv
    ├── performance_metrics.json
    ├── cumulative_returns.png
    ├── predictions_vs_actual.png
    ├── portfolio_allocation.png
    ├── confusion_matrix.png
    ├── drawdown_chart.png
    └── dashboard.html
```

## Configuration

All hyperparameters and settings are centralized in `config.py`:

**Data Configuration:**
- `START_DATE`: Start date for historical data
- `END_DATE`: End date for historical data
- `SECTOR_TICKERS`: List of sector ETF tickers

**Model Hyperparameters:**
- `SEQUENCE_LENGTH`: LSTM sequence length (default: 60)
- `LSTM_UNITS_1`: First LSTM layer units (default: 128)
- `LSTM_UNITS_2`: Second LSTM layer units (default: 64)
- `DROPOUT_RATE`: Dropout rate (default: 0.3)
- `LEARNING_RATE`: Adam learning rate (default: 0.001)
- `BATCH_SIZE`: Training batch size (default: 32)
- `EPOCHS`: Maximum training epochs (default: 100)

**Portfolio Settings:**
- `OPTIMIZATION_METHOD`: 'mean_variance', 'min_variance', 'risk_parity', 'equal_weight'
- `MIN_WEIGHT`: Minimum asset weight (default: 0.0)
- `MAX_WEIGHT`: Maximum asset weight (default: 0.30)
- `REBALANCING_FREQUENCY`: Days between rebalancing (default: 20)

**Backtesting:**
- `INITIAL_CAPITAL`: Starting capital (default: $100,000)
- `TRANSACTION_COST`: Cost per trade (default: 0.1%)
- `TRAIN_RATIO`: Training data ratio (default: 0.70)
- `VALIDATION_RATIO`: Validation data ratio (default: 0.15)
- `TEST_RATIO`: Test data ratio (default: 0.15)

Modify `config.py` to customize the strategy to your needs.

## Dependencies

**Core Libraries:**
- `numpy`, `pandas`, `scipy`: Data manipulation and scientific computing
- `tensorflow`, `keras`: Deep learning framework
- `scikit-learn`: Machine learning utilities
- `yfinance`: Financial data download
- `arch`: GARCH volatility modeling
- `statsmodels`: Statistical models

**Visualization:**
- `matplotlib`, `seaborn`: Static plots
- `plotly`: Interactive visualizations

**Others:**
- `joblib`: Model serialization
- `jupyter`: Interactive notebooks

See `requirements.txt` for complete list with version specifications.

## Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

**Areas for Contribution:**
- Additional ML models (GRU, Transformers, XGBoost)
- More sophisticated portfolio optimization (Black-Litterman, HRP)
- Alternative data sources (sentiment, macroeconomic indicators)
- Enhanced risk management (stop-loss, position sizing)
- Live trading integration
- Performance improvements and code optimization

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

**IMPORTANT**: This project is for **educational and research purposes only**. It is NOT financial advice.

- Past performance does not guarantee future results
- Trading involves substantial risk of loss
- Do NOT use this strategy with real money without thorough testing and understanding
- The authors are not responsible for any financial losses incurred
- Always consult with a qualified financial advisor before making investment decisions

By using this code, you acknowledge that you understand and accept these risks.

---

## Contact

For questions, suggestions, or collaboration:

- **GitHub Issues**: [Open an issue](https://github.com/yourusername/ml-sp500-trading-strategy/issues)
- **Email**: your.email@example.com

---

## Acknowledgments

- Yahoo Finance for providing free financial data via `yfinance`
- TensorFlow and Keras teams for the excellent deep learning framework
- The quantitative finance community for research and insights
- All contributors who help improve this project

---

**Star this repository** if you find it useful! ⭐

**Happy Trading!** 📈
