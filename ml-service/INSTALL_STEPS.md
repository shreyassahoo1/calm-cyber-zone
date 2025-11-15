# Installation Steps - Run These Commands

## Quick Installation (Copy and Paste)

### Step 1: Navigate to ML Service Directory
```bash
cd ml-service
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Upgrade pip
```bash
python -m pip install --upgrade pip
```

### Step 5: Install Dependencies
```bash
pip install -r requirements.txt
```

**⏰ This will take 10-15 minutes** - PyTorch and Transformers are large packages!

### Step 6: Verify Installation
```bash
python verify_installation.py
```

### Step 7: Run the Service
```bash
python main.py
```

## What to Expect

1. **Step 5 will take the longest** - You'll see progress bars for:
   - fastapi, uvicorn, pydantic (quick, ~1 minute)
   - numpy, pandas, scikit-learn (medium, ~2-3 minutes)
   - torch (LONG, ~5-8 minutes) - This is the big one!
   - transformers (medium, ~3-5 minutes)
   - langdetect, datasets (quick, ~1 minute)

2. **First run of the service** will download models (~5-10 minutes):
   - Toxicity model: ~440 MB
   - Sentiment model: ~500 MB

## If Installation Fails

If you get errors, try installing in smaller batches:

```bash
# Basic packages first
pip install fastapi uvicorn pydantic python-multipart requests

# Scientific libraries
pip install numpy pandas scikit-learn

# ML libraries (these take longest)
pip install torch transformers

# Language detection
pip install langdetect datasets
```

## Troubleshooting

### "Module not found" after installation
- Make sure virtual environment is activated
- Check: `pip list` should show all packages

### "Permission denied" errors
- Make sure you're in the virtual environment
- Try: `python -m pip install -r requirements.txt`

### Installation is too slow
- This is normal! PyTorch is ~2GB
- Be patient, it's a one-time setup
- Make sure you have good internet connection

## That's It!

Once installation completes:
1. Verify: `python verify_installation.py`
2. Run service: `python main.py`
3. Test: Open browser to `http://localhost:8000`

Good luck! 🚀

