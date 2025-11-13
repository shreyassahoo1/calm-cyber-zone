# SafeGuard ML Service - Setup Guide

This guide will help you set up and run the ML service for your SafeGuard Platform.

## Prerequisites

1. **Python 3.9 or higher**
   - Check your Python version: `python --version`
   - Download from: https://www.python.org/downloads/

2. **Internet connection** (for downloading models on first run)

3. **At least 2GB RAM** (models need memory)

## Installation Steps

### 1. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
cd ml-service
pip install -r requirements.txt
```

**Note**: The first installation may take a few minutes as it downloads PyTorch and other large packages.

### 3. Run the Service

```bash
# Development mode
python main.py

# Or production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

The service will start on `http://localhost:8000`

**First Run**: The models will be downloaded automatically (this may take 5-10 minutes). Subsequent runs will be faster.

### 4. Test the Service

In a new terminal, run:

```bash
python test_api.py
```

Or manually test with curl:

```bash
# Health check
curl http://localhost:8000/health

# Analyze text
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test message", "platform": "discord"}'
```

## Integration with Discord Bot

### 1. Update Your Discord Bot

Add this code to your Discord bot to call the ML service:

```python
import requests

ML_SERVICE_URL = "http://localhost:8000"

def analyze_message(text: str):
    """Call ML service to analyze a message"""
    try:
        response = requests.post(
            f"{ML_SERVICE_URL}/analyze",
            json={"text": text, "platform": "discord"},
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling ML service: {e}")
        return None

# In your message handler
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    analysis = analyze_message(message.content)
    
    if analysis:
        if analysis["severity"] in ["high", "critical"]:
            # Handle incident
            # Save to Supabase, delete message, etc.
            pass
```

### 2. Environment Variables

Create a `.env` file or set environment variables:

```bash
ML_SERVICE_URL=http://localhost:8000
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
DISCORD_TOKEN=your-discord-bot-token
```

### 3. Full Example

See `discord_bot_example.py` for a complete integration example.

## API Reference

### Health Check

```bash
GET /health
```

Returns:
```json
{
  "status": "healthy",
  "models_loaded": true
}
```

### Analyze Text

```bash
POST /analyze
Content-Type: application/json

{
  "text": "Your text to analyze",
  "platform": "discord"  // optional
}
```

Returns:
```json
{
  "toxicity_score": 0.85,
  "sentiment_score": -0.92,
  "severity": "critical",
  "is_threat": true,
  "confidence": 0.85,
  "details": {
    "toxicity_breakdown": {
      "score": 0.85,
      "level": "high",
      "labels": {
        "toxic": 0.85,
        "severe_toxic": 0.72,
        "obscene": 0.45,
        "threat": 0.91,
        "insult": 0.78,
        "identity_hate": 0.23
      }
    },
    "sentiment_breakdown": {
      "score": -0.92,
      "label": "negative"
    },
    "threat_analysis": {
      "detected": true,
      "model_probability": 0.91,
      "reason": "model_detection"
    },
    "severity_reasoning": {
      "severity": "critical",
      "factors": {
        "toxicity": 0.85,
        "sentiment": -0.92,
        "threat": true,
        "threat_probability": 0.91
      }
    }
  }
}
```

## Severity Classification

- **Critical**: Threats detected or toxicity score >= 0.8
- **High**: Toxicity score >= 0.6
- **Medium**: Toxicity score >= 0.4
- **Low**: Toxicity score < 0.4

## Models Used

1. **Toxicity Model**: `unitary/toxic-bert`
   - Multi-label classification
   - Detects: toxic, severe_toxic, obscene, threat, insult, identity_hate
   - Size: ~440 MB

2. **Sentiment Model**: `cardiffnlp/twitter-roberta-base-sentiment-latest`
   - Three-class classification: negative, neutral, positive
   - Trained on Twitter data (good for social media)
   - Size: ~500 MB

## Troubleshooting

### Models Not Loading

- Check your internet connection
- Models are downloaded to `~/.cache/huggingface/`
- Ensure you have at least 2GB free disk space

### Out of Memory

- Close other applications
- Use CPU mode (models will be slower)
- Reduce batch size if processing multiple messages

### API Not Responding

- Check if service is running: `curl http://localhost:8000/health`
- Check port conflicts: `netstat -an | grep 8000`
- Check logs for errors

### Slow Response Times

- First request is slower (models load into memory)
- Subsequent requests are faster
- Consider using GPU for faster inference (optional)

## Deployment

### Local Development

```bash
python main.py
```

### Production (Railway/Render)

1. Create a `Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. Set environment variables:
- `PORT`: Server port (usually set by hosting platform)

3. Deploy to Railway or Render:
- Connect your repository
- Set Python version: 3.9+
- Install dependencies: `pip install -r requirements.txt`
- Run: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Docker (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t safeguard-ml .
docker run -p 8000:8000 safeguard-ml
```

## Performance

- **First request**: ~2-5 seconds (models load)
- **Subsequent requests**: ~100-500ms per message
- **Memory usage**: ~2-3GB RAM
- **CPU usage**: Moderate (depends on message length)

## Security

- The service runs locally - no external API calls
- All models are open-source and free
- No data is sent to external services
- All processing happens on your server

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the logs for errors
3. Test with `test_api.py`
4. Check model loading: `GET /health`

## Next Steps

1. ✅ Set up the ML service
2. ✅ Test with `test_api.py`
3. ✅ Integrate with your Discord bot
4. ✅ Deploy to production (optional)
5. ✅ Monitor performance and adjust thresholds

Enjoy using SafeGuard ML Service! 🚀

