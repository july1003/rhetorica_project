import uuid
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# LangChain & Observability Imports
from langchain_community.chat_models import ChatOllama
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from openinference.instrumentation.langchain import LangChainInstrumentor
from opentelemetry import trace as trace_api
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

app = FastAPI(title="Logos AI System")

# Template 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

# Load .env from project root (../../.env)
load_dotenv(os.path.join(base_dir, "../../.env"))

# Configuration
FULL_OLLAMA_URL = os.getenv("LOGOS_LLM_URL", "http://192.168.40.61:11434/api/generate")
OLLAMA_BASE_URL = FULL_OLLAMA_URL.replace("/api/generate", "")
MODEL_NAME = os.getenv("LOGOS_LLM_MODEL", "gpt-oss:20b")
PHOENIX_ENDPOINT = os.getenv("PHOENIX_TRACES_ENDPOINT", "http://phoenix:6006/v1/traces")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0") # Default Redis service in docker-compose

# Setup OpenTelemetry for Phoenix
resource = Resource(attributes={
    "service.name": "Logos-AI",
    "project_name": "rhetorica_project"
})
tracer_provider = TracerProvider(resource=resource)
tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=PHOENIX_ENDPOINT)))
trace_api.set_tracer_provider(tracer_provider)
LangChainInstrumentor().instrument()

# Initialize Chat Model
chat_model = ChatOllama(
    base_url=OLLAMA_BASE_URL,
    model=MODEL_NAME
)

# Redis History
def get_message_history(session_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(session_id, url=REDIS_URL)

chat_with_history = RunnableWithMessageHistory(
    chat_model,
    get_message_history,
)

class ChatRequest(BaseModel):
    prompt: str

@app.get("/", response_class=HTMLResponse)
async def read_items(request: Request):
    session_id = request.cookies.get("session_id")
    history_data = []
    
    if session_id:
        try:
            # Fetch history from Redis
            redis_history = get_message_history(session_id)
            # redis_history.messages returns List[BaseMessage]
            for msg in redis_history.messages:
                # msg.type is usually 'human' or 'ai'
                sender = "user" if msg.type == "human" else "bot"
                history_data.append({"sender": sender, "content": msg.content})
        except Exception as e:
            print(f"Error loading history: {e}")

    # Serialize to JSON for safe embedding in HTML
    import json
    history_json = json.dumps(history_data)
    
    response = templates.TemplateResponse("chat.html", {
        "request": request, 
        "history_json": history_json
    })
    
    # Check for session_id cookie (create if missing)
    if not session_id:
        new_session_id = str(uuid.uuid4())
        response.set_cookie(key="session_id", value=new_session_id)
        
    return response

@app.post("/generate")
async def generate_response(request: ChatRequest, req: Request, res: Response):
    try:
        # Get Session ID
        session_id = req.cookies.get("session_id")
        if not session_id:
            # If API call without cookie (e.g. CLI), allow temp session or error
            # For robustness, we create one, but client needs to handle it
            session_id = str(uuid.uuid4())
            res.set_cookie(key="session_id", value=session_id)

        # Using LangChain with History
        config = {"configurable": {"session_id": session_id}}
        response = chat_with_history.invoke(
            [HumanMessage(content=request.prompt)],
            config=config
        )
        return {"response": response.content, "session_id": session_id}
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Logos"}
