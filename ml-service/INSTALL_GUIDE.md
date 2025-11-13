# Installation Guide - ML Service

Complete guide to install and set up the SafeGuard ML Service.

## Quick Installation

### Option 1: Automated Setup (Recommended)

```bash
cd ml-service
python setup.py
```

This will:
- Check Python version
- Create virtual environment
- Install all dependencies
- Verify installation

### Option 2: Manual Installation

```bash
cd ml-service

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

## Step-by-Step Installation

### 1. Check Python Version

Make sure you have Python 3.9 or higher:

```bash
python --version
```

If you don't have Python 3.9+, download it from https://www.python.org/downloads/

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Upgrade pip

```bash
pip install --upgrade pip
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** This may take 10-15 minutes because:
- PyTorch is large (~2GB)
- Transformers library is large (~500MB)
- Models will be downloaded on first run

### 6. Verify Installation

```bash
python verify_installation.py
```

Or manually check:

```bash
python -c "import torch; import transformers; import fastapi; print('All packages installed!')"
```

## Required Packages

- **fastapi** - Web framework for API
- **uvicorn** - ASGI server
- **pydantic** - Data validation
- **torch** - PyTorch (deep learning framework)
- **transformers** - Hugging Face Transformers (ML models)
- **numpy** - Numerical computing
- **langdetect** - Language detection
- **datasets** - Dataset handling
- **scikit-learn** - Machine learning utilities
- **pandas** - Data manipulation
- **requests** - HTTP library

## Troubleshooting

### Issue: Python version too old

**Solution:** Install Python 3.9 or higher

### Issue: pip install fails

**Solution:** 
1. Upgrade pip: `pip install --upgrade pip`
2. Try installing packages individually
3. Check internet connection
4. Try using `pip install --no-cache-dir -r requirements.txt`

### Issue: PyTorch installation fails

**Solution:**
1. Check your system (CPU/GPU)
2. Install PyTorch separately:
   ```bash
   pip install torch torchvision torchaudio
   ```
3. Then install other requirements

### Issue: Transformers installation fails

**Solution:**
1. Make sure PyTorch is installed first
2. Try: `pip install transformers --no-cache-dir`
3. Check disk space (need ~2GB free)

### Issue: Virtual environment not activating

**Windows:**
- Make sure you're in the correct directory
- Try: `.\venv\Scripts\activate`
- If that doesn't work, check if PowerShell execution policy allows scripts

**macOS/Linux:**
- Make sure you have execute permissions
- Try: `chmod +x venv/bin/activate`
- Then: `source venv/bin/activate`

### Issue: Models not downloading

**Solution:**
1. Check internet connection
2. Models download on first run (5-10 minutes)
3. Check disk space (need ~2GB for models)
4. Check Hugging Face connectivity

### Issue: Memory errors

**Solution:**
1. Close other applications
2. Models need ~2-3GB RAM
3. Consider using CPU-only PyTorch (smaller)
4. Reduce batch size if processing multiple messages

## Verification

After installation, verify everything works:

```bash
# Check packages
python verify_installation.py

# Test ML service
python main.py
```

The service should start on `http://localhost:8000`

## Next Steps

1. ✅ Install dependencies
2. ✅ Verify installation
3. ✅ Start ML service: `python main.py`
4. ✅ Test with: `python test_api.py`
5. ✅ Integrate with Discord bot

## System Requirements

- **Python:** 3.9 or higher
- **RAM:** 2-3GB (for models)
- **Disk Space:** ~2GB (for models)
- **Internet:** Required for first run (downloading models)

## Support

If you encounter issues:
1. Check the troubleshooting section
2. Run `python verify_installation.py`
3. Check logs for errors
4. Make sure all dependencies are installed

## Common Issues

### "Module not found" errors

**Solution:** Make sure virtual environment is activated and packages are installed

### "Permission denied" errors

**Solution:** 
- Windows: Run as administrator
- macOS/Linux: Use `sudo` if needed (but prefer virtual environment)

### "Out of memory" errors

**Solution:**
- Close other applications
- Use CPU-only PyTorch
- Reduce model size

### "Connection timeout" errors

**Solution:**
- Check internet connection
- Models download on first run
- May take 5-10 minutes

## That's It!

Once installation is complete, you can:
1. Start the ML service: `python main.py`
2. Test it: `python test_api.py`
3. Integrate with Discord bot

Happy coding! 🚀

