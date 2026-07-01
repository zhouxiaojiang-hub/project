from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.deps import get_current_user
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    UserResponse
)
from app.services import auth_service
from app.models.user import User
from app.core.security import decode_token
from app.core.exceptions import BadRequestException, AuthenticationException

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    用户注册

    - **username**: 用户名（3-50字符）
    - **phone**: 手机号（11位）
    - **password**: 密码（6-50字符）
    - **role**: 角色（merchant或consumer）
    - **shop_name**: 商户名称（仅商户注册时需要）
    """
    try:
        user = auth_service.register_user(
            db=db,
            username=request.username,
            phone=request.phone,
            password=request.password,
            role=request.role,
            shop_name=request.shop_name
        )
        return user
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.detail))


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    用户登录

    - **username**: 用户名或手机号
    - **password**: 密码

    返回访问令牌和刷新令牌
    """
    user = auth_service.authenticate_user(db, request.username, request.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    access_token, refresh_token = auth_service.generate_tokens(user)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    刷新访问令牌

    - **refresh_token**: 刷新令牌

    返回新的访问令牌和刷新令牌
    """
    payload = decode_token(request.refresh_token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌"
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌类型错误"
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌数据无效"
        )

    user = auth_service.get_user_by_id(db, int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )

    access_token, refresh_token = auth_service.generate_tokens(user)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    获取当前登录用户信息

    需要在Header中携带访问令牌：
    Authorization: Bearer <access_token>
    """
    return current_user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(current_user: User = Depends(get_current_user)):
    """
    退出登录

    前端需要清除本地存储的token
    后端暂不维护token黑名单（可在生产环境添加）
    """
    # 这里可以添加token黑名单逻辑
    # 目前仅作为占位符，实际退出由前端清除token完成
    return None
