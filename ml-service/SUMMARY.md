# SafeGuard ML Service - Summary

## What I've Created

I've built a complete **real-time ML service** for your SafeGuard Platform that detects cyberbullying, toxicity, threats, and sentiment in messages from Discord and Reddit.

## What's Included

### ✅ Core ML Service
- **FastAPI service** (`main.py`) - REST API for text analysis
- **Text Predictor** (`predictor.py`) - ML model loading and prediction
- **Free pre-trained models** - No API costs, runs locally

### ✅ Features
- **Toxicity Detection** - Detects toxic, abusive, and harmful content
- **Sentiment Analysis** - Analyzes sentiment (positive, neutral, negative)
- **Threat Detection** - Identifies threats and violent language
- **Severity Classification** - Classifies incidents (low, medium, high, critical)

### ✅ Integration
- **Discord Bot Example** (`discord_bot_example.py`) - Full integration example
- **API Test Script** (`test_api.py`) - Test the API endpoints
- **Supabase Integration** - Save incidents to your database

### ✅ Documentation
- **Quick Start Guide** (`QUICK_START.md`) - Get started in 5 minutes
- **Setup Guide** (`SETUP_GUIDE.md`) - Detailed setup instructions
- **Architecture** (`ARCHITECTURE.md`) - System architecture overview
- **README** (`README.md`) - API documentation

### ✅ Scripts
- **Start Scripts** (`start.sh`, `start.bat`) - Easy startup
- **Requirements** (`requirements.txt`) - Python dependencies
- **Bot Requirements** (`requirements_bot.txt`) - Discord bot dependencies

## Models Used

1. **Toxicity Model**: `unitary/toxic-bert`
   - Detects: toxic, severe_toxic, obscene, threat, insult, identity_hate
   - Size: ~440 MB
   - Free, open-source

2. **Sentiment Model**: `cardiffnlp/twitter-roberta-base-sentiment-latest`
   - Detects: negative, neutral, positive
   - Size: ~500 MB
   - Free, open-source

## How It Works

1. **Discord Bot** receives a message
2. **Bot calls ML Service** API (`POST /analyze`)
3. **ML Service analyzes** the text:
   - Toxicity score (0.0 to 1.0)
   - Sentiment score (-1.0 to 1.0)
   - Threat detection (boolean)
   - Severity classification (low, medium, high, critical)
4. **Service returns** analysis results
5. **Bot processes** results:
   - If severity is high/critical: Save to Supabase
   - If threat detected: Delete message, alert moderators
   - If toxic: Log incident

## Quick Start

1. **Install Dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run the Service**:
   ```bash
   python main.py
   ```

3. **Test the Service**:
   ```bash
   python test_api.py
   ```

4. **Integrate with Discord Bot**:
   - See `discord_bot_example.py` for full example
   - Add the code to your Discord bot
   - Call the API for each message

## API Endpoints

### Health Check
```bash
GET /health
```

### Analyze Text
```bash
POST /analyze
Content-Type: application/json

{
  "text": "Your text to analyze",
  "platform": "discord"
}
```

### Response
```json
{
  "toxicity_score": 0.85,
  "sentiment_score": -0.92,
  "severity": "critical",
  "is_threat": true,
  "confidence": 0.85,
  "details": {
    "toxicity_breakdown": {...},
    "sentiment_breakdown": {...},
    "threat_analysis": {...},
    "severity_reasoning": {...}
  }
}
```

## Severity Classification

- **Critical**: Threats detected OR toxicity >= 0.8
- **High**: Toxicity >= 0.6
- **Medium**: Toxicity >= 0.4
- **Low**: Toxicity < 0.4

## Integration with Discord Bot

```python
import requests

ML_SERVICE_URL = "http://localhost:8000"

def analyze_message(text: str):
    response = requests.post(
        f"{ML_SERVICE_URL}/analyze",
        json={"text": text, "platform": "discord"},
        timeout=5
    )
    return response.json()

# In your message handler
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    analysis = analyze_message(message.content)
    
    if analysis["severity"] in ["high", "critical"]:
        # Save to Supabase, delete message, etc.
        pass
```

## Integration with Supabase

```python
from supabase import create_client

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Save incident
incident = {
    "platform": "discord",
    "severity": analysis["severity"],
    "content": message.content,
    "toxicity_score": analysis["toxicity_score"],
    "sentiment_score": analysis["sentiment_score"],
    "author_id": str(message.author.id),
    "author_name": message.author.name,
    ...
}

supabase.table("incidents").insert(incident).execute()
```

## Performance

- **First Request**: ~2-5 seconds (models load into memory)
- **Subsequent Requests**: ~100-500ms per message
- **Memory Usage**: ~2-3GB RAM
- **CPU Usage**: Moderate (depends on message length)

## Deployment

### Local Development
```bash
python main.py
```

### Production (Railway/Render)
1. Create `Procfile`:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
2. Deploy to Railway or Render
3. Set environment variables
4. Service will be available at your deployed URL

## Free & Open Source

- ✅ **No API costs** - All models are free
- ✅ **Runs locally** - No external API calls
- ✅ **Open source** - All models are open-source
- ✅ **Privacy** - All processing happens locally
- ✅ **No limits** - No rate limits or quotas

## Next Steps

1. ✅ Set up the ML service (see `QUICK_START.md`)
2. ✅ Test with `test_api.py`
3. ✅ Integrate with your Discord bot (see `discord_bot_example.py`)
4. ✅ Deploy to production (optional)
5. ✅ Monitor performance and adjust thresholds

## Files Created

```
ml-service/
├── main.py                  # FastAPI service
├── predictor.py             # ML model loading and prediction
├── requirements.txt         # Python dependencies
├── requirements_bot.txt     # Discord bot dependencies
├── discord_bot_example.py   # Discord bot integration example
├── test_api.py             # API test script
├── README.md               # API documentation
├── QUICK_START.md          # Quick start guide
├── SETUP_GUIDE.md          # Detailed setup guide
├── ARCHITECTURE.md         # System architecture
├── SUMMARY.md              # This file
├── start.sh                # Startup script (Linux/Mac)
├── start.bat               # Startup script (Windows)
└── .gitignore             # Git ignore file
```

## Support

- **Quick Start**: See `QUICK_START.md`
- **Setup**: See `SETUP_GUIDE.md`
- **Architecture**: See `ARCHITECTURE.md`
- **API Docs**: See `README.md`
- **Discord Bot**: See `discord_bot_example.py`

## Troubleshooting

### Models Not Loading
- Check internet connection
- Wait for download (5-10 minutes first time)
- Check disk space (need ~2GB)

### Service Not Starting
- Check Python version (need 3.9+)
- Check if port 8000 is available
- Check for errors in console

### Slow Performance
- First request is slower (models loading)
- Subsequent requests are faster
- Normal: ~100-500ms per message

## That's It! 🎉

Your ML service is ready to use! Follow the `QUICK_START.md` guide to get started.

## Questions?

Check the documentation files:
- `QUICK_START.md` - Quick start guide
- `SETUP_GUIDE.md` - Detailed setup
- `ARCHITECTURE.md` - System architecture
- `README.md` - API documentation

Happy coding! 🚀

