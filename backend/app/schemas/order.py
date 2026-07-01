from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal


class OrderItemCreate(BaseModel):
    """创建订单项"""
    product_id: int = Field(..., description="产品ID")
    quantity: int = Field(..., gt=0, description="数量")


class OrderCreate(BaseModel):
    """创建订单请求"""
    items: List[OrderItemCreate] = Field(..., min_items=1, description="订单项列表")
    payment_method: str = Field(default="mock", description="支付方式")


class OrderItemResponse(BaseModel):
    """订单项响应"""
    id: int
    product_id: int
    product_name: str
    unit_price: Decimal
    quantity: int
    subtotal: Decimal

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """订单响应"""
    id: int
    order_no: str
    consumer_id: int
    merchant_id: int
    total_amount: Decimal
    commission: Decimal
    merchant_income: Decimal
    status: str
    payment_method: str
    paid_at: Optional[datetime]
    created_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True


class PaymentRequest(BaseModel):
    """支付请求"""
    order_id: int = Field(..., description="订单ID")


class PaymentResponse(BaseModel):
    """支付响应"""
    order_id: int
    order_no: str
    payment_method: str
    amount: Decimal
    payment_url: Optional[str] = None
    qr_code: Optional[str] = None
