# API接口文档

## 基础信息

- 基础URL: `http://localhost:8000/api/v1`
- 认证方式: JWT Bearer Token
- 请求格式: `application/json`
- 响应格式: `application/json`

## 通用响应格式

### 成功响应
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

### 错误响应
```json
{
  "code": 400,
  "message": "错误信息",
  "detail": "详细错误信息"
}
```

## 认证接口

### 注册
```
POST /api/v1/auth/register
```

请求体:
```json
{
  "username": "testuser",
  "phone": "13800138000",
  "password": "password123",
  "role": "merchant",
  "shop_name": "测试商户"
}
```

响应:
```json
{
  "id": 1,
  "username": "testuser",
  "phone": "13800138000",
  "role": "merchant"
}
```

### 登录
```
POST /api/v1/auth/login
```

请求体:
```json
{
  "username": "testuser",
  "password": "password123"
}
```

响应:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### 获取当前用户
```
GET /api/v1/auth/me
```

Headers:
```
Authorization: Bearer <access_token>
```

响应:
```json
{
  "id": 1,
  "username": "testuser",
  "role": "merchant"
}
```

## 商户接口

### 获取商户档案
```
GET /api/v1/merchant/profile
```

需要认证: 是 (商户)

响应:
```json
{
  "id": 1,
  "shop_name": "测试商户",
  "balance": "1000.00",
  "total_income": "5000.00"
}
```

### 获取收入统计
```
GET /api/v1/merchant/stats?period=week
```

需要认证: 是 (商户)

参数:
- `period`: day/week/month/all

响应:
```json
{
  "total_income": "5000.00",
  "net_income": "4500.00",
  "commission": "500.00",
  "order_count": 100
}
```

## 产品接口

### 获取产品列表
```
GET /api/v1/products?merchant_id=1
```

参数:
- `merchant_id`: 商户ID（可选）
- `keyword`: 搜索关键词（可选）
- `page`: 页码，默认1
- `page_size`: 每页数量，默认20

响应:
```json
{
  "total": 10,
  "items": [
    {
      "id": 1,
      "name": "商品名称",
      "price": "99.00",
      "stock": 100,
      "image_url": "/static/uploads/..."
    }
  ]
}
```

### 创建产品
```
POST /api/v1/products
```

需要认证: 是 (商户)

请求体:
```json
{
  "name": "新商品",
  "description": "商品描述",
  "price": 99.00,
  "stock": 100
}
```

## 订单接口

### 创建订单
```
POST /api/v1/orders
```

需要认证: 是 (消费者)

请求体:
```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ],
  "payment_method": "wechat"
}
```

响应:
```json
{
  "id": 1,
  "order_no": "ORDER20240101001",
  "total_amount": "198.00",
  "status": "pending"
}
```

### 获取订单详情
```
GET /api/v1/orders/{order_id}
```

需要认证: 是

响应:
```json
{
  "id": 1,
  "order_no": "ORDER20240101001",
  "total_amount": "198.00",
  "commission": "19.80",
  "merchant_income": "178.20",
  "status": "paid",
  "items": [
    {
      "product_name": "商品名称",
      "quantity": 2,
      "unit_price": "99.00"
    }
  ]
}
```

## 支付接口

### 创建微信支付
```
POST /api/v1/payment/wechat/create
```

需要认证: 是 (消费者)

请求体:
```json
{
  "order_id": 1
}
```

响应:
```json
{
  "code_url": "weixin://wxpay/bizpayurl?pr=xxxxx"
}
```

### 查询支付状态
```
GET /api/v1/payment/{order_id}/status
```

需要认证: 是

响应:
```json
{
  "order_id": 1,
  "status": "paid",
  "paid_at": "2024-01-01T12:00:00"
}
```

## 提现接口

### 申请提现
```
POST /api/v1/withdrawals
```

需要认证: 是 (商户)

请求体:
```json
{
  "amount": 1000.00,
  "channel": "wechat",
  "account": "微信账号",
  "account_name": "真实姓名"
}
```

### 获取提现记录
```
GET /api/v1/withdrawals
```

需要认证: 是 (商户)

响应:
```json
{
  "total": 5,
  "items": [
    {
      "id": 1,
      "amount": "1000.00",
      "channel": "wechat",
      "status": "paid",
      "created_at": "2024-01-01T12:00:00"
    }
  ]
}
```

## 错误码

| 错误码 | 说明 |
|-------|------|
| 400 | 请求参数错误 |
| 401 | 未授权，需要登录 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

完整的交互式API文档请访问: http://localhost:8000/docs
