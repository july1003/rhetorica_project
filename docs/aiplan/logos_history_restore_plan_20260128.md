# Logos LLM 테스트 및 채팅 인터페이스 구현 계획

## 목표 설명

`src/Logos` 내에 LLM 테스트 및 채팅 서버를 구현하고, Docker 컨테이너가 이 서버(`src/Logos/main.py`)를 실행하도록 설정합니다.
추가적으로 **Redis를 활용한 대화 기록 저장(Memory)** 기능을 구현하여 멀티턴 대화가 가능하도록 합니다.
또한 **화면 새로고침 시 이전 대화 내용을 복원**하여 사용자 경험을 향상시킵니다.

## 사용자 검토 필요 사항
>
> [!NOTE]
> `docs/dockers/Logos/docker-compose.yml`의 실행 명령어를 `uvicorn src.main:app ...`에서 `uvicorn src.Logos.main:app ...`으로 변경합니다.

> [!IMPORTANT]
> Redis 연동을 위해 `langchain-community` 및 `redis` 라이브러리가 필요합니다 (이미 설치됨).
> 세션 관리를 위해 브라우저 쿠키(`session_id`)를 사용합니다.

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
- [NEW] Session Middleware: 요청 시 `session_id` 쿠키 확인 및 생성.
- [NEW] LangChain Memory: `RedisChatMessageHistory`를 사용하여 세션별 대화 내용 저장.
- **[NEW] History Restoration**: `GET /` 요청 시 Redis에서 대화 내용을 조회하여 템플릿에 전달.
- POST `/generate`: Ollama와 통신 (Memory 적용).
- GET `/`: 채팅 UI 제공.

#### [NEW] [templates/chat.html](file:///c:/big20/rhetorica_project/src/Logos/templates/chat.html)

- 채팅 인터페이스 (HTML/JS).
- [NEW] Session Persistence: 브라우저가 `session_id` 쿠키를 유지하도록 함.
- **[NEW] History Rendering**: 페이지 로드 시 서버로부터 전달받은 대화 내용을 화면에 표시.
