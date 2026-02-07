# 🔧 npm start 에러 해결 (package.json 없음)

## 🎯 상황

```
npm error enoent Could not read package.json
```

**원인**: `package.json` 파일이 없어서 npm이 설정을 읽을 수 없음

---

## ✅ 해결 방법 (2가지)

### 방법 1️⃣ : 제공된 파일 사용 (권장)

**모든 파일을 같은 폴더에 복사하세요:**

```
/Volumes/Elements/project/python/local-api-server/
├── package.json          ← 여기에!
├── vite.config.js        ← 여기에!
├── tailwind.config.js
├── postcss.config.js
├── index.html
├── api_server.py
├── LocalAPIClient.java
├── README.md
├── SETUP_GUIDE.md
├── REACT_QUICKSTART.md
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── App.css
    └── components/
        └── APITester.jsx
```

**그 다음:**

```bash
# 프로젝트 폴더로 이동
cd /Volumes/Elements/project/python/local-api-server

# 의존성 설치
npm install

# 서버 시작
npm start
```

✅ 끝! 브라우저가 자동으로 http://localhost:3000 열림

---

### 방법 2️⃣ : 수동 설정 (Create React App)

Create React App을 사용하고 싶다면:

```bash
# 프로젝트 폴더로 이동
cd /Volumes/Elements/project/python

# 새 React 프로젝트 생성
npx create-react-app local-api-server

# 생성된 폴더로 이동
cd local-api-server

# src/App.jsx를 다운로드한 api_ui.jsx로 교체

# 의존성 추가
npm install lucide-react

# 서버 시작
npm start
```

---

## 📋 필수 파일 확인 목록

현재 폴더에 다음 파일들이 있는지 확인하세요:

- [ ] `package.json` - npm 설정
- [ ] `vite.config.js` - Vite 빌드 설정
- [ ] `index.html` - HTML 진입점
- [ ] `src/main.jsx` - React 시작점
- [ ] `src/App.jsx` - App 컴포넌트
- [ ] `src/components/APITester.jsx` - API 테스터 UI

> **팁**: 모든 파일이 다운로드 폴더에 있으면, 프로젝트 폴더로 옮기세요.

---

## 🚀 실행 순서 (중요!)

### 1단계: Python API 서버 (먼저!)

```bash
# 새 터미널 창에서
python api_server.py
```

**확인:**
```bash
curl http://localhost:8000/health
```

### 2단계: React UI (그 다음!)

```bash
# 다른 터미널 창에서
cd /Volumes/Elements/project/python/local-api-server
npm install    # 처음 한 번만
npm start
```

**결과:**
- Python: http://localhost:8000
- React: http://localhost:3000

---

## ❓ FAQ

### Q: npm이 설치되지 않았어요

```bash
# macOS
brew install node

# 또는 https://nodejs.org에서 설치
```

**확인:**
```bash
node --version
npm --version
```

### Q: `npm install` 중 에러가 발생해요

```bash
# 캐시 삭제
npm cache clean --force

# node_modules 삭제
rm -rf node_modules package-lock.json

# 재설치
npm install
```

### Q: `npm start`가 아무 것도 열지 않음

프로젝트 폴더가 맞는지 확인하세요:

```bash
# 현재 위치 확인
pwd

# 다음과 같아야 함:
# /Volumes/Elements/project/python/local-api-server

# package.json이 있는지 확인
ls package.json
```

### Q: "Port 3000 already in use" 에러

```bash
# macOS/Linux
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# 또는 다른 포트 사용
PORT=3001 npm start
```

### Q: API가 로드되지 않음 (로딩 중...)

Python 서버가 실행 중인지 확인하세요:

```bash
# 새 터미널에서
curl http://localhost:8000/health

# 응답이 없으면
python api_server.py
```

---

## 📦 npm vs yarn

`yarn`을 사용하고 싶다면:

```bash
npm install -g yarn

# npm 대신 yarn 사용
yarn install
yarn start
```

---

## 🎯 성공 체크리스트

다음이 모두 작동하면 성공입니다:

- [ ] `npm install` 완료됨
- [ ] Python API 서버 실행 중 (http://localhost:8000/health)
- [ ] `npm start` 실행됨
- [ ] 브라우저에 http://localhost:3000 자동 열림
- [ ] "API Tester" 제목 보임
- [ ] 왼쪽에 태그(Users, Tasks, System) 표시됨
- [ ] 엔드포인트 클릭 가능
- [ ] "API 호출" 버튼 실행 → 응답 표시됨

모두 체크되면: **축하합니다! 🎉**

---

## 📚 다음 단계

1. **API 테스트**
   - 좌측에서 엔드포인트 선택
   - 파라미터 입력
   - "API 호출" 클릭

2. **Java 프로젝트 연동**
   - `LocalAPIClient.java` 다운로드
   - Maven 의존성 추가 (okhttp3, json)
   - 코드에서 호출

3. **프로덕션 빌드**
   ```bash
   npm run build
   # dist/ 폴더에 최적화된 파일 생성
   ```

---

## 📞 추가 도움이 필요하면

- `REACT_QUICKSTART.md` - React 전용 가이드
- `SETUP_GUIDE.md` - 전체 설정 가이드
- `README.md` - 전체 개요 및 예제

모든 파일이 이 폴더에 있습니다! 📁
