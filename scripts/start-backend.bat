@echo off
REM 启动后端服务脚本 (Windows)

cd /d "%~dp0\..\backend"

echo 正在启动后端服务...

REM 检查虚拟环境
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo √ 虚拟环境已激活
) else (
    echo × 虚拟环境不存在，请先运行: python -m venv venv
    pause
    exit /b 1
)

REM 检查环境变量
if not exist ".env" (
    echo × .env 文件不存在，从模板复制...
    copy .env.example .env
    echo 请编辑 .env 文件配置参数
)

REM 启动服务
echo 启动 FastAPI 服务...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
