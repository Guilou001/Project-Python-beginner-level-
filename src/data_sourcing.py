"""
Data Sourcing Module
====================

This module handles downloading historical market data from Yahoo Finance,
including S&P 500, VIX, and sector ETFs for portfolio optimization.

Functions:
---------
- download_sp500_data: Download S&P 500 historical data
- download_vix_data: Download VIX (volatility index) data
- download_sector_etfs: Download sector ETF data for portfolio
- merge_datasets: Merge all datasets into a single DataFrame
- clean_data: Handle missing values and data quality issues
- save_data: Save processed data to disk
- load_data: Load data from disk
"""

import os
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DataDownloader:
    """
    Class to handle downloading and preprocessing market data.
    """

    def __init__(self, start_date, end_date, data_dir="data"):
        """
        Initialize DataDownloader.

        Parameters:
        -----------
        start_date : str
            Start date for data download (format: 'YYYY-MM-DD')
        end_date : str
            End date for data download (format: 'YYYY-MM-DD')
        data_dir : str
            Directory to save downloaded data
        """
        self.start_date = start_date
        self.end_date = end_date
        self.data_dir = data_dir

        os.makedirs(self.data_dir, exist_ok=True)

    def download_ticker(self, ticker, name=None):
        """
        Download data for a single ticker.

        Parameters:
        -----------
        ticker : str
            Ticker symbol
        name : str, optional
            Name for the dataset (defaults to ticker)

        Returns:
        --------
        pd.DataFrame
            Downloaded data with OHLCV columns
        """
        if name is None:
            name = ticker

        logger.info(f"Downloading {name} ({ticker})...")

        try:
            data = yf.download(ticker, start=self.start_date, end=self.end_date, progress=False)

            if data.empty:
                logger.warning(f"No data downloaded for {ticker}")
                return None

            logger.info(f"Successfully downloaded {len(data)} rows for {name}")
            return data

        except Exception as e:
            logger.error(f"Error downloading {ticker}: {str(e)}")
            return None

    def download_sp500(self, ticker="^GSPC"):
        """
        Download S&P 500 index data.

        Parameters:
        -----------
        ticker : str
            S&P 500 ticker symbol (default: ^GSPC)

        Returns:
        --------
        pd.DataFrame
            S&P 500 OHLCV data
        """
        data = self.download_ticker(ticker, "S&P 500")

        if data is not None:
            # Rename columns for clarity
            data.columns = [col.lower() for col in data.columns]

        return data

    def download_vix(self, ticker="^VIX"):
        """
        Download VIX (Volatility Index) data.

        Parameters:
        -----------
        ticker : str
            VIX ticker symbol (default: ^VIX)

        Returns:
        --------
        pd.DataFrame
            VIX data
        """
        data = self.download_ticker(ticker, "VIX")

        if data is not None:
            # Keep only Close for VIX
            data = data[['Close']].copy()
            data.columns = ['vix']

        return data

    def download_sector_etfs(self, tickers):
        """
        Download sector ETF data for portfolio optimization.

        Parameters:
        -----------
        tickers : list
            List of sector ETF ticker symbols

        Returns:
        --------
        pd.DataFrame
            DataFrame with adjusted close prices for all sector ETFs
        """
        logger.info(f"Downloading {len(tickers)} sector ETFs...")

        sector_data = {}

        for ticker in tickers:
            data = self.download_ticker(ticker, f"Sector ETF {ticker}")

            if data is not None and 'Adj Close' in data.columns:
                sector_data[ticker] = data['Adj Close']

        if not sector_data:
            logger.warning("No sector ETF data downloaded")
            return None

        # Combine into single DataFrame
        df = pd.DataFrame(sector_data)
        logger.info(f"Successfully downloaded data for {len(df.columns)} sector ETFs")

        return df

    def clean_data(self, data):
        """
        Clean data by handling missing values and outliers.

        Parameters:
        -----------
        data : pd.DataFrame
            Raw data

        Returns:
        --------
        pd.DataFrame
            Cleaned data
        """
        logger.info("Cleaning data...")

        if data is None or data.empty:
            logger.error("Cannot clean empty data")
            return None

        initial_rows = len(data)

        # Forward fill missing values (use previous day's value)
        data = data.ffill()

        # Backward fill any remaining NaN at the beginning
        data = data.bfill()

        # Drop rows with any remaining NaN values
        data = data.dropna()

        final_rows = len(data)

        if initial_rows != final_rows:
            logger.info(f"Removed {initial_rows - final_rows} rows with missing data")

        return data

    def save_data(self, data, filename):
        """
        Save data to disk.

        Parameters:
        -----------
        data : pd.DataFrame
            Data to save
        filename : str
            Filename (without path)
        """
        if data is None or data.empty:
            logger.warning(f"Cannot save empty data to {filename}")
            return

        filepath = os.path.join(self.data_dir, filename)

        # Save as parquet for efficient storage
        data.to_parquet(filepath)
        logger.info(f"Saved data to {filepath} ({len(data)} rows)")

    def load_data(self, filename):
        """
        Load data from disk.

        Parameters:
        -----------
        filename : str
            Filename (without path)

        Returns:
        --------
        pd.DataFrame
            Loaded data
        """
        filepath = os.path.join(self.data_dir, filename)

        if not os.path.exists(filepath):
            logger.warning(f"File not found: {filepath}")
            return None

        data = pd.read_parquet(filepath)
        logger.info(f"Loaded data from {filepath} ({len(data)} rows)")

        return data

    def download_all(self, sp500_ticker="^GSPC", vix_ticker="^VIX", sector_tickers=None):
        """
        Download all required data.

        Parameters:
        -----------
        sp500_ticker : str
            S&P 500 ticker symbol
        vix_ticker : str
            VIX ticker symbol
        sector_tickers : list
            List of sector ETF tickers

        Returns:
        --------
        dict
            Dictionary with 'sp500', 'vix', and 'sectors' DataFrames
        """
        logger.info("Starting data download...")

        # Download S&P 500
        sp500_data = self.download_sp500(sp500_ticker)

        # Download VIX
        vix_data = self.download_vix(vix_ticker)

        # Download sector ETFs
        sector_data = None
        if sector_tickers:
            sector_data = self.download_sector_etfs(sector_tickers)

        # Clean data
        sp500_data = self.clean_data(sp500_data)
        vix_data = self.clean_data(vix_data)
        if sector_data is not None:
            sector_data = self.clean_data(sector_data)

        # Save data
        if sp500_data is not None:
            self.save_data(sp500_data, "sp500_raw.parquet")
        if vix_data is not None:
            self.save_data(vix_data, "vix_raw.parquet")
        if sector_data is not None:
            self.save_data(sector_data, "sectors_raw.parquet")

        logger.info("Data download completed!")

        return {
            'sp500': sp500_data,
            'vix': vix_data,
            'sectors': sector_data
        }


def merge_market_data(sp500_data, vix_data):
    """
    Merge S&P 500 and VIX data.

    Parameters:
    -----------
    sp500_data : pd.DataFrame
        S&P 500 data
    vix_data : pd.DataFrame
        VIX data

    Returns:
    --------
    pd.DataFrame
        Merged dataset
    """
    logger.info("Merging market data...")

    # Merge on index (date)
    merged = sp500_data.join(vix_data, how='left')

    # Forward fill VIX values if there are any missing
    merged['vix'] = merged['vix'].ffill()

    logger.info(f"Merged data shape: {merged.shape}")

    return merged


if __name__ == "__main__":
    # Example usage
    from config import START_DATE, END_DATE, DATA_DIR, SP500_TICKER, VIX_TICKER, SECTOR_TICKERS

    # Initialize downloader
    downloader = DataDownloader(START_DATE, END_DATE, DATA_DIR)

    # Download all data
    data = downloader.download_all(
        sp500_ticker=SP500_TICKER,
        vix_ticker=VIX_TICKER,
        sector_tickers=SECTOR_TICKERS
    )

    # Merge S&P 500 and VIX
    if data['sp500'] is not None and data['vix'] is not None:
        merged_data = merge_market_data(data['sp500'], data['vix'])
        downloader.save_data(merged_data, "market_data.parquet")

        print(f"\nData Summary:")
        print(f"Date range: {merged_data.index.min()} to {merged_data.index.max()}")
        print(f"Total days: {len(merged_data)}")
        print(f"\nColumns: {list(merged_data.columns)}")
        print(f"\nFirst few rows:")
        print(merged_data.head())
