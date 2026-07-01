# 街头地摊推广系统

一个支持商户和消费者的线上交易平台，帮助街头地摊商户数字化管理业务。

## 项目概述

本系统为街头地摊商户提供线上推广和交易平台，支持：
- 商户端：产品管理、订单管理、收入统计、在线提现
- 消费者端：浏览商户、在线下单、在线支付、订单查询
- 平台抽佣：10%

## 技术栈

### 后端
- **框架**: FastAPI 0.109.0
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **ORM**: SQLAlchemy 2.0
- **认证**: JWT (python-jose)
- **密码加密**: bcrypt (passlib)

### 前端
- **框架**: React 18 + TypeScript
- **构建工具**: Vite 5
- **路由**: React Router 6
- **状态管理**: Zustand
- **数据请求**: TanStack Query (React Query)
- **UI组件**: Ant Design 5
- **图表**: Recharts

## 项目结构

```
地摊经济/
├── backend/                    # 后端API服务
│   ├── app/
│   │   ├── models/             # 数据库模型
│   │   ├── schemas/            # Pydantic模型
│   │   ├── api/v1/             # API路由
│   │   ├── services/           # 业务逻辑
│   │   ├── core/               # 核心功能(JWT、异常)
│   │   ├── integrations/       # 第三方集成(支付)
│   │   └── utils/              # 工具函数
│   ├── migrations/             # 数据库迁移
│   ├── tests/                  # 单元测试
│   └── requirements.txt        # Python依赖
├── frontend-merchant/          # 商户端前端
│   ├── src/
│   │   ├── pages/              # 页面组件
│   │   ├── components/         # 通用组件
│   │   ├── api/                # API封装
│   │   ├── store/              # 状态管理
│   │   └── router/             # 路由配置
│   └── package.json
├── frontend-consumer/          # 消费者端前端
│   └── src/                    # 同商户端结构
├── docs/                       # 项目文档
└── scripts/                    # 脚本工具
```

## 快速开始

### 前置要求

- Python 3.9+
- Node.js 18+
- npm 或 yarn

### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 复制环境变量配置
cp .env.example .env

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问: http://localhost:8000

API文档: http://localhost:8000/docs

### 商户端启动

```bash
cd frontend-merchant

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问: http://localhost:3001

### 消费者端启动

```bash
cd frontend-consumer

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问: http://localhost:3002

## 核心功能

### 商户端功能

1. **账户管理**
   - 商户注册/登录
   - 商户档案编辑

2. **产品管理**
   - 添加/编辑/删除产品
   - 产品图片上传
   - 库存管理

3. **订单管理**
   - 查看消费记录
   - 按时间、金额筛选
   - 订单详情查看

4. **收入统计**
   - 总收入/净收入/平台抽佣
   - 按日/周/月统计
   - 收入趋势图表

5. **提现管理**
   - 申请提现(微信/支付宝)
   - 查看提现记录
   - 可提现余额查询

### 消费者端功能

1. **账户管理**
   - 消费者注册/登录
   - 个人资料编辑

2. **商户浏览**
   - 浏览商户列表
   - 按分类筛选
   - 商户详情查看

3. **购物下单**
   - 查看商品详情
   - 添加购物车
   - 创建订单

4. **支付功能**
   - 微信支付
   - 支付宝支付
   - 支付状态查询

5. **订单管理**
   - 查看订单历史
   - 订单详情
   - 取消订单

## API接口

### 认证接口 `/api/v1/auth`

- `POST /auth/register` - 注册
- `POST /auth/login` - 登录
- `POST /auth/refresh` - 刷新token
- `GET /auth/me` - 当前用户信息

### 商户接口 `/api/v1/merchant`

- `GET /merchant/profile` - 商户档案
- `PUT /merchant/profile` - 更新档案
- `GET /merchant/orders` - 消费记录
- `GET /merchant/stats` - 收入统计
- `GET /merchant/balance` - 可提现余额

### 产品接口 `/api/v1/products`

- `GET /products` - 产品列表
- `POST /products` - 创建产品
- `PUT /products/{id}` - 更新产品
- `DELETE /products/{id}` - 删除产品

### 订单接口 `/api/v1/orders`

- `POST /orders` - 创建订单
- `GET /orders/{id}` - 订单详情
- `POST /orders/{id}/cancel` - 取消订单

### 支付接口 `/api/v1/payment`

- `POST /payment/wechat/create` - 创建微信支付
- `POST /payment/alipay/create` - 创建支付宝支付
- `GET /payment/{order_id}/status` - 支付状态

### 提现接口 `/api/v1/withdrawals`

- `POST /withdrawals` - 申请提现
- `GET /withdrawals` - 提现记录

## 数据库设计

### 核心表

- **users** - 用户账户表
- **merchants** - 商户档案表
- **products** - 产品表
- **orders** - 订单表
- **order_items** - 订单明细表
- **transactions** - 支付流水表
- **withdrawals** - 提现记录表

详细设计见 `docs/database.md`

## 开发规范

### 代码规范

- 后端: PEP 8
- 前端: ESLint + Prettier

### Git提交规范

```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试相关
chore: 构建/工具
```

## 安全考虑

1. **认证安全**
   - JWT token认证
   - 密码bcrypt加密
   - token过期机制

2. **支付安全**
   - 支付回调验签
   - 幂等性处理
   - 金额使用Decimal

3. **数据安全**
   - SQL注入防护
   - XSS防护
   - CSRF防护

## 部署

### Docker部署

```bash
docker-compose up -d
```

### 手动部署

参考 `docs/deployment.md`

## 开发进度

- [x] 阶段1: 项目骨架搭建
- [ ] 阶段2: 用户认证
- [ ] 阶段3: 产品管理
- [ ] 阶段4: 订单支付
- [ ] 阶段5: 统计提现
- [ ] 阶段6: 生产部署

## 许可证

MIT License

## 联系方式

项目问题反馈: [GitHub Issues]

---

*开发团队 @ 2024*
