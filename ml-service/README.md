# SafeGuard ML Service

Real-time cyberbullying detection service using pre-trained machine learning models.

## Features

- **Toxicity Detection**: Detects toxic, abusive, and harmful content
- **Sentiment Analysis**: Analyzes sentiment (positive, neutral, negative)
- **Threat Detection**: Identifies threats and violent language
- **Severity Classification**: Classifies incidents as low, medium, high, or critical

## Models Used

1. **Toxicity Model**: `unitary/toxic-bert`
   - Lightweight BERT model trained for toxicity detection
   - Detects multiple toxic categories

2. **Sentiment Model**: `cardiffnlp/twitter-roberta-base-sentiment-latest`
   - RoBERTa model trained on Twitter data
   - Good for social media text analysis

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Service

### Development Mode
```bash
python main.py
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

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
  "text": "Your text to analyze here",
  "platform": "discord"  # optional
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
    "toxicity_breakdown": {
      "score": 0.85,
      "level": "high"
    },
    "sentiment_breakdown": {
      "score": -0.92,
      "label": "negative"
    },
    "threat_analysis": {
      "detected": true,
      "reason": "threat_keywords"
    },
    "severity_reasoning": {
      "severity": "critical",
      "factors": {
        "toxicity": 0.85,
        "sentiment": -0.92,
        "threat": true
      }
    }
  }
}
```

## Integration with Discord Bot

Your Discord bot can call this API for each message:

```python
import requests

def analyze_message(text):
    response = requests.post(
        "http://localhost:8000/analyze",
        json={"text": text, "platform": "discord"}
    )
    return response.json()

# Example usage
result = analyze_message("Some toxic message here")
if result["severity"] in ["high", "critical"]:
    # Handle incident
    pass
```

## Severity Classification

- **Critical**: Threats detected or toxicity score >= 0.8
- **High**: Toxicity score >= 0.6
- **Medium**: Toxicity score >= 0.4
- **Low**: Toxicity score < 0.4

## Notes

- Models are downloaded automatically on first run (requires internet)
- First request may be slower as models load into memory
- Runs entirely locally - no external API calls needed
- Free to use (all models are open-source)

## Deployment

For production deployment, consider:

1. **Railway** (Free tier available)
2. **Render** (Free tier available)
3. **Google Cloud Run** (Pay per use)
4. **AWS Lambda** (Serverless)

Make sure to set environment variables and adjust port/host as needed.

