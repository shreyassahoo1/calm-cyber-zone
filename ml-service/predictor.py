import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from typing import Dict, Tuple
import re

class TextPredictor:
    """
    Text analysis predictor using pre-trained models for:
    - Toxicity detection
    - Sentiment analysis
    - Threat detection
    - Severity classification
    """
    
    def __init__(self):
        self.models_loaded = False
        self.toxicity_tokenizer = None
        self.toxicity_model = None
        self.sentiment_tokenizer = None
        self.sentiment_model = None
        
        # Threat keywords (common threat patterns)
        self.threat_keywords = [
            'kill', 'murder', 'die', 'death', 'hurt', 'harm', 'attack',
            'destroy', 'bomb', 'shoot', 'stab', 'rape', 'suicide',
            'threat', 'threaten', 'violence', 'beat up', 'beat you',
            'end you', 'ruin you', 'destroy you', 'get you', 'revenge'
        ]
        
        self.load_models()
    
    def load_models(self):
        """Load pre-trained models from Hugging Face"""
        try:
            print("Loading toxicity model...")
            # Using a lightweight toxicity detection model
            toxicity_model_name = "unitary/toxic-bert"
            self.toxicity_tokenizer = AutoTokenizer.from_pretrained(toxicity_model_name)
            self.toxicity_model = AutoModelForSequenceClassification.from_pretrained(toxicity_model_name)
            self.toxicity_model.eval()  # Set to evaluation mode
            
            print("Loading sentiment model...")
            # Using Twitter RoBERTa for sentiment (good for social media text)
            sentiment_model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
            self.sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
            self.sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)
            self.sentiment_model.eval()
            
            self.models_loaded = True
            print("All models loaded successfully!")
            
        except Exception as e:
            print(f"Error loading models: {e}")
            raise
    
    def predict_toxicity(self, text: str) -> Tuple[float, dict]:
        """
        Predict toxicity score (0.0 to 1.0) and label probabilities
        Returns the overall toxicity probability and individual label probabilities
        """
        try:
            # Tokenize input
            inputs = self.toxicity_tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            )
            
            # Get prediction
            with torch.no_grad():
                outputs = self.toxicity_model(**inputs)
                logits = outputs.logits
                # Apply sigmoid for multi-label classification
                probs = torch.nn.functional.sigmoid(logits)
                
                # The model has 6 labels: toxic, severe_toxic, obscene, threat, insult, identity_hate
                # Each label is independent (multi-label classification)
                prob_scores = probs[0].cpu().numpy()
                
                # Label names (in order)
                labels = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
                label_probs = {label: float(prob) for label, prob in zip(labels, prob_scores)}
                
                # Overall toxicity score: max of all toxic labels or weighted average
                # Using max for more aggressive detection
                overall_toxicity = float(prob_scores.max())
                
                # Alternative: weighted average (weight threat and severe_toxic more)
                # weights = [1.0, 1.5, 1.0, 2.0, 1.0, 1.0]  # threat and severe_toxic weighted higher
                # weighted_avg = sum(w * p for w, p in zip(weights, prob_scores)) / sum(weights)
                
                return overall_toxicity, label_probs
                
        except Exception as e:
            print(f"Error in toxicity prediction: {e}")
            return 0.0, {}
    
    def predict_sentiment(self, text: str) -> float:
        """
        Predict sentiment score (-1.0 to 1.0)
        -1.0 = very negative, 0.0 = neutral, 1.0 = very positive
        """
        try:
            # Tokenize input
            inputs = self.sentiment_tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            )
            
            # Get prediction
            with torch.no_grad():
                outputs = self.sentiment_model(**inputs)
                logits = outputs.logits
                probs = torch.nn.functional.softmax(logits, dim=-1)
                
                # Model outputs: negative (0), neutral (1), positive (2)
                negative_prob = probs[0][0].item()
                neutral_prob = probs[0][1].item()
                positive_prob = probs[0][2].item()
                
                # Convert to -1 to 1 scale
                # Weighted average: negative = -1, neutral = 0, positive = 1
                sentiment_score = (positive_prob - negative_prob)
                
                return sentiment_score
                
        except Exception as e:
            print(f"Error in sentiment prediction: {e}")
            return 0.0
    
    def detect_threat(self, text: str, toxicity_score: float, threat_prob: float = None) -> bool:
        """
        Detect threats in text
        Uses keyword matching combined with toxicity score and model's threat label
        """
        text_lower = text.lower()
        
        # Check for threat keywords
        keyword_match = any(keyword in text_lower for keyword in self.threat_keywords)
        
        # Check if toxicity model detected threat label
        model_threat = threat_prob is not None and threat_prob > 0.5
        
        # Combine signals: keyword match OR model detection with high toxicity
        is_threat = False
        
        if model_threat:
            # Model detected threat
            is_threat = True
        elif keyword_match and toxicity_score > 0.3:
            # Keywords found with some toxicity
            is_threat = True
        elif toxicity_score > 0.8:
            # Very high toxicity might indicate threats
            is_threat = True
        
        return is_threat
    
    def classify_severity(self, toxicity_score: float, sentiment_score: float, is_threat: bool) -> str:
        """
        Classify severity: 'low', 'medium', 'high', 'critical'
        """
        if is_threat:
            return 'critical'
        
        if toxicity_score >= 0.8:
            return 'critical'
        elif toxicity_score >= 0.6:
            return 'high'
        elif toxicity_score >= 0.4:
            return 'medium'
        elif toxicity_score >= 0.2:
            return 'low'
        else:
            return 'low'
    
    def predict(self, text: str) -> Dict:
        """
        Main prediction function that returns all analysis results
        """
        # Get predictions
        toxicity_score, toxicity_labels = self.predict_toxicity(text)
        sentiment_score = self.predict_sentiment(text)
        
        # Get threat probability from model
        threat_prob = toxicity_labels.get('threat', 0.0)
        is_threat = self.detect_threat(text, toxicity_score, threat_prob)
        severity = self.classify_severity(toxicity_score, sentiment_score, is_threat)
        
        # Calculate overall confidence
        confidence = max(toxicity_score, abs(sentiment_score))
        
        # Prepare details
        details = {
            "toxicity_breakdown": {
                "score": round(toxicity_score, 3),
                "level": "high" if toxicity_score > 0.6 else "medium" if toxicity_score > 0.3 else "low",
                "labels": {
                    label: round(prob, 3) 
                    for label, prob in toxicity_labels.items()
                }
            },
            "sentiment_breakdown": {
                "score": round(sentiment_score, 3),
                "label": "positive" if sentiment_score > 0.2 else "negative" if sentiment_score < -0.2 else "neutral"
            },
            "threat_analysis": {
                "detected": is_threat,
                "model_probability": round(threat_prob, 3),
                "reason": "model_detection" if threat_prob > 0.5 else "keyword_match" if is_threat else "none"
            },
            "severity_reasoning": {
                "severity": severity,
                "factors": {
                    "toxicity": round(toxicity_score, 3),
                    "sentiment": round(sentiment_score, 3),
                    "threat": is_threat,
                    "threat_probability": round(threat_prob, 3)
                }
            }
        }
        
        return {
            "toxicity_score": round(toxicity_score, 3),
            "sentiment_score": round(sentiment_score, 3),
            "severity": severity,
            "is_threat": is_threat,
            "confidence": round(confidence, 3),
            "details": details
        }

