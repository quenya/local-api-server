# 🎯 React UI 빠른 시작 (3단계 해결)

## 📋 전제 조건

- Node.js 16+ 설치 ([https://nodejs.org](https://nodejs.org))
- Python API 서버 실행 중 (`python api_server.py`)

---

## 🚀 3단계로 실행하기

### 1️⃣ 프로젝트 디렉토리 이동

```bash
cd /path/to/local-api-server
# 예: cd /Volumes/Elements/project/python/local-api-server
```

### 2️⃣ 의존성 설치

```bash
npm install
```

이 명령은 `package.json`을 읽고 필요한 모든 라이브러리를 `node_modules`에 설치합니다.

**설치 내용:**
- React & ReactDOM
- Tailwind CSS (스타일링)
- Lucide React (아이콘)
- Vite (개발 서버 & 빌드 도구)

### 3️⃣ 개발 서버 시작

```bash
npm start
```

**또는:**

```bash
npm run dev
```

✅ **자동 실행:**
- 브라우저가 자동으로 http://localhost:3000 열림
- API 명세 자동 로드 (http://localhost:8000/openapi.json)
- 파일 변경시 자동 새로고침 (Hot Reload)

---

## 📁 프로젝트 구조

```
local-api-server/
├── src/
│   ├── main.jsx                    # React 진입점
│   ├── App.jsx                     # 메인 App 컴포넌트
│   ├── App.css                     # 스타일
│   └── components/
│       └── APITester.jsx           # API 테스터 컴포넌트
├── index.html                      # HTML 메인 파일
├── package.json                    # npm 설정
├── vite.config.js                  # Vite 설정
├── tailwind.config.js              # Tailwind 설정
└── postcss.config.js               # PostCSS 설정
```

---

## 🛠️ npm 명령어

| 명령어 | 설명 |
|--------|------|
| `npm start` | 개발 서버 실행 (권장) |
| `npm run dev` | Vite 개발 서버 실행 |
| `npm run build` | 프로덕션 빌드 생성 (`dist/` 폴더) |
| `npm run preview` | 빌드된 파일 미리보기 |
| `npm install` | 의존성 설치 |
| `npm update` | 의존성 업데이트 |

---

## ⚠️ 트러블슈팅

### `npm: command not found`

Node.js를 설치하지 않으셨어요.

**해결:**
```bash
# macOS (Homebrew)
brew install node

# Windows
# https://nodejs.org에서 설치 프로그램 다운로드
```

### `Port 3000 is already in use`

다른 프로세스가 3000 포트를 사용 중입니다.

**해결 방법 1: 다른 포트 사용**
```bash
PORT=3001 npm start
```

**해결 방법 2: 기존 프로세스 종료**
```bash
# macOS/Linux
lsof -i :3000
kill -9 <PID>

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### `API 명세 로딩 중...` (계속 로딩)

Python 백엔드가 실행되지 않았습니다.

**해결:**
```bash
# 새 터미널 창에서
python api_server.py
```

**또는 API 서버 확인:**
```bash
curl http://localhost:8000/health
```

### `node_modules` 폴더가 너무 큼

이는 정상입니다. `.gitignore`에 포함되어 있으니 git 커밋에서 제외됩니다.

**디스크 공간 절약:**
```bash
npm ci --omit=dev  # 프로덕션 의존성만 설치
```

---

## 🎨 UI 기능

- ✅ **API 명세 자동 로드** - OpenAPI JSON에서 파싱
- ✅ **엔드포인트 탐색** - 태그별 정렬
- ✅ **파라미터 입력** - Path, Query, Body 모두 지원
- ✅ **실시간 테스트** - `API 호출` 버튼으로 즉시 실행
- ✅ **응답 표시** - JSON 형식으로 예쁘게 출력
- ✅ **복사 기능** - URL, 응답 데이터 복사

---

## 📦 Vite vs Create React App

이 프로젝트는 **Vite**를 사용합니다 (더 빠름):

| 항목 | Create React App | Vite |
|------|------------------|------|
| 설치 시간 | 길음 | 빠름 |
| 개발 서버 시작 | 느림 | ⚡ 매우 빠름 |
| Hot Reload | 느림 | ⚡ 매우 빠름 |
| 번들 크기 | 큼 | 작음 |

---

## 🚀 다음 단계

### 1. 프로덕션 빌드 생성

```bash
npm run build
```

결과: `dist/` 폴더에 정적 파일 생성

### 2. 정적 파일 제공 (선택)

```bash
npm run preview
```

http://localhost:4173에서 프로덕션 빌드 테스트

### 3. 커스터마이징

**API 서버 호스트 변경:**
```javascript
// src/components/APITester.jsx에서
const API_BASE = 'http://your-api-host:8000';
```

**테마 변경:**
```javascript
// Tailwind 색상 수정 (tailwind.config.js)
// 또는 src/components/APITester.jsx의 스타일 태그 수정
```

---

## 📝 유용한 팁

### npm 캐시 초기화 (문제 발생 시)

```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### 특정 버전의 의존성 설치

```bash
npm install react@18.2.0
```

### 전역 명령어 사용

```bash
# npm 버전 확인
npm --version

# npm 업데이트
npm install -g npm@latest
```

---

## 🎯 성공 확인

브라우저에서 http://localhost:3000을 열었을 때:

1. ✅ "API Tester" 제목 보임
2. ✅ 왼쪽에 "Users", "Tasks", "System" 태그 표시
3. ✅ 엔드포인트 목록 로드됨
4. ✅ 엔드포인트 클릭 후 파라미터 입력 가능
5. ✅ "API 호출" 버튼 실행 → 응답 표시됨

모두 작동하면 **성공! 🎉**

---

## 🔗 참고자료

- [Node.js 설치](https://nodejs.org)
- [npm 공식 문서](https://docs.npmjs.com)
- [Vite 가이드](https://vitejs.dev)
- [React 공식 문서](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
