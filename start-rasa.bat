@echo off
echo Starting Rasa services...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not running. Starting Docker Desktop...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    echo Waiting for Docker to start...
    timeout /t 20 /nobreak
)

cd C:\Users\mateu\Documents\python\Rasa_Customizable_Framework

REM Check if containers are already running
docker-compose ps | find "rasa" >nul
if %errorlevel% equ 0 (
    echo Rasa services are already running.
) else (
    echo Starting Rasa services...
    docker-compose up -d
    echo Rasa services are starting...
)

echo Access your bot at http://localhost:5005
pause