from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.models.merchant import Merchant
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.core.exceptions import BadRequestException, AuthenticationException
from typing import Optional, Tuple


def register_user(
    db: Session,
    username: str,
    phone: str,
    password: str,
    role: str,
    shop_name: Optional[str] = None
) -> User:
    """
    注册新用户

    Args:
        db: 数据库会话
        username: 用户名
        phone: 手机号
        password: 密码
        role: 角色 (merchant/consumer)
        shop_name: 商户名称（仅商户注册时需要）

    Returns:
        User: 创建的用户对象

    Raises:
        BadRequestException: 参数错误或用户已存在
    """
    # 验证商户注册必须提供商户名
    if role == "merchant" and not shop_name:
        raise BadRequestException("商户注册必须提供商户名称")

    # 检查用户名是否已存在
    existing_user = db.query(User).filter(
        (User.username == username) | (User.phone == phone)
    ).first()

    if existing_user:
        if existing_user.username == username:
            raise BadRequestException("用户名已存在")
        if existing_user.phone == phone:
            raise BadRequestException("手机号已被注册")

    # 创建用户
    user = User(
        username=username,
        phone=phone,
        password_hash=hash_password(password),
        role=role,
        status="active"
    )

    try:
        db.add(user)
        db.flush()  # 获取user.id

        # 如果是商户，创建商户档案
        if role == "merchant":
            merchant = Merchant(
                user_id=user.id,
                shop_name=shop_name,
                balance=0,
                total_income=0
            )
            db.add(merchant)

        db.commit()
        db.refresh(user)
        return user

    except IntegrityError:
        db.rollback()
        raise BadRequestException("用户注册失败，请检查信息是否重复")


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    验证用户登录

    Args:
        db: 数据库会话
        username: 用户名或手机号
        password: 密码

    Returns:
        User: 验证成功返回用户对象，失败返回None
    """
    # 支持用户名或手机号登录
    user = db.query(User).filter(
        (User.username == username) | (User.phone == username)
    ).first()

    if not user:
        return None

    if user.status != "active":
        raise AuthenticationException("用户已被禁用")

    if not verify_password(password, user.password_hash):
        return None

    return user


def generate_tokens(user: User) -> Tuple[str, str]:
    """
    生成访问令牌和刷新令牌

    Args:
        user: 用户对象

    Returns:
        Tuple[str, str]: (access_token, refresh_token)
    """
    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role
    }

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return access_token, refresh_token


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    根据ID获取用户

    Args:
        db: 数据库会话
        user_id: 用户ID

    Returns:
        User: 用户对象或None
    """
    return db.query(User).filter(User.id == user_id).first()
