# ML Service Architecture

## Overview

The SafeGuard ML Service is a real-time text analysis service that detects cyberbullying, toxicity, threats, and sentiment in messages from Discord and Reddit.

## Architecture

```
┌─────────────────┐
│  Discord Bot    │
│  (Your Bot)     │
└────────┬────────┘
         │
         │ HTTP POST /analyze
         │
         ▼
┌─────────────────┐
│  ML Service     │
│  (FastAPI)      │
│  Port: 8000     │
└────────┬────────┘
         │
         ├─────────────────┐
         │                 │
         ▼                 ▼
┌─────────────┐   ┌─────────────┐
│  Toxicity   │   │  Sentiment  │
│  Model      │   │  Model      │
│  (BERT)     │   │  (RoBERTa)  │
└─────────────┘   └─────────────┘
         │                 │
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────┐
         │  Analysis   │
         │  Results    │
         └─────────────┘
                  │
                  ▼
         ┌─────────────┐
         │  Supabase   │
         │  Database   │
         └─────────────┘
```

## Components

### 1. ML Service (FastAPI)

- **Location**: `main.py`
- **Port**: 8000
- **Endpoints**:
  - `GET /health` - Health check
  - `POST /analyze` - Analyze text

### 2. Text Predictor

- **Location**: `predictor.py`
- **Function**: Loads models and performs predictions
- **Models**:
  - Toxicity: `unitary/toxic-bert`
  - Sentiment: `cardiffnlp/twitter-roberta-base-sentiment-latest`

### 3. Models

#### Toxicity Model (`unitary/toxic-bert`)

- **Type**: Multi-label classification
- **Labels**: toxic, severe_toxic, obscene, threat, insult, identity_hate
- **Output**: Probability scores for each label (0.0 to 1.0)
- **Size**: ~440 MB

#### Sentiment Model (`cardiffnlp/twitter-roberta-base-sentiment-latest`)

- **Type**: Three-class classification
- **Labels**: negative, neutral, positive
- **Output**: Probability scores for each class
- **Size**: ~500 MB

### 4. Analysis Pipeline

1. **Text Input**: Receive text from Discord/Reddit
2. **Toxicity Detection**: Run through toxicity model
3. **Sentiment Analysis**: Run through sentiment model
4. **Threat Detection**: Combine model output + keyword matching
5. **Severity Classification**: Determine severity (low, medium, high, critical)
6. **Response**: Return analysis results

## Data Flow

```
1. Discord Bot receives message
2. Bot calls ML Service API
3. ML Service analyzes text:
   a. Toxicity score (0.0 to 1.0)
   b. Sentiment score (-1.0 to 1.0)
   c. Threat detection (boolean)
   d. Severity classification (low, medium, high, critical)
4. ML Service returns results
5. Bot processes results:
   a. If severity is high/critical: Save to Supabase
   b. If threat detected: Delete message, alert moderators
   c. If toxic: Log incident
6. Bot updates Supabase:
   a. Insert incident record
   b. Update bot status
```

## Response Format

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

- **Critical**: Threats detected OR toxicity >= 0.8
- **High**: Toxicity >= 0.6
- **Medium**: Toxicity >= 0.4
- **Low**: Toxicity < 0.4

## Threat Detection

Threats are detected using:

1. **Model Detection**: Toxicity model's threat label > 0.5
2. **Keyword Matching**: Threat keywords found in text
3. **High Toxicity**: Toxicity score > 0.8

## Performance

- **First Request**: ~2-5 seconds (models load into memory)
- **Subsequent Requests**: ~100-500ms per message
- **Memory Usage**: ~2-3GB RAM
- **CPU Usage**: Moderate (depends on message length)

## Scalability

- **Single Instance**: Can handle ~10-20 requests/second
- **Multiple Instances**: Use load balancer for higher throughput
- **Caching**: Consider caching for frequently analyzed messages
- **Queue**: Use message queue for high-volume processing

## Security

- **Local Processing**: All processing happens locally
- **No External APIs**: No data sent to external services
- **Open Source Models**: All models are open-source
- **Free**: No API costs

## Deployment Options

1. **Local Development**: Run on local machine
2. **Railway**: Free tier available
3. **Render**: Free tier available
4. **Docker**: Containerized deployment
5. **AWS/GCP**: Cloud deployment

## Integration

### Discord Bot

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
```

### Supabase

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
    ...
}

supabase.table("incidents").insert(incident).execute()
```

## Monitoring

- **Health Check**: `GET /health`
- **Logs**: Check console output
- **Metrics**: Monitor response times, error rates
- **Alerts**: Set up alerts for service downtime

## Future Improvements

1. **GPU Support**: Use GPU for faster inference
2. **Model Caching**: Cache model predictions
3. **Batch Processing**: Process multiple messages at once
4. **Custom Models**: Train custom models on your data
5. **A/B Testing**: Test different models
6. **Real-time Streaming**: Stream analysis results

