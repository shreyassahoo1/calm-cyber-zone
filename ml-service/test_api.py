"""
Test script for ML Service API

Run this to test the API endpoints.
Make sure the ML service is running first: python main.py
"""

import requests
import json

# Configuration
API_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

def test_analyze(text: str):
    """Test analyze endpoint"""
    print(f"Testing analyze endpoint with text: '{text}'...")
    try:
        response = requests.post(
            f"{API_URL}/analyze",
            json={"text": text, "platform": "discord"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

def main():
    """Run all tests"""
    print("=" * 50)
    print("ML Service API Test")
    print("=" * 50)
    print()
    
    # Test health
    test_health()
    
    # Test with various messages
    test_messages = [
        "Hello, how are you?",
        "You're an idiot!",
        "I'm going to kill you!",
        "This is a great project!",
        "I hate this so much, you should die!",
        "Thanks for your help!",
    ]
    
    for message in test_messages:
        test_analyze(message)
        print("-" * 50)
        print()

if __name__ == "__main__":
    main()

