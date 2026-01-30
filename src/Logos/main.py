import uuid
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from passlib.context import CryptContext

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

# Database
from .database import get_db_connection

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

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
try:
    chat_model = ChatOllama(
        base_url=OLLAMA_BASE_URL,
        model=MODEL_NAME
    )
except Exception as e:
    print(f"Warning: Failed to initialize ChatOllama: {e}")
    chat_model = None

# Redis History
def get_message_history(session_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(session_id, url=REDIS_URL)

if chat_model:
    chat_with_history = RunnableWithMessageHistory(
        chat_model,
        get_message_history,
    )
else:
    chat_with_history = None

class ChatRequest(BaseModel):
    prompt: str

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

@app.get("/", response_class=HTMLResponse)
async def read_landing(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_user(user: UserLogin, response: Response):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT user_id, password_hash, name, role FROM users WHERE email = :1", [user.email])
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 잘못되었습니다.")
            
        user_id, password_hash, name, role = row
        
        if not pwd_context.verify(user.password, password_hash):
            raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 잘못되었습니다.")
            
        # Create session
        session_id = str(uuid.uuid4())
        
        # In a real app, we would store session_id in a server-side session store (Redis) with user info.
        # For this MVP, we just set the cookie.
        # Ideally: redis.set(f"session:{session_id}", json.dumps({"user_id": user_id, "role": role}))
        
        response.set_cookie(key="session_id", value=session_id)
        return {"message": "Login successful"}
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        print(f"Login Error: {e}")
        raise HTTPException(status_code=500, detail="로그인 처리 중 오류 발생")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@app.get("/chat", response_class=HTMLResponse)
async def read_chat(request: Request):
    session_id = request.cookies.get("session_id")
    history_data = []
    
    # If no session, redirect to login (Uncomment for strict auth)
    # if not session_id:
    #     return RedirectResponse("/login")
    
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
    
    # Check for session_id cookie (create if missing for guest access, or force login)
    if not session_id:
        new_session_id = str(uuid.uuid4())
        response.set_cookie(key="session_id", value=new_session_id)
        
    return response

@app.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register_user(user: UserRegister):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if email exists
        cursor.execute("SELECT user_id FROM users WHERE email = :1", [user.email])
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 존재하는 이메일입니다."
            )
            
        # Hash password
        hashed_password = pwd_context.hash(user.password)
        
        # Insert user
        cursor.execute(
            "INSERT INTO users (email, password_hash, name, role) VALUES (:1, :2, :3, 'CANDIDATE')",
            [user.email, hashed_password, user.name]
        )
        conn.commit()
        
        return {"message": "User registered successfully"}
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        print(f"Registration Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="서버 오류가 발생했습니다."
        )
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

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

        if not chat_with_history:
             return {"response": "AI 모델이 초기화되지 않았습니다.", "session_id": session_id}

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

