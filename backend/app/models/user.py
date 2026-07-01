from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    phone = Column(String(20), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # merchant / consumer
    avatar_url = Column(String(255), nullable=True)
    status = Column(String(20), default="active")  # active / disabled
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # 关系
    merchant = relationship("Merchant", back_populates="user", uselist=False)
    consumer_orders = relationship("Order", foreign_keys="Order.consumer_id", back_populates="consumer")
