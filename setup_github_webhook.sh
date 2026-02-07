#!/bin/bash

# GitHub 자동 배포 설정 스크립트 (macOS)
# 사용: bash setup_github_webhook.sh

set -e  # 에러 발생 시 중단

echo "🚀 GitHub 자동 배포 설정 시작"
echo "================================"
echo ""

# 1. 프로젝트 경로 입력
read -p "프로젝트 경로 (기본: /Volumes/Elements/project/python/local-api-server): " PROJECT_PATH
PROJECT_PATH=${PROJECT_PATH:-/Volumes/Elements/project/python/local-api-server}

if [ ! -d "$PROJECT_PATH" ]; then
    echo "❌ 경로가 존재하지 않습니다: $PROJECT_PATH"
    exit 1
fi

cd "$PROJECT_PATH"
echo "✅ 프로젝트 경로: $PROJECT_PATH"
echo ""

# 2. Git 저장소 확인
echo "🔍 Git 저장소 확인..."
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Git 저장소가 아닙니다"
    exit 1
fi

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "✅ 현재 브랜치: $CURRENT_BRANCH"
git remote -v
echo ""

# 3. GitHub Secret 생성
echo "🔐 GitHub Secret 생성 중..."
GITHUB_SECRET=$(openssl rand -hex 32)
echo "✅ 생성된 Secret: $GITHUB_SECRET"
echo ""

# 4. .env.webhook 파일 생성
echo "📝 .env.webhook 파일 생성 중..."

read -p "Webhook 포트 (기본: 5000): " WEBHOOK_PORT
WEBHOOK_PORT=${WEBHOOK_PORT:-5000}

cat > .env.webhook << EOF
# GitHub Webhook Secret
GITHUB_WEBHOOK_SECRET=$GITHUB_SECRET

# 로컬 레포지토리 경로
REPO_PATH=$PROJECT_PATH

# Webhook 서버 포트
WEBHOOK_PORT=$WEBHOOK_PORT
EOF

echo "✅ .env.webhook 생성됨"
echo ""

# 5. .gitignore에 .env.webhook 추가
echo "🚫 .gitignore 업데이트 중..."
if [ -f .gitignore ]; then
    if ! grep -q "\.env\.webhook" .gitignore; then
        echo ".env.webhook" >> .gitignore
        echo "✅ .env.webhook을 .gitignore에 추가했습니다"
    else
        echo "✅ .env.webhook이 이미 .gitignore에 있습니다"
    fi
else
    echo ".env.webhook" > .gitignore
    echo "✅ .gitignore 생성 및 .env.webhook 추가"
fi
echo ""

# 6. Flask 의존성 설치 확인
echo "📦 필요한 라이브러리 설치 중..."
pip install flask python-dotenv > /dev/null 2>&1
echo "✅ flask, python-dotenv 설치됨"
echo ""

# 7. webhook_server.py 존재 확인
echo "📄 webhook_server.py 확인..."
if [ ! -f webhook_server.py ]; then
    echo "⚠️  webhook_server.py가 없습니다"
    echo "   다운로드한 파일에서 webhook_server.py를 이 폴더에 복사하세요"
else
    echo "✅ webhook_server.py 있음"
fi
echo ""

# 8. 로컬 IP 확인
echo "🌐 로컬 IP 주소 확인..."
LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)
if [ -z "$LOCAL_IP" ]; then
    echo "⚠️  로컬 IP를 자동으로 찾을 수 없습니다"
    echo "   다음 명령어로 확인하세요: ifconfig"
else
    echo "✅ 로컬 IP: $LOCAL_IP"
fi
echo ""

# 9. 안내
echo "============================================"
echo "✅ 설정 완료!"
echo "============================================"
echo ""
echo "📋 다음 단계:"
echo ""
echo "1️⃣  GitHub Webhook 생성:"
echo "   Settings → Webhooks → Add webhook"
echo ""
echo "2️⃣  Webhook 설정:"
echo "   Payload URL: http://$LOCAL_IP:$WEBHOOK_PORT/webhook/github"
echo "   Content type: application/json"
echo "   Secret: $GITHUB_SECRET"
echo "   Events: Push events"
echo "   Active: ✓"
echo ""
echo "3️⃣  Webhook 서버 시작:"
echo "   python webhook_server.py"
echo ""
echo "4️⃣  배포 로그 확인:"
echo "   tail -f deployment.log"
echo ""
echo "5️⃣  상태 확인:"
echo "   curl http://localhost:$WEBHOOK_PORT/status"
echo ""
echo "📂 생성된 파일:"
ls -la .env.webhook 2>/dev/null || echo "   (파일이 자동으로 생성됩니다)"
echo ""

# 10. Git 커밋 (선택)
echo "💾 변경사항 커밋하시겠습니까? (y/n)"
read -p "> " COMMIT_CHOICE

if [ "$COMMIT_CHOICE" = "y" ] || [ "$COMMIT_CHOICE" = "Y" ]; then
    git add .gitignore
    git commit -m "Add webhook configuration to gitignore" 2>/dev/null || echo "⚠️  커밋 실패 (변경사항이 없을 수 있음)"
    echo "✅ 커밋됨"
fi

echo ""
echo "🎉 모든 설정이 완료되었습니다!"
echo "webhook_server.py를 시작하세요!"
