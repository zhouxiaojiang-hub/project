from fastapi import APIRouter
from app.api.v1 import auth, product, order

# 创建v1版本的总路由
api_router = APIRouter()

# 注册各个模块的路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(product.router, prefix="/products", tags=["产品"])
api_router.include_router(order.router, prefix="/orders", tags=["订单"])
