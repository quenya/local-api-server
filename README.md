# 🚀 로컬 API 서버 완전 가이드

## 📦 프로젝트 구조

```
local-api-server/
├── api_server.py           # FastAPI 백엔드 (Python)
├── api_ui.jsx              # React UI 컴포넌트
├── LocalAPIClient.java     # Java 클라이언트 예제
├── requirements.txt        # Python 의존성
├── Dockerfile              # Docker 컨테이너 설정
├── SETUP_GUIDE.md          # 상세 설정 가이드
└── README.md               # 이 파일
```

---

## ⚡ 5분 안에 시작하기

### 1️⃣ Python 백엔드 실행

```bash
# 라이브러리 설치
pip install fastapi uvicorn pydantic python-multipart

# 서버 시작
python api_server.py
```

✅ **출력:** `Uvicorn running on http://127.0.0.1:8000`

### 2️⃣ Swagger UI 확인 (선택)

- 브라우저: http://localhost:8000/docs
- 모든 API를 여기서 직접 테스트 가능

### 3️⃣ React UI 실행 (선택)

```bash
# React 프로젝트가 있다면
npm install

# src/App.jsx에 api_ui.jsx 내용 복사 후
npm start
```

✅ **열림:** http://localhost:3000

### 4️⃣ Java 프로젝트에서 사용

```bash
# 다운로드한 LocalAPIClient.java를 프로젝트에 추가
# Maven 의존성 추가:
# - okhttp3:okhttp:4.11.0
# - org.json:json:20231013
```

---

## 🎯 API 명세

### Users (사용자)

```
GET    /api/users              모든 사용자 조회
GET    /api/users/{id}         특정 사용자 조회
POST   /api/users              새 사용자 생성
PUT    /api/users/{id}         사용자 수정
DELETE /api/users/{id}         사용자 삭제
```

**사용자 객체:**
```json
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com",
  "age": 28
}
```

### Tasks (작업)

```
GET    /api/tasks              모든 작업 조회 (user_id로 필터 가능)
GET    /api/tasks/{id}         특정 작업 조회
POST   /api/tasks              새 작업 생성
PATCH  /api/tasks/{id}         작업 상태 업데이트
```

**작업 객체:**
```json
{
  "id": 1,
  "title": "학습",
  "description": "FastAPI 배우기",
  "completed": false,
  "user_id": 1
}
```

### System

```
GET    /health                 서버 상태 확인
```

---

## 📝 실전 예제

### Python에서 호출

```python
import requests

BASE_URL = "http://localhost:8000"

# 모든 사용자 조회
response = requests.get(f"{BASE_URL}/api/users")
print(response.json())

# 새 사용자 생성
new_user = {
    "name": "Charlie",
    "email": "charlie@example.com",
    "age": 30
}
response = requests.post(f"{BASE_URL}/api/users", json=new_user)
print(response.json())
```

### JavaScript/Node.js에서 호출

```javascript
const BASE_URL = 'http://localhost:8000';

// 모든 사용자 조회
const response = await fetch(`${BASE_URL}/api/users`);
const users = await response.json();
console.log(users);

// 새 사용자 생성
const newUser = {
  name: 'David',
  email: 'david@example.com',
  age: 32
};

const createResponse = await fetch(`${BASE_URL}/api/users`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(newUser)
});

const createdUser = await createResponse.json();
console.log(createdUser);
```

### Java에서 호출

```java
LocalAPIClient client = new LocalAPIClient();

// 모든 사용자 조회
client.getAllUsers();

// 새 사용자 생성
client.createUser("Emma", "emma@example.com", 26);

// 작업 생성
client.createTask("개발 완료", "Java API 클라이언트 개발", false, 1);
```

---

## 🐳 Docker를 사용한 배포

### 1. 이미지 빌드

```bash
docker build -t local-api-server .
```

### 2. 컨테이너 실행

```bash
docker run -p 8000:8000 local-api-server
```

### 3. 확인

```bash
curl http://localhost:8000/health
```

---

## 🔧 커스터마이징

### 새 API 엔드포인트 추가

`api_server.py`에 다음을 추가:

```python
@app.get("/api/custom", tags=["Custom"], summary="커스텀 엔드포인트")
def get_custom_data():
    """새로운 커스텀 엔드포인트입니다."""
    return {"message": "Hello from custom endpoint"}
```

### 데이터베이스 연동

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 테이블 정의
class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    age = Column(Integer)

# 테이블 생성
Base.metadata.create_all(bind=engine)
```

### 인증 추가

```python
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthenticationCredentials

security = HTTPBearer()

@app.get("/api/secure")
def secure_endpoint(credentials: HTTPAuthenticationCredentials = Depends(security)):
    token = credentials.credentials
    if token != "your-secret-token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message": "Access granted"}
```

---

## ❓ FAQ

### Q: 다른 포트에서 실행하고 싶어요
```bash
python -c "import uvicorn; uvicorn.run('api_server:app', host='127.0.0.1', port=8001)"
```

### Q: 로컬 네트워크에서 접근하고 싶어요
```python
# api_server.py에서
uvicorn.run(app, host="0.0.0.0", port=8000)
```
**주의**: 이 경우 **반드시 방화벽과 인증을 추가하세요**!

### Q: API 응답이 느려요
- Redis 캐싱 추가
- 데이터베이스 인덱싱
- 비동기 작업 처리

### Q: Java에서 CORS 에러가 발생해요
- `api_server.py`의 `allow_origins` 확인
- UI가 실행 중인 포트 추가

### Q: OpenAPI 문서가 안 보여요
- 브라우저 캐시 삭제
- http://localhost:8000/redoc 시도
- http://localhost:8000/openapi.json에서 직접 확인

---

## 🚦 다음 단계

1. **프로덕션 준비**
   - 데이터베이스 영속성 추가
   - JWT 기반 인증 구현
   - 로깅 및 모니터링

2. **성능 최적화**
   - Redis 캐싱
   - 데이터베이스 연결 풀링
   - 비동기 작업 처리

3. **AI Agent 연동** (당신의 관심사!)
   - LangChain/LlamaIndex로 API 자동 호출
   - 자연어 쿼리 처리
   - 복합 작업 오케스트레이션

---

## 📚 유용한 링크

- **FastAPI 문서**: https://fastapi.tiangolo.com/
- **OpenAPI 명세**: https://swagger.io/specification/
- **OkHttp (Java)**: https://square.github.io/okhttp/
- **React 문서**: https://react.dev/
- **Docker 가이드**: https://docs.docker.com/

---

## 💡 추천: AI Agent 활용 아이디어

당신이 AI Agent에 관심이 많다고 했으니, 이 API 서버를 활용한 아이디어:

### 1. 자동 작업 관리 AI

```python
# AI Agent가 자연어로 작업을 생성하고 관리
"Alice의 작업 중 완료되지 않은 항목 5개를 목록화하고, 
 그 중 3개를 오늘 완료하도록 스케줄링해"
```

### 2. 지능형 분석 대시보드

```python
# 사용자별 생산성 분석
@app.get("/api/ai/productivity-report/{user_id}")
def get_productivity_report(user_id: int):
    # AI로 사용자 패턴 분석
    # 추천사항 생성
```

### 3. LangChain 통합

```python
from langchain.agents import Tool
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent

tools = [
    Tool(
        name="Get User Tasks",
        func=lambda user_id: requests.get(f"{BASE_URL}/api/tasks?user_id={user_id}").json(),
        description="사용자의 모든 작업 조회"
    ),
    Tool(
        name="Create Task",
        func=create_task,
        description="새 작업 생성"
    )
]

agent = initialize_agent(tools, ChatOpenAI(temperature=0))
```

---

## 📞 지원

- **버그 리포트**: 서버 로그 확인
- **성능 문제**: `uvicorn --reload` 제거 후 재시작
- **API 테스트**: `/docs`에서 Swagger UI 사용

**행운을 빕니다! 🎉**
