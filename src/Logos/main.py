from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

app = FastAPI(title="Logos AI System")

# Template 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

# Load .env from project root (../../.env)
load_dotenv(os.path.join(base_dir, "../../.env"))

# Ollama 설정
OLLAMA_URL = os.getenv("LOGOS_LLM_URL", "http://192.168.40.61:11434/api/generate")
# docker-compose에서 환경변수로 모델명을 받을 수 있게 하거나 기본값 설정
MODEL_NAME = os.getenv("LOGOS_LLM_MODEL", "gpt-oss:20b")

class ChatRequest(BaseModel):
    prompt: str

@app.get("/", response_class=HTMLResponse)
async def read_items(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/generate")
async def generate_response(request: ChatRequest):
    payload = {
        "model": MODEL_NAME,
        "prompt": request.prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=300)
        response.raise_for_status()
        result = response.json()
        return {"response": result.get("response", "")}
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Logos"}
