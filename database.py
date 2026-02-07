"""
인메모리 데이터베이스
"""
from typing import List
from models import User, Task


# 사용자 데이터베이스
users_db: List[User] = [
    User(id=1, name="Alice", email="alice@example.com", age=28),
    User(id=2, name="Bob", email="bob@example.com", age=35),
]

# 작업 데이터베이스
tasks_db: List[Task] = [
    Task(id=1, title="학습", description="FastAPI 배우기", completed=False, user_id=1),
    Task(id=2, title="프로젝트", description="API 서버 구축", completed=True, user_id=1),
]
