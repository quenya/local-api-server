"""
시스템 관련 API 라우터
"""
from fastapi import APIRouter
from database import users_db, tasks_db

router = APIRouter(tags=["System"])


@router.get("/health", summary="서버 상태 확인")
def health_check() -> dict:
    """서버가 정상 작동 중인지 확인합니다."""
    return {
        "status": "healthy",
        "users_count": len(users_db),
        "tasks_count": len(tasks_db)
    }
