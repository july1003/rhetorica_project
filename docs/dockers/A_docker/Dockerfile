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
# 여기에 Arize Phoenix 관련 패키지가 포함된 requirements.txt가 필요합니다.
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 5. 소스 코드 복사
COPY . .

# 6. 환경 변수 설정
ENV PYTHONUNBUFFERED=1

# 7. Arize Phoenix 수집기 주소 설정 (기본값)
# 실제 주소는 docker-compose.yml의 environment 섹션에서 덮어씌워집니다.
ENV PHOENIX_COLLECTOR_ENDPOINT=http://phoenix:6006

# 8. 실행
CMD ["python3", "main.py"]