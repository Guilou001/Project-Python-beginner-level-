# Quick Start Guide

Get the ML Trading Strategy up and running in 5 minutes!

## Option 1: Local Installation (Recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/ml-sp500-trading-strategy.git
cd ml-sp500-trading-strategy
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Pipeline
```bash
python main.py
```

That's it! The script will:
1. Download 10 years of market data (~2 minutes)
2. Engineer 60+ features (~1 minute)
3. Train the LSTM model (~5-10 minutes on CPU, ~2 minutes on GPU)
4. Run backtest and generate visualizations (~1 minute)

### Step 5: View Results
Results are saved in the `results/` directory:
- Open `results/dashboard.html` in your browser for interactive charts
- Check `results/performance_metrics.json` for detailed metrics
- View all PNG plots in `results/`

## Option 2: Google Colab (No Installation Required)

### Step 1: Open Colab Notebook
Click here: [Open in Colab](https://colab.research.google.com/github/yourusername/ml-sp500-trading-strategy/blob/main/notebooks/Google_Colab_Complete_Pipeline.ipynb)

### Step 2: Run All Cells
Click `Runtime` → `Run all` and wait ~15-20 minutes.

That's it! Everything runs in the cloud.

## Option 3: Jupyter Notebook (Local)

If you prefer interactive exploration:

```bash
# After installing dependencies
jupyter notebook notebooks/01_data_exploration.ipynb
```

## Command-Line Options

### Skip Data Download (Use Existing Data)
```bash
python main.py --skip-download
```

### Skip Model Training (Use Existing Model)
```bash
python main.py --skip-training
```

### Only Train Model (Skip Backtesting)
```bash
python main.py --skip-backtest
```

## Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:** Make sure you activated the virtual environment and installed requirements.
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: "No data downloaded"
**Solution:** Check your internet connection. Yahoo Finance might be temporarily down.
Wait a few minutes and try again.

### Issue: Out of Memory
**Solution:** Reduce batch size in `config.py`:
```python
BATCH_SIZE = 16  # Instead of 32
```

### Issue: Training is Too Slow
**Solution:**
1. Reduce epochs: `EPOCHS = 50` in `config.py`
2. Use GPU if available (TensorFlow will automatically detect)
3. Reduce sequence length: `SEQUENCE_LENGTH = 30` in `config.py`

## What to Expect

### Performance Metrics (Example)
After running the complete pipeline, you should see something like:

```
PERFORMANCE METRICS SUMMARY
============================================================
Total Return:           45.2%
Annualized Return:      18.5%
Annualized Volatility:  12.3%
Sharpe Ratio:           1.42
Maximum Drawdown:       -8.7%
Win Rate:               56.8%

Model Accuracy:         58.3%
AUC:                    0.64
```

### File Structure After Running
```
ml-sp500-trading-strategy/
├── data/
│   ├── market_data.parquet       ✓ Generated
│   ├── features.parquet           ✓ Generated
│   └── sectors_raw.parquet        ✓ Generated
├── models/
│   ├── lstm_sp500_predictor.keras ✓ Generated
│   ├── feature_scaler.pkl         ✓ Generated
│   └── feature_names.pkl          ✓ Generated
└── results/
    ├── backtest_results.csv       ✓ Generated
    ├── performance_metrics.json   ✓ Generated
    ├── cumulative_returns.png     ✓ Generated
    ├── predictions_vs_actual.png  ✓ Generated
    ├── portfolio_allocation.png   ✓ Generated
    ├── confusion_matrix.png       ✓ Generated
    ├── drawdown_chart.png         ✓ Generated
    └── dashboard.html             ✓ Generated
```

## Customization

### Change Data Range
Edit `config.py`:
```python
START_DATE = "2015-01-01"  # Start from 2015 instead of 2014
END_DATE = "2023-12-31"    # End at specific date
```

### Change Model Hyperparameters
Edit `config.py`:
```python
LSTM_UNITS_1 = 64          # Smaller model (faster training)
DROPOUT_RATE = 0.5         # More regularization
LEARNING_RATE = 0.0005     # Lower learning rate
```

### Change Portfolio Optimization Method
Edit `config.py`:
```python
OPTIMIZATION_METHOD = "min_variance"  # Or "risk_parity", "equal_weight"
```

## Next Steps

1. **Explore the Data**: Open `notebooks/01_data_exploration.ipynb`
2. **Modify Strategy**: Edit parameters in `config.py`
3. **Experiment**: Try different models or features
4. **Analyze Results**: Study the generated plots and metrics

## Need Help?

- **Documentation**: See [README.md](README.md) for detailed info
- **Issues**: Open an issue on GitHub
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## Remember

⚠️ **This is for educational purposes only!**
- Do NOT use with real money without extensive testing
- Past performance does not guarantee future results
- Always consult a financial advisor

Happy coding! 🚀📈
