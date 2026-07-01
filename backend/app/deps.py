from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import decode_token
from app.models.user import User
from app.core.exceptions import AuthenticationException, AuthorizationException

# HTTP Bearer认证
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """获取当前登录用户"""
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload is None:
        raise AuthenticationException("无效的令牌")
    
    if payload.get("type") != "access":
        raise AuthenticationException("令牌类型错误")
    
    user_id = payload.get("sub")
    if user_id is None:
        raise AuthenticationException("令牌数据无效")
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise AuthenticationException("用户不存在")
    
    if user.status != "active":
        raise AuthenticationException("用户已被禁用")
    
    return user


def require_merchant(current_user: User = Depends(get_current_user)) -> User:
    """要求商户角色"""
    if current_user.role != "merchant":
        raise AuthorizationException("需要商户权限")
    return current_user


def require_consumer(current_user: User = Depends(get_current_user)) -> User:
    """要求消费者角色"""
    if current_user.role != "consumer":
        raise AuthorizationException("需要消费者权限")
    return current_user
