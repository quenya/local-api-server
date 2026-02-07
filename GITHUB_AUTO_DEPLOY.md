# 🚀 GitHub 자동 배포 시스템 (Mac Mini)

## 📋 개요

GitHub에 push하면 자동으로:
1. ✅ 로컬 레포지토리에서 `git pull` 
2. ✅ 의존성 업데이트 (requirements.txt)
3. ✅ 실행 중인 API 서버 종료
4. ✅ API 서버 자동 재시작

---

## 🛠️ 1단계: 사전 준비

### 1.1 Git 저장소 확인

```bash
cd /Volumes/Elements/project/python/local-api-server

# GitHub 연동 확인
git remote -v
# 출력 예:
# origin  https://github.com/username/repo.git (fetch)
# origin  https://github.com/username/repo.git (push)
```

### 1.2 SSH 키 또는 GitHub 토큰 설정

**방법 A: SSH 키 (권장)**
```bash
# SSH 키 생성 (이미 있으면 생략)
ssh-keygen -t ed25519 -C "your-email@example.com"

# 공개 키 내용 복사
cat ~/.ssh/id_ed25519.pub

# GitHub Settings → SSH and GPG keys → New SSH key
# 위에서 복사한 내용 붙여넣기
```

**방법 B: GitHub 토큰**
```bash
# GitHub Settings → Developer settings → Personal access tokens → New token
# 권한: repo 선택
# 토큰 복사

# git 설정
git config --global credential.helper osxkeychain
```

### 1.3 Webhook 서버 라이브러리 설치

```bash
pip install flask python-dotenv
```

---

## 🔐 2단계: GitHub Webhook 설정

### 2.1 로컬 IP 확인 (Mac Mini)

```bash
# Mac Mini의 로컬 IP 주소 확인
ifconfig | grep "inet " | grep -v 127.0.0.1

# 출력 예:
# inet 192.168.0.100 netmask 0xffffff00 broadcast 192.168.0.255
```

**기억할 것:** `192.168.0.100` (또는 당신의 IP)

### 2.2 GitHub Repository 설정

1. **GitHub 브라우저에서:**
   ```
   Settings → Webhooks → Add webhook
   ```

2. **Webhook 설정:**
   - **Payload URL**: `http://192.168.0.100:5000/webhook/github`
     (IP 주소와 포트를 당신의 것으로 변경)
   
   - **Content type**: `application/json`
   
   - **Secret**: (중요!) 복잡한 시크릿 생성
     ```bash
     # 터미널에서 난수 생성
     openssl rand -hex 32
     # 출력 예: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6...
     ```
     이 값을 복사해서 GitHub에 입력
   
   - **Events**: "Push events" 선택
   
   - **Active**: ✓ 체크

3. **Save webhook**

---

## ⚙️ 3단계: Webhook 서버 설정

### 3.1 .env.webhook 파일 생성

프로젝트 루트에 `.env.webhook` 파일 생성:

```bash
cd /Volumes/Elements/project/python/local-api-server

cat > .env.webhook << 'EOF'
# GitHub Webhook Secret (위에서 생성한 값)
GITHUB_WEBHOOK_SECRET=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6...

# 로컬 레포지토리 경로
REPO_PATH=/Volumes/Elements/project/python/local-api-server

# Webhook 서버 포트
WEBHOOK_PORT=5000
EOF
```

### 3.2 webhook_server.py 저장

`webhook_server.py` 파일을 프로젝트 루트에 저장합니다.

```bash
# 파일 구조 확인
ls -la | grep webhook_server.py
ls -la | grep .env.webhook
```

---

## 🚀 4단계: 실행

### 4.1 Webhook 서버 시작

**터미널 1 (Webhook 서버):**
```bash
cd /Volumes/Elements/project/python/local-api-server
python webhook_server.py
```

**정상 출력:**
```
============================================================
GitHub Webhook 서버 시작
포트: 5000
리포지토리: /Volumes/Elements/project/python/local-api-server
============================================================

⚠️  주의: 본인의 로컬 네트워크에서만 실행하세요!

 * Serving Flask app 'webhook_server'
 * Running on http://0.0.0.0:5000
```

### 4.2 API 서버 시작 (또 다른 터미널)

**터미널 2 (API 서버):**
```bash
cd /Volumes/Elements/project/python/local-api-server
python api_server.py
```

**정상 출력:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 4.3 테스트

```bash
# Webhook 서버 헬스체크
curl http://localhost:5000/health

# 응답:
# {"status":"healthy","service":"GitHub Webhook Server"}

# 상태 확인
curl http://localhost:5000/status
```

---

## 🧪 5단계: 자동 배포 테스트

### 5.1 로컬에서 테스트

```bash
# 작은 변경 커밋
echo "# Test" >> README.md
git add README.md
git commit -m "Test webhook"
git push
```

### 5.2 배포 로그 확인

```bash
# 배포 로그 실시간 확인
tail -f deployment.log

# 또는 상태 확인
curl http://localhost:5000/status | python -m json.tool
```

**성공 로그 예:**
```
[2024-02-07 14:30:45] [INFO] GitHub Push 감지
[2024-02-07 14:30:45] [INFO]   리포지토리: local-api-server
[2024-02-07 14:30:45] [INFO]   브랜치: main
[2024-02-07 14:30:45] [INFO] ============================================================
[2024-02-07 14:30:45] [INFO] 자동 배포 시작
[2024-02-07 14:30:45] [INFO] [1/4] Git pull 중...
[2024-02-07 14:30:47] [INFO] Git pull 성공
[2024-02-07 14:30:47] [INFO] [2/4] 의존성 확인 중...
[2024-02-07 14:30:48] [INFO] [3/4] 기존 API 서버 종료 중...
[2024-02-07 14:30:48] [INFO] API 서버 종료 (PID: 12345)
[2024-02-07 14:30:50] [INFO] [4/4] API 서버 재시작 중...
[2024-02-07 14:30:51] [INFO] API 서버 시작 (PID: 12346)
[2024-02-07 14:30:51] [INFO] 자동 배포 완료 ✅
```

---

## 🔄 6단계: 백그라운드 실행 (선택)

### 6.1 Mac Mini에서 자동 시작 (launchd)

**주의: 터미널을 계속 열어놓지 않으려면 이 설정 사용**

```bash
# Webhook 서버용 plist 파일 생성
cat > ~/Library/LaunchAgents/com.github.webhook-server.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.github.webhook-server</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Volumes/Elements/project/python/local-api-server/webhook_server.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Volumes/Elements/project/python/local-api-server/webhook_server.log</string>
    <key>StandardErrorPath</key>
    <string>/Volumes/Elements/project/python/local-api-server/webhook_server_error.log</string>
    <key>WorkingDirectory</key>
    <string>/Volumes/Elements/project/python/local-api-server</string>
</dict>
</plist>
EOF

# 서비스 로드
launchctl load ~/Library/LaunchAgents/com.github.webhook-server.plist

# 상태 확인
launchctl list | grep webhook-server

# 중지 (나중에)
launchctl unload ~/Library/LaunchAgents/com.github.webhook-server.plist
```

### 6.2 systemd 사용 (Linux)

Linux 머신을 사용하는 경우:

```bash
sudo cat > /etc/systemd/system/webhook-server.service << 'EOF'
[Unit]
Description=GitHub Webhook Server
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/Volumes/Elements/project/python/local-api-server
ExecStart=/usr/bin/python3 /Volumes/Elements/project/python/local-api-server/webhook_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable webhook-server
sudo systemctl start webhook-server
```

---

## 📊 7단계: 모니터링

### 7.1 배포 로그 실시간 확인

```bash
# 터미널 3에서
cd /Volumes/Elements/project/python/local-api-server
tail -f deployment.log
```

### 7.2 프로세스 상태 확인

```bash
# Webhook 서버
ps aux | grep webhook_server

# API 서버
ps aux | grep api_server

# 포트 확인
lsof -i :5000   # Webhook
lsof -i :8000   # API
```

### 7.3 GitHub 웹훅 배송 기록 확인

```
GitHub → Repository Settings → Webhooks → 해당 Webhook
→ Recent Deliveries 탭
```

각 배송의 상세 정보를 확인할 수 있습니다.

---

## ⚠️ 보안 주의사항

### 1. 로컬 네트워크에서만 실행

```bash
# 현재 설정: 0.0.0.0:5000 (로컬 네트워크만)
# 외부 인터넷에서는 접근 불가
```

### 2. 방화벽 설정

```bash
# Mac Mini 방화벽 활성화
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on

# 포트 5000만 허용
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/bin/python3
```

### 3. Secret 보호

- `.env.webhook` 파일을 `.gitignore`에 추가
- GitHub Secret과 로컬 Secret이 일치해야 함
- 정기적으로 Secret 변경

```bash
echo ".env.webhook" >> .gitignore
git add .gitignore
git commit -m "Add .env.webhook to .gitignore"
git push
```

---

## 🔧 트러블슈팅

### 문제 1: Webhook이 트리거되지 않음

```bash
# GitHub Webhooks 페이지에서 "Recent Deliveries" 확인
# 응답 코드 확인:
# - 200: 성공
# - 401: Secret 불일치
# - 404: URL 잘못됨
# - 500: 서버 에러
```

**해결:**
```bash
# 1. Secret 확인
cat .env.webhook | grep GITHUB_WEBHOOK_SECRET

# 2. 로컬 IP 확인
ifconfig | grep "inet " | grep -v 127.0.0.1

# 3. Webhook 서버 실행 중 확인
curl http://localhost:5000/health

# 4. 로그 확인
tail -f deployment.log
```

### 문제 2: 포트 5000 이미 사용 중

```bash
# 포트 확인
lsof -i :5000

# 다른 포트 사용
# .env.webhook에서 WEBHOOK_PORT=5001로 변경
# GitHub Webhook URL도 수정
```

### 문제 3: Git pull 실패

```bash
# SSH 키 확인
ssh -T git@github.com

# HTTPS URL 사용 중이면
git remote set-url origin git@github.com:username/repo.git

# 자격증명 저장 확인
git config --global credential.helper osxkeychain
```

### 문제 4: API 서버가 재시작되지 않음

```bash
# API 서버 로그 확인
tail -f api_server.log

# 수동으로 시작 확인
python api_server.py

# 의존성 확인
pip install -r requirements.txt
```

---

## 📈 다음 단계

1. **Slack 알림**: Webhook 성공/실패 시 Slack 메시지
2. **이메일 알림**: 배포 결과를 이메일로 수신
3. **배포 통계**: 배포 횟수, 시간 추적
4. **롤백 기능**: 배포 실패 시 이전 버전으로 복구
5. **다중 브랜치**: develop, staging, main 브랜치 자동화

---

## 📚 참고자료

- [GitHub Webhooks](https://docs.github.com/en/developers/webhooks-and-events/webhooks)
- [Flask 문서](https://flask.palletsprojects.com/)
- [macOS launchd](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchDaemons.html)

---

## ✅ 완료 체크리스트

- [ ] Git 저장소 설정 (SSH 또는 토큰)
- [ ] Mac Mini 로컬 IP 확인
- [ ] GitHub Webhook 생성
- [ ] Secret 생성 및 저장
- [ ] .env.webhook 파일 생성
- [ ] webhook_server.py 저장
- [ ] Webhook 서버 시작
- [ ] 배포 테스트 (작은 변경)
- [ ] 배포 로그 확인
- [ ] (선택) 백그라운드 실행 설정

모두 완료되면 자동 배포가 작동합니다! 🎉
