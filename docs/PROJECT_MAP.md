# 街头地摊推广系统 - 项目地图

## 项目概览

本系统为街头地摊商户提供数字化管理平台，包含商户端、消费者端两个前端应用和统一的后端API服务。

## 系统架构图

```
┌─────────────────┐         ┌─────────────────┐
│   商户端Web应用  │         │  消费者端Web应用 │
│   (React SPA)   │         │   (React SPA)   │
│   Port: 3001    │         │   Port: 3002    │
└────────┬────────┘         └────────┬────────┘
         │                           │
         └───────────┬───────────────┘
                     │ REST API
         ┌───────────▼───────────┐
         │   FastAPI后端服务     │
         │   Port: 8000          │
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │   SQLite数据库        │
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │  第三方支付集成       │
         │  微信支付/支付宝      │
         └───────────────────────┘
```

## 核心功能模块

### 商户端
1. 账户管理（注册/登录）
2. 商户档案管理
3. 产品管理（增删改查、图片上传）
4. 订单管理（查看、筛选）
5. 收入统计（图表展示）
6. 提现管理（申请、记录）

### 消费者端
1. 账户管理（注册/登录）
2. 商户浏览（列表、详情）
3. 产品浏览
4. 购物车
5. 下单支付（微信/支付宝）
6. 订单管理

### 后端服务
1. 用户认证（JWT）
2. 商户服务
3. 产品服务
4. 订单服务
5. 支付服务（微信/支付宝）
6. 提现服务

## 技术栈地图

```
后端技术栈
├── FastAPI (Web框架)
├── SQLAlchemy (ORM)
├── Alembic (数据库迁移)
├── JWT (认证)
├── Bcrypt (密码加密)
└── Pydantic (数据验证)

前端技术栈
├── React 18 (UI框架)
├── TypeScript (类型系统)
├── Vite (构建工具)
├── React Router (路由)
├── Zustand (状态管理)
├── TanStack Query (数据请求)
├── Ant Design (UI组件)
└── Recharts (图表)
```

## API接口地图

### 认证模块 `/api/v1/auth`
- POST `/register` - 注册
- POST `/login` - 登录
- POST `/refresh` - 刷新token
- GET `/me` - 当前用户

### 商户模块 `/api/v1/merchant`
- GET `/profile` - 商户档案
- PUT `/profile` - 更新档案
- GET `/orders` - 消费记录
- GET `/stats` - 收入统计
- GET `/balance` - 可提现余额

### 产品模块 `/api/v1/products`
- GET `/products` - 产品列表
- POST `/products` - 创建产品
- PUT `/products/{id}` - 更新产品
- DELETE `/products/{id}` - 删除产品
- POST `/products/{id}/upload-image` - 上传图片

### 订单模块 `/api/v1/orders`
- POST `/orders` - 创建订单
- GET `/orders/{id}` - 订单详情
- POST `/orders/{id}/cancel` - 取消订单

### 支付模块 `/api/v1/payment`
- POST `/payment/wechat/create` - 微信支付
- POST `/payment/alipay/create` - 支付宝支付
- GET `/payment/{order_id}/status` - 支付状态

### 提现模块 `/api/v1/withdrawals`
- POST `/withdrawals` - 申请提现
- GET `/withdrawals` - 提现记录

## 数据库设计图

```
users (用户表)
├── id
├── username
├── phone
├── password_hash
├── role (merchant/consumer)
└── status

merchants (商户表)
├── id
├── user_id (FK)
├── shop_name
├── balance (可提现余额)
└── total_income

products (产品表)
├── id
├── merchant_id (FK)
├── name
├── price
├── stock
└── status

orders (订单表)
├── id
├── order_no
├── consumer_id (FK)
├── merchant_id (FK)
├── total_amount
├── commission (10%)
├── merchant_income (90%)
└── status

order_items (订单明细)
├── id
├── order_id (FK)
├── product_id (FK)
├── quantity
└── subtotal

transactions (交易流水)
├── id
├── order_id (FK)
├── transaction_no
├── amount
├── channel
└── status

withdrawals (提现记录)
├── id
├── merchant_id (FK)
├── amount
├── channel
├── status
└── account
```

## 业务流程图

### 下单支付流程
```
1. 消费者选购商品 → 加入购物车
2. 确认订单 → 创建订单(计算10%抽佣)
3. 选择支付方式 → 调起微信/支付宝
4. 支付完成 → 回调验签
5. 更新订单状态 → 商户余额增加90%
6. 扣减产品库存
```

### 商户提现流程
```
1. 商户查看可提现余额
2. 填写提现信息(金额、渠道、账户)
3. 提交申请 → 余额校验
4. 创建提现记录 → 冻结余额
5. 平台审核(可选)
6. 审核通过 → 打款 → 扣减余额
```

## 开发路线图

- [x] 阶段1: 项目骨架搭建
- [ ] 阶段2: 用户认证系统
- [ ] 阶段3: 产品管理功能
- [ ] 阶段4: 订单支付功能
- [ ] 阶段5: 统计提现功能
- [ ] 阶段6: 生产环境部署

---

*更新时间: 2024*
