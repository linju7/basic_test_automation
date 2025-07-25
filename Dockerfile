# Playwright Python 베이스 이미지
FROM mcr.microsoft.com/playwright/python:v1.45.1-jammy

# Python 환경 변수
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 비root 사용자 생성
RUN groupadd -r playwright && useradd -r -g playwright playwright

# 의존성 설치 (캐싱 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 브라우저 설치
RUN playwright install --with-deps

# 소스 코드 복사
COPY . .
RUN chown -R playwright:playwright /app

USER playwright

CMD ["python", "-m", "pytest"] 