"""
Test script for multilingual ML Service API

Tests the API with Kannada, Hindi, and code-mixed text.
Make sure the ML service is running first: python main.py
"""

import requests
import json

# Configuration
API_URL = "http://localhost:8000"

def test_analyze(text: str, language: str = "unknown"):
    """Test analyze endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing with {language} text: '{text}'")
    print(f"{'='*60}")
    try:
        response = requests.post(
            f"{API_URL}/analyze",
            json={"text": text, "platform": "discord"},
            timeout=10
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"\nResponse:")
        print(f"  Toxicity Score: {result.get('toxicity_score', 0):.3f}")
        print(f"  Sentiment Score: {result.get('sentiment_score', 0):.3f}")
        print(f"  Severity: {result.get('severity', 'unknown')}")
        print(f"  Threat Detected: {result.get('is_threat', False)}")
        print(f"  Detected Language: {result.get('detected_language', 'unknown')}")
        print(f"  Confidence: {result.get('confidence', 0):.3f}")
        
        # Language detection details
        if 'details' in result and 'language_detection' in result['details']:
            lang_info = result['details']['language_detection']
            print(f"\nLanguage Detection:")
            print(f"  Language: {lang_info.get('language', 'unknown')}")
            print(f"  Confidence: {lang_info.get('confidence', 0):.3f}")
            print(f"  Primary Language: {lang_info.get('primary_language', 'unknown')}")
            print(f"  Mixed Languages: {lang_info.get('mixed_languages', [])}")
        
        # Toxicity breakdown
        if 'details' in result and 'toxicity_breakdown' in result['details']:
            tox_info = result['details']['toxicity_breakdown']
            print(f"\nToxicity Breakdown:")
            print(f"  Score: {tox_info.get('score', 0):.3f}")
            print(f"  Level: {tox_info.get('level', 'unknown')}")
            if 'labels' in tox_info:
                print(f"  Labels:")
                for label, score in tox_info['labels'].items():
                    print(f"    {label}: {score:.3f}")
        
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        print()

def main():
    """Run all tests"""
    print("=" * 60)
    print("Multilingual ML Service API Test")
    print("=" * 60)
    
    # Test health
    print("\nTesting health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        print(f"Status: {response.status_code}")
        health = response.json()
        print(f"Response: {json.dumps(health, indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test with English text
    test_messages_en = [
        ("Hello, how are you?", "English"),
        ("You're an idiot!", "English"),
        ("I'm going to kill you!", "English"),
        ("This is a great project!", "English"),
        ("Thanks for your help!", "English"),
    ]
    
    # Test with Kannada text
    test_messages_kn = [
        ("ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?", "Kannada"),
        ("ನೀವು ಮೂರ್ಖರಾಗಿದ್ದೀರಿ!", "Kannada"),
        ("ನಾನು ನಿಮ್ಮನ್ನು ಕೊಲ್ಲುತ್ತೇನೆ!", "Kannada"),
        ("ಇದು ಒಂದು ಉತ್ತಮ ಯೋಜನೆ!", "Kannada"),
        ("ನಿಮ್ಮ ಸಹಾಯಕ್ಕೆ ಧನ್ಯವಾದಗಳು!", "Kannada"),
    ]
    
    # Test with Hindi text
    test_messages_hi = [
        ("नमस्ते, आप कैसे हैं?", "Hindi"),
        ("तुम मूर्ख हो!", "Hindi"),
        ("मैं तुम्हें मार दूंगा!", "Hindi"),
        ("यह एक बेहतरीन परियोजना है!", "Hindi"),
        ("आपकी मदद के लिए धन्यवाद!", "Hindi"),
    ]
    
    # Test with code-mixed text
    test_messages_mixed = [
        ("You are a madarchod", "Code-mixed (English + Hindi)"),
        ("ನೀವು ಒಂದು idiot", "Code-mixed (Kannada + English)"),
        ("तुम एक fool हो", "Code-mixed (Hindi + English)"),
        ("You are a chakke", "Code-mixed (English + Kannada)"),
        ("Hello, ನೀವು ಹೇಗಿದ್ದೀರಿ?", "Code-mixed (English + Kannada)"),
    ]
    
    print("\n" + "=" * 60)
    print("Testing with English text")
    print("=" * 60)
    for text, lang in test_messages_en:
        test_analyze(text, lang)
    
    print("\n" + "=" * 60)
    print("Testing with Kannada text")
    print("=" * 60)
    for text, lang in test_messages_kn:
        test_analyze(text, lang)
    
    print("\n" + "=" * 60)
    print("Testing with Hindi text")
    print("=" * 60)
    for text, lang in test_messages_hi:
        test_analyze(text, lang)
    
    print("\n" + "=" * 60)
    print("Testing with code-mixed text")
    print("=" * 60)
    for text, lang in test_messages_mixed:
        test_analyze(text, lang)
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()

