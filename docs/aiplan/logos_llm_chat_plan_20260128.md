# Logos LLM 테스트 및 채팅 인터페이스 구현 계획

## 목표 설명

`src/Logos` 내에 LLM 테스트 및 채팅 서버를 구현하고, Docker 컨테이너가 이 서버(`src/Logos/main.py`)를 실행하도록 설정합니다.

## 사용자 검토 필요 사항
>
> [!NOTE]
> `docs/dockers/Logos/docker-compose.yml`의 실행 명령어를 `uvicorn src.main:app ...`에서 `uvicorn src.Logos.main:app ...`으로 변경합니다.

## 변경 제안

### docs/dockers/Logos

#### [MODIFY] [docker-compose.yml](file:///c:/big20/rhetorica_project/docs/dockers/Logos/docker-compose.yml)

- `web` 서비스의 `command` 수정.
- 변경 전: `uvicorn src.main:app ...`
- 변경 후: `uvicorn src.Logos.main:app --host 0.0.0.0 --port 8000 --reload`

### src/Logos

#### [NEW] [test_llm.py](file:///c:/big20/rhetorica_project/src/Logos/test_llm.py)

- `http://ollama_server:11434/api/generate`로 POST 요청을 보내는 스크립트.
- Qwen 2.5 (7B) 모델 연결 테스트.

#### [NEW] [main.py](file:///c:/big20/rhetorica_project/src/Logos/main.py)

- FastAPI 앱 정의 (`app = FastAPI()`).
- POST `/generate`: Ollama와 통신.
- GET `/`: 채팅 UI 제공.

#### [NEW] [templates/chat.html](file:///c:/big20/rhetorica_project/src/Logos/templates/chat.html)

- 채팅 인터페이스 (HTML/JS).
