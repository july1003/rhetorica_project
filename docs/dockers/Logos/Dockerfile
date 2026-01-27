# 1. GPU 지원 및 파이썬 환경을 위한 NVIDIA CUDA 베이스 이미지 사용
FROM nvidia/cuda:12.1.0-base-ubuntu22.04

# 2. 파이썬 및 필수 시스템 패키지 설치
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libpq-dev \
    libaio1 \
    wget \
    unzip \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 3. 작업 디렉토리 설정
WORKDIR /app

# 4. 파이썬 패키지 설치
COPY requirements.txt .
# pip 업그레이드 및 패키지 설치
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# 5. 소스 코드 복사
COPY . .

# 6. 환경 변수 설정
ENV PYTHONUNBUFFERED=1
# Arize Phoenix 및 OpenTelemetry 설정을 위한 환경 변수
ENV PHOENIX_COLLECTOR_ENDPOINT=http://phoenix:6006
ENV OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf

# 7. 실행 (FastAPI 서버를 위해 Uvicorn 사용)
# main.py 안에 app = FastAPI() 가 있다고 가정합니다.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]