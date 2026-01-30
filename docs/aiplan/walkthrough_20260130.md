# 회원가입 및 로그인 페이지 구현 가이드

Oracle 데이터베이스 연동을 포함한 회원가입 및 로그인, 메인 랜딩 페이지를 구현했습니다.

## 변경 사항

### 1. 웹 페이지 구조 변경

- **메인 페이지 (`/`)**: 프로젝트 소개와 로그인/회원가입 진입점을 제공하는 `index.html`을 생성했습니다.
- **로그인 페이지 (`/login`)**: 사용자 인증을 위한 `login.html`을 생성했습니다.
- **채팅 페이지 (`/chat`)**: 기존 메인 화면이었던 채팅 창을 `/chat` 경로로 이동했습니다.
- **회원가입 페이지 (`/register`)**: 기존 구현 유지.

### 2. 백엔드 로직 (`src/Logos/main.py`)

- **라우트 재설정**: URL 경로에 맞춰 템플릿 반환 로직을 수정했습니다.
- **로그인 구현**:
  - `POST /login` 엔드포인트 생성.
  - 입력된 이메일로 DB 조회 및 비밀번호 해시(`bcrypt`) 검증.
  - 인증 성공 시 `session_id` 쿠키 발급 및 로그인 처리.

## 테스트 방법 (Docker 환경)

1. **Docker 재빌드 및 실행**
    코드가 수정되었으므로 이미지를 다시 빌드해야 합니다.

    ```bash
    cd c:\big20\rhetorica_project\docs\dockers\Logos
    docker-compose build web
    docker-compose up -d web
    ```

2. **접속 확인**
    - **메인 페이지**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) 접속 시 Rhetorica Landing Page가 보여야 합니다.
    - **로그인**: 메인에서 "로그인" 버튼 클릭 -> `/login` 이동 -> 이메일/비번 입력 -> 성공 시 `/chat`으로 이동.
    - **회원가입**: 메인에서 "회원가입" 버튼 클릭 -> `/register` 이동.

## 문서 아카이빙

다음 문서들이 `docs\aiplan` 폴더에 백업되었습니다:

- `docs\aiplan\task_20260130.md`
- `docs\aiplan\implementation_plan_20260130.md`
