# 구현 계획 - 메인 및 로그인 페이지

`rhetorica_project` (`Logos` 서비스)의 진입점 역할을 하는 메인 페이지를 생성합니다. 이 페이지에는 프로젝트 설명과 로그인/회원가입 페이지로 이동하는 기능을 포함합니다.

## 사용자 검토 필요

없음.

## 제안된 변경 사항

### Logos 서비스 (`src/Logos`)

#### [NEW] [index.html](file:///c:/big20/rhetorica_project/src/Logos/templates/index.html)

* 메인 랜딩 페이지.
* 프로젝트 제목 "AI Mock Interview System - Rhetorica Project" 표시.
* `README.md`의 프로젝트 설명 표시 ("아리스토텔레스의 수사학을 AI 기술로 재해석...").
* 버튼: [로그인], [회원가입].

#### [NEW] [login.html](file:///c:/big20/rhetorica_project/src/Logos/templates/login.html)

* 간단한 로그인 폼 (이메일, 비밀번호).
* UI 구현 및 백엔드 연동.

#### [MODIFY] [main.py](file:///c:/big20/rhetorica_project/src/Logos/main.py)

* **라우트 재구성**:
  * `GET /`: `chat.html` 대신 `index.html` 제공.
  * `GET /chat`: 기존 채팅 인터페이스(`chat.html`) 제공.
  * `GET /login`: `login.html` 제공.
* **로그인 로직**:
  * `POST /login` 구현: DB 확인 및 비밀번호 해시 검증.
  * 성공 시 `session_id` 쿠키 설정 후 `/chat`으로 리다이렉트.

## 검증 계획

### 자동화 테스트

* `browser_subagent`를 사용하여 확인:
    1. 메인 페이지(`/`) 접속.
    2. 설명 및 버튼 표시 확인.
    3. "회원가입" 클릭 -> `/register` 이동 확인.
    4. "로그인" 클릭 -> `/login` 이동 확인.
    5. (선택 사항) 로그인 시도 -> `/chat` 리다이렉트 확인.

### 수동 검증

* 사용자가 Docker 이미지 빌드 및 실행하여 확인.
