#!/bin/bash
# 启动商户端服务脚本

cd "$(dirname "$0")/../frontend-merchant"

echo "正在启动商户端服务..."

# 检查依赖
if [ ! -d "node_modules" ]; then
    echo "⚠ 依赖未安装，正在安装..."
    npm install
fi

# 检查环境变量
if [ ! -f ".env" ]; then
    echo "⚠ .env 文件不存在，从模板复制..."
    cp .env.example .env
fi

# 启动服务
echo "启动商户端开发服务器..."
npm run dev
