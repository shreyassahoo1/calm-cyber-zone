from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
import sys
import traceback
import os

# Use multilingual predictor if MULTILINGUAL env var is set to "true"
USE_MULTILINGUAL = os.getenv("MULTILINGUAL", "true").lower() == "true"

if USE_MULTILINGUAL:
    try:
        from predictor_multilingual import MultilingualTextPredictor as TextPredictor
        print("Using multilingual predictor (supports English, Kannada, Hindi)")
    except ImportError:
        print("Warning: Multilingual predictor not available. Using English-only predictor.")
        from predictor import TextPredictor
else:
    from predictor import TextPredictor
    print("Using English-only predictor")

app = FastAPI(
    title="SafeGuard ML Service",
    description="Real-time cyberbullying detection API",
    version="1.0.0"
)

# Initialize the predictor (loads models on startup)
try:
    predictor = TextPredictor()
except Exception as e:
    print(f"Error loading models: {e}")
    print(traceback.format_exc())
    print("Please check your internet connection and try again.")
    sys.exit(1)

class TextAnalysisRequest(BaseModel):
    text: str
    platform: Optional[str] = "discord"

class TextAnalysisResponse(BaseModel):
    toxicity_score: float
    sentiment_score: float
    severity: str
    is_threat: bool
    confidence: float
    detected_language: Optional[str] = "unknown"
    details: dict

@app.get("/")
async def root():
    return {
        "service": "SafeGuard ML Service",
        "status": "running",
        "version": "1.0.0",
        "multilingual": USE_MULTILINGUAL,
        "supported_languages": ["en", "kn", "hi"] if USE_MULTILINGUAL else ["en"]
    }

@app.get("/health")
async def health_check():
    try:
        return {
            "status": "healthy",
            "models_loaded": predictor.models_loaded if hasattr(predictor, 'models_loaded') else False
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "models_loaded": False
        }

@app.post("/analyze", response_model=TextAnalysisResponse)
async def analyze_text(request: TextAnalysisRequest):
    """
    Analyze text for toxicity, sentiment, threats, and severity.
    Supports English, Kannada, Hindi, and code-mixed text (if multilingual mode enabled).
    
    Returns:
    - toxicity_score: 0.0 to 1.0 (higher = more toxic)
    - sentiment_score: -1.0 to 1.0 (-1 = negative, 0 = neutral, 1 = positive)
    - severity: 'low', 'medium', 'high', 'critical'
    - is_threat: boolean indicating if threat detected
    - confidence: overall confidence score
    - detected_language: detected language (en, kn, hi, mixed, unknown)
    - details: additional analysis details including language detection
    """
    try:
        if not request.text or len(request.text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        result = predictor.predict(request.text)
        
        # Ensure detected_language is in the response
        if "detected_language" not in result:
            result["detected_language"] = "unknown"
        
        return TextAnalysisResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing text: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

