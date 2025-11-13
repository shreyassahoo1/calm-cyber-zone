# What to Do After Installation

## 1. Verify Installation

```bash
python verify_installation.py
```

You should see:
```
✅ fastapi
✅ uvicorn
✅ pydantic
✅ torch
✅ transformers
✅ numpy
✅ langdetect
✅ datasets
✅ sklearn
✅ pandas
✅ requests
✅ All packages are installed correctly!
```

## 2. Start the ML Service

```bash
python main.py
```

You should see:
```
Loading models for multilingual support...
Loading toxicity model (English, works for code-mixed text)...
✓ Toxicity model loaded
Loading multilingual sentiment model...
✓ Multilingual sentiment model loaded
All models loaded successfully!
Multilingual support: English (full), Kannada/Hindi (keyword-based + sentiment)
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**⏰ First run will download models (5-10 minutes)** - This is normal!

## 3. Test the Service

Open a new terminal and run:

```bash
python test_api.py
```

Or test manually:

```bash
# Health check
curl http://localhost:8000/health

# Test analysis
curl -X POST http://localhost:8000/analyze -H "Content-Type: application/json" -d "{\"text\": \"Hello, how are you?\", \"platform\": \"discord\"}"
```

## 4. Test Multilingual Support

```bash
python test_multilingual.py
```

This will test:
- English text
- Kannada text
- Hindi text
- Code-mixed text

## Common Issues

### Models not loading
- **First run takes 5-10 minutes** to download models
- Check internet connection
- Check disk space (need ~2GB free)
- Models are downloaded to `~/.cache/huggingface/`

### Service not starting
- Check if port 8000 is available
- Check for errors in console
- Make sure all packages are installed

### "Module not found" errors
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt` again

## Next Steps

1. ✅ Install dependencies
2. ✅ Verify installation
3. ✅ Start ML service
4. ✅ Test with test scripts
5. ✅ Integrate with Discord bot

## That's It!

Your ML service is now running and ready to analyze messages! 🎉

