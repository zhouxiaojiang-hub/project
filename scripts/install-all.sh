#!/bin/bash
# 一键安装所有依赖

echo "========================================="
echo "  街头地摊推广系统 - 依赖安装脚本"
echo "========================================="

# 后端依赖
echo ""
echo "[1/3] 安装后端依赖..."
cd "$(dirname "$0")/../backend"
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
echo "✓ 后端依赖安装完成"

# 商户端依赖
echo ""
echo "[2/3] 安装商户端依赖..."
cd ../frontend-merchant
npm install
cp .env.example .env
echo "✓ 商户端依赖安装完成"

# 消费者端依赖
echo ""
echo "[3/3] 安装消费者端依赖..."
cd ../frontend-consumer
npm install
cp .env.example .env
echo "✓ 消费者端依赖安装完成"

echo ""
echo "========================================="
echo "  所有依赖安装完成！"
echo "========================================="
echo ""
echo "下一步："
echo "1. 编辑 backend/.env 配置环境变量"
echo "2. 运行 scripts/start-backend.sh 启动后端"
echo "3. 运行 scripts/start-merchant.sh 启动商户端"
echo "4. 运行 scripts/start-consumer.sh 启动消费者端"
echo ""
