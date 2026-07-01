from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
import uuid

from app.models.order import Order, OrderItem, Transaction
from app.models.product import Product
from app.models.merchant import Merchant
from app.core.exceptions import NotFoundException, BadRequestException
from app.config import settings


def generate_order_no() -> str:
    """生成订单号"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = str(uuid.uuid4().hex[:6]).upper()
    return f"ORD{timestamp}{random_str}"


def create_order(
    db: Session,
    consumer_id: int,
    items: List[dict],
    payment_method: str = "mock"
) -> Order:
    """
    创建订单

    Args:
        db: 数据库会话
        consumer_id: 消费者ID
        items: 订单项列表 [{"product_id": 1, "quantity": 2}, ...]
        payment_method: 支付方式

    Returns:
        Order: 创建的订单对象

    Raises:
        BadRequestException: 参数错误或库存不足
    """
    if not items:
        raise BadRequestException("订单项不能为空")

    # 验证并计算订单
    total_amount = Decimal("0")
    order_items_data = []
    merchant_id = None

    for item in items:
        product = db.query(Product).filter(Product.id == item["product_id"]).first()
        if not product:
            raise BadRequestException(f"产品ID {item['product_id']} 不存在")

        if product.status != "on_sale":
            raise BadRequestException(f"产品 {product.name} 已下架")

        quantity = item["quantity"]
        if quantity <= 0:
            raise BadRequestException("购买数量必须大于0")

        # 检查库存
        if product.stock != -1 and product.stock < quantity:
            raise BadRequestException(f"产品 {product.name} 库存不足")

        # 所有产品必须来自同一商户
        if merchant_id is None:
            merchant_id = product.merchant_id
        elif merchant_id != product.merchant_id:
            raise BadRequestException("一个订单只能包含同一商户的产品")

        subtotal = product.price * quantity
        total_amount += subtotal

        order_items_data.append({
            "product": product,
            "product_name": product.name,
            "unit_price": product.price,
            "quantity": quantity,
            "subtotal": subtotal
        })

    # 计算抽佣
    commission = total_amount * Decimal(str(settings.COMMISSION_RATE))
    merchant_income = total_amount - commission

    # 创建订单
    order = Order(
        order_no=generate_order_no(),
        consumer_id=consumer_id,
        merchant_id=merchant_id,
        total_amount=total_amount,
        commission=commission,
        merchant_income=merchant_income,
        status="pending",
        payment_method=payment_method
    )

    db.add(order)
    db.flush()

    # 创建订单明细
    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item_data["product"].id,
            product_name=item_data["product_name"],
            unit_price=item_data["unit_price"],
            quantity=item_data["quantity"],
            subtotal=item_data["subtotal"]
        )
        db.add(order_item)

        # 扣减库存
        if item_data["product"].stock != -1:
            item_data["product"].stock -= item_data["quantity"]

    db.commit()
    db.refresh(order)
    return order


def get_order_by_id(db: Session, order_id: int) -> Optional[Order]:
    """根据ID获取订单"""
    return db.query(Order).filter(Order.id == order_id).first()


def get_order_by_order_no(db: Session, order_no: str) -> Optional[Order]:
    """根据订单号获取订单"""
    return db.query(Order).filter(Order.order_no == order_no).first()


def get_user_orders(
    db: Session,
    user_id: int,
    role: str,
    skip: int = 0,
    limit: int = 20
) -> tuple[List[Order], int]:
    """
    获取用户订单列表

    Args:
        db: 数据库会话
        user_id: 用户ID
        role: 角色 (merchant/consumer)
        skip: 跳过数量
        limit: 返回数量

    Returns:
        tuple: (订单列表, 总数)
    """
    query = db.query(Order)

    if role == "consumer":
        query = query.filter(Order.consumer_id == user_id)
    elif role == "merchant":
        # 通过user_id找到merchant_id
        merchant = db.query(Merchant).filter(Merchant.user_id == user_id).first()
        if merchant:
            query = query.filter(Order.merchant_id == merchant.id)
        else:
            return [], 0

    total = query.count()
    orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

    return orders, total


def process_payment(
    db: Session,
    order_id: int,
    transaction_no: str,
    payment_method: str = "mock"
) -> Order:
    """
    处理支付

    Args:
        db: 数据库会话
        order_id: 订单ID
        transaction_no: 交易流水号
        payment_method: 支付方式

    Returns:
        Order: 更新后的订单对象

    Raises:
        NotFoundException: 订单不存在
        BadRequestException: 订单状态错误
    """
    order = get_order_by_id(db, order_id)
    if not order:
        raise NotFoundException("订单不存在")

    if order.status != "pending":
        raise BadRequestException("订单状态不正确")

    # 创建交易记录
    transaction = Transaction(
        order_id=order.id,
        transaction_no=transaction_no,
        amount=order.total_amount,
        channel=payment_method,
        type="payment",
        status="success"
    )
    db.add(transaction)

    # 更新订单状态
    order.status = "paid"
    order.paid_at = datetime.now()

    # 更新商户余额
    merchant = db.query(Merchant).filter(Merchant.id == order.merchant_id).first()
    if merchant:
        merchant.balance += order.merchant_income
        merchant.total_income += order.merchant_income

    # 更新产品销量
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.sales_count += item.quantity

    db.commit()
    db.refresh(order)
    return order


def cancel_order(db: Session, order_id: int, user_id: int) -> Order:
    """
    取消订单

    Args:
        db: 数据库会话
        order_id: 订单ID
        user_id: 用户ID（用于权限验证）

    Returns:
        Order: 更新后的订单对象

    Raises:
        NotFoundException: 订单不存在
        BadRequestException: 订单状态错误或无权操作
    """
    order = get_order_by_id(db, order_id)
    if not order:
        raise NotFoundException("订单不存在")

    if order.consumer_id != user_id:
        raise BadRequestException("无权操作此订单")

    if order.status != "pending":
        raise BadRequestException("只能取消待支付订单")

    # 恢复库存
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product and product.stock != -1:
            product.stock += item.quantity

    order.status = "cancelled"

    db.commit()
    db.refresh(order)
    return order
