# Quick Start Guide

Get the ML service running in 5 minutes!

## Step 1: Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Run the Service

```bash
python main.py
```

The service will start on `http://localhost:8000`

**Note**: First run will download models (5-10 minutes). Be patient!

## Step 3: Test the Service

In a new terminal:

```bash
python test_api.py
```

Or test manually:

```bash
# Test health
curl http://localhost:8000/health

# Test analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I hate you!", "platform": "discord"}'
```

## Step 4: Integrate with Discord Bot

Add this to your Discord bot:

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
        # Handle incident - save to Supabase, delete message, etc.
        print(f"⚠️ Incident detected: {analysis['severity']}")
```

## That's it! 🎉

Your ML service is now running and ready to analyze messages!

## Next Steps

- See `SETUP_GUIDE.md` for detailed setup
- See `discord_bot_example.py` for full integration example
- See `README.md` for API documentation

## Troubleshooting

**Models not loading?**
- Check internet connection
- Wait for download (5-10 minutes first time)
- Check disk space (need ~2GB)

**Service not starting?**
- Check Python version (need 3.9+)
- Check if port 8000 is available
- Check for errors in console

**Slow performance?**
- First request is slower (models loading)
- Subsequent requests are faster
- Normal: ~100-500ms per message

## Need Help?

Check `SETUP_GUIDE.md` for detailed troubleshooting!

