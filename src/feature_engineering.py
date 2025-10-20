"""
Feature Engineering Module
===========================

This module creates features for the ML model, including:
- Technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands, ATR)
- GARCH volatility predictions
- Temporal features
- Lagged returns
- Volume-based features

Functions:
---------
- calculate_returns: Calculate price returns
- add_sma_features: Add Simple Moving Average features
- add_ema_features: Add Exponential Moving Average features
- add_rsi_features: Add Relative Strength Index
- add_macd_features: Add MACD indicator
- add_bollinger_bands: Add Bollinger Bands
- add_atr_features: Add Average True Range
- add_garch_volatility: Add GARCH predicted volatility
- add_temporal_features: Add time-based features
- add_lagged_features: Add lagged return features
- create_all_features: Create all features
- create_target: Create target variable (1=up, 0=down)
"""

import pandas as pd
import numpy as np
from arch import arch_model
import logging
import warnings

warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FeatureEngineer:
    """
    Class to handle feature engineering for the ML model.
    """

    def __init__(self, data):
        """
        Initialize FeatureEngineer.

        Parameters:
        -----------
        data : pd.DataFrame
            Raw market data with OHLCV columns
        """
        self.data = data.copy()
        self.features = None

    def calculate_returns(self, column='close', periods=1):
        """
        Calculate returns.

        Parameters:
        -----------
        column : str
            Column to calculate returns from
        periods : int
            Number of periods for return calculation

        Returns:
        --------
        pd.Series
            Returns
        """
        return self.data[column].pct_change(periods=periods)

    def add_sma_features(self, periods=[5, 10, 20, 50, 200]):
        """
        Add Simple Moving Average features.

        Parameters:
        -----------
        periods : list
            List of periods for SMA calculation
        """
        logger.info(f"Adding SMA features for periods: {periods}")

        for period in periods:
            col_name = f'sma_{period}'
            self.data[col_name] = self.data['close'].rolling(window=period).mean()

            # Create ratio features (price / SMA)
            ratio_name = f'price_to_sma_{period}'
            self.data[ratio_name] = self.data['close'] / self.data[col_name]

    def add_ema_features(self, periods=[12, 26, 50]):
        """
        Add Exponential Moving Average features.

        Parameters:
        -----------
        periods : list
            List of periods for EMA calculation
        """
        logger.info(f"Adding EMA features for periods: {periods}")

        for period in periods:
            col_name = f'ema_{period}'
            self.data[col_name] = self.data['close'].ewm(span=period, adjust=False).mean()

            # Create ratio features
            ratio_name = f'price_to_ema_{period}'
            self.data[ratio_name] = self.data['close'] / self.data[col_name]

    def add_rsi_features(self, period=14):
        """
        Add Relative Strength Index (RSI).

        Parameters:
        -----------
        period : int
            Period for RSI calculation
        """
        logger.info(f"Adding RSI feature with period {period}")

        # Calculate price changes
        delta = self.data['close'].diff()

        # Separate gains and losses
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        # Calculate average gain and loss
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        # Calculate RS and RSI
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        self.data[f'rsi_{period}'] = rsi

    def add_macd_features(self, fast=12, slow=26, signal=9):
        """
        Add MACD (Moving Average Convergence Divergence) features.

        Parameters:
        -----------
        fast : int
            Fast EMA period
        slow : int
            Slow EMA period
        signal : int
            Signal line period
        """
        logger.info(f"Adding MACD features (fast={fast}, slow={slow}, signal={signal})")

        # Calculate MACD line
        ema_fast = self.data['close'].ewm(span=fast, adjust=False).mean()
        ema_slow = self.data['close'].ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow

        # Calculate signal line
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()

        # Calculate histogram
        histogram = macd_line - signal_line

        self.data['macd'] = macd_line
        self.data['macd_signal'] = signal_line
        self.data['macd_histogram'] = histogram

    def add_bollinger_bands(self, period=20, std_dev=2):
        """
        Add Bollinger Bands features.

        Parameters:
        -----------
        period : int
            Period for moving average
        std_dev : float
            Number of standard deviations
        """
        logger.info(f"Adding Bollinger Bands (period={period}, std={std_dev})")

        # Calculate middle band (SMA)
        middle_band = self.data['close'].rolling(window=period).mean()

        # Calculate standard deviation
        rolling_std = self.data['close'].rolling(window=period).std()

        # Calculate upper and lower bands
        upper_band = middle_band + (rolling_std * std_dev)
        lower_band = middle_band - (rolling_std * std_dev)

        # Calculate bandwidth and %B
        bandwidth = (upper_band - lower_band) / middle_band
        percent_b = (self.data['close'] - lower_band) / (upper_band - lower_band)

        self.data['bb_upper'] = upper_band
        self.data['bb_middle'] = middle_band
        self.data['bb_lower'] = lower_band
        self.data['bb_bandwidth'] = bandwidth
        self.data['bb_percent_b'] = percent_b

    def add_atr_features(self, period=14):
        """
        Add Average True Range (ATR) for volatility.

        Parameters:
        -----------
        period : int
            Period for ATR calculation
        """
        logger.info(f"Adding ATR feature with period {period}")

        # Calculate True Range
        high_low = self.data['high'] - self.data['low']
        high_close = np.abs(self.data['high'] - self.data['close'].shift())
        low_close = np.abs(self.data['low'] - self.data['close'].shift())

        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)

        # Calculate ATR
        atr = true_range.rolling(window=period).mean()

        self.data[f'atr_{period}'] = atr

        # Normalized ATR (ATR / Close)
        self.data[f'atr_{period}_normalized'] = atr / self.data['close']

    def add_garch_volatility(self, p=1, q=1, forecast_horizon=1):
        """
        Add GARCH(p,q) predicted volatility.

        Parameters:
        -----------
        p : int
            GARCH lag order
        q : int
            ARCH lag order
        forecast_horizon : int
            Forecast horizon in days
        """
        logger.info(f"Adding GARCH({p},{q}) volatility forecasts")

        # Calculate returns (percentage)
        returns = self.calculate_returns(column='close', periods=1) * 100

        # Remove NaN values for GARCH fitting
        returns_clean = returns.dropna()

        if len(returns_clean) < 100:
            logger.warning("Not enough data for GARCH model. Skipping GARCH features.")
            self.data['garch_volatility'] = np.nan
            return

        try:
            # Fit GARCH model
            model = arch_model(returns_clean, vol='Garch', p=p, q=q, rescale=False)
            fitted_model = model.fit(disp='off', show_warning=False)

            # Get conditional volatility (fitted values)
            conditional_vol = fitted_model.conditional_volatility

            # Create forecast for each point (rolling forecast)
            volatility_forecast = pd.Series(index=self.data.index, dtype=float)

            # Align conditional volatility with original data
            for date in conditional_vol.index:
                if date in volatility_forecast.index:
                    volatility_forecast[date] = conditional_vol[date]

            # Forward fill for missing dates
            volatility_forecast = volatility_forecast.fillna(method='ffill')

            # Store in dataframe
            self.data['garch_volatility'] = volatility_forecast

            logger.info("GARCH volatility features added successfully")

        except Exception as e:
            logger.error(f"Error fitting GARCH model: {str(e)}")
            self.data['garch_volatility'] = np.nan

    def add_temporal_features(self):
        """
        Add temporal (time-based) features.
        """
        logger.info("Adding temporal features")

        # Day of week (0=Monday, 6=Sunday)
        self.data['day_of_week'] = self.data.index.dayofweek

        # Month (1-12)
        self.data['month'] = self.data.index.month

        # Quarter (1-4)
        self.data['quarter'] = self.data.index.quarter

        # Day of month (1-31)
        self.data['day_of_month'] = self.data.index.day

        # Year
        self.data['year'] = self.data.index.year

        # Cyclical encoding for day of week
        self.data['day_of_week_sin'] = np.sin(2 * np.pi * self.data['day_of_week'] / 7)
        self.data['day_of_week_cos'] = np.cos(2 * np.pi * self.data['day_of_week'] / 7)

        # Cyclical encoding for month
        self.data['month_sin'] = np.sin(2 * np.pi * self.data['month'] / 12)
        self.data['month_cos'] = np.cos(2 * np.pi * self.data['month'] / 12)

    def add_lagged_features(self, return_lags=[1, 2, 3, 5, 10, 20], volume_lags=[1, 5, 10]):
        """
        Add lagged features.

        Parameters:
        -----------
        return_lags : list
            Lags for return features
        volume_lags : list
            Lags for volume features
        """
        logger.info(f"Adding lagged features (returns: {return_lags}, volume: {volume_lags})")

        # Calculate returns
        returns = self.calculate_returns(column='close', periods=1)

        # Add lagged returns
        for lag in return_lags:
            self.data[f'return_lag_{lag}'] = returns.shift(lag)

        # Add lagged volume changes
        if 'volume' in self.data.columns:
            volume_change = self.data['volume'].pct_change()

            for lag in volume_lags:
                self.data[f'volume_change_lag_{lag}'] = volume_change.shift(lag)

            # Add volume moving averages
            self.data['volume_ma_10'] = self.data['volume'].rolling(window=10).mean()
            self.data['volume_ratio'] = self.data['volume'] / self.data['volume_ma_10']

    def add_volatility_features(self):
        """
        Add additional volatility features.
        """
        logger.info("Adding volatility features")

        # Historical volatility (standard deviation of returns)
        returns = self.calculate_returns(column='close', periods=1)

        for window in [5, 10, 20, 60]:
            self.data[f'volatility_{window}d'] = returns.rolling(window=window).std() * np.sqrt(252)

        # VIX features (if VIX is in the data)
        if 'vix' in self.data.columns:
            self.data['vix_change'] = self.data['vix'].pct_change()
            self.data['vix_ma_10'] = self.data['vix'].rolling(window=10).mean()
            self.data['vix_ratio'] = self.data['vix'] / self.data['vix_ma_10']

    def create_target(self, horizon=1):
        """
        Create target variable (next day's direction).

        Parameters:
        -----------
        horizon : int
            Prediction horizon in days

        Returns:
        --------
        pd.Series
            Target variable (1 = up, 0 = down)
        """
        logger.info(f"Creating target variable with horizon={horizon} day(s)")

        # Calculate future returns
        future_return = self.data['close'].pct_change(periods=horizon).shift(-horizon)

        # Create binary target (1 if positive return, 0 otherwise)
        target = (future_return > 0).astype(int)

        return target

    def create_all_features(self, config):
        """
        Create all features using configuration.

        Parameters:
        -----------
        config : module
            Configuration module with feature parameters

        Returns:
        --------
        pd.DataFrame
            DataFrame with all features
        """
        logger.info("Creating all features...")

        # Technical indicators
        self.add_sma_features(periods=config.SMA_PERIODS)
        self.add_ema_features(periods=config.EMA_PERIODS)
        self.add_rsi_features(period=config.RSI_PERIOD)
        self.add_macd_features(fast=config.MACD_FAST, slow=config.MACD_SLOW, signal=config.MACD_SIGNAL)
        self.add_bollinger_bands(period=config.BBANDS_PERIOD, std_dev=config.BBANDS_STD)
        self.add_atr_features(period=config.ATR_PERIOD)

        # Volatility features
        self.add_volatility_features()
        self.add_garch_volatility(p=config.GARCH_P, q=config.GARCH_Q, forecast_horizon=config.GARCH_FORECAST_HORIZON)

        # Temporal features
        self.add_temporal_features()

        # Lagged features
        self.add_lagged_features(return_lags=config.RETURN_LAGS, volume_lags=config.VOLUME_LAGS)

        # Create target
        target = self.create_target(horizon=1)
        self.data['target'] = target

        # Drop rows with NaN values
        initial_rows = len(self.data)
        self.data = self.data.dropna()
        final_rows = len(self.data)

        logger.info(f"Dropped {initial_rows - final_rows} rows with NaN values")
        logger.info(f"Final dataset shape: {self.data.shape}")
        logger.info(f"Features created: {len(self.data.columns) - 1}")  # -1 for target

        return self.data

    def get_feature_names(self):
        """
        Get list of feature names (excluding target and original OHLCV columns).

        Returns:
        --------
        list
            List of feature names
        """
        exclude_cols = ['open', 'high', 'low', 'close', 'volume', 'adj close', 'target']
        feature_names = [col for col in self.data.columns if col.lower() not in exclude_cols]

        return feature_names


if __name__ == "__main__":
    # Example usage
    import sys
    sys.path.append('..')
    import config
    from src.data_sourcing import DataDownloader

    # Load data
    downloader = DataDownloader(config.START_DATE, config.END_DATE, config.DATA_DIR)
    data = downloader.load_data("market_data.parquet")

    if data is not None:
        # Create features
        fe = FeatureEngineer(data)
        features_df = fe.create_all_features(config)

        print(f"\nFeature Engineering Summary:")
        print(f"Total features: {len(fe.get_feature_names())}")
        print(f"Dataset shape: {features_df.shape}")
        print(f"\nTarget distribution:")
        print(features_df['target'].value_counts(normalize=True))
        print(f"\nSample features:")
        print(features_df[fe.get_feature_names()[:5]].head())

        # Save features
        downloader.save_data(features_df, "features.parquet")
