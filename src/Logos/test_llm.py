import requests
import json
import os
from dotenv import load_dotenv

# Load .env from project root
base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, "../../.env"))

def test_generate():
    url = os.getenv("LOGOS_LLM_URL", "http://192.168.40.61:11434/api/generate")
    model = os.getenv("LOGOS_LLM_MODEL", "gpt-oss:20b")
    
    payload = {
        "model": model,
        "prompt": "Hello, introduce yourself.",
        "stream": False
    }
    
    try:
        print(f"Sending request to {url}...")
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        
        data = response.json()
        print("\n=== Response ===")
        print(data.get("response", "No response field found"))
        print("================")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama: {e}")
        return False

if __name__ == "__main__":
    test_generate()
