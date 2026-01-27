from fastapi import FastAPI

app = FastAPI(title="AI Mock Interview System")

@app.get("/")
def read_root():
    return {"message": "AI Mock Interview System is running!", "status": "healthy"}
    # return {"Hello": "World"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}

# 이 파일을 아래와 같이 실행
# (venv) C:\big20\final\src>uvicorn main:app --reload
# 그리고 나서 브라우저 띄우고 http://127.0.0.1:8000 접속
# 
# FastAPI의 킬러 콘텐츠: 자동 문서화
# FastAPI의 가장 큰 장점은 코드를 짜면 API 문서가 자동으로 생성된다는 점입니다. 서버가 켜진 상태에서 아래 주소로 접속해 보세요.
# Swagger UI: http://127.0.0.1:8000/docs (대화형 문서, 바로 테스트 가능)
# ReDoc: http://127.0.0.1:8000/redoc (깔끔하게 정리된 문서)