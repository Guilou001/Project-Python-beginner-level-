# Models Directory

This directory stores trained machine learning models and preprocessing artifacts.

## Files Generated

After training, this directory will contain:

- `lstm_sp500_predictor.keras` - Trained LSTM model (TensorFlow/Keras format)
- `feature_scaler.pkl` - StandardScaler fitted on training data
- `feature_names.pkl` - List of feature names used for training

## Model Architecture

**LSTM Neural Network:**
- Input: (60 time steps, 60+ features)
- Bidirectional LSTM Layer 1: 128 units, 30% dropout
- Bidirectional LSTM Layer 2: 64 units, 30% dropout
- Dense Layer: 32 units, ReLU activation, 20% dropout
- Output Layer: 1 unit, Sigmoid activation (binary classification)

**Training Configuration:**
- Optimizer: Adam (lr=0.001)
- Loss: Binary Cross-Entropy
- Metrics: Accuracy, Precision, Recall, AUC
- Early Stopping: Patience=15 epochs
- Batch Size: 32
- Max Epochs: 100

## Loading Models

```python
from src.model import LSTMModel
import config

# Initialize and load
model = LSTMModel(config)
model.load_model()

# Make predictions
predictions = model.predict(X_test)
```

## Note

This directory is git-ignored to avoid committing large model files.
Models are regenerated when you run `python main.py`.
