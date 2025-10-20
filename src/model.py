"""
LSTM Model Module
=================

This module implements the LSTM neural network for predicting S&P 500 direction.

Architecture:
------------
- Input layer with sequence data
- Bidirectional LSTM layer 1
- Dropout layer
- Bidirectional LSTM layer 2
- Dropout layer
- Dense output layer with sigmoid activation

Functions:
---------
- create_sequences: Create sequences for LSTM input
- build_lstm_model: Build LSTM architecture
- train_model: Train the model
- evaluate_model: Evaluate model performance
- save_model: Save trained model
- load_model: Load saved model
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, callbacks
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, accuracy_score
import joblib
import logging
import os

# Configure TensorFlow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set random seeds for reproducibility
def set_random_seed(seed=42):
    """Set random seeds for reproducibility."""
    np.random.seed(seed)
    tf.random.set_seed(seed)


class LSTMModel:
    """
    LSTM model for time series classification.
    """

    def __init__(self, config):
        """
        Initialize LSTM model.

        Parameters:
        -----------
        config : module
            Configuration module
        """
        self.config = config
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = None
        self.history = None

        # Set random seed
        set_random_seed(config.RANDOM_SEED)

    def create_sequences(self, X, y, sequence_length):
        """
        Create sequences for LSTM input.

        Parameters:
        -----------
        X : np.array
            Feature array
        y : np.array
            Target array
        sequence_length : int
            Length of sequences

        Returns:
        --------
        tuple
            (X_sequences, y_sequences)
        """
        X_sequences = []
        y_sequences = []

        for i in range(sequence_length, len(X)):
            X_sequences.append(X[i - sequence_length:i])
            y_sequences.append(y[i])

        return np.array(X_sequences), np.array(y_sequences)

    def prepare_data(self, features_df, feature_cols, target_col='target'):
        """
        Prepare data for training.

        Parameters:
        -----------
        features_df : pd.DataFrame
            DataFrame with features and target
        feature_cols : list
            List of feature column names
        target_col : str
            Target column name

        Returns:
        --------
        dict
            Dictionary with train, validation, and test data
        """
        logger.info("Preparing data for LSTM model...")

        # Store feature names
        self.feature_names = feature_cols

        # Extract features and target
        X = features_df[feature_cols].values
        y = features_df[target_col].values

        # Calculate split indices
        n_samples = len(X)
        train_end = int(n_samples * self.config.TRAIN_RATIO)
        val_end = int(n_samples * (self.config.TRAIN_RATIO + self.config.VALIDATION_RATIO))

        # Split data chronologically
        X_train = X[:train_end]
        X_val = X[train_end:val_end]
        X_test = X[val_end:]

        y_train = y[:train_end]
        y_val = y[train_end:val_end]
        y_test = y[val_end:]

        logger.info(f"Train set: {len(X_train)} samples")
        logger.info(f"Validation set: {len(X_val)} samples")
        logger.info(f"Test set: {len(X_test)} samples")

        # Scale features (fit on train only)
        self.scaler.fit(X_train)
        X_train_scaled = self.scaler.transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        X_test_scaled = self.scaler.transform(X_test)

        # Create sequences
        sequence_length = self.config.SEQUENCE_LENGTH

        X_train_seq, y_train_seq = self.create_sequences(X_train_scaled, y_train, sequence_length)
        X_val_seq, y_val_seq = self.create_sequences(X_val_scaled, y_val, sequence_length)
        X_test_seq, y_test_seq = self.create_sequences(X_test_scaled, y_test, sequence_length)

        logger.info(f"Sequence shape: {X_train_seq.shape}")
        logger.info(f"Train sequences: {len(X_train_seq)}")
        logger.info(f"Validation sequences: {len(X_val_seq)}")
        logger.info(f"Test sequences: {len(X_test_seq)}")

        # Class distribution
        logger.info(f"Train target distribution: {np.bincount(y_train_seq.astype(int))}")
        logger.info(f"Val target distribution: {np.bincount(y_val_seq.astype(int))}")
        logger.info(f"Test target distribution: {np.bincount(y_test_seq.astype(int))}")

        return {
            'X_train': X_train_seq,
            'y_train': y_train_seq,
            'X_val': X_val_seq,
            'y_val': y_val_seq,
            'X_test': X_test_seq,
            'y_test': y_test_seq,
        }

    def build_model(self, input_shape):
        """
        Build LSTM model architecture.

        Parameters:
        -----------
        input_shape : tuple
            Shape of input sequences (sequence_length, n_features)

        Returns:
        --------
        keras.Model
            Compiled LSTM model
        """
        logger.info(f"Building LSTM model with input shape {input_shape}...")

        model = keras.Sequential([
            # Input layer
            layers.Input(shape=input_shape),

            # First LSTM layer (bidirectional)
            layers.Bidirectional(
                layers.LSTM(
                    self.config.LSTM_UNITS_1,
                    return_sequences=True,
                    activation=self.config.ACTIVATION
                )
            ) if self.config.USE_BIDIRECTIONAL else layers.LSTM(
                self.config.LSTM_UNITS_1,
                return_sequences=True,
                activation=self.config.ACTIVATION
            ),

            # Dropout
            layers.Dropout(self.config.DROPOUT_RATE),

            # Second LSTM layer
            layers.Bidirectional(
                layers.LSTM(
                    self.config.LSTM_UNITS_2,
                    return_sequences=False,
                    activation=self.config.ACTIVATION
                )
            ) if self.config.USE_BIDIRECTIONAL else layers.LSTM(
                self.config.LSTM_UNITS_2,
                return_sequences=False,
                activation=self.config.ACTIVATION
            ),

            # Dropout
            layers.Dropout(self.config.DROPOUT_RATE),

            # Dense layers
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.2),

            # Output layer (binary classification)
            layers.Dense(1, activation='sigmoid')
        ])

        # Compile model
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self.config.LEARNING_RATE),
            loss=self.config.LOSS,
            metrics=[
                'accuracy',
                keras.metrics.Precision(name='precision'),
                keras.metrics.Recall(name='recall'),
                keras.metrics.AUC(name='auc')
            ]
        )

        logger.info("Model architecture:")
        model.summary(print_fn=logger.info)

        self.model = model
        return model

    def train(self, data):
        """
        Train the LSTM model.

        Parameters:
        -----------
        data : dict
            Dictionary with training and validation data

        Returns:
        --------
        keras.callbacks.History
            Training history
        """
        logger.info("Training LSTM model...")

        # Build model if not already built
        if self.model is None:
            input_shape = (data['X_train'].shape[1], data['X_train'].shape[2])
            self.build_model(input_shape)

        # Callbacks
        early_stopping = callbacks.EarlyStopping(
            monitor='val_loss',
            patience=self.config.EARLY_STOPPING_PATIENCE,
            restore_best_weights=True,
            verbose=1
        )

        reduce_lr = callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )

        # Train model
        history = self.model.fit(
            data['X_train'],
            data['y_train'],
            batch_size=self.config.BATCH_SIZE,
            epochs=self.config.EPOCHS,
            validation_data=(data['X_val'], data['y_val']),
            callbacks=[early_stopping, reduce_lr],
            verbose=self.config.VERBOSE
        )

        self.history = history
        logger.info("Training completed!")

        return history

    def evaluate(self, X_test, y_test):
        """
        Evaluate model on test set.

        Parameters:
        -----------
        X_test : np.array
            Test features
        y_test : np.array
            Test targets

        Returns:
        --------
        dict
            Dictionary with evaluation metrics
        """
        logger.info("Evaluating model on test set...")

        # Get predictions
        y_pred_proba = self.model.predict(X_test, verbose=0)
        y_pred = (y_pred_proba > 0.5).astype(int).flatten()

        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        auc_score = roc_auc_score(y_test, y_pred_proba)

        # Classification report
        report = classification_report(y_test, y_pred, output_dict=True)

        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)

        metrics = {
            'accuracy': accuracy,
            'auc': auc_score,
            'precision': report['1']['precision'],
            'recall': report['1']['recall'],
            'f1_score': report['1']['f1-score'],
            'confusion_matrix': cm,
            'classification_report': report
        }

        logger.info(f"Test Accuracy: {accuracy:.4f}")
        logger.info(f"Test AUC: {auc_score:.4f}")
        logger.info(f"Test Precision: {metrics['precision']:.4f}")
        logger.info(f"Test Recall: {metrics['recall']:.4f}")
        logger.info(f"Test F1 Score: {metrics['f1_score']:.4f}")
        logger.info(f"\nConfusion Matrix:\n{cm}")

        return metrics

    def predict(self, X):
        """
        Make predictions.

        Parameters:
        -----------
        X : np.array
            Input features

        Returns:
        --------
        tuple
            (predictions, probabilities)
        """
        y_pred_proba = self.model.predict(X, verbose=0)
        y_pred = (y_pred_proba > 0.5).astype(int).flatten()

        return y_pred, y_pred_proba.flatten()

    def save_model(self, model_path=None, scaler_path=None, feature_names_path=None):
        """
        Save model and scaler.

        Parameters:
        -----------
        model_path : str
            Path to save model
        scaler_path : str
            Path to save scaler
        feature_names_path : str
            Path to save feature names
        """
        if model_path is None:
            model_path = self.config.MODEL_PATH
        if scaler_path is None:
            scaler_path = self.config.SCALER_PATH
        if feature_names_path is None:
            feature_names_path = self.config.FEATURE_NAMES_PATH

        # Save model
        self.model.save(model_path)
        logger.info(f"Model saved to {model_path}")

        # Save scaler
        joblib.dump(self.scaler, scaler_path)
        logger.info(f"Scaler saved to {scaler_path}")

        # Save feature names
        joblib.dump(self.feature_names, feature_names_path)
        logger.info(f"Feature names saved to {feature_names_path}")

    def load_model(self, model_path=None, scaler_path=None, feature_names_path=None):
        """
        Load model and scaler.

        Parameters:
        -----------
        model_path : str
            Path to load model from
        scaler_path : str
            Path to load scaler from
        feature_names_path : str
            Path to load feature names from
        """
        if model_path is None:
            model_path = self.config.MODEL_PATH
        if scaler_path is None:
            scaler_path = self.config.SCALER_PATH
        if feature_names_path is None:
            feature_names_path = self.config.FEATURE_NAMES_PATH

        # Load model
        self.model = keras.models.load_model(model_path)
        logger.info(f"Model loaded from {model_path}")

        # Load scaler
        self.scaler = joblib.load(scaler_path)
        logger.info(f"Scaler loaded from {scaler_path}")

        # Load feature names
        self.feature_names = joblib.load(feature_names_path)
        logger.info(f"Feature names loaded from {feature_names_path}")


if __name__ == "__main__":
    # Example usage
    import sys
    sys.path.append('..')
    import config
    from src.data_sourcing import DataDownloader

    # Load features
    downloader = DataDownloader(config.START_DATE, config.END_DATE, config.DATA_DIR)
    features_df = downloader.load_data("features.parquet")

    if features_df is not None:
        # Get feature columns (exclude target and OHLCV)
        exclude_cols = ['open', 'high', 'low', 'close', 'volume', 'adj close', 'target']
        feature_cols = [col for col in features_df.columns if col.lower() not in exclude_cols]

        # Initialize model
        lstm_model = LSTMModel(config)

        # Prepare data
        data = lstm_model.prepare_data(features_df, feature_cols)

        # Build and train model
        lstm_model.build_model(input_shape=(config.SEQUENCE_LENGTH, len(feature_cols)))
        history = lstm_model.train(data)

        # Evaluate
        metrics = lstm_model.evaluate(data['X_test'], data['y_test'])

        # Save model
        lstm_model.save_model()
