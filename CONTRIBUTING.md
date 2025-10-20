# Contributing to ML Trading Strategy

Thank you for considering contributing to this project! 🎉

This document provides guidelines for contributing to the ML Trading Strategy for S&P 500 Prediction.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Areas for Contribution](#areas-for-contribution)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code:

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

If you find a bug, please create an issue with:

1. **Clear title**: Describe the bug in one line
2. **Description**: Detailed description of the bug
3. **Steps to reproduce**: How to trigger the bug
4. **Expected behavior**: What should happen
5. **Actual behavior**: What actually happens
6. **Environment**: OS, Python version, etc.
7. **Code snippet**: If applicable

**Template:**
```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: Ubuntu 20.04
- Python: 3.8.10
- TensorFlow: 2.13.0
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:

1. **Clear title**: Feature request in one line
2. **Motivation**: Why is this feature needed?
3. **Description**: Detailed description of the feature
4. **Examples**: How would it work?
5. **Alternatives**: Other approaches considered

### Contributing Code

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Make your changes**
4. **Test your changes**
5. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
6. **Push to the branch** (`git push origin feature/AmazingFeature`)
7. **Open a Pull Request**

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/yourusername/ml-sp500-trading-strategy.git
cd ml-sp500-trading-strategy

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install pytest black flake8 mypy
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_model.py

# Run with coverage
pytest --cov=src tests/
```

## Coding Standards

### Python Style Guide

We follow **PEP 8** style guide with some modifications:

- **Line length**: 100 characters (instead of 79)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings

### Code Formatting

Use **Black** for automatic formatting:

```bash
# Format all Python files
black .

# Check formatting without changing files
black --check .
```

### Linting

Use **flake8** for linting:

```bash
# Lint all files
flake8 src/ --max-line-length=100

# Ignore specific errors
flake8 src/ --ignore=E203,W503 --max-line-length=100
```

### Type Hints

Use type hints for function signatures:

```python
def calculate_returns(prices: pd.Series, periods: int = 1) -> pd.Series:
    """Calculate returns from prices."""
    return prices.pct_change(periods=periods)
```

### Docstrings

Use **Google-style** docstrings:

```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Brief description of function.

    Longer description if needed.

    Parameters:
    -----------
    param1 : type
        Description of param1
    param2 : type
        Description of param2

    Returns:
    --------
    return_type
        Description of return value

    Examples:
    ---------
    >>> function_name(value1, value2)
    expected_output
    """
    pass
```

### Comments

- Use comments to explain **why**, not **what**
- Keep comments up-to-date with code changes
- Use docstrings for functions and classes
- Use inline comments sparingly

### Project Structure

When adding new modules:

```python
src/
├── __init__.py
├── your_module.py        # Your new module
└── tests/
    └── test_your_module.py  # Corresponding tests
```

## Pull Request Process

### Before Submitting

1. **Test your code**: Ensure all tests pass
2. **Format your code**: Run `black` and `flake8`
3. **Update documentation**: Update README.md if needed
4. **Add tests**: Include tests for new features
5. **Update CHANGELOG**: Add entry to CHANGELOG.md (if exists)

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested your changes

## Checklist
- [ ] Code follows project style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests pass locally
- [ ] No breaking changes (or documented)
```

### Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged
4. Your contribution will be acknowledged!

## Areas for Contribution

We especially welcome contributions in these areas:

### 1. New ML Models

- Implement GRU architecture
- Add Transformer-based models
- Integrate XGBoost for comparison
- Ensemble methods

**Skills needed**: Deep learning, Python, TensorFlow/PyTorch

### 2. Alternative Data Sources

- Sentiment analysis from news/social media
- Macroeconomic indicators
- Earnings reports
- Options market data

**Skills needed**: Data engineering, APIs, Python

### 3. Portfolio Optimization

- Black-Litterman model
- Hierarchical Risk Parity (HRP)
- Conditional Value-at-Risk (CVaR)
- Kelly Criterion position sizing

**Skills needed**: Finance, optimization, Python

### 4. Risk Management

- Implement stop-loss logic
- Dynamic position sizing
- Drawdown constraints
- Volatility targeting

**Skills needed**: Risk management, Python

### 5. Visualization

- Interactive dashboards with Streamlit/Dash
- Real-time monitoring
- Performance attribution
- Factor analysis plots

**Skills needed**: Data visualization, web development

### 6. Testing

- Unit tests for all modules
- Integration tests
- Performance benchmarking
- Data validation tests

**Skills needed**: Testing, pytest, Python

### 7. Documentation

- Tutorial notebooks
- Code examples
- API documentation
- Video tutorials

**Skills needed**: Technical writing, teaching

### 8. Infrastructure

- CI/CD pipeline setup
- Docker containerization
- Cloud deployment (AWS/GCP/Azure)
- Monitoring and logging

**Skills needed**: DevOps, cloud platforms

## Questions?

If you have any questions, feel free to:

- Open an issue
- Email: your.email@example.com
- Start a discussion on GitHub

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Project documentation
- Release notes

Thank you for contributing! 🙏
