# 로컬 API 서버 구축 가이드

## 개요
- **백엔드**: FastAPI (Python) - `api_server.py`
- **프론트엔드**: React 기반 API 테스터 UI - `api_ui.jsx`
- **통신**: REST API + OpenAPI 명세

---

## 1. Python 백엔드 실행

### 1.1 필수 라이브러리 설치
```bash
pip install fastapi uvicorn pydantic python-multipart
```

### 1.2 서버 시작
```bash
python api_server.py
```

**출력:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 1.3 기본 제공 문서 확인
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 2. React UI 실행

### 2.1 React 프로젝트 생성 (만약 없다면)
```bash
npx create-react-app api-tester
cd api-tester
```

### 2.2 컴포넌트 추가
`api_ui.jsx`의 내용을 `src/App.jsx`에 복사하거나, 별도 컴포넌트로 추가

### 2.3 개발 서버 실행
```bash
npm start
```

**자동으로 열림**: http://localhost:3000

---

## 3. API 테스트

### 3.1 웹 UI를 통한 테스트 (권장)
React UI의 인터페이스에서:
1. 왼쪽 **태그** 선택 (Users, Tasks, System)
2. **엔드포인트** 클릭
3. **파라미터** 입력 (필요한 경우)
4. **요청 본문** 입력 (POST/PUT/PATCH의 경우)
5. **API 호출** 버튼 클릭
6. 하단에서 응답 확인

### 3.2 직접 요청 테스트 (curl)

#### 사용자 조회
```bash
curl http://localhost:8000/api/users
```

#### 새 사용자 생성
```bash
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "David",
    "email": "david@example.com",
    "age": 32
  }'
```

#### 사용자 수정
```bash
curl -X PUT http://localhost:8000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Updated",
    "email": "alice.updated@example.com",
    "age": 29
  }'
```

#### 작업 생성
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "새 작업",
    "description": "이것은 테스트 작업입니다",
    "completed": false,
    "user_id": 1
  }'
```

#### 특정 사용자의 작업 조회
```bash
curl "http://localhost:8000/api/tasks?user_id=1"
```

---

## 4. API 엔드포인트 명세

### Users API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/users` | 모든 사용자 조회 |
| GET | `/api/users/{user_id}` | 특정 사용자 조회 |
| POST | `/api/users` | 새 사용자 생성 |
| PUT | `/api/users/{user_id}` | 사용자 정보 수정 |
| DELETE | `/api/users/{user_id}` | 사용자 삭제 |

### Tasks API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/tasks` | 모든 작업 조회 (user_id로 필터 가능) |
| GET | `/api/tasks/{task_id}` | 특정 작업 조회 |
| POST | `/api/tasks` | 새 작업 생성 |
| PATCH | `/api/tasks/{task_id}` | 작업 상태 업데이트 |

### System API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/health` | 서버 상태 확인 |

---

## 5. Java 프로젝트에서 사용하기

### 5.1 HTTP 클라이언트 라이브러리 추가
```java
// Maven
<dependency>
    <groupId>com.squareup.okhttp3</groupId>
    <artifactId>okhttp</artifactId>
    <version>4.11.0</version>
</dependency>

// or Gradle
implementation 'com.squareup.okhttp3:okhttp:4.11.0'
```

### 5.2 API 호출 예제
```java
import okhttp3.*;
import org.json.JSONObject;

public class APIClient {
    private static final String BASE_URL = "http://localhost:8000";
    private final OkHttpClient client = new OkHttpClient();

    // 사용자 조회
    public void getUsers() throws Exception {
        Request request = new Request.Builder()
            .url(BASE_URL + "/api/users")
            .build();
        
        try (Response response = client.newCall(request).execute()) {
            System.out.println(response.body().string());
        }
    }

    // 새 사용자 생성
    public void createUser(String name, String email, int age) throws Exception {
        JSONObject json = new JSONObject();
        json.put("name", name);
        json.put("email", email);
        json.put("age", age);
        
        RequestBody body = RequestBody.create(
            json.toString(),
            MediaType.parse("application/json")
        );
        
        Request request = new Request.Builder()
            .url(BASE_URL + "/api/users")
            .post(body)
            .build();
        
        try (Response response = client.newCall(request).execute()) {
            System.out.println(response.body().string());
        }
    }

    public static void main(String[] args) throws Exception {
        APIClient client = new APIClient();
        client.getUsers();
        client.createUser("Charlie", "charlie@example.com", 30);
    }
}
```

---

## 6. 커스터마이징

### 6.1 새 API 엔드포인트 추가

```python
# api_server.py에 추가

@app.get("/api/analytics", tags=["Analytics"], summary="분석 데이터 조회")
def get_analytics(user_id: int):
    """특정 사용자의 분석 데이터를 반환합니다."""
    user_tasks = [t for t in tasks_db if t.user_id == user_id]
    completed = sum(1 for t in user_tasks if t.completed)
    
    return {
        "user_id": user_id,
        "total_tasks": len(user_tasks),
        "completed_tasks": completed,
        "completion_rate": (completed / len(user_tasks) * 100) if user_tasks else 0
    }
```

### 6.2 데이터베이스 연동

FastAPI는 SQLAlchemy, Tortoise ORM, MongoDB 등과 쉽게 통합됩니다:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite 데이터베이스 생성
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 그 후 쿼리 수행
```

### 6.3 인증 추가

```python
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

@app.get("/api/users")
def get_users(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "admin" or credentials.password != "password":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return users_db
```

---

## 7. 트러블슈팅

### 포트가 이미 사용 중인 경우
```bash
# 포트 8000을 사용하는 프로세스 찾기
lsof -i :8000

# 다른 포트에서 실행
python -c "import uvicorn; uvicorn.run('api_server:app', host='127.0.0.1', port=8001)"
```

### CORS 에러
- `api_server.py`의 `CORSMiddleware` 설정 확인
- `allow_origins`에 프론트엔드 URL 추가

### OpenAPI 문서 보이지 않음
- `/docs` 또는 `/redoc`으로 접근 시 빈 페이지가 나타나면 브라우저 캐시 삭제

---

## 8. 배포

### 로컬에서만 사용하기
현재 설정(127.0.0.1)이 안전하며, 외부 접근 불가능합니다.

### 네트워크 접근 허용 (주의!)
```python
# api_server.py에서
uvicorn.run(app, host="0.0.0.0", port=8000)  # 모든 인터페이스에서 접근 가능
```

**주의**: 이 경우 방화벽 설정과 인증을 반드시 추가하세요.

---

## 다음 단계

1. **데이터 영속성**: SQLite/PostgreSQL 연동
2. **인증/권한**: JWT 토큰 기반 인증
3. **캐싱**: Redis를 통한 성능 최적화
4. **배포**: Docker 컨테이너화 또는 클라우드 호스팅
5. **모니터링**: 로깅 및 성능 분석
