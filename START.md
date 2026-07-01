# 街头地摊推广系统 - 启动指南

## 🚀 快速启动

### 方式一：使用脚本（推荐）

#### Windows:
```batch
# 启动后端
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 启动商户端（新终端）
cd frontend-merchant
npm install
npm run dev

# 启动消费者端（新终端）
cd frontend-consumer
npm install
npm run dev
```

#### Linux/Mac:
```bash
# 启动后端
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 启动商户端（新终端）
cd frontend-merchant
npm install
npm run dev

# 启动消费者端（新终端）
cd frontend-consumer
npm install
npm run dev
```

## 📍 访问地址

| 服务 | 地址 | 说明 |
|-----|------|------|
| 后端API | http://localhost:8000 | FastAPI服务 |
| API文档 | http://localhost:8000/docs | Swagger文档 |
| 健康检查 | http://localhost:8000/health | 服务状态 |
| 商户端 | http://localhost:3001 | 商户管理后台 |
| 消费者端 | http://localhost:3002 | 消费者购物平台 |

## ✅ 验证服务

### 1. 检查后端
```bash
curl http://localhost:8000/health
# 应返回: {"status":"ok","message":"服务运行正常"}
```

### 2. 检查前端
- 商户端: 浏览器访问 http://localhost:3001
- 消费者端: 浏览器访问 http://localhost:3002

## 🧪 测试流程

### 商户端测试
1. 访问 http://localhost:3001/register
2. 注册商户账号（需填写商户名称）
3. 登录进入Dashboard
4. 创建产品
5. 上传产品图片
6. 查看订单管理

### 消费者端测试
1. 访问 http://localhost:3002/register
2. 注册消费者账号
3. 登录进入首页
4. 浏览产品列表
5. 加入购物车
6. 结算下单（自动Mock支付）
7. 查看我的订单

## 🔧 常见问题

### 端口被占用
- 后端: 修改启动命令 `--port 8001`
- 前端: 修改 `vite.config.ts` 中的 `server.port`

### 依赖安装失败
- 后端: 使用清华镜像 `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`
- 前端: 使用淘宝镜像 `npm install --registry=https://registry.npmmirror.com`

### 数据库文件
- SQLite文件自动创建在 `backend/street_vendor.db`
- 如需重置，删除该文件后重启后端

## 📝 注意事项

1. **首次启动**: 需要安装所有依赖，大约需要5-10分钟
2. **环境变量**: 后端需要 `.env` 文件，从 `.env.example` 复制
3. **数据库**: SQLite自动创建，无需手动配置
4. **Mock支付**: 当前使用Mock支付，自动完成支付流程

## 🎯 下一步

启动成功后，建议按以下顺序测试：
1. 注册并登录商户账号
2. 创建几个测试产品
3. 注册并登录消费者账号
4. 浏览产品并下单
5. 商户端查看订单和收入

---

**项目完成度**: ✅ 核心功能已全部实现
**当前状态**: 可以开始测试使用
