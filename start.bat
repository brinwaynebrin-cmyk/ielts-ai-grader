@echo off
chcp 65001
echo 正在启动雅思学习平台...
echo.

REM 进入脚本所在目录
cd /d "%~dp0"

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python
    pause
    exit /b 1
)

REM 启动服务（不使用reload避免Windows路径问题）
echo 启动服务器中...
python -m uvicorn api.index:app --host 0.0.0.0 --port 8000

pause
