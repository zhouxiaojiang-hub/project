from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Merchant(Base):
    """商户档案表"""
    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    shop_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=True)  # 小吃/服饰/手作等
    location = Column(String(200), nullable=True)
    longitude = Column(Numeric(10, 7), nullable=True)
    latitude = Column(Numeric(10, 7), nullable=True)
    cover_url = Column(String(255), nullable=True)
    balance = Column(Numeric(12, 2), default=0)  # 可提现余额
    total_income = Column(Numeric(12, 2), default=0)  # 累计净收入
    created_at = Column(DateTime, default=func.now())

    # 关系
    user = relationship("User", back_populates="merchant")
    products = relationship("Product", back_populates="merchant")
    orders = relationship("Order", foreign_keys="Order.merchant_id", back_populates="merchant")
    withdrawals = relationship("Withdrawal", back_populates="merchant")
