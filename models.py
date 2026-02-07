"""
데이터 모델 정의
"""
from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    """사용자 정보"""
    id: Optional[int] = None
    name: str
    email: str
    age: int


class Task(BaseModel):
    """작업 정보"""
    id: Optional[int] = None
    title: str
    description: str
    completed: bool = False
    user_id: int


class NewsArticle(BaseModel):
    """뉴스 기사 정보"""
    id: Optional[int] = None
    title: str
    url: str
    source: str  # 뉴스 소스 (예: "네이버", "다음", "조선일보")
    published_at: str  # ISO 8601 형식
    summary: Optional[str] = None
    view_count: Optional[int] = 0
    comment_count: Optional[int] = 0
    hotness_score: Optional[float] = 0.0
