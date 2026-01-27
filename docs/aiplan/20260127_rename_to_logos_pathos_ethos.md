# Logos, Pathos, Ethos로 이름 변경 계획

## 목표

기존 도커 서비스 디렉토리 이름을 새로운 명명 규칙(Logos, Pathos, Ethos)에 맞춰 변경하고, `src` 내에 해당 소스 디렉토리를 생성합니다. 또한 관련 문서를 업데이트합니다.

## 변경 제안 내용

### 도커 디렉토리 (docs/dockers)

- `realtime_ai` -> `Logos` (기존 A: 실시간 AI)
- `vision_analysis` -> `Pathos` (기존 B: 비전 분석)
- `central_data` -> `Ethos` (기존 C: 데이터 센터)

### 소스 디렉토리 (src)

- `src/Logos` 생성
- `src/Pathos` 생성
- `src/Ethos` 생성
- 각 디렉토리에 `__init__.py` 파이썬 파일을 추가하여 패키지로 인식되도록 함.

### 문서 업데이트

- `docs/dockers/실행절차.md` 수정:
  - `A_docker` / `realtime_ai` -> `Logos`
  - `B_docker` / `vision_analysis` -> `Pathos`
  - `C_docker` / `central_data` -> `Ethos`
  - 관련 명령어 예시 업데이트.

## 검증 계획

1. **디렉토리 구조 확인**:
   - `docs/dockers/` 하위에 Logos, Pathos, Ethos 폴더 존재 확인.
   - `src/` 하위에 Logos, Pathos, Ethos 폴더 존재 확인.
2. **문서 내용 확인**:
   - `docs/dockers/실행절차.md` 내의 참조 이름이 올바르게 변경되었는지 확인.
