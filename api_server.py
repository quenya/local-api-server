from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json

app = FastAPI(
    title="Local API Server",
    description="로컬 환경에서 실행되는 API 서버",
    version="1.0.0"
)

# CORS 설정 (로컬 웹 UI 접근 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === 데이터 모델 정의 ===
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

# === 인메모리 데이터 저장소 ===
users_db: List[User] = [
    User(id=1, name="Alice", email="alice@example.com", age=28),
    User(id=2, name="Bob", email="bob@example.com", age=35),
]

tasks_db: List[Task] = [
    Task(id=1, title="학습", description="FastAPI 배우기", completed=False, user_id=1),
    Task(id=2, title="프로젝트", description="API 서버 구축", completed=True, user_id=1),
]

# === User API ===
@app.get("/api/users", tags=["Users"], summary="모든 사용자 조회")
def get_users(skip: int = 0, limit: int = 10):
    """
    모든 사용자 정보를 조회합니다.
    - **skip**: 건너뛸 항목 수
    - **limit**: 반환할 최대 항목 수
    """
    return users_db[skip:skip + limit]

@app.get("/api/users/{user_id}", tags=["Users"], summary="특정 사용자 조회")
def get_user(user_id: int):
    """특정 ID의 사용자 정보를 조회합니다."""
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return user

@app.post("/api/users", tags=["Users"], summary="새 사용자 생성", response_model=User)
def create_user(user: User):
    """
    새로운 사용자를 생성합니다.
    
    요청 예시:
    ```json
    {
        "name": "Charlie",
        "email": "charlie@example.com",
        "age": 30
    }
    ```
    """
    new_id = max((u.id for u in users_db), default=0) + 1
    user.id = new_id
    users_db.append(user)
    return user

@app.put("/api/users/{user_id}", tags=["Users"], summary="사용자 정보 수정")
def update_user(user_id: int, updated_user: User):
    """특정 ID의 사용자 정보를 수정합니다."""
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    user.name = updated_user.name
    user.email = updated_user.email
    user.age = updated_user.age
    return user

@app.delete("/api/users/{user_id}", tags=["Users"], summary="사용자 삭제")
def delete_user(user_id: int):
    """특정 ID의 사용자를 삭제합니다."""
    global users_db
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    users_db = [u for u in users_db if u.id != user_id]
    return {"message": "사용자가 삭제되었습니다", "id": user_id}

# === Task API ===
@app.get("/api/tasks", tags=["Tasks"], summary="모든 작업 조회")
def get_tasks(user_id: Optional[int] = None, skip: int = 0, limit: int = 10):
    """
    작업 목록을 조회합니다.
    - **user_id**: (선택) 특정 사용자의 작업만 필터링
    """
    filtered = tasks_db
    if user_id:
        filtered = [t for t in tasks_db if t.user_id == user_id]
    return filtered[skip:skip + limit]

@app.get("/api/tasks/{task_id}", tags=["Tasks"], summary="특정 작업 조회")
def get_task(task_id: int):
    """특정 ID의 작업 정보를 조회합니다."""
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="작업을 찾을 수 없습니다")
    return task

@app.post("/api/tasks", tags=["Tasks"], summary="새 작업 생성", response_model=Task)
def create_task(task: Task):
    """새로운 작업을 생성합니다."""
    new_id = max((t.id for t in tasks_db), default=0) + 1
    task.id = new_id
    tasks_db.append(task)
    return task

@app.patch("/api/tasks/{task_id}", tags=["Tasks"], summary="작업 상태 업데이트")
def update_task_status(task_id: int, completed: bool):
    """작업의 완료 상태를 업데이트합니다."""
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="작업을 찾을 수 없습니다")
    
    task.completed = completed
    return task

# === 헬스체크 ===
@app.get("/health", tags=["System"], summary="서버 상태 확인")
def health_check():
    """서버가 정상 작동 중인지 확인합니다."""
    return {
        "status": "healthy",
        "users_count": len(users_db),
        "tasks_count": len(tasks_db)
    }

if __name__ == "__main__":
    import uvicorn
    # http://localhost:8000 에서 실행
    # API 문서: http://localhost:8000/docs (Swagger UI)
    # 대체 문서: http://localhost:8000/redoc (ReDoc)
    port = 8000
    uvicorn.run(app, host="127.0.0.1", port=port)
