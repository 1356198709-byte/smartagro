@echo off
chcp 65001 >nul
cd /d "%~dp0frontend"
echo 前端启动中...
echo 系统页面: http://localhost:3000
start "" http://localhost:3000
npm run dev
pause
