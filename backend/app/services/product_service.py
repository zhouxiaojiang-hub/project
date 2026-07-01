from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from app.models.product import Product
from app.models.merchant import Merchant
from app.core.exceptions import NotFoundException, BadRequestException, AuthorizationException
from decimal import Decimal


def create_product(
    db: Session,
    merchant_id: int,
    name: str,
    description: Optional[str],
    price: Decimal,
    stock: int,
    status: str = "on_sale"
) -> Product:
    """
    创建产品

    Args:
        db: 数据库会话
        merchant_id: 商户ID
        name: 产品名称
        description: 产品描述
        price: 价格
        stock: 库存
        status: 状态

    Returns:
        Product: 创建的产品对象
    """
    product = Product(
        merchant_id=merchant_id,
        name=name,
        description=description,
        price=price,
        stock=stock,
        status=status
    )

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
    """根据ID获取产品"""
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(
    db: Session,
    merchant_id: Optional[int] = None,
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 20
) -> tuple[List[Product], int]:
    """
    获取产品列表

    Args:
        db: 数据库会话
        merchant_id: 商户ID（可选）
        keyword: 搜索关键词（可选）
        status: 状态过滤（可选）
        skip: 跳过数量
        limit: 返回数量

    Returns:
        tuple: (产品列表, 总数)
    """
    query = db.query(Product)

    # 过滤条件
    if merchant_id:
        query = query.filter(Product.merchant_id == merchant_id)

    if keyword:
        query = query.filter(Product.name.like(f"%{keyword}%"))

    if status:
        query = query.filter(Product.status == status)

    # 获取总数
    total = query.count()

    # 分页
    products = query.order_by(Product.created_at.desc()).offset(skip).limit(limit).all()

    return products, total


def update_product(
    db: Session,
    product_id: int,
    merchant_id: int,
    **kwargs
) -> Product:
    """
    更新产品

    Args:
        db: 数据库会话
        product_id: 产品ID
        merchant_id: 商户ID（用于权限验证）
        **kwargs: 要更新的字段

    Returns:
        Product: 更新后的产品对象

    Raises:
        NotFoundException: 产品不存在
        AuthorizationException: 无权操作
    """
    product = get_product_by_id(db, product_id)

    if not product:
        raise NotFoundException("产品不存在")

    if product.merchant_id != merchant_id:
        raise AuthorizationException("无权操作此产品")

    # 更新字段
    for key, value in kwargs.items():
        if value is not None and hasattr(product, key):
            setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int, merchant_id: int) -> None:
    """
    删除产品

    Args:
        db: 数据库会话
        product_id: 产品ID
        merchant_id: 商户ID（用于权限验证）

    Raises:
        NotFoundException: 产品不存在
        AuthorizationException: 无权操作
    """
    product = get_product_by_id(db, product_id)

    if not product:
        raise NotFoundException("产品不存在")

    if product.merchant_id != merchant_id:
        raise AuthorizationException("无权操作此产品")

    db.delete(product)
    db.commit()


def update_product_image(
    db: Session,
    product_id: int,
    merchant_id: int,
    image_url: str
) -> Product:
    """
    更新产品图片

    Args:
        db: 数据库会话
        product_id: 产品ID
        merchant_id: 商户ID
        image_url: 图片URL

    Returns:
        Product: 更新后的产品对象
    """
    return update_product(db, product_id, merchant_id, image_url=image_url)


def get_merchant_products(
    db: Session,
    merchant_id: int,
    skip: int = 0,
    limit: int = 20
) -> tuple[List[Product], int]:
    """
    获取商户的所有产品

    Args:
        db: 数据库会话
        merchant_id: 商户ID
        skip: 跳过数量
        limit: 返回数量

    Returns:
        tuple: (产品列表, 总数)
    """
    return get_products(db, merchant_id=merchant_id, skip=skip, limit=limit)
