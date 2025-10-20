# Results Directory

This directory stores all output files from backtesting and analysis.

## Files Generated

After running the complete pipeline, this directory will contain:

### Data Files
- `backtest_results.csv` - Complete backtest results with daily portfolio values
- `predictions.csv` - Model predictions on test set
- `performance_metrics.json` - Comprehensive performance metrics

### Visualizations (PNG)
- `cumulative_returns.png` - Strategy vs benchmark performance
- `predictions_vs_actual.png` - Model predictions visualization
- `portfolio_allocation.png` - Portfolio weights over time (stacked area)
- `confusion_matrix.png` - Classification performance heatmap
- `drawdown_chart.png` - Drawdown analysis
- `training_history.png` - Model training metrics (loss, accuracy, etc.)

### Interactive Dashboards
- `dashboard.html` - Interactive Plotly dashboard

## Performance Metrics

The `performance_metrics.json` file includes:

**Returns:**
- Total Return
- Annualized Return
- Cumulative Return

**Risk:**
- Annualized Volatility
- Maximum Drawdown

**Risk-Adjusted:**
- Sharpe Ratio
- Sortino Ratio
- Calmar Ratio

**Trading Statistics:**
- Win Rate
- Profit Factor
- Average Win/Loss

**Benchmark Comparison:**
- Benchmark Return
- Excess Return
- Benchmark Sharpe

**Model Performance:**
- Accuracy
- Precision
- Recall
- F1 Score
- AUC

## Viewing Results

### Static Plots
Open PNG files with any image viewer.

### Interactive Dashboard
Open `dashboard.html` in your web browser for interactive exploration.

### Data Analysis
```python
import pandas as pd
import json

# Load backtest results
results = pd.read_csv('results/backtest_results.csv')

# Load metrics
with open('results/performance_metrics.json', 'r') as f:
    metrics = json.load(f)

print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.4f}")
```

## Note

This directory is git-ignored. Results are regenerated each time you run the backtest.
