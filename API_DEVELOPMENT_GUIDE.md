# 🚀 새로운 API 추가 가이드

> 이 가이드는 local-api-server 프로젝트에 새로운 API를 추가하는 방법을 단계별로 설명합니다.

---

## 📋 목차

1. [시작하기 전에](#시작하기-전에)
2. [모듈화된 구조 이해하기](#모듈화된-구조-이해하기)
3. [새 API 추가 단계](#새-api-추가-단계)
4. [실전 예제](#실전-예제)
5. [베스트 프랙티스](#베스트-프랙티스)
6. [테스트 방법](#테스트-방법)
7. [문제 해결](#문제-해결)

---

## 시작하기 전에

### 필수 사항
- ✅ Python 3.8 이상 설치
- ✅ FastAPI 기본 개념 이해
- ✅ RESTful API 설계 원칙 숙지
- ✅ 프로젝트 구조 파악 (`PROJECT_ANALYSIS.md` 참고)

### 권장 사항
- 📚 Pydantic 데이터 검증 이해
- 📚 HTTP 메서드 (GET, POST, PUT, PATCH, DELETE) 이해
- 📚 OpenAPI/Swagger 문서화 방식 이해

---

## 모듈화된 구조 이해하기

### 프로젝트 구조

```
local-api-server/
├── models.py                  # 데이터 모델 정의
├── database.py                # 인메모리 데이터베이스
├── api_server_modular.py      # 메인 애플리케이션
├── routers/                   # API 라우터 모듈
│   ├── __init__.py
│   ├── users.py               # 사용자 API
│   ├── tasks.py               # 작업 API
│   ├── system.py              # 시스템 API
│   └── news.py                # 뉴스 API
└── services/                  # 비즈니스 로직 서비스
    ├── __init__.py
    ├── news_fetcher.py        # 뉴스 수집
    ├── news_processor.py      # 뉴스 처리
    └── news_summarizer.py     # 뉴스 요약
```

### 각 파일의 역할

| 파일 | 역할 | 수정 빈도 |
|------|------|----------|
| `models.py` | 데이터 모델 (Pydantic) | 새 엔티티 추가 시 |
| `database.py` | 데이터 저장소 | 새 데이터 추가 시 |
| `routers/*.py` | API 엔드포인트 | 새 API 추가 시 |
| `api_server_modular.py` | 앱 초기화 및 라우터 등록 | 새 라우터 추가 시 |

---

## 새 API 추가 단계

### Step 1: 데이터 모델 정의

**파일**: `models.py`

```python
from pydantic import BaseModel
from typing import Optional

class YourModel(BaseModel):
    """모델 설명"""
    id: Optional[int] = None
    field1: str
    field2: int
    field3: bool = False  # 기본값 설정 가능
```

**체크리스트**:
- [ ] 클래스명은 단수형 (예: `Product`, `Order`)
- [ ] Docstring 작성
- [ ] 필수 필드와 선택 필드 구분
- [ ] 적절한 타입 힌트 사용
- [ ] 기본값 설정 (필요시)

### Step 2: 데이터베이스 초기화

**파일**: `database.py`

```python
from typing import List
from models import YourModel

# 초기 데이터 정의
your_model_db: List[YourModel] = [
    YourModel(id=1, field1="example", field2=100),
    YourModel(id=2, field1="sample", field2=200),
]
```

**체크리스트**:
- [ ] 변수명은 복수형 + `_db` (예: `products_db`)
- [ ] 타입 힌트 명시
- [ ] 테스트용 초기 데이터 2-3개 추가

### Step 3: 라우터 생성

**파일**: `routers/your_router.py`

```python
"""
[기능] 관련 API 라우터
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from models import YourModel
from database import your_model_db

router = APIRouter(prefix="/api/your-resource", tags=["YourResource"])


@router.get("", summary="모든 항목 조회")
def get_all(skip: int = 0, limit: int = 10) -> List[YourModel]:
    """모든 항목을 조회합니다."""
    return your_model_db[skip:skip + limit]


@router.get("/{item_id}", summary="특정 항목 조회")
def get_one(item_id: int) -> YourModel:
    """특정 ID의 항목을 조회합니다."""
    item = next((i for i in your_model_db if i.id == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="항목을 찾을 수 없습니다")
    return item


@router.post("", summary="새 항목 생성", response_model=YourModel)
def create(item: YourModel) -> YourModel:
    """새로운 항목을 생성합니다."""
    new_id = max((i.id for i in your_model_db), default=0) + 1
    item.id = new_id
    your_model_db.append(item)
    return item


@router.put("/{item_id}", summary="항목 수정")
def update(item_id: int, updated_item: YourModel) -> YourModel:
    """특정 ID의 항목을 수정합니다."""
    item = next((i for i in your_model_db if i.id == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="항목을 찾을 수 없습니다")
    
    # 필드 업데이트
    item.field1 = updated_item.field1
    item.field2 = updated_item.field2
    return item


@router.delete("/{item_id}", summary="항목 삭제")
def delete(item_id: int) -> dict:
    """특정 ID의 항목을 삭제합니다."""
    global your_model_db
    item = next((i for i in your_model_db if i.id == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="항목을 찾을 수 없습니다")
    
    your_model_db = [i for i in your_model_db if i.id != item_id]
    return {"message": "항목이 삭제되었습니다", "id": item_id}
```

**체크리스트**:
- [ ] 파일 상단에 Docstring 작성
- [ ] `APIRouter` prefix는 `/api/` 시작
- [ ] tags는 리소스명 (복수형, PascalCase)
- [ ] 모든 함수에 summary와 docstring 작성
- [ ] 404 에러 처리 포함
- [ ] 타입 힌트 명시

### Step 4: 라우터 등록

**파일**: `routers/__init__.py`

```python
from . import users, tasks, system, your_router

__all__ = ["users", "tasks", "system", "your_router"]
```

**파일**: `api_server_modular.py`

```python
from routers import users, tasks, system, your_router

# ... (기존 코드)

# 라우터 등록
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(system.router)
app.include_router(your_router.router)  # 새 라우터 추가
```

**체크리스트**:
- [ ] `__init__.py`에 import 추가
- [ ] `__all__` 리스트에 추가
- [ ] 메인 앱에 `include_router` 호출

### Step 5: 테스트

```bash
# 서버 실행
python api_server_modular.py

# 브라우저에서 확인
# http://localhost:8000/docs
```

---

## 실전 예제

### 예제 1: 제품(Product) API 추가

#### 1. 모델 정의 (`models.py`)

```python
class Product(BaseModel):
    """제품 정보"""
    id: Optional[int] = None
    name: str
    price: float
    stock: int
    category: str
```

#### 2. 데이터베이스 (`database.py`)

```python
products_db: List[Product] = [
    Product(id=1, name="노트북", price=1500000, stock=10, category="전자제품"),
    Product(id=2, name="마우스", price=30000, stock=50, category="전자제품"),
]
```

#### 3. 라우터 (`routers/products.py`)

```python
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from models import Product
from database import products_db

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("", summary="모든 제품 조회")
def get_products(category: Optional[str] = None) -> List[Product]:
    """
    제품 목록을 조회합니다.
    - **category**: (선택) 카테고리로 필터링
    """
    if category:
        return [p for p in products_db if p.category == category]
    return products_db


@router.get("/{product_id}", summary="특정 제품 조회")
def get_product(product_id: int) -> Product:
    """특정 ID의 제품을 조회합니다."""
    product = next((p for p in products_db if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="제품을 찾을 수 없습니다")
    return product


@router.post("", summary="새 제품 생성", response_model=Product)
def create_product(product: Product) -> Product:
    """새로운 제품을 생성합니다."""
    new_id = max((p.id for p in products_db), default=0) + 1
    product.id = new_id
    products_db.append(product)
    return product


@router.patch("/{product_id}/stock", summary="재고 업데이트")
def update_stock(product_id: int, stock: int) -> Product:
    """제품의 재고를 업데이트합니다."""
    product = next((p for p in products_db if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="제품을 찾을 수 없습니다")
    
    product.stock = stock
    return product
```

#### 4. 등록

```python
# routers/__init__.py
from . import users, tasks, system, products

# api_server_modular.py
from routers import products
app.include_router(products.router)
```

---

### 예제 2: 댓글(Comment) API 추가 (관계형 데이터)

#### 1. 모델 정의

```python
class Comment(BaseModel):
    """댓글 정보"""
    id: Optional[int] = None
    content: str
    author_id: int  # User와 관계
    task_id: int    # Task와 관계
    created_at: str
```

#### 2. 라우터 (필터링 예제)

```python
@router.get("", summary="댓글 조회")
def get_comments(
    task_id: Optional[int] = None,
    author_id: Optional[int] = None
) -> List[Comment]:
    """
    댓글을 조회합니다.
    - **task_id**: 특정 작업의 댓글만
    - **author_id**: 특정 작성자의 댓글만
    """
    filtered = comments_db
    
    if task_id:
        filtered = [c for c in filtered if c.task_id == task_id]
    
    if author_id:
        filtered = [c for c in filtered if c.author_id == author_id]
    
    return filtered
```

---

### 예제 3: 통계(Statistics) API 추가 (읽기 전용)

```python
# routers/statistics.py
from fastapi import APIRouter
from database import users_db, tasks_db, products_db

router = APIRouter(prefix="/api/statistics", tags=["Statistics"])


@router.get("/summary", summary="전체 통계")
def get_summary() -> dict:
    """전체 시스템 통계를 반환합니다."""
    completed_tasks = sum(1 for t in tasks_db if t.completed)
    
    return {
        "total_users": len(users_db),
        "total_tasks": len(tasks_db),
        "completed_tasks": completed_tasks,
        "completion_rate": completed_tasks / len(tasks_db) if tasks_db else 0,
        "total_products": len(products_db),
    }


@router.get("/user/{user_id}/stats", summary="사용자별 통계")
def get_user_stats(user_id: int) -> dict:
    """특정 사용자의 통계를 반환합니다."""
    user_tasks = [t for t in tasks_db if t.user_id == user_id]
    completed = sum(1 for t in user_tasks if t.completed)
    
    return {
        "user_id": user_id,
        "total_tasks": len(user_tasks),
        "completed_tasks": completed,
        "pending_tasks": len(user_tasks) - completed,
    }
```

---

## 베스트 프랙티스

### 1. 명명 규칙

| 항목 | 규칙 | 예시 |
|------|------|------|
| 모델 클래스 | PascalCase, 단수형 | `User`, `Product` |
| 데이터베이스 변수 | snake_case, 복수형 + `_db` | `users_db`, `products_db` |
| 라우터 파일 | snake_case, 복수형 | `users.py`, `products.py` |
| API 경로 | kebab-case, 복수형 | `/api/users`, `/api/products` |
| 함수명 | snake_case, 동사 시작 | `get_users`, `create_product` |

### 2. HTTP 메서드 선택

| 작업 | 메서드 | 예시 |
|------|--------|------|
| 조회 (목록) | GET | `GET /api/users` |
| 조회 (단일) | GET | `GET /api/users/1` |
| 생성 | POST | `POST /api/users` |
| 전체 수정 | PUT | `PUT /api/users/1` |
| 부분 수정 | PATCH | `PATCH /api/users/1` |
| 삭제 | DELETE | `DELETE /api/users/1` |

### 3. 에러 처리

```python
from fastapi import HTTPException

# 404 Not Found
if not item:
    raise HTTPException(status_code=404, detail="항목을 찾을 수 없습니다")

# 400 Bad Request
if invalid_data:
    raise HTTPException(status_code=400, detail="잘못된 요청입니다")

# 409 Conflict
if duplicate:
    raise HTTPException(status_code=409, detail="이미 존재하는 항목입니다")
```

### 4. 문서화

```python
@router.get("/{item_id}", summary="짧은 요약")
def get_item(item_id: int) -> Item:
    """
    상세한 설명을 여기에 작성합니다.
    
    - **item_id**: 항목의 고유 ID
    
    반환값:
    - Item 객체
    
    예외:
    - 404: 항목을 찾을 수 없음
    """
    pass
```

### 5. 쿼리 파라미터 vs 경로 파라미터

```python
# 경로 파라미터: 특정 리소스 식별
@router.get("/{user_id}")
def get_user(user_id: int):
    pass

# 쿼리 파라미터: 필터링, 페이지네이션
@router.get("")
def get_users(skip: int = 0, limit: int = 10, role: Optional[str] = None):
    pass
```

---

## 테스트 방법

### 1. Swagger UI 사용

```bash
# 서버 실행
python api_server_modular.py

# 브라우저에서 접속
# http://localhost:8000/docs
```

1. 원하는 엔드포인트 클릭
2. "Try it out" 버튼 클릭
3. 파라미터 입력
4. "Execute" 버튼 클릭
5. 응답 확인

### 2. curl 사용

```bash
# GET 요청
curl http://localhost:8000/api/products

# POST 요청
curl -X POST http://localhost:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"키보드","price":80000,"stock":30,"category":"전자제품"}'

# PUT 요청
curl -X PUT http://localhost:8000/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"노트북 Pro","price":2000000,"stock":5,"category":"전자제품"}'

# DELETE 요청
curl -X DELETE http://localhost:8000/api/products/1
```

### 3. Python requests 사용

```python
import requests

BASE_URL = "http://localhost:8000"

# GET
response = requests.get(f"{BASE_URL}/api/products")
print(response.json())

# POST
new_product = {
    "name": "키보드",
    "price": 80000,
    "stock": 30,
    "category": "전자제품"
}
response = requests.post(f"{BASE_URL}/api/products", json=new_product)
print(response.json())
```

---

## 문제 해결

### 문제 1: 라우터가 인식되지 않음

**증상**: API 문서에 새 엔드포인트가 나타나지 않음

**해결**:
1. `routers/__init__.py`에 import 확인
2. `api_server_modular.py`에 `include_router` 확인
3. 서버 재시작

### 문제 2: 404 에러 발생

**증상**: 엔드포인트 호출 시 404 반환

**해결**:
1. URL 경로 확인 (prefix + 함수 경로)
2. HTTP 메서드 확인 (GET, POST 등)
3. Swagger UI에서 정확한 경로 확인

### 문제 3: 데이터 검증 오류

**증상**: 422 Unprocessable Entity 에러

**해결**:
1. 요청 본문의 필드명 확인
2. 데이터 타입 확인 (str, int, bool 등)
3. 필수 필드 누락 확인
4. Swagger UI에서 스키마 확인

### 문제 4: CORS 에러

**증상**: 브라우저에서 "CORS policy" 에러

**해결**:
```python
# api_server_modular.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://your-frontend-url"],
    # ...
)
```

---

## 고급 기능

### 1. 의존성 주입

```python
from fastapi import Depends

def get_current_user():
    # 현재 사용자 확인 로직
    return {"user_id": 1, "username": "admin"}

@router.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello {current_user['username']}"}
```

### 2. 백그라운드 작업

```python
from fastapi import BackgroundTasks

def send_notification(email: str):
    # 이메일 전송 로직
    print(f"Sending email to {email}")

@router.post("/users")
def create_user(user: User, background_tasks: BackgroundTasks):
    users_db.append(user)
    background_tasks.add_task(send_notification, user.email)
    return user
```

### 3. 파일 업로드

```python
from fastapi import File, UploadFile

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}
```

---

## 체크리스트

새 API를 추가할 때 이 체크리스트를 사용하세요:

- [ ] **모델 정의** (`models.py`)
  - [ ] Pydantic BaseModel 상속
  - [ ] 타입 힌트 명시
  - [ ] Docstring 작성
  
- [ ] **데이터베이스** (`database.py`)
  - [ ] 초기 데이터 추가
  - [ ] 타입 힌트 명시
  
- [ ] **라우터 생성** (`routers/your_router.py`)
  - [ ] APIRouter 생성 (prefix, tags)
  - [ ] CRUD 엔드포인트 구현
  - [ ] 에러 처리 추가
  - [ ] Docstring 작성
  
- [ ] **라우터 등록**
  - [ ] `routers/__init__.py` 업데이트
  - [ ] `api_server_modular.py`에 include_router
  
- [ ] **테스트**
  - [ ] Swagger UI에서 확인
  - [ ] 각 엔드포인트 테스트
  - [ ] 에러 케이스 테스트

---

## 다음 단계

1. **데이터베이스 연동**: SQLite, PostgreSQL
2. **인증 추가**: JWT, OAuth2
3. **캐싱**: Redis
4. **로깅**: 구조화된 로깅
5. **테스트**: pytest를 사용한 자동화 테스트

---

**Happy Coding! 🎉**
