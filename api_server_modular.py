"""
FastAPI 메인 애플리케이션
모듈화된 구조로 재구성
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, tasks, system

# FastAPI 앱 생성
app = FastAPI(
    title="Local API Server",
    description="로컬 환경에서 실행되는 모듈화된 API 서버",
    version="2.0.0"
)

# CORS 설정 (로컬 웹 UI 접근 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(system.router)


if __name__ == "__main__":
    import uvicorn
    # http://localhost:8000 에서 실행
    # API 문서: http://localhost:8000/docs (Swagger UI)
    # 대체 문서: http://localhost:8000/redoc (ReDoc)
    port = 8000
    print(f"🚀 서버 시작: http://127.0.0.1:{port}")
    print(f"📚 API 문서: http://127.0.0.1:{port}/docs")
    uvicorn.run(app, host="127.0.0.1", port=port)
