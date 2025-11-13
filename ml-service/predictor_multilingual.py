import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import numpy as np
from typing import Dict, Tuple, Optional
import re
from langdetect import detect, LangDetectException

class MultilingualTextPredictor:
    """
    Multilingual text analysis predictor using pre-trained models for:
    - Toxicity detection (English, Kannada, Hindi)
    - Sentiment analysis (English, Kannada, Hindi)
    - Threat detection (English, Kannada, Hindi)
    - Severity classification
    - Language detection
    - Code-mixing support
    """
    
    def __init__(self, use_multilingual: bool = True):
        self.models_loaded = False
        self.use_multilingual = use_multilingual
        self.toxicity_tokenizer = None
        self.toxicity_model = None
        self.sentiment_tokenizer = None
        self.sentiment_model = None
        self.language_detector = None
        
        # Threat keywords - English
        self.threat_keywords_en = [
            'kill', 'murder', 'die', 'death', 'hurt', 'harm', 'attack',
            'destroy', 'bomb', 'shoot', 'stab', 'rape', 'suicide',
            'threat', 'threaten', 'violence', 'beat up', 'beat you',
            'end you', 'ruin you', 'destroy you', 'get you', 'revenge'
        ]
        
        # Threat keywords - Kannada (transliterated and in Kannada script)
        self.threat_keywords_kn = [
            # Transliterated
            'kollu', 'kol', 'sathisu', 'sathi', 'mare', 'chakke', 'chakka',
            'nayi', 'huli', 'puli', 'thika muchkond', 'thika muchko',
            # Kannada script (common toxic words)
            'ಕೊಲ್ಲು', 'ಕೊಲೆ', 'ಸಾಯು', 'ಸಾಯಿಸು', 'ಮಾರು', 'ಚಕ್ಕೆ', 'ಚಕ್ಕಾ',
            'ನಾಯಿ', 'ಹುಲಿ', 'ಪುಲಿ', 'ತಿಕ ಮುಚ್ಕೊಂಡ್', 'ತಿಕ ಮುಚ್ಕೊ'
        ]
        
        # Threat keywords - Hindi (transliterated and in Devanagari)
        self.threat_keywords_hi = [
            # Transliterated
            'maar', 'maarunga', 'maarunga', 'mar', 'marunga', 'mar ja',
            'mar dunga', 'maar dunga', 'khatam', 'khatam kar', 'khatam kar dunga',
            'teri', 'tujhe', 'tu', 'teri maa', 'behen', 'behenchod', 'madarchod',
            'chutiya', 'bhosdike', 'lund', 'gaand', 'gaandu',
            # Hindi script (common toxic words)
            'मार', 'मारूंगा', 'मार दूंगा', 'मर', 'मर जा', 'खत्म', 'खत्म कर',
            'तेरी', 'तुझे', 'तू', 'तेरी माँ', 'बहन', 'बहनचोद', 'मादरचोद',
            'चूतिया', 'भोसड़ीके', 'लुंड', 'गांड', 'गांडू'
        ]
        
        # Combined threat keywords
        self.threat_keywords = (
            self.threat_keywords_en + 
            self.threat_keywords_kn + 
            self.threat_keywords_hi
        )
        
        self.load_models()
    
    def load_models(self):
        """Load pre-trained models from Hugging Face"""
        try:
            print("Loading models for multilingual support...")
            
            # For multilingual support, we use a hybrid approach:
            # 1. English models for English text and code-mixed text
            # 2. Keyword-based detection for Kannada/Hindi
            # 3. Language detection to choose the right approach
            
            # Load English toxicity model (works well for code-mixed text too)
            print("Loading toxicity model (English, works for code-mixed text)...")
            toxicity_model_name = "unitary/toxic-bert"
            try:
                self.toxicity_tokenizer = AutoTokenizer.from_pretrained(toxicity_model_name)
                self.toxicity_model = AutoModelForSequenceClassification.from_pretrained(toxicity_model_name)
                self.toxicity_model.eval()
                print("✓ Toxicity model loaded")
            except Exception as e:
                print(f"Warning: Could not load toxicity model: {e}")
                self.toxicity_model = None
                self.toxicity_tokenizer = None
            
            # Load multilingual sentiment model (supports multiple languages)
            print("Loading multilingual sentiment model...")
            sentiment_model_name = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
            try:
                self.sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
                self.sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)
                self.sentiment_model.eval()
                print("✓ Multilingual sentiment model loaded")
            except Exception as e:
                print(f"Warning: Could not load multilingual sentiment model: {e}")
                print("Falling back to English sentiment model...")
                # Fallback to English sentiment model
                sentiment_model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
                try:
                    self.sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
                    self.sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)
                    self.sentiment_model.eval()
                    print("✓ English sentiment model loaded (fallback)")
                except Exception as e2:
                    print(f"Error: Could not load sentiment model: {e2}")
                    raise
            
            self.models_loaded = True
            print("All models loaded successfully!")
            print("Multilingual support: English (full), Kannada/Hindi (keyword-based + sentiment)")
            
        except Exception as e:
            print(f"Error loading models: {e}")
            print("Note: Some models may not be available. Check your internet connection.")
            raise
    
    def detect_language(self, text: str) -> Dict[str, any]:
        """
        Detect language of the text
        Returns: {'language': 'en'|'kn'|'hi'|'mixed'|'unknown', 'confidence': float}
        """
        try:
            # Detect primary language
            detected_lang = detect(text)
            
            # Map to our language codes
            lang_map = {
                'en': 'en',
                'kn': 'kn',  # Kannada
                'hi': 'hi',  # Hindi
            }
            
            primary_lang = lang_map.get(detected_lang, 'unknown')
            
            # Check for code-mixing (English + Kannada/Hindi)
            has_english = bool(re.search(r'[a-zA-Z]', text))
            has_kannada = bool(re.search(r'[\u0C80-\u0CFF]', text))  # Kannada Unicode range
            has_hindi = bool(re.search(r'[\u0900-\u097F]', text))    # Hindi/Devanagari Unicode range
            
            languages_present = []
            if has_english:
                languages_present.append('en')
            if has_kannada:
                languages_present.append('kn')
            if has_hindi:
                languages_present.append('hi')
            
            # Determine if code-mixed
            if len(languages_present) > 1:
                detected_language = 'mixed'
                mixed_languages = languages_present
            else:
                detected_language = primary_lang if primary_lang != 'unknown' else languages_present[0] if languages_present else 'unknown'
                mixed_languages = []
            
            return {
                'language': detected_language,
                'confidence': 0.8,  # langdetect doesn't provide confidence, using default
                'primary_language': primary_lang,
                'mixed_languages': mixed_languages if mixed_languages else [detected_language]
            }
            
        except LangDetectException:
            # Fallback: check Unicode ranges
            has_kannada = bool(re.search(r'[\u0C80-\u0CFF]', text))
            has_hindi = bool(re.search(r'[\u0900-\u097F]', text))
            has_english = bool(re.search(r'[a-zA-Z]', text))
            
            if has_kannada and has_english:
                return {'language': 'mixed', 'confidence': 0.7, 'primary_language': 'kn', 'mixed_languages': ['en', 'kn']}
            elif has_hindi and has_english:
                return {'language': 'mixed', 'confidence': 0.7, 'primary_language': 'hi', 'mixed_languages': ['en', 'hi']}
            elif has_kannada:
                return {'language': 'kn', 'confidence': 0.7, 'primary_language': 'kn', 'mixed_languages': ['kn']}
            elif has_hindi:
                return {'language': 'hi', 'confidence': 0.7, 'primary_language': 'hi', 'mixed_languages': ['hi']}
            elif has_english:
                return {'language': 'en', 'confidence': 0.7, 'primary_language': 'en', 'mixed_languages': ['en']}
            else:
                return {'language': 'unknown', 'confidence': 0.5, 'primary_language': 'unknown', 'mixed_languages': []}
        except Exception as e:
            print(f"Error detecting language: {e}")
            return {'language': 'unknown', 'confidence': 0.0, 'primary_language': 'unknown', 'mixed_languages': []}
    
    def predict_toxicity(self, text: str, language_info: Dict = None) -> Tuple[float, dict]:
        """
        Predict toxicity score (0.0 to 1.0) and label probabilities
        Works with English, Kannada, Hindi, and code-mixed text
        """
        # Get keyword-based toxicity (works for all languages)
        keyword_toxicity = self._check_keyword_toxicity(text, language_info)
        threat_prob = self._check_threat_keywords(text, language_info)
        
        # Try to use English model (works for English and code-mixed text)
        model_toxicity = 0.0
        if self.toxicity_model and self.toxicity_tokenizer:
            try:
                # Check if text has English content (for model prediction)
                has_english = bool(re.search(r'[a-zA-Z]', text))
                
                if has_english or language_info is None or language_info.get('language') in ['en', 'mixed', 'unknown']:
                    # Use English model for English or code-mixed text
                    inputs = self.toxicity_tokenizer(
                        text,
                        return_tensors="pt",
                        truncation=True,
                        max_length=512,
                        padding=True
                    )
                    
                    with torch.no_grad():
                        outputs = self.toxicity_model(**inputs)
                        logits = outputs.logits
                        
                        # Apply sigmoid for multi-label classification
                        probs = torch.nn.functional.sigmoid(logits)
                        prob_scores = probs[0].cpu().numpy()
                        
                        # Get max probability (overall toxicity)
                        model_toxicity = float(prob_scores.max())
                        
                        # Get individual label probabilities
                        labels = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
                        if len(prob_scores) >= 6:
                            label_probs_model = {label: float(prob) for label, prob in zip(labels, prob_scores)}
                        else:
                            # If model doesn't have all labels, create from overall score
                            label_probs_model = {
                                'toxic': model_toxicity,
                                'severe_toxic': model_toxicity * 0.8 if model_toxicity > 0.7 else 0.0,
                                'obscene': model_toxicity * 0.6 if model_toxicity > 0.5 else 0.0,
                                'threat': max(model_toxicity * 0.7, threat_prob),
                                'insult': model_toxicity * 0.7 if model_toxicity > 0.4 else 0.0,
                                'identity_hate': model_toxicity * 0.5 if model_toxicity > 0.6 else 0.0
                            }
                        
                        # Combine model prediction with keyword matching
                        # Weight based on language: more weight to keywords for local languages
                        detected_lang = language_info.get('language', 'unknown') if language_info else 'unknown'
                        
                        if detected_lang in ['kn', 'hi']:
                            # For local languages, prioritize keywords (60% keywords, 40% model if available)
                            if model_toxicity > 0:
                                combined_toxicity = 0.4 * model_toxicity + 0.6 * keyword_toxicity
                            else:
                                combined_toxicity = keyword_toxicity
                        else:
                            # For English/code-mixed, prioritize model (70% model, 30% keywords)
                            if model_toxicity > 0:
                                combined_toxicity = 0.7 * model_toxicity + 0.3 * keyword_toxicity
                            else:
                                combined_toxicity = keyword_toxicity
                        
                        # Update threat probability
                        threat_prob = max(threat_prob, label_probs_model.get('threat', 0.0))
                        
                        # Create final label probabilities
                        label_probs = {
                            'toxic': combined_toxicity,
                            'severe_toxic': max(combined_toxicity * 0.8 if combined_toxicity > 0.7 else 0.0, 
                                              label_probs_model.get('severe_toxic', 0.0)),
                            'obscene': max(combined_toxicity * 0.6 if combined_toxicity > 0.5 else 0.0,
                                          label_probs_model.get('obscene', 0.0)),
                            'threat': threat_prob,
                            'insult': max(combined_toxicity * 0.7 if combined_toxicity > 0.4 else 0.0,
                                         label_probs_model.get('insult', 0.0)),
                            'identity_hate': max(combined_toxicity * 0.5 if combined_toxicity > 0.6 else 0.0,
                                                label_probs_model.get('identity_hate', 0.0))
                        }
                        
                        overall_toxicity = max(combined_toxicity, max(label_probs.values()))
                        
                        return min(overall_toxicity, 1.0), label_probs
            except Exception as e:
                print(f"Error in model-based toxicity prediction: {e}")
                # Fall through to keyword-based detection
        
        # Fallback: keyword-based detection (works for all languages)
        combined_toxicity = keyword_toxicity
        label_probs = {
            'toxic': combined_toxicity,
            'severe_toxic': combined_toxicity * 0.8 if combined_toxicity > 0.7 else 0.0,
            'obscene': combined_toxicity * 0.6 if combined_toxicity > 0.5 else 0.0,
            'threat': threat_prob,
            'insult': combined_toxicity * 0.7 if combined_toxicity > 0.4 else 0.0,
            'identity_hate': combined_toxicity * 0.5 if combined_toxicity > 0.6 else 0.0
        }
        
        return min(combined_toxicity, 1.0), label_probs
    
    def _check_keyword_toxicity(self, text: str, language_info: Dict = None) -> float:
        """Check toxicity using keyword matching (supports multiple languages)"""
        text_lower = text.lower()
        
        # Check for toxic keywords in all languages
        toxic_keywords = self.threat_keywords
        
        # Count matches
        matches = sum(1 for keyword in toxic_keywords if keyword.lower() in text_lower)
        
        # Calculate toxicity score based on matches
        if matches > 0:
            # Base score + additional score per match (capped at 0.9)
            toxicity = min(0.5 + (matches * 0.1), 0.9)
            return toxicity
        
        return 0.0
    
    def _check_threat_keywords(self, text: str, language_info: Dict = None) -> float:
        """Check for threat keywords specifically"""
        text_lower = text.lower()
        
        # Check threat keywords
        threat_matches = sum(1 for keyword in self.threat_keywords if keyword.lower() in text_lower)
        
        if threat_matches > 0:
            return min(0.6 + (threat_matches * 0.15), 1.0)
        
        return 0.0
    
    def predict_sentiment(self, text: str, language_info: Dict = None) -> float:
        """
        Predict sentiment score (-1.0 to 1.0)
        Works with English, Kannada, Hindi, and code-mixed text
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
                if probs.shape[1] >= 3:
                    negative_prob = probs[0][0].item()
                    neutral_prob = probs[0][1].item()
                    positive_prob = probs[0][2].item()
                else:
                    # Binary classification
                    negative_prob = probs[0][0].item()
                    positive_prob = 1 - negative_prob
                    neutral_prob = 0.0
                
                # Convert to -1 to 1 scale
                sentiment_score = (positive_prob - negative_prob)
                
                return sentiment_score
                
        except Exception as e:
            print(f"Error in sentiment prediction: {e}")
            return 0.0
    
    def detect_threat(self, text: str, toxicity_score: float, threat_prob: float = None, language_info: Dict = None) -> bool:
        """
        Detect threats in text (supports multiple languages)
        """
        text_lower = text.lower()
        
        # Check for threat keywords in all languages
        keyword_match = any(keyword.lower() in text_lower for keyword in self.threat_keywords)
        
        # Check if model detected threat
        model_threat = threat_prob is not None and threat_prob > 0.5
        
        # Combine signals
        is_threat = False
        
        if model_threat:
            is_threat = True
        elif keyword_match and toxicity_score > 0.3:
            is_threat = True
        elif toxicity_score > 0.8:
            is_threat = True
        
        return is_threat
    
    def classify_severity(self, toxicity_score: float, sentiment_score: float, is_threat: bool) -> str:
        """Classify severity: 'low', 'medium', 'high', 'critical'"""
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
        Supports English, Kannada, Hindi, and code-mixed text
        """
        # Detect language
        language_info = self.detect_language(text)
        
        # Get predictions
        toxicity_score, toxicity_labels = self.predict_toxicity(text, language_info)
        sentiment_score = self.predict_sentiment(text, language_info)
        
        # Get threat probability
        threat_prob = toxicity_labels.get('threat', 0.0)
        is_threat = self.detect_threat(text, toxicity_score, threat_prob, language_info)
        severity = self.classify_severity(toxicity_score, sentiment_score, is_threat)
        
        # Calculate overall confidence
        confidence = max(toxicity_score, abs(sentiment_score))
        
        # Prepare details
        details = {
            "language_detection": language_info,
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
            "detected_language": language_info.get('language', 'unknown'),
            "details": details
        }

