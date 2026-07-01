from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RegisterRequest(BaseModel):
    """注册请求"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    phone: str = Field(..., pattern=r"^1[3-9]\d{9}$", description="手机号")
    password: str = Field(..., min_length=6, max_length=50, description="密码")
    role: str = Field(..., pattern="^(merchant|consumer)$", description="角色: merchant或consumer")
    
    # 商户注册时的额外信息
    shop_name: Optional[str] = Field(None, max_length=100, description="商户名称(仅商户注册)")


class LoginRequest(BaseModel):
    """登录请求"""
    username: str = Field(..., description="用户名或手机号")
    password: str = Field(..., description="密码")


class TokenResponse(BaseModel):
    """令牌响应"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """刷新令牌请求"""
    refresh_token: str


class UserResponse(BaseModel):
    """用户响应"""
    id: int
    username: str
    phone: str
    role: str
    avatar_url: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
