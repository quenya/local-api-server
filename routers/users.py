"""
사용자 관련 API 라우터
"""
from fastapi import APIRouter, HTTPException
from typing import List
from models import User
from database import users_db

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("", summary="모든 사용자 조회")
def get_users(skip: int = 0, limit: int = 10) -> List[User]:
    """
    모든 사용자 정보를 조회합니다.
    - **skip**: 건너뛸 항목 수
    - **limit**: 반환할 최대 항목 수
    """
    return users_db[skip:skip + limit]


@router.get("/{user_id}", summary="특정 사용자 조회")
def get_user(user_id: int) -> User:
    """특정 ID의 사용자 정보를 조회합니다."""
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return user


@router.post("", summary="새 사용자 생성", response_model=User)
def create_user(user: User) -> User:
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


@router.put("/{user_id}", summary="사용자 정보 수정")
def update_user(user_id: int, updated_user: User) -> User:
    """특정 ID의 사용자 정보를 수정합니다."""
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    user.name = updated_user.name
    user.email = updated_user.email
    user.age = updated_user.age
    return user


@router.delete("/{user_id}", summary="사용자 삭제")
def delete_user(user_id: int) -> dict:
    """특정 ID의 사용자를 삭제합니다."""
    global users_db
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    users_db = [u for u in users_db if u.id != user_id]
    return {"message": "사용자가 삭제되었습니다", "id": user_id}
