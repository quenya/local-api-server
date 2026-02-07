"""
작업 관련 API 라우터
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from models import Task
from database import tasks_db

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.get("", summary="모든 작업 조회")
def get_tasks(user_id: Optional[int] = None, skip: int = 0, limit: int = 10) -> List[Task]:
    """
    작업 목록을 조회합니다.
    - **user_id**: (선택) 특정 사용자의 작업만 필터링
    """
    filtered = tasks_db
    if user_id:
        filtered = [t for t in tasks_db if t.user_id == user_id]
    return filtered[skip:skip + limit]


@router.get("/{task_id}", summary="특정 작업 조회")
def get_task(task_id: int) -> Task:
    """특정 ID의 작업 정보를 조회합니다."""
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="작업을 찾을 수 없습니다")
    return task


@router.post("", summary="새 작업 생성", response_model=Task)
def create_task(task: Task) -> Task:
    """새로운 작업을 생성합니다."""
    new_id = max((t.id for t in tasks_db), default=0) + 1
    task.id = new_id
    tasks_db.append(task)
    return task


@router.patch("/{task_id}", summary="작업 상태 업데이트")
def update_task_status(task_id: int, completed: bool) -> Task:
    """작업의 완료 상태를 업데이트합니다."""
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="작업을 찾을 수 없습니다")
    
    task.completed = completed
    return task
