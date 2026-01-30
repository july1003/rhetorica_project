
# web_server.py
import os
import sys
import shutil
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Path Configuration: Add Ethos directory for importing processing logic
# Current file: c:\big20\final\src\Logos\web_server.py
# Ethos file: c:\big20\final\src\Ethos\resume_processor.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # c:\big20\final\src\Logos
SRC_DIR = os.path.dirname(BASE_DIR)                   # c:\big20\final\src
ETHOS_DIR = os.path.join(SRC_DIR, "Ethos")             # c:\big20\final\src\Ethos

if ETHOS_DIR not in sys.path:
    sys.path.append(ETHOS_DIR)

try:
    from resume_processor import process_resume
except ImportError as e:
    print(f"Error importing resume_processor: {e}")
    # Define a dummy function for local testing if Ethos is missing
    def process_resume(path):
        print(f"Dummy process: {path}")

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(SRC_DIR), ".env"))

app = FastAPI(title="Rhetorica AI Dashboard")

# Template configuration
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Temporary file storage
TEMP_DIR = os.path.join(BASE_DIR, "temp_uploads")
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_resume(request: Request, file: UploadFile = File(...)):
    import time
    from datetime import datetime

    if not file.filename.lower().endswith(".pdf"):
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "message": "오류: PDF 파일만 업로드 가능합니다."
        })

    # Start timing
    start_time = time.time()
    start_str = datetime.now().strftime("%H:%M:%S")
    
    temp_file_path = os.path.join(TEMP_DIR, file.filename)
    analysis_data = None
    
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Call the processing pipeline
        analysis_data = process_resume(temp_file_path)
        
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        end_str = datetime.now().strftime("%H:%M:%S")
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "message": f"성공: '{file.filename}' 분석이 완료되었습니다.",
            "analysis": analysis_data,
            "start_time": start_str,
            "end_time": end_str,
            "duration": duration
        })

    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "message": f"오류: {str(e)}"
        })
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "__main__":
    import uvicorn
    # In production, this would run on Logos Server (192.168.40.61)
    uvicorn.run(app, host="0.0.0.0", port=8000)
