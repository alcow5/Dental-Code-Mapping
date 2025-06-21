#!/usr/bin/env python3
"""
Test script to verify Ollama setup and model availability.
"""

import requests
import json
import sys
from config import OLLAMA_URL, OLLAMA_MODEL

def test_ollama_connection():
    """Test if Ollama is running and accessible."""
    try:
        # Test basic connection
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running and accessible")
            return True
        else:
            print(f"❌ Ollama returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama. Is it running?")
        print("   Start Ollama with: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error connecting to Ollama: {e}")
        return False

def test_model_availability():
    """Test if the specified model is available."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model["name"] for model in models]
            
            if OLLAMA_MODEL in model_names:
                print(f"✅ Model '{OLLAMA_MODEL}' is available")
                return True
            else:
                print(f"❌ Model '{OLLAMA_MODEL}' not found")
                print(f"Available models: {', '.join(model_names)}")
                print(f"To install {OLLAMA_MODEL}, run: ollama pull {OLLAMA_MODEL}")
                return False
        else:
            print(f"❌ Failed to get model list: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking model availability: {e}")
        return False

def test_model_response():
    """Test if the model can generate a response."""
    try:
        test_prompt = {
            "model": OLLAMA_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": "Hello, can you respond with a simple JSON object containing a greeting?"
                }
            ],
            "stream": False
        }
        
        print(f"Testing model response with '{OLLAMA_MODEL}'...")
        response = requests.post(OLLAMA_URL, json=test_prompt, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if "message" in result and "content" in result["message"]:
                print("✅ Model responded successfully")
                print(f"Response: {result['message']['content'][:100]}...")
                return True
            else:
                print("❌ Unexpected response format")
                return False
        else:
            print(f"❌ Model request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing model response: {e}")
        return False

def main():
    """Run all tests."""
    print("🔍 Testing Ollama Setup")
    print("=" * 40)
    
    # Test 1: Connection
    if not test_ollama_connection():
        sys.exit(1)
    
    # Test 2: Model availability
    if not test_model_availability():
        sys.exit(1)
    
    # Test 3: Model response
    if not test_model_response():
        sys.exit(1)
    
    print("\n" + "=" * 40)
    print("🎉 All tests passed! Ollama is ready to use.")
    print(f"Model: {OLLAMA_MODEL}")
    print("You can now run the Streamlit app with: streamlit run app.py")

if __name__ == "__main__":
    main() 