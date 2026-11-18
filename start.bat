@echo off
title KubeSight Launcher
echo ===================================================
echo           Starting KubeSight Platform...
echo ===================================================
echo.

cd /d "%~dp0"

:: 1. Check if Docker Desktop is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Docker Desktop is not running yet!
    echo     Please start Docker Desktop from your Start Menu,
    echo     wait for the green icon, and run start.bat again.
    echo.
    pause
    exit /b 1
)

:: 2. Start all containers
echo [1/2] Starting Docker containers...
docker compose up -d
echo [2/2] Checking services...

echo.
echo ===================================================
echo   SUCCESS! KubeSight is running and fully healthy!
echo.
echo   URL:      http://localhost:3001
echo   Username: admin
echo   Password: admin123
echo ===================================================
echo.
echo Opening browser...
start http://localhost:3001
timeout /t 3 >nul
exit /b 0
