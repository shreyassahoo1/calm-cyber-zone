# Quick Installation Guide

## Step 1: Navigate to ML Service Directory

```bash
cd ml-service
```

## Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
```

**macOS/Linux:**
```bash
python3 -m venv venv
```

## Step 3: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

## Step 4: Upgrade pip

```bash
python -m pip install --upgrade pip
```

## Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** This may take 10-15 minutes because:
- PyTorch is large (~2GB)
- Transformers library is large (~500MB)
- Models will be downloaded on first run

## Step 6: Verify Installation

```bash
python verify_installation.py
```

## Step 7: Run the Service

```bash
python main.py
```

The service will start on `http://localhost:8000`

## Troubleshooting

### If installation fails:

1. **Try installing packages individually:**
   ```bash
   pip install fastapi uvicorn pydantic
   pip install torch transformers
   pip install numpy pandas scikit-learn
   pip install langdetect datasets requests
   ```

2. **Check internet connection** (models download on first run)

3. **Check disk space** (need ~2GB free)

4. **Check Python version** (need 3.9+)

## That's It!

Once installation is complete, you can run the service!

