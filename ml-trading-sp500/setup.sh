#!/bin/bash

# ML Trading Strategy - Setup Script
# This script sets up the development environment

set -e  # Exit on error

echo "========================================"
echo "ML Trading Strategy - Setup Script"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Check if Python >= 3.8
required_version="3.8"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.8 or higher is required"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

echo "✓ Python version OK"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists"
    read -p "Do you want to recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo "✓ Virtual environment recreated"
    fi
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
echo "This may take a few minutes..."
pip install -r requirements.txt --quiet
echo "✓ Dependencies installed"
echo ""

# Create necessary directories
echo "Creating project directories..."
mkdir -p data models results
echo "✓ Directories created"
echo ""

# Test imports
echo "Testing imports..."
python test_imports.py
if [ $? -eq 0 ]; then
    echo "✓ All imports successful"
else
    echo "✗ Import test failed"
    echo "Please check error messages above"
    exit 1
fi
echo ""

echo "========================================"
echo "Setup completed successfully! ✓"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Run the pipeline:"
echo "   python main.py"
echo ""
echo "3. Or explore interactively:"
echo "   jupyter notebook notebooks/01_data_exploration.ipynb"
echo ""
echo "For more information, see QUICKSTART.md"
echo ""
