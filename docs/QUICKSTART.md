# 快速开始指南

## 一、环境准备

### 必需软件
- Python 3.9+
- Node.js 18+
- Git

### 检查版本
```bash
python --version
node --version
npm --version
```

## 二、克隆项目（如果从Git获取）

```bash
git clone <repository-url>
cd 地摊经济
```

## 三、后端设置

### 1. 进入后端目录
```bash
cd backend
```

### 2. 创建虚拟环境
```bash
python -m venv venv

# Windows激活
venv\Scripts\activate

# Linux/Mac激活
source venv/bin/activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置环境变量
```bash
# 复制配置模板
cp .env.example .env

# 编辑.env文件，至少修改SECRET_KEY
# SECRET_KEY=your-random-secret-key-here
```

### 5. 初始化数据库
```bash
# 数据库会自动创建，也可以手动运行迁移
# alembic upgrade head
```

### 6. 启动后端服务
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

成功后访问：
- API: http://localhost:8000
- 文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

## 四、商户端设置

### 1. 新开终端，进入商户端目录
```bash
cd frontend-merchant
```

### 2. 安装依赖
```bash
npm install
```

### 3. 配置环境变量
```bash
# 复制配置模板
cp .env.example .env
```

### 4. 启动开发服务器
```bash
npm run dev
```

访问: http://localhost:3001

## 五、消费者端设置

### 1. 新开终端，进入消费者端目录
```bash
cd frontend-consumer
```

### 2. 安装依赖
```bash
npm install
```

### 3. 启动开发服务器
```bash
npm run dev
```

访问: http://localhost:3002

## 六、验证安装

### 1. 检查后端
访问 http://localhost:8000/health 应该返回:
```json
{
  "status": "ok",
  "message": "服务运行正常"
}
```

### 2. 检查前端
- 商户端: http://localhost:3001 应显示"商户端 - 街头地摊推广系统"
- 消费者端: http://localhost:3002 应显示"消费者端 - 街头地摊推广系统"

## 七、开始开发

现在你已经完成了基础搭建！接下来可以：

1. 查看 `PLAN.md` 了解详细实施计划
2. 查看 `docs/PROJECT_MAP.md` 了解项目结构
3. 使用 `.claude/skills/` 中的技能文件快速开发
4. 访问 http://localhost:8000/docs 查看API文档

## 常见问题

### Q: 端口被占用
A: 修改启动命令中的端口号
- 后端: `--port 8001`
- 前端: 修改 `vite.config.ts` 中的 `port`

### Q: Python依赖安装失败
A: 
- 确保pip是最新版: `pip install --upgrade pip`
- 使用国内镜像: `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

### Q: npm安装很慢
A: 使用国内镜像
```bash
npm config set registry https://registry.npmmirror.com
npm install
```

### Q: 数据库文件在哪里
A: SQLite文件位于 `backend/street_vendor.db`

## 下一步

完成基础搭建后，按照 `PLAN.md` 中的阶段2开始开发用户认证功能。
