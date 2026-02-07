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
