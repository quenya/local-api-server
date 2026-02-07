FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필수 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY api_server.py .

# 포트 노출
EXPOSE 8000

# 서버 실행
CMD ["python", "api_server.py"]
