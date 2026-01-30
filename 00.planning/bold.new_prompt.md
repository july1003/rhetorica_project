**AI 웹 모의 면접 시스템**  **'레토리카'** **는 기능의 복잡도와 인프라 구성(Docker, Minio 등)이 구체적이므로,** **Bolt.new**에서 프로젝트 구조를 잡을 때 이를 명확히 지시해야 합니다.

Bolt.new에 입력하기 가장 좋은 **구조화된 영문 프롬프트**입니다. 이 내용을 그대로 복사해서 입력해 보세요.

🚀 Bolt.new 입력용 최적화 프롬프트

markdown

```
Create a full-stack web application named "Rhetorica" (AI Mock Interview System).

Core Tech Stack:
- Frontend: Next.js (App Router), Tailwind CSS, Shadcn/UI, Lucide React, Recharts (for graphs).
- Storage/Infra: Dockerized environment with Minio for PDF storage.

Key Features to Implement:
1. Landing Page: Service introduction for guests, News dashboard for logged-in users (based on job field & target companies).
2. Auth System: Sign up (Name, Email, Password, Job Category, 3 Target Companies), Email verification, and Login.
3. Credit System: Each user gets 3 free interview tokens by default.
4. Company Info Section: Display "Core Values" and "Recruitment Info" for selected fields.
5. Resume Upload (PDF): 
   - Save to Minio bucket 'Ethos-resumes' under path: /YYYY-MM-DD/interviewID_resume_{timestamp}.pdf.
   - Analysis logic to assign 1 of 3 AI Interviewers.
6. Mock Interview Interface: Video/Audio-based interview UI.
7. Post-Interview Report:
   - History List: Interview Date, Candidate ID/Name, Duration, Score, Result.
   - Analytics: Score graphs, Strengths/Weaknesses breakdown, and AI General Review.

Design Requirement: Modern, professional, and trustworthy enterprise-blue theme.
```

코드를 사용할 때는 주의가 필요합니다.

---

💡 개발 시 참고할 구현 전략

1. **Docker & Minio 설정** **: Bolt.new 환경에서는 실제 Docker 실행이 제한될 수 있습니다. 우선**  **Minio SDK(S3 compatible)** **를 사용하는 코드를 작성한 뒤, 실제 배포 시** **Minio 공식 가이드**를 참고하여 `docker-compose.yml`을 구성하세요.
2. **PDF 업로드** **: 브라우저에서 Minio로 직접 업로드하려면** **AWS SDK for JavaScript**를 사용하면 됩니다. (Minio는 S3 호환 API를 제공합니다.)
3. **데이터 시각화** **: 점수 그래프는** **Recharts** **라이브러리를 사용하여 오각형 레이더 차트나 선형 차트로 구현하면 면접 결과 분석 느낌을 잘 살릴 수 있습니다.**
4. **AI 연동** **: AI 면접관 로직은** **OpenAI API**를 연결하여 이력서 텍스트 추출 후 질문을 생성하도록 지시하세요.

**위 프롬프트를 Bolt.new에 넣으신 후, 생성된 화면 중**  **가장 먼저 수정하거나 보완하고 싶은 특정 페이지(예: 면접 결과 리포트)** **가 있으신가요? 바로 상세 설계를 도와드릴 수 있습니다.**
