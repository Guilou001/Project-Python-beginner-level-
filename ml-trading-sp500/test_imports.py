"""
Quick test script to verify all imports work correctly.
Run this before running the main pipeline to catch any import errors.
"""

import sys
print("Python version:", sys.version)
print("\nTesting imports...\n")

errors = []

# Test standard library imports
print("✓ Testing standard library imports...")
try:
    import os
    import json
    import logging
    from datetime import datetime
    print("  ✓ Standard library OK")
except ImportError as e:
    errors.append(f"Standard library error: {e}")
    print(f"  ✗ Error: {e}")

# Test numpy and pandas
print("✓ Testing numpy and pandas...")
try:
    import numpy as np
    import pandas as pd
    print(f"  ✓ numpy {np.__version__}")
    print(f"  ✓ pandas {pd.__version__}")
except ImportError as e:
    errors.append(f"numpy/pandas error: {e}")
    print(f"  ✗ Error: {e}")

# Test scientific computing
print("✓ Testing scipy...")
try:
    import scipy
    from scipy.optimize import minimize
    print(f"  ✓ scipy {scipy.__version__}")
except ImportError as e:
    errors.append(f"scipy error: {e}")
    print(f"  ✗ Error: {e}")

# Test TensorFlow and Keras
print("✓ Testing TensorFlow and Keras...")
try:
    import tensorflow as tf
    from tensorflow import keras
    print(f"  ✓ TensorFlow {tf.__version__}")
    print(f"  ✓ Keras {keras.__version__}")
except ImportError as e:
    errors.append(f"TensorFlow/Keras error: {e}")
    print(f"  ✗ Error: {e}")

# Test scikit-learn
print("✓ Testing scikit-learn...")
try:
    import sklearn
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score
    print(f"  ✓ scikit-learn {sklearn.__version__}")
except ImportError as e:
    errors.append(f"scikit-learn error: {e}")
    print(f"  ✗ Error: {e}")

# Test yfinance
print("✓ Testing yfinance...")
try:
    import yfinance as yf
    print(f"  ✓ yfinance OK")
except ImportError as e:
    errors.append(f"yfinance error: {e}")
    print(f"  ✗ Error: {e}")

# Test arch (GARCH)
print("✓ Testing arch (GARCH)...")
try:
    from arch import arch_model
    print(f"  ✓ arch OK")
except ImportError as e:
    errors.append(f"arch error: {e}")
    print(f"  ✗ Error: {e}")

# Test statsmodels
print("✓ Testing statsmodels...")
try:
    import statsmodels
    print(f"  ✓ statsmodels {statsmodels.__version__}")
except ImportError as e:
    errors.append(f"statsmodels error: {e}")
    print(f"  ✗ Error: {e}")

# Test matplotlib and seaborn
print("✓ Testing matplotlib and seaborn...")
try:
    import matplotlib
    import matplotlib.pyplot as plt
    import seaborn as sns
    print(f"  ✓ matplotlib {matplotlib.__version__}")
    print(f"  ✓ seaborn {sns.__version__}")
except ImportError as e:
    errors.append(f"visualization error: {e}")
    print(f"  ✗ Error: {e}")

# Test plotly
print("✓ Testing plotly...")
try:
    import plotly
    import plotly.graph_objects as go
    print(f"  ✓ plotly {plotly.__version__}")
except ImportError as e:
    errors.append(f"plotly error: {e}")
    print(f"  ✗ Error: {e}")

# Test joblib
print("✓ Testing joblib...")
try:
    import joblib
    print(f"  ✓ joblib OK")
except ImportError as e:
    errors.append(f"joblib error: {e}")
    print(f"  ✗ Error: {e}")

# Test project modules
print("\n✓ Testing project modules...")
try:
    import config
    print("  ✓ config")
except ImportError as e:
    errors.append(f"config error: {e}")
    print(f"  ✗ Error importing config: {e}")

try:
    from src import data_sourcing
    print("  ✓ src.data_sourcing")
except ImportError as e:
    errors.append(f"data_sourcing error: {e}")
    print(f"  ✗ Error importing data_sourcing: {e}")

try:
    from src import feature_engineering
    print("  ✓ src.feature_engineering")
except ImportError as e:
    errors.append(f"feature_engineering error: {e}")
    print(f"  ✗ Error importing feature_engineering: {e}")

try:
    from src import model
    print("  ✓ src.model")
except ImportError as e:
    errors.append(f"model error: {e}")
    print(f"  ✗ Error importing model: {e}")

try:
    from src import portfolio_optimization
    print("  ✓ src.portfolio_optimization")
except ImportError as e:
    errors.append(f"portfolio_optimization error: {e}")
    print(f"  ✗ Error importing portfolio_optimization: {e}")

try:
    from src import backtesting
    print("  ✓ src.backtesting")
except ImportError as e:
    errors.append(f"backtesting error: {e}")
    print(f"  ✗ Error importing backtesting: {e}")

try:
    from src import plotting
    print("  ✓ src.plotting")
except ImportError as e:
    errors.append(f"plotting error: {e}")
    print(f"  ✗ Error importing plotting: {e}")

try:
    from src import utils
    print("  ✓ src.utils")
except ImportError as e:
    errors.append(f"utils error: {e}")
    print(f"  ✗ Error importing utils: {e}")

# Summary
print("\n" + "="*60)
if errors:
    print("IMPORT TEST FAILED")
    print("="*60)
    print(f"\n{len(errors)} error(s) found:\n")
    for error in errors:
        print(f"  ✗ {error}")
    print("\nPlease install missing dependencies:")
    print("  pip install -r requirements.txt")
    sys.exit(1)
else:
    print("ALL IMPORTS SUCCESSFUL! ✓")
    print("="*60)
    print("\nYou can now run the main pipeline:")
    print("  python main.py")
    sys.exit(0)
