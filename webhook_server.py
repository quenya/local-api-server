"""
GitHub Webhook 자동 배포 서버

역할:
1. GitHub에서 push 이벤트를 감지
2. 레포지토리 자동 pull
3. 로컬 API 서버 자동 재시작
4. 배포 로그 기록

설치:
pip install flask python-dotenv PyGithub

실행:
python webhook_server.py
"""

import os
import sys
import json
import subprocess
import hmac
import hashlib
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv('.env.webhook')

app = Flask(__name__)

# ========== 설정 ==========
GITHUB_SECRET = os.getenv('GITHUB_WEBHOOK_SECRET', 'your-secret-key')
REPO_PATH = os.getenv('REPO_PATH', '/Volumes/Elements/project/python/local-api-server')
WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', 5000))
LOG_FILE = os.path.join(REPO_PATH, 'deployment.log')
PID_FILE = os.path.join(REPO_PATH, 'api_server.pid')

# ========== 로깅 함수 ==========
def log_deployment(message, level='INFO'):
    """배포 로그 기록"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f'[{timestamp}] [{level}] {message}'
    
    # 콘솔 출력
    print(log_message)
    
    # 파일 기록
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(log_message + '\n')
    except Exception as e:
        print(f'로그 기록 실패: {e}')

# ========== GitHub Webhook 검증 ==========
def verify_github_signature(payload_body, signature_header):
    """GitHub 서명 검증 (보안)"""
    if not signature_header:
        return False
    
    # HMAC-SHA256 서명 생성
    expected_signature = 'sha256=' + hmac.new(
        GITHUB_SECRET.encode(),
        payload_body,
        hashlib.sha256
    ).hexdigest()
    
    # 서명 비교 (시간 공격 방지)
    return hmac.compare_digest(signature_header, expected_signature)

# ========== 프로세스 관리 ==========
def get_api_server_pid():
    """저장된 API 서버 PID 읽기"""
    try:
        if os.path.exists(PID_FILE):
            with open(PID_FILE, 'r') as f:
                return int(f.read().strip())
    except Exception as e:
        log_deployment(f'PID 파일 읽기 실패: {e}', 'ERROR')
    return None

def save_pid(pid):
    """API 서버 PID 저장"""
    try:
        with open(PID_FILE, 'w') as f:
            f.write(str(pid))
    except Exception as e:
        log_deployment(f'PID 파일 저장 실패: {e}', 'ERROR')

def kill_api_server():
    """실행 중인 API 서버 종료"""
    try:
        pid = get_api_server_pid()
        if pid:
            os.kill(pid, 15)  # SIGTERM
            log_deployment(f'API 서버 종료 (PID: {pid})', 'INFO')
            return True
        
        # PID 파일이 없으면 포트로 찾기
        result = subprocess.run(
            ['lsof', '-i', ':8000', '-t'],
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for p in pids:
                try:
                    os.kill(int(p), 15)
                    log_deployment(f'API 서버 종료 (PID: {p})', 'INFO')
                except:
                    pass
            return True
        
        log_deployment('실행 중인 API 서버를 찾을 수 없음', 'WARNING')
        return False
    except Exception as e:
        log_deployment(f'API 서버 종료 실패: {e}', 'ERROR')
        return False

def start_api_server():
    """API 서버 시작"""
    try:
        # api_server.py가 있는지 확인
        api_script = os.path.join(REPO_PATH, 'api_server.py')
        if not os.path.exists(api_script):
            log_deployment(f'api_server.py를 찾을 수 없음: {api_script}', 'ERROR')
            return False
        
        # 서버 시작 (백그라운드 실행)
        # macOS 방식: nohup 사용
        process = subprocess.Popen(
            [sys.executable, api_script],
            cwd=REPO_PATH,
            stdout=open(os.path.join(REPO_PATH, 'api_server.log'), 'a'),
            stderr=subprocess.STDOUT,
            preexec_fn=os.setpgrp if sys.platform != 'win32' else None
        )
        
        save_pid(process.pid)
        log_deployment(f'API 서버 시작 (PID: {process.pid})', 'INFO')
        return True
    except Exception as e:
        log_deployment(f'API 서버 시작 실패: {e}', 'ERROR')
        return False

# ========== Git 작업 ==========
def git_pull():
    """GitHub에서 최신 코드 pull"""
    try:
        # 현재 브랜치 확인
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=REPO_PATH,
            capture_output=True,
            text=True,
            timeout=10
        )
        current_branch = result.stdout.strip()
        log_deployment(f'현재 브랜치: {current_branch}', 'INFO')
        
        # Pull 실행
        result = subprocess.run(
            ['git', 'pull', 'origin', current_branch],
            cwd=REPO_PATH,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            log_deployment(f'Git pull 성공\n{result.stdout}', 'INFO')
            return True
        else:
            log_deployment(f'Git pull 실패: {result.stderr}', 'ERROR')
            return False
    except subprocess.TimeoutExpired:
        log_deployment('Git pull 타임아웃 (30초 초과)', 'ERROR')
        return False
    except Exception as e:
        log_deployment(f'Git pull 오류: {e}', 'ERROR')
        return False

def check_dependencies():
    """필요한 Python 패키지 업데이트 (requirements.txt가 있으면)"""
    try:
        req_file = os.path.join(REPO_PATH, 'requirements.txt')
        if os.path.exists(req_file):
            log_deployment('requirements.txt 의존성 설치 중...', 'INFO')
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-r', req_file],
                cwd=REPO_PATH,
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                log_deployment('의존성 설치 성공', 'INFO')
                return True
            else:
                log_deployment(f'의존성 설치 실패: {result.stderr}', 'WARNING')
                return True  # 서버는 계속 시작
    except Exception as e:
        log_deployment(f'의존성 확인 오류: {e}', 'WARNING')
    return True

# ========== Webhook 엔드포인트 ==========
@app.route('/webhook/github', methods=['POST'])
def github_webhook():
    """
    GitHub Webhook 수신 엔드포인트
    
    GitHub 설정:
    1. Repository Settings → Webhooks
    2. Add webhook
    3. Payload URL: http://your-ip:5000/webhook/github
    4. Content type: application/json
    5. Secret: (GITHUB_WEBHOOK_SECRET와 동일)
    6. Events: Push events 선택
    """
    
    # GitHub 서명 검증
    signature = request.headers.get('X-Hub-Signature-256', '')
    payload_body = request.get_data()
    
    if not verify_github_signature(payload_body, signature):
        log_deployment('Webhook 서명 검증 실패 (잘못된 시크릿)', 'WARNING')
        return jsonify({'error': 'Invalid signature'}), 401
    
    # JSON 파싱
    try:
        payload = request.get_json()
    except Exception as e:
        log_deployment(f'JSON 파싱 실패: {e}', 'ERROR')
        return jsonify({'error': 'Invalid JSON'}), 400
    
    # Push 이벤트 확인
    if 'push' not in request.headers.get('X-GitHub-Event', ''):
        log_deployment(f'Webhook 이벤트: {request.headers.get("X-GitHub-Event", "unknown")} (무시됨)', 'INFO')
        return jsonify({'status': 'Event ignored (not a push)'}), 200
    
    # 푸시 정보 추출
    repository = payload.get('repository', {}).get('name', 'unknown')
    branch = payload.get('ref', '').split('/')[-1]
    pusher = payload.get('pusher', {}).get('name', 'unknown')
    commit_count = len(payload.get('commits', []))
    
    log_deployment(
        f'GitHub Push 감지\n'
        f'  리포지토리: {repository}\n'
        f'  브랜치: {branch}\n'
        f'  푸셔: {pusher}\n'
        f'  커밋: {commit_count}개',
        'INFO'
    )
    
    # ========== 자동 배포 프로세스 ==========
    log_deployment('=' * 60, 'INFO')
    log_deployment('자동 배포 시작', 'INFO')
    log_deployment('=' * 60, 'INFO')
    
    try:
        # 1단계: Git pull
        log_deployment('[1/4] Git pull 중...', 'INFO')
        if not git_pull():
            return jsonify({'error': 'Git pull failed'}), 500
        
        # 2단계: 의존성 확인
        log_deployment('[2/4] 의존성 확인 중...', 'INFO')
        check_dependencies()
        
        # 3단계: API 서버 종료
        log_deployment('[3/4] 기존 API 서버 종료 중...', 'INFO')
        kill_api_server()
        
        # 잠시 대기 (포트 해제 시간)
        import time
        time.sleep(2)
        
        # 4단계: API 서버 재시작
        log_deployment('[4/4] API 서버 재시작 중...', 'INFO')
        if not start_api_server():
            log_deployment('API 서버 시작 실패!', 'ERROR')
            return jsonify({'error': 'Failed to start API server'}), 500
        
        log_deployment('=' * 60, 'INFO')
        log_deployment('자동 배포 완료 ✅', 'INFO')
        log_deployment('=' * 60, 'INFO')
        
        return jsonify({
            'status': 'Deployment successful',
            'repository': repository,
            'branch': branch,
            'commits': commit_count
        }), 200
        
    except Exception as e:
        log_deployment(f'배포 중 오류 발생: {e}', 'ERROR')
        return jsonify({'error': str(e)}), 500

# ========== 상태 확인 엔드포인트 ==========
@app.route('/status', methods=['GET'])
def status():
    """배포 상태 확인"""
    try:
        # API 서버 상태
        api_running = False
        api_pid = get_api_server_pid()
        
        if api_pid:
            try:
                os.kill(api_pid, 0)  # 프로세스 존재 확인
                api_running = True
            except OSError:
                pass
        
        # 최근 로그 읽기
        recent_logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                recent_logs = f.readlines()[-10:]  # 최근 10줄
        
        return jsonify({
            'webhook_server': 'running',
            'webhook_port': WEBHOOK_PORT,
            'api_server': 'running' if api_running else 'stopped',
            'api_pid': api_pid,
            'repo_path': REPO_PATH,
            'recent_logs': [log.strip() for log in recent_logs]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== 헬스체크 ==========
@app.route('/health', methods=['GET'])
def health_check():
    """Webhook 서버 헬스체크"""
    return jsonify({'status': 'healthy', 'service': 'GitHub Webhook Server'}), 200

# ========== 메인 ==========
if __name__ == '__main__':
    log_deployment('=' * 60, 'INFO')
    log_deployment('GitHub Webhook 서버 시작', 'INFO')
    log_deployment(f'포트: {WEBHOOK_PORT}', 'INFO')
    log_deployment(f'리포지토리: {REPO_PATH}', 'INFO')
    log_deployment('=' * 60, 'INFO')
    log_deployment('', 'INFO')
    log_deployment('⚠️  주의: 본인의 로컬 네트워크에서만 실행하세요!', 'INFO')
    log_deployment('', 'INFO')
    
    # 외부 접근 허용 (로컬 네트워크만)
    app.run(
        host='0.0.0.0',  # 로컬 네트워크 접근 허용
        port=WEBHOOK_PORT,
        debug=False,
        use_reloader=False
    )
