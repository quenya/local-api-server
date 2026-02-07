# ⚡ GitHub 자동 배포 빠른 가이드 (5분)

## 🎯 목표
GitHub에 push → 자동으로 로컬 서버 pull & 재시작

---

## 📋 준비물
- ✅ GitHub 레포지토리 (로컬과 연동)
- ✅ Mac Mini (로컬)
- ✅ Python 3.8+
- ✅ Flask (`pip install flask python-dotenv`)

---

## 🚀 5분 빠른 시작

### 1단계: 스크립트 실행 (2분)

```bash
cd /Volumes/Elements/project/python/local-api-server
bash setup_github_webhook.sh
```

**자동으로:**
- ✅ .env.webhook 생성
- ✅ GitHub Secret 생성
- ✅ 로컬 IP 확인
- ✅ Flask 라이브러리 설치

### 2단계: GitHub Webhook 추가 (2분)

1. GitHub에서 Settings → Webhooks → Add webhook
2. 스크립트 실행 후 나온 정보 입력:
   - **Payload URL**: `http://192.168.0.100:5000/webhook/github`
   - **Secret**: (스크립트가 보여줌)
   - **Events**: "Push events" 선택
3. **Save**

### 3단계: 시작 (1분)

```bash
# 터미널 1: Webhook 서버
python webhook_server.py

# 터미널 2: API 서버 (선택)
python api_server.py
```

✅ **완료!** 이제 GitHub에 push하면 자동 배포됩니다.

---

## 🧪 테스트

```bash
# 작은 변경 push
echo "# Test" >> README.md
git add README.md
git commit -m "Test"
git push

# 배포 로그 확인
tail -f deployment.log
```

**성공 메시지:**
```
[2024-02-07 14:30:45] [INFO] GitHub Push 감지
[2024-02-07 14:30:47] [INFO] Git pull 성공
[2024-02-07 14:30:50] [INFO] API 서버 재시작 중...
[2024-02-07 14:30:51] [INFO] 자동 배포 완료 ✅
```

---

## 🔍 상태 확인

### Webhook 서버 상태
```bash
curl http://localhost:5000/status | python -m json.tool
```

### API 서버 상태
```bash
curl http://localhost:8000/health
```

### 배포 로그
```bash
tail -10 deployment.log
```

---

## 🛠️ 트러블슈팅

### 문제: "Webhook이 안 된다"
```bash
# 1. Webhook 서버 실행 중 확인
curl http://localhost:5000/health

# 2. 로컬 IP 확인
ifconfig | grep "inet "

# 3. GitHub Webhook 페이지에서 "Recent Deliveries" 확인
#    (응답 코드 200이 아니면 에러)
```

### 문제: "API 서버가 재시작 안 됨"
```bash
# 1. 수동으로 시작 확인
python api_server.py

# 2. 의존성 확인
pip install -r requirements.txt

# 3. 배포 로그 확인
tail -f deployment.log
```

### 문제: "포트가 이미 사용 중"
```bash
# 포트 확인
lsof -i :5000

# 다른 포트 사용 (.env.webhook 수정)
WEBHOOK_PORT=5001
```

---

## 🔐 보안 팁

1. **Secret 보호**: `.env.webhook`을 `.gitignore`에 추가
   ```bash
   echo ".env.webhook" >> .gitignore
   git add .gitignore && git commit -m "Add .env.webhook"
   ```

2. **로컬 네트워크만**: 방화벽 설정으로 외부 접근 차단
   ```bash
   # Mac Mini 방화벽 켜기
   sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
   ```

3. **정기적 Secret 변경**: 3개월마다 Secret 업데이트

---

## 📊 모니터링

### 실시간 배포 로그
```bash
watch -n 1 'tail -5 deployment.log'
```

### GitHub 배송 기록
```
GitHub → Repository → Settings → Webhooks → 해당 Webhook
→ Recent Deliveries 탭
```

### 프로세스 확인
```bash
ps aux | grep -E "webhook_server|api_server" | grep -v grep
```

---

## ⚙️ 고급 설정

### 1. 특정 브랜치만 배포
```python
# webhook_server.py 수정
branch = payload.get('ref', '').split('/')[-1]
if branch != 'main':
    return jsonify({'status': 'Ignored (not main branch)'}), 200
```

### 2. 배포 전 테스트
```python
# webhook_server.py의 check_dependencies() 함수 확장
def run_tests():
    result = subprocess.run(['pytest', '.'], cwd=REPO_PATH)
    return result.returncode == 0
```

### 3. Slack 알림
```python
# webhook_server.py에 추가
import requests

def notify_slack(message):
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    requests.post(webhook_url, json={'text': message})
```

### 4. 자동 백업
```python
def backup_database():
    backup_file = f'backup_{datetime.now().isoformat()}.db'
    shutil.copy('data.db', backup_file)
```

---

## 📈 다음 단계

1. **다중 환경**: develop, staging, main 분리
2. **배포 알림**: Slack, 이메일, Discord
3. **성능 모니터링**: 배포 시간, 성공률 추적
4. **자동 테스트**: push 전 테스트 실행
5. **롤백**: 배포 실패 시 이전 버전 복구

---

## 📚 파일 구조

```
/Volumes/Elements/project/python/local-api-server/
├── webhook_server.py      # 메인 서버
├── .env.webhook            # 설정 (비밀)
├── api_server.py           # API 서버
├── requirements.txt        # 의존성
├── deployment.log          # 배포 로그
└── api_server.pid          # 프로세스 ID
```

---

## ✅ 체크리스트

- [ ] `setup_github_webhook.sh` 실행
- [ ] GitHub Webhook 추가
- [ ] `python webhook_server.py` 시작
- [ ] 테스트 커밋 & push
- [ ] 배포 로그 확인
- [ ] `deployment.log` 확인

**모두 완료되면 자동 배포 완성!** 🎉

---

## 🆘 긴급 정지

만약 자동 배포를 중단하고 싶으면:

```bash
# Webhook 서버 중단
# 터미널에서 Ctrl+C

# 또는 프로세스 강제 종료
pkill -f webhook_server

# GitHub Webhook 비활성화
# Settings → Webhooks → 해당 webhook → 비활성화
```

---

**모든 설정이 완료되었습니다!** 🚀
이제 GitHub에 push하기만 하면 자동으로 배포됩니다.
