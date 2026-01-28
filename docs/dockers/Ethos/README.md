# Ethos (에토스) - Central Data Node

## 이름의 유래

**Ethos**는 '성품', '신뢰'를 뜻하며 '윤리(Ethics)'의 어원입니다.
수사학에서 화자의 **고유한 성품과 신뢰성**을 의미하듯, 이 서버는 시스템 전체의 **데이터를 안전하게 보관**하고, **신뢰할 수 있는 정보(Golden Record)**를 제공하는 가장 기초가 되는 기지이기 때문에 붙여진 이름입니다.

## 주요 역할

데이터베이스, 벡터 저장소, 오브젝트 스토리지, 공통 배치 작업 등 **인프라와 데이터 지속성(Persistence)**을 담당합니다.

## 포함된 서비스 (Service Stack)

이 폴더의 `docker-compose.yml`은 다음 컨테이너들을 실행합니다:

1. **`postgres` (Vector DB)**:

   * **역할**: RAG(검색 증강 생성)를 위한 벡터 데이터와 일반 관계형 데이터를 저장합니다.
   * **이미지**: `pgvector/pgvector:pg16`
   * **포트**: 5432
2. **`oracle` (Enterprise DB)**:

   * **역할**: 기업 수준의 정형 데이터, 사용자 정보, 채용 공고 등 신뢰할 수 있는 정보를 저장합니다.
   * **이미지**: `gvenzl/oracle-xe:latest`
   * **포트**: 1521
   * 접근 계정 :
     - ORACLE_USER=rhetorica
     - ORACLE_PASSWORD=rhetorica_project2026
3. **`embedding_server` (Ollama)**:

   * **역할**: 텍스트를 벡터로 변환(Embedding)하는 전용 모델(`nomic-embed-text`)을 구동하며, 다른 서버(Pathos, Logos)에서 접근 가능합니다.
   * **이미지**: `ollama/ollama`
   * **포트**: 11435 (내부 11434)
4. **`minio` (Object Storage)**:

   * **역할**: 이력서(PDF), 면접 영상, 표정 이미지 등 대용량 비정형 파일을 모든 서버 노드에서 공유할 수 있도록 관리합니다. (S3 호환 API 지원)
   * **이미지**: `minio/minio:latest`
   * **포트**: 9000 (API), 9001 (Console GUI)
   * 사용방법 : http://192.168.40.54:9000  [minioadmin / minio_secret_pass]
5. **`batch_app`**:

   * **역할**: DB 초기화, 데이터 마이그레이션, 주기적 데이터 수집(Batch) 기능을 수행합니다.
   * **이미지**: 자체 빌드 (Dockerfile.batch)

## 실행 방법

`.env` 파일이 상위 폴더(`../.env`)에 위치해 있는지 확인 후 아래 명령어를 실행합니다.

```bash
# Ethos 디렉토리에서 실행
docker-compose up -d --build
```

> **참고**: YAML 문법 호환성을 위해 `version` 속성이 주석 처리되어 있을 수 있습니다. 최신 Docker Compose 환경에서는 생략해도 무방합니다.
