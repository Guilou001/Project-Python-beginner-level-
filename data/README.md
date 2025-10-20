# Data Directory

This directory stores all downloaded and processed data files.

## Files Generated

After running the pipeline, this directory will contain:

- `sp500_raw.parquet` - Raw S&P 500 OHLCV data from Yahoo Finance
- `vix_raw.parquet` - Raw VIX (Volatility Index) data
- `sectors_raw.parquet` - Raw sector ETF price data (11 sectors)
- `market_data.parquet` - Merged S&P 500 + VIX data
- `features.parquet` - Fully engineered features dataset (60+ features)

## Data Sources

All data is downloaded from Yahoo Finance using the `yfinance` library:
- **S&P 500**: ^GSPC
- **VIX**: ^VIX
- **Sector ETFs**: XLK, XLF, XLV, XLE, XLI, XLY, XLP, XLU, XLRE, XLB, XLC

## Date Range

Default: 2014-01-01 to present (configurable in `config.py`)

## File Format

All files are stored in Parquet format for efficient storage and fast loading.

## Note

This directory is git-ignored to avoid committing large data files.
Run `python main.py` to download and generate the data.
