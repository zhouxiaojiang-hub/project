from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Order(Base):
    """订单表"""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(32), unique=True, nullable=False, index=True)
    consumer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=False, index=True)
    total_amount = Column(Numeric(10, 2), nullable=False)
    commission = Column(Numeric(10, 2), nullable=False)  # 平台抽佣10%
    merchant_income = Column(Numeric(10, 2), nullable=False)  # 商户实收90%
    status = Column(String(20), default="pending")  # pending / paid / cancelled / refunded
    payment_method = Column(String(20), nullable=True)  # wechat / alipay
    paid_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())

    # 关系
    consumer = relationship("User", foreign_keys=[consumer_id], back_populates="consumer_orders")
    merchant = relationship("Merchant", foreign_keys=[merchant_id], back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    transactions = relationship("Transaction", back_populates="order")


class OrderItem(Base):
    """订单明细表"""
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product_name = Column(String(100), nullable=False)  # 快照
    unit_price = Column(Numeric(10, 2), nullable=False)  # 快照
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    # 关系
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


class Transaction(Base):
    """支付流水表"""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    transaction_no = Column(String(64), unique=True, nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    channel = Column(String(20), nullable=False)  # wechat / alipay / mock
    type = Column(String(20), nullable=False)  # payment / refund
    status = Column(String(20), default="pending")  # success / failed / pending
    raw_response = Column(Text, nullable=True)  # 原始回调JSON
    created_at = Column(DateTime, default=func.now())

    # 关系
    order = relationship("Order", back_populates="transactions")
