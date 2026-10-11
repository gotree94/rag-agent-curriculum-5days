@echo off
chcp 65001 >nul
title RAG Agent Curriculum - 환경 설정

echo ============================================================
echo  RAG 기반 AI 에이전트 개발 (5일 과정) 환경 설정
echo ============================================================
echo.

echo [1/5] Python 버전 확인
python --version
if errorlevel 1 (
    echo [!] Python이 설치되어 있지 않습니다.  https://www.python.org/downloads/  에서 3.11 이상 설치 후 다시 실행하세요.
    pause
    exit /b 1
)

echo.
echo [2/5] 가상환경(.venv) 생성
if not exist .venv (
    python -m venv .venv
    echo     - .venv 생성 완료
) else (
    echo     - .venv 이미 존재합니다.
)

echo.
echo [3/5] 가상환경 활성화 및 pip 업그레이드
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip

echo.
echo [4/5] 패키지 설치 (requirements.txt)
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [!] 패키지 설치에 실패했습니다. 네트워크 상태를 확인하고 다시 실행하세요.
    pause
    exit /b 1
)

echo.
echo [5/5] 환경 설정 완료 / .env 파일 생성 안내
if not exist .env (
    copy .env.example .env >nul
    echo     - .env.example 를 .env 로 복사했습니다.
)
echo     - .env 파일에서 OPENAI_API_KEY 값을 채워 넣으세요.
echo     - VS Code에서 이 폴더를 열고 F5(또는 Run)로 실행하면 됩니다.

echo.
echo 설치 완료!  이제 00-environment/environment-setup.md 의 '환경 검증' 단계를 진행하세요.
pause