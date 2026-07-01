# 街头地摊推广系统 - 实施计划

## 项目概述

**系统名称**：街头地摊推广系统  
**技术栈**：Python (FastAPI) + React + SQLite  
**目标**：为街头地摊商户和消费者提供线上交易平台，支持商户管理、消费者购物、在线支付和提现功能

## 核心功能

### 商户端
- 商户注册/登录
- 产品管理（增删改查）
- 消费记录查询（时间、金额筛选）
- 收入统计（总收入、净收入、平台抽佣）
- 提现功能（微信、支付宝）

### 消费者端
- 消费者注册/登录
- 浏览商户列表
- 选择商户查看产品
- 下单购买
- 在线支付（微信、支付宝）
- 消费历史查询

### 平台规则
- 平台抽佣：10%
- 商户提现时按净收入（90%）结算

## 技术架构

### 后端架构（FastAPI）

```
backend/
├── app/
│   ├── main.py              # 应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── deps.py              # 依赖注入
│   ├── models/              # SQLAlchemy ORM模型
│   │   ├── user.py
│   │   ├── merchant.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── transaction.py
│   │   └── withdrawal.py
│   ├── schemas/             # Pydantic请求/响应模型
│   ├── api/v1/              # API路由
│   │   ├── auth.py
│   │   ├── merchant.py
│   │   ├── consumer.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── payment.py
│   │   └── withdrawal.py
│   ├── services/            # 业务逻辑层
│   ├── core/                # 基础设施（JWT、异常、日志）
│   ├── integrations/        # 第三方支付集成
│   └── utils/               # 工具函数
├── migrations/              # Alembic数据库迁移
├── tests/                   # 单元测试
└── requirements.txt
```

### 前端架构（React）

**商户端** (`frontend-merchant/`)
```
src/
├── pages/
│   ├── Login/              # 登录
│   ├── Register/           # 注册
│   ├── Dashboard/          # 收入概览
│   ├── Orders/             # 消费记录
│   ├── Products/           # 产品管理
│   ├── Withdrawal/         # 提现
│   └── Profile/            # 商户档案
├── components/             # 通用组件
├── api/                    # 接口封装
├── store/                  # Zustand状态管理
└── router/                 # 路由配置
```

**消费者端** (`frontend-consumer/`)
```
src/
├── pages/
│   ├── Login/              # 登录
│   ├── Register/           # 注册
│   ├── Home/               # 商户列表
│   ├── MerchantDetail/     # 商户详情
│   ├── Cart/               # 购物车
│   ├── Checkout/           # 结算
│   ├── Payment/            # 支付
│   └── Orders/             # 订单历史
├── components/
├── api/
├── store/
└── router/
```

## 数据库设计

### 核心数据表

#### users（用户表）
- 统一账户表，区分商户/消费者角色
- 字段：id, username, phone, password_hash, role, avatar_url, status, created_at, updated_at

#### merchants（商户档案）
- 1:1扩展users表
- 字段：id, user_id, shop_name, description, category, location, longitude, latitude, cover_url, balance（可提现余额）, total_income, created_at

#### products（产品表）
- 字段：id, merchant_id, name, description, price, stock, image_url, status, sales_count, created_at, updated_at

#### orders（订单表）
- 字段：id, order_no, consumer_id, merchant_id, total_amount, commission（10%）, merchant_income（90%）, status, payment_method, paid_at, created_at

#### order_items（订单明细）
- 字段：id, order_id, product_id, product_name, unit_price, quantity, subtotal

#### transactions（支付流水）
- 字段：id, order_id, transaction_no, amount, channel, type, status, raw_response, created_at

#### withdrawals（提现记录）
- 字段：id, merchant_id, amount, channel, account, account_name, status, remark, reviewed_at, paid_at, created_at

### 数据关系
- users (1) → merchants (1) → products (N)
- users (消费者) (1) → orders (N) → order_items (N)
- merchants (1) → orders (N) → transactions (N)
- merchants (1) → withdrawals (N)

## API设计

### 认证接口 `/api/v1/auth`
- POST `/auth/register` - 注册
- POST `/auth/login` - 登录（返回JWT token）
- POST `/auth/refresh` - 刷新token
- GET `/auth/me` - 获取当前用户信息

### 商户接口 `/api/v1/merchant`
- GET `/merchant/profile` - 获取商户档案
- PUT `/merchant/profile` - 更新商户档案
- GET `/merchant/orders` - 消费记录列表（支持筛选）
- GET `/merchant/orders/{id}` - 订单详情
- GET `/merchant/stats` - 收入统计
- GET `/merchant/balance` - 可提现余额

### 产品接口 `/api/v1/products`
- GET `/products` - 产品列表（公开）
- GET `/products/{id}` - 产品详情（公开）
- POST `/products` - 创建产品（商户）
- PUT `/products/{id}` - 更新产品（商户）
- DELETE `/products/{id}` - 删除产品（商户）
- POST `/products/{id}/upload-image` - 上传产品图片

### 消费者接口 `/api/v1/consumer`
- GET `/consumer/merchants` - 商户列表
- GET `/consumer/merchants/{id}` - 商户详情
- GET `/consumer/orders` - 我的订单
- GET `/consumer/orders/{id}` - 订单详情

### 订单接口 `/api/v1/orders`
- POST `/orders` - 创建订单
- POST `/orders/{id}/cancel` - 取消订单
- GET `/orders/{id}` - 查询订单

### 支付接口 `/api/v1/payment`
- POST `/payment/wechat/create` - 创建微信支付
- POST `/payment/alipay/create` - 创建支付宝支付
- POST `/payment/wechat/notify` - 微信支付回调
- POST `/payment/alipay/notify` - 支付宝支付回调
- GET `/payment/{order_id}/status` - 查询支付状态

### 提现接口 `/api/v1/withdrawals`
- POST `/withdrawals` - 申请提现
- GET `/withdrawals` - 提现记录列表
- GET `/withdrawals/{id}` - 提现详情
- POST `/withdrawals/{id}/review` - 审核提现（管理员）

## 核心技术方案

### 1. JWT认证
- 使用 `python-jose` + `passlib[bcrypt]`
- access_token 有效期：2小时
- refresh_token 有效期：7天
- 前端axios拦截器自动注入Authorization header
- 401时自动刷新token

### 2. 支付集成
- 抽象统一支付接口
- 微信支付：使用 `wechatpayv3` SDK
- 支付宝：使用 `python-alipay-sdk`
- 支持mock支付通道用于开发测试
- 支付回调处理：验签 → 幂等检查 → 事务更新 → 返回响应

### 3. 文件上传
- 产品图片存储：`backend/static/uploads/products/{merchant_id}/{uuid}.{ext}`
- 校验：扩展名、大小（≤5MB）、MIME类型
- 生产环境可切换到对象存储（OSS/COS/S3）

### 4. 权限控制
- 路由层：依赖注入 `require_merchant` / `require_consumer`
- 资源层：校验资源归属（product.merchant_id == current_user.id）
- 前端：ProtectedRoute组件 + 角色路由过滤

### 5. 抽佣计算
- 平台抽佣比例：10%
- 下单时计算并写入订单表（commission, merchant_income）
- 支付成功后累加商户余额（merchants.balance += merchant_income）
- 提现时扣减余额并校验（amount <= balance）
- 所有金额使用Decimal类型，避免浮点误差

## 分阶段实施计划

### 阶段1：基础脚手架（1-2天）
**目标**：搭建项目骨架，确保环境可运行

**交付物**：
- ✅ 后端FastAPI项目结构
- ✅ 前端两个React应用（商户端、消费者端）
- ✅ SQLite数据库连接
- ✅ Alembic迁移初始化
- ✅ 健康检查接口 `/health`
- ✅ README启动说明
- ✅ .env.example配置模板

**验收标准**：
- 后端启动成功，访问 `/health` 返回200
- 前端两个应用启动成功，显示初始页面
- 数据库文件创建成功

### 阶段2：用户与认证（2-3天）
**目标**：实现完整的用户认证流程

**交付物**：
- ✅ users、merchants数据表及模型
- ✅ 注册、登录、刷新token接口
- ✅ JWT认证中间件
- ✅ 商户/消费者注册登录页面
- ✅ 前端JWT拦截器
- ✅ ProtectedRoute组件
- ✅ 单元测试（auth相关）

**验收标准**：
- 可以注册商户/消费者账号
- 登录后获取token，访问受保护接口成功
- 未登录访问受保护接口返回401
- token过期后自动刷新

### 阶段3：产品与商户浏览（3-4天）
**目标**：商户可管理产品，消费者可浏览

**交付物**：
- ✅ products数据表及模型
- ✅ 产品CRUD接口
- ✅ 图片上传接口
- ✅ 商户端产品管理页面（列表、新增、编辑）
- ✅ 消费者端商户列表页面
- ✅ 消费者端商户详情页面
- ✅ 消费者端产品浏览页面
- ✅ 静态文件服务配置

**验收标准**：
- 商户可以创建、编辑、删除产品
- 商户可以上传产品图片
- 消费者可以浏览商户列表
- 消费者可以查看商户详情和在售商品
- 图片可以正常显示

### 阶段4：下单与支付（4-5天）
**目标**：完成下单到支付的完整流程

**交付物**：
- ✅ orders、order_items、transactions数据表
- ✅ 创建订单接口（含抽佣计算）
- ✅ 支付接口（mock通道）
- ✅ 支付回调处理
- ✅ 消费者端购物车（前端状态）
- ✅ 消费者端结算页面
- ✅ 消费者端支付页面
- ✅ 消费者端订单历史页面
- ✅ 库存扣减逻辑
- ✅ 订单取消逻辑

**验收标准**：
- 消费者可以加入购物车
- 消费者可以创建订单
- 订单创建时正确计算抽佣（10%）和商户收入（90%）
- 使用mock支付完成支付流程
- 支付成功后订单状态更新
- 支付成功后商户余额增加
- 支付成功后产品库存减少
- 消费者可以查看订单历史

### 阶段5：商户统计与提现（3-4天）
**目标**：商户可查看统计和提现

**交付物**：
- ✅ withdrawals数据表
- ✅ 商户消费记录查询接口（支持筛选）
- ✅ 商户收入统计接口
- ✅ 提现申请接口
- ✅ 提现记录查询接口
- ✅ 商户端Dashboard页面（收入概览、图表）
- ✅ 商户端消费记录页面（筛选、分页）
- ✅ 商户端提现页面（申请、历史）
- ✅ 余额校验逻辑

**验收标准**：
- 商户可以查看收入统计（总收入、净收入、抽佣）
- 商户可以按时间、金额筛选消费记录
- 商户可以申请提现
- 提现金额不能超过可用余额
- 商户可以查看提现历史

### 阶段6：真实支付与上线准备（3-5天）
**目标**：接入真实支付，准备上线

**交付物**：
- ✅ 接入微信支付沙箱
- ✅ 接入支付宝沙箱
- ✅ 支付回调验签
- ✅ 支付幂等处理
- ✅ 异常处理和日志
- ✅ API限流中间件
- ✅ 端到端测试
- ✅ Docker Compose配置
- ✅ 部署文档

**验收标准**：
- 可以使用微信扫码支付
- 可以使用支付宝支付
- 支付回调正确处理
- 重复回调不会重复增加余额
- 异常情况有明确错误提示
- 关键操作有日志记录
- 可以通过Docker一键启动
- 有完整的部署文档

## 技术依赖

### 后端依赖（requirements.txt）
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
alembic==1.13.1
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
wechatpayv3==1.2.7
python-alipay-sdk==3.0.4
pillow==10.2.0
pytest==7.4.4
httpx==0.26.0
```

### 前端依赖
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.0",
    "axios": "^1.6.5",
    "zustand": "^4.4.7",
    "@tanstack/react-query": "^5.17.0",
    "antd": "^5.12.8",
    "recharts": "^2.10.3",
    "zod": "^3.22.4"
  },
  "devDependencies": {
    "@types/react": "^18.2.47",
    "@types/react-dom": "^18.2.18",
    "@vitejs/plugin-react": "^4.2.1",
    "typescript": "^5.3.3",
    "vite": "^5.0.11"
  }
}
```

## 安全考虑

### 认证安全
- 密码使用bcrypt哈希存储
- JWT token设置合理的过期时间
- 敏感操作需要重新验证
- 防止暴力破解（登录限流）

### 支付安全
- 所有支付回调必须验签
- 幂等性处理防止重复支付
- 金额计算使用Decimal避免精度问题
- 敏感配置（密钥）存储在环境变量

### 数据安全
- SQL注入防护（使用ORM参数化查询）
- XSS防护（前端输入验证、后端转义）
- CSRF防护（SameSite Cookie）
- 文件上传限制类型和大小

### 权限安全
- 路由级权限控制
- 资源级权限校验
- 角色隔离（商户/消费者）
- 敏感操作日志记录

## 性能优化

### 后端优化
- 数据库索引（user_id, order_no, created_at等）
- 分页查询避免全表扫描
- 图片压缩和缩略图
- API响应缓存（Redis可选）

### 前端优化
- React Query缓存服务端数据
- 图片懒加载
- 路由懒加载
- 打包优化（代码分割）

## 监控与运维

### 日志
- 关键操作日志（登录、下单、支付、提现）
- 错误日志（异常栈、请求参数）
- 支付回调日志（完整请求响应）

### 监控
- API响应时间
- 错误率统计
- 支付成功率
- 系统资源使用

### 备份
- 数据库定期备份
- 上传文件备份
- 配置文件版本控制

## 下一步行动

1. **确认需求**：与用户确认功能需求和优先级
2. **环境准备**：确认开发环境（Python、Node.js版本）
3. **开始阶段1**：搭建项目脚手架
4. **迭代开发**：按阶段推进，每个阶段演示验收
5. **测试验证**：功能测试、支付测试、压力测试
6. **上线部署**：配置生产环境、域名、HTTPS

## 项目时间线

- 阶段1：基础脚手架（2天）
- 阶段2：用户与认证（3天）
- 阶段3：产品与商户浏览（4天）
- 阶段4：下单与支付（5天）
- 阶段5：商户统计与提现（4天）
- 阶段6：真实支付与上线准备（5天）

**预计总开发时间：23天**

---

*本计划将根据实际开发进度和需求变化进行调整*
