# 시스템 요구사항 명세서 (SRS)
**프로젝트명:** 웹 AI 모의면접 플랫폼

## 1. 개요
본 문서는 파이썬 기반 웹 AI 모의면접 플랫폼의 기능적, 비기능적 요구사항을 정의합니다.

## 2. 기능적 요구사항 (Functional Requirements)

### 2.1 면접 시뮬레이션 엔진 (Interview Simulation Engine)
| ID | 요구사항명 | 상세 내용 | 비고 |
| :--- | :--- | :--- | :--- |
| **REQ-F-001** | **적응형 질문 생성**<br>(Adaptive Questioning) | - 지원자의 답변을 실시간으로 분석하여 꼬리 질문(Follow-up Questions) 생성<br>- LangChain 메모리 모듈 및 RAG 기술 활용 | 예: "MSA 경험" 언급 시 트랜잭션 관리 관련 심층 질문 생성 |
| **REQ-F-002** | **멀티모달 인터랙션**<br>(Multimodal Interaction) | - 음성(Audio), 화상(Video), 텍스트(Chat/Code), 드로잉(Whiteboard) 동시 처리<br>- 비언어적 지표(표정, 목소리 떨림 등) 추출하여 태도 분석 | '자신감', '당황함' 등 감지 |
| **REQ-F-003** | **실시간 개입**<br>(Interruption Handling) | - 답변이 길어지거나 주제를 벗어날 경우 AI 면접관이 정중하게 개입 및 화제 전환<br>- VAD(Voice Activity Detection) 및 Turn-taking 알고리즘 고도화 | |

### 2.2 기술 역량 평가 (Technical Assessment)
| ID | 요구사항명 | 상세 내용 | 비고 |
| :--- | :--- | :--- | :--- |
| **REQ-F-004** | **라이브 코딩 환경** | - Python, JavaScript 등 주요 언어 지원 웹 IDE 내장<br>- 샌드박스 환경 실행 결과 분석<br>- 시간 복잡도, 코드 스타일, 주석 여부 등 종합 평가 | |
| **REQ-F-005** | **시스템 설계 화이트보드** | - 아키텍처 다이어그램 작성을 위한 캔버스 제공<br>- Vision AI(GPT-4V 등)를 활용한 아키텍처 타당성 시각적 인식 및 평가 | |

### 2.3 결과 분석 및 리포팅 (Reporting)
| ID | 요구사항명 | 상세 내용 | 비고 |
| :--- | :--- | :--- | :--- |
| **REQ-F-006** | **상세 피드백 리포트** | - STAR 기법(Situation, Task, Action, Result) 기반 답변 구조 분석<br>- 핵심 키워드, 발화 속도, 발음, 시선 처리 데이터 포함 | 면접 종료 직후 생성 |
| **REQ-F-007** | **채용 적합도 스코어링** | - 루브릭(Rubric)에 따른 역량별 점수(1~5점) 산출<br>- 합격/불합격 추천 의견 제시 | |

## 3. 비기능적 요구사항 (Non-Functional Requirements)

### 3.1 성능 및 확장성 (Performance & Scalability)
| ID | 요구사항명 | 상세 내용 | 목표치 |
| :--- | :--- | :--- | :--- |
| **REQ-N-001** | **초저지연 통신** | - WebRTC 기반 영상/음성 처리 지연 최소화<br>- STT 및 LLM 추론 포함 전체 응답 지연 시간 단축 | **End-to-End Latency < 1.5s** |
| **REQ-N-002** | **동시 접속 처리** | - 수평적 확장(Horizontal Scaling) 지원<br>- Kubernetes 오케스트레이션 활용 | 수백 개 세션 안정적 처리 |

### 3.2 보안 및 규정 준수 (Security & Compliance)
| ID | 요구사항명 | 상세 내용 | 규격/표준 |
| :--- | :--- | :--- | :--- |
| **REQ-N-003** | **생체 데이터 보호** | - 개인정보보호법(GDPR, CCPA 등) 준수<br>- 전송 시 TLS 1.3, 저장 시 AES-256 암호화<br>- 즉시 영구 삭제(Right to be forgotten) 기능 제공 | GDPR, AES-256 |
| **REQ-N-004** | **공정성 및 편향 방지** | - 인종, 성별, 억양에 따른 편향 제거를 위한 데이터셋 검증<br>- 평가 결과에 대한 설명 가능성(Explainability) 제공 | |
