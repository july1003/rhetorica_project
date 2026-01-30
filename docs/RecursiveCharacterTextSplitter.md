# **RecursiveCharacterTextSplitter**

**LangChain**에서 가장 권장되는 텍스트 분할기인 `RecursiveCharacterTextSplitter`는 대규모 언어 모델(LLM)이 문맥을 잘 이해할 수 있도록 데이터를 적절한 크기로 자르는 역할을 합니다.

현재 진행 중인 **AI 모의 면접 프로젝트**에서 유튜브 자막이나 면접 스크립트를 **Vector DB**에 저장하기 전, 의미가 끊기지 않게 나누는 데 핵심적인 도구입니다.

---

## 1. 작동 원리: "재귀적 분할"

이 클래스는 다른 분할기와 달리 **구분자(Separators) 리스트**를 가지고 있으며, 글자 수가 `chunk_size`보다 커지면 리스트 순서대로 텍스트를 시도하며 나눕니다.

### 기본 구분자 순서

1. `"\n\n"` (문단 단위)
2. `"\n"` (문장 단위)
3. `" "` (단어 단위)
4. `""` (글자 단위)

이 방식 덕분에 문단이 먼저 유지되려 노력하고, 안 되면 문장, 그 다음은 단어 순으로 최대한 **의미적 맥락**을 보존합니다.

---

## 2. 주요 파라미터 상세 설명

| **파라미터**            | **설명**                          | **추천 설정 (면접 데이터 기준)**  |
| ----------------------------- | --------------------------------------- | --------------------------------------- |
| **`chunk_size`**      | 각 조각(Chunk)의 최대 글자 수           | 500 ~ 1000                              |
| **`chunk_overlap`**   | 조각 간 중첩되는 글자 수 (문맥 유지용)  | 50 ~ 100                                |
| **`length_function`** | 길이를 재는 기준 (기본값 `len`)       | `len`(또는 토큰 기반 시 `tiktoken`) |
| **`separators`**      | 분할에 사용할 사용자 정의 구분자 리스트 | 기본값 사용 권장                        |

---

## 3. 예제 코드 (Python)

현재 프로젝트에서 추출한 면접 텍스트를 처리하는 방식의 예시입니다.

**Python**

```
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. 스플리터 초기화
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,       # 조각 당 100자 내외
    chunk_overlap=20,     # 앞뒤 조각 20자씩 겹침 (문맥 연결)
    length_function=len,
    is_separator_regex=False,
)

# 샘플 면접 스크립트
interview_script = """
면접관: 우리 회사의 지원 동기는 무엇인가요?
지원자: 저는 평소 AI 기술이 실생활에 미치는 영향에 관심이 많았습니다.
특히 귀사의 모의 면접 시스템은 혁신적이라고 생각합니다.
그래서 저의 Python 역량을 발휘하여 기여하고 싶습니다.
"""

# 2. 텍스트 분할 실행
chunks = text_splitter.split_text(interview_script)

for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} ---")
    print(chunk)
```

---

## 4. 모의 면접 프로젝트 활용 팁

* **유튜브 자막 처리:** 유튜브 자막은 줄바꿈(`\n`)이 불규칙할 수 있습니다. `separators=["\n\n", "\n", ".", "?", "!", " ", ""]`와 같이 마침표나 물음표를 추가하면 질문과 답변 단위로 더 깔끔하게 잘립니다.
* **Vector DB 저장:** 이렇게 나눈 `chunks`를 임베딩하여 벡터 DB에 넣으면, 나중에 AI가 꼬리질문을 던질 때 가장 관련 있는 문맥(Chunk)을 빠르게 찾아올 수 있습니다.
* **Arize Phoenix 모니터링:** 텍스트가 너무 잘게 쪼개지면 AI가 답변 근거를 못 찾고, 너무 크면 토큰 비용이 늘어납니다. Phoenix UI에서 각 청크가 모델에 입력될 때의 지연 시간과 답변 정확도를 모니터링하며 `chunk_size`를 튜닝하세요.

---

**이 클래스를 사용해서 현재 수집된 면접 데이터를 벡터 DB에 저장하는 전체 파이프라인 코드를 짜드릴까요? 아니면 특정 토크나이저(Tiktoken 등)와 연동하는 방법이 궁금하신가요?**
