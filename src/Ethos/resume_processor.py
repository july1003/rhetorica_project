
# resume_processor.py
# (venv) C:\big20\final\src\Ethos> pip install boto3 pymupdf psycopg2-binary ollama python-dotenv requests oracledb
import os
import fitz  # PyMuPDF
import boto3
import psycopg2
import oracledb
import ollama
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
from botocore.client import Config

# Load environment variables
load_dotenv(r'c:\big20\final\.env')

# --- Configuration ---
# 1. MinIO
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT')
MINIO_USER = os.getenv('MINIO_ROOT_USER')
MINIO_PWD = os.getenv('MINIO_ROOT_PASSWORD')
BUCKET_NAME = "resumes"

# 2. Postgres (Vector DB)
PG_HOST = os.getenv('ETHOS_SERVER')
PG_DB = "interview_db"
PG_USER = "admin"
PG_PWD = "interview_pass"

# 3. Ollama (Embedding)
EMBED_SERVER = f"http://{os.getenv('ETHOS_SERVER')}:11435"
EMBED_MODEL = "nomic-embed-text"

# 4. Logos LLM
# Replace {LOGOS_SERVER} with the actual IP address
logos_ip = os.getenv('LOGOS_SERVER')
LOGOS_LLM_URL = os.getenv('LOGOS_LLM_URL').replace('{LOGOS_SERVER}', logos_ip)

# 5. Oracle (Rhetorica Schema)
ORA_USER = os.getenv('ORACLE_USER')
ORA_PWD = os.getenv('ORACLE_PASSWORD')
ORA_DSN = f"{os.getenv('ORACLE_HOST')}:{os.getenv('ORACLE_PORT')}/{os.getenv('ORACLE_SERVICE_NAME')}"

# Initialize MinIO Client
s3_client = boto3.client(
    's3',
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_USER,
    aws_secret_access_key=MINIO_PWD,
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

def init_resources():
    """Create buckets and tables if they don't exist"""
    # 1. MinIO Bucket
    try:
        s3_client.head_bucket(Bucket=BUCKET_NAME)
    except:
        s3_client.create_bucket(Bucket=BUCKET_NAME)
        print(f"Created MinIO bucket: {BUCKET_NAME}")

    # 2. Postgres Table (pgvector)
    try:
        conn = psycopg2.connect(host=PG_HOST, database=PG_DB, user=PG_USER, password=PG_PWD)
        cur = conn.cursor()
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS resume_indices (
                id SERIAL PRIMARY KEY,
                file_name TEXT,
                s3_path TEXT,
                content TEXT,
                embedding vector(768),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
    except Exception as e:
        print(f"Postgres init error: {e}")
    finally:
        if 'conn' in locals(): conn.close()

def extract_text_from_pdf(pdf_path):
    """Extract all text from PDF file"""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"PDF Extraction Error: {e}")
        return ""

def upload_to_minio(file_path):
    """Upload file to MinIO with date folder structure"""
    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%H%M%S")
    file_ext = os.path.splitext(file_path)[1]
    
    # Prefix changed to English for consistency and future variable mapping (e.g., user_id or interview_id)
    s3_file_name = f"{today}/candidate_resume_{timestamp}{file_ext}"
    
    s3_client.upload_file(file_path, BUCKET_NAME, s3_file_name)
    return f"{BUCKET_NAME}/{s3_file_name}"

def generate_embedding(text):
    """Generate embedding vector using Ollama's model"""
    try:
        client = ollama.Client(host=EMBED_SERVER)
        # 텍스트가 너무 길면 임베딩 실패할 수 있으므로 슬라이싱 (nomic은 8k까지 지원)
        response = client.embeddings(model=EMBED_MODEL, prompt=text[:8000])
        return response['embedding']
    except Exception as e:
        print(f"Embedding error on {EMBED_SERVER}: {e}")
        return None

def analyze_resume_with_llm(text):
    """Call Logos LLM with increased timeout (120s)"""
    prompt = f"""
다음은 채용 응시자의 이력서 텍스트입니다. 
당신은 베테랑 면접관으로서 이 정보를 분석하여 반드시 JSON 형식으로 요약해 주세요.
키: 'summary' (3줄 요약), 'tech_stack' (기술 목록), 'experience' (핵심 경력)

내용:
{text[:4000]}
"""
    try:
        payload = {
            "model": "gpt-oss:20b",
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        # 타임아웃을 120초로 대폭 늘림 (로컬 LLM 응답 대기 시간 고려)
        res = requests.post(LOGOS_LLM_URL, json=payload, timeout=120)
        res.raise_for_status() 
        
        response_json = res.json().get('response', '{}')
        return json.loads(response_json)
    except Exception as e:
        print(f"LLM Analysis Error on {LOGOS_LLM_URL}: {e}")
        return {"summary": "분석 중 타임아웃 또는 연결 오류가 발생했습니다.", "tech_stack": "N/A", "experience": "N/A"}

def save_to_oracle(file_name, s3_path, analysis_result):
    """Save the analysis report into Oracle RESUME_ANALYSES table"""
    try:
        conn = oracledb.connect(user=ORA_USER, password=ORA_PWD, dsn=ORA_DSN)
        cur = conn.cursor()
        
        sql = """
            INSERT INTO RESUME_ANALYSES (FILE_NAME, S3_PATH, SUMMARY, TECH_STACK, EXPERIENCE) 
            VALUES (:1, :2, :3, :4, :5)
        """
        cur.execute(sql, (
            file_name,
            s3_path,
            analysis_result.get('summary', ''),
            analysis_result.get('tech_stack', ''),
            analysis_result.get('experience', '')
        ))
        conn.commit()
        print("Report successfully saved to Oracle DB.")
    except Exception as e:
        print(f"Oracle Save Error: {e}")
    finally:
        if 'conn' in locals(): conn.close()

def process_resume(local_pdf_path):
    """Full Pipeline: PDF -> MinIO -> Postgres -> LLM -> Oracle"""
    if not os.path.exists(local_pdf_path):
        return {"error": "파일을 찾을 수 없습니다."}

    results = {}
    init_resources()
    
    content = extract_text_from_pdf(local_pdf_path)
    if not content: return {"error": "PDF 텍스트 추출 실패"}

    s3_path = upload_to_minio(local_pdf_path)
    
    vector = generate_embedding(content)
    if vector:
        try:
            conn = psycopg2.connect(host=PG_HOST, database=PG_DB, user=PG_USER, password=PG_PWD)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO resume_indices (file_name, s3_path, content, embedding) VALUES (%s, %s, %s, %s)",
                (os.path.basename(local_pdf_path), s3_path, content, vector)
            )
            conn.commit()
        finally:
            if 'conn' in locals(): conn.close()

    # 분석 수행
    analysis = analyze_resume_with_llm(content)
    save_to_oracle(os.path.basename(local_pdf_path), s3_path, analysis)
    
    return analysis

if __name__ == "__main__":
    # Example usage:
    # process_resume(r"C:\temp\my_resume.pdf")
    pass
