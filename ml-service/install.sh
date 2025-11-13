#!/bin/bash

# SafeGuard ML Service - Installation Script (Linux/Mac)

echo "========================================="
echo "SafeGuard ML Service - Installation"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

# Check if Python 3.9+
if python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
    echo "✅ Python version is 3.9 or higher"
else
    echo "ERROR: Python 3.9 or higher is required"
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

echo ""
echo "========================================="
echo "Creating virtual environment..."
echo "========================================="
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo ""
echo "========================================="
echo "Activating virtual environment..."
echo "========================================="
source venv/bin/activate

echo ""
echo "========================================="
echo "Upgrading pip..."
echo "========================================="
pip install --upgrade pip

echo ""
echo "========================================="
echo "Installing dependencies..."
echo "========================================="
echo "This may take 10-15 minutes (downloading large packages)..."
echo "Please be patient, especially for PyTorch and Transformers"
echo ""
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo ""
    echo "WARNING: Some packages may not have installed correctly"
    echo "Try installing manually: pip install -r requirements.txt"
    exit 1
fi

echo ""
echo "========================================="
echo "Verifying installation..."
echo "========================================="
python verify_installation.py
if [ $? -ne 0 ]; then
    echo ""
    echo "WARNING: Installation verification failed"
    echo "Please check the errors above"
    exit 1
fi

echo ""
echo "========================================="
echo "Installation completed successfully!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Run the ML service:"
echo "   python main.py"
echo ""

