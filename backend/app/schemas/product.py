from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class ProductCreate(BaseModel):
    """创建产品请求"""
    name: str = Field(..., min_length=1, max_length=100, description="产品名称")
    description: Optional[str] = Field(None, description="产品描述")
    price: Decimal = Field(..., gt=0, description="价格")
    stock: int = Field(default=-1, description="库存，-1表示不限")
    status: str = Field(default="on_sale", pattern="^(on_sale|off_shelf)$")


class ProductUpdate(BaseModel):
    """更新产品请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0)
    stock: Optional[int] = None
    status: Optional[str] = Field(None, pattern="^(on_sale|off_shelf)$")


class ProductResponse(BaseModel):
    """产品响应"""
    id: int
    merchant_id: int
    name: str
    description: Optional[str]
    price: Decimal
    stock: int
    image_url: Optional[str]
    status: str
    sales_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
