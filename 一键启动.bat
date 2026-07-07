echo off
chcp 65001 >nul
title 智慧农业 - 一键启动

echo ================================
echo   智慧农业系统启动中...
echo ================================

echo.
echo [1/2] 启动后端 (8008端口)...
start "智慧农业-后端" "C:\Users\86138\PycharmProjects\pythonProject16\.venv\Scripts\python.exe" "C:\Users\86138\Desktop\khk\backend\run.py"

echo [2/2] 启动前端 (3000端口)...
start "智慧农业-前端" cmd /c "cd /d C:\Users\86138\Desktop\khk\frontend && npm run dev"

echo.
echo ================================
echo   启动中，请稍候...
echo   后端: http://localhost:8008/docs
echo   前端: http://localhost:3000
echo ================================
echo.
timeout /t 5 /nobreak >nul
echo 正在打开浏览器...
start "" http://localhost:3000
echo 完成！按任意键关闭此窗口...
pause >nul
