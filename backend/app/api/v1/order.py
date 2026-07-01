from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.deps import get_current_user, require_consumer
from app.schemas.order import OrderCreate, OrderResponse, PaymentRequest, PaymentResponse
from app.services import order_service
from app.models.user import User
from app.core.exceptions import NotFoundException, BadRequestException
import uuid

router = APIRouter()


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_consumer)
):
    """
    创建订单（仅消费者）

    - **items**: 订单项列表，每项包含product_id和quantity
    - **payment_method**: 支付方式（默认mock）
    """
    try:
        items = [item.dict() for item in order_data.items]
        order = order_service.create_order(
            db=db,
            consumer_id=current_user.id,
            items=items,
            payment_method=order_data.payment_method
        )
        return order
    except BadRequestException as e:
        raise HTTPException(status_code=400, detail=str(e.detail))


@router.get("", response_model=dict)
def get_orders(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取订单列表

    商户看到的是消费记录，消费者看到的是购买记录
    """
    skip = (page - 1) * page_size
    orders, total = order_service.get_user_orders(
        db=db,
        user_id=current_user.id,
        role=current_user.role,
        skip=skip,
        limit=page_size
    )

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": jsonable_encoder(orders)
    }


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取订单详情

    只能查看自己的订单（消费者）或自己商户的订单（商户）
    """
    order = order_service.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    # 权限验证
    if current_user.role == "consumer":
        if order.consumer_id != current_user.id:
            raise HTTPException(status_code=403, detail="无权查看此订单")
    elif current_user.role == "merchant":
        from app.models.merchant import Merchant
        merchant = db.query(Merchant).filter(Merchant.user_id == current_user.id).first()
        if not merchant or order.merchant_id != merchant.id:
            raise HTTPException(status_code=403, detail="无权查看此订单")

    return order


@router.post("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_consumer)
):
    """
    取消订单（仅消费者，且只能取消待支付订单）
    """
    try:
        order = order_service.cancel_order(db, order_id, current_user.id)
        return order
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e.detail))
    except BadRequestException as e:
        raise HTTPException(status_code=400, detail=str(e.detail))


@router.post("/payment/mock", response_model=PaymentResponse)
def create_mock_payment(
    payment_data: PaymentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_consumer)
):
    """
    创建Mock支付（测试用）

    自动完成支付，无需真实支付流程
    """
    order = order_service.get_order_by_id(db, payment_data.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    if order.consumer_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权操作此订单")

    try:
        # 生成模拟交易号
        transaction_no = f"MOCK_{uuid.uuid4().hex.upper()[:16]}"

        # 处理支付
        updated_order = order_service.process_payment(
            db=db,
            order_id=order.id,
            transaction_no=transaction_no,
            payment_method="mock"
        )

        return PaymentResponse(
            order_id=updated_order.id,
            order_no=updated_order.order_no,
            payment_method="mock",
            amount=updated_order.total_amount,
            payment_url=None,
            qr_code=None
        )
    except (NotFoundException, BadRequestException) as e:
        raise HTTPException(status_code=400, detail=str(e.detail))
