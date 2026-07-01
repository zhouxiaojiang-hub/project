from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Withdrawal(Base):
    """提现记录表"""
    __tablename__ = "withdrawals"

    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    channel = Column(String(20), nullable=False)  # wechat / alipay
    account = Column(String(100), nullable=False)  # 收款账户
    account_name = Column(String(50), nullable=False)  # 真实姓名
    status = Column(String(20), default="pending")  # pending / approved / paid / rejected
    remark = Column(String(255), nullable=True)  # 拒绝原因
    reviewed_at = Column(DateTime, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())

    # 关系
    merchant = relationship("Merchant", back_populates="withdrawals")
