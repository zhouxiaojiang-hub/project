from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.deps import get_current_user, require_merchant
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services import product_service
from app.models.user import User
from app.models.merchant import Merchant
from app.core.exceptions import NotFoundException, AuthorizationException
import os
import uuid
from pathlib import Path

router = APIRouter()


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_merchant)
):
    """
    创建产品（仅商户）

    - **name**: 产品名称
    - **description**: 产品描述
    - **price**: 价格
    - **stock**: 库存（-1表示不限）
    - **status**: 状态（on_sale/off_shelf）
    """
    # 获取商户信息
    merchant = db.query(Merchant).filter(Merchant.user_id == current_user.id).first()
    if not merchant:
        raise HTTPException(status_code=400, detail="商户信息不存在")

    new_product = product_service.create_product(
        db=db,
        merchant_id=merchant.id,
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        status=product.status
    )

    return new_product


@router.get("", response_model=dict)
def get_products(
    merchant_id: Optional[int] = None,
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    """
    获取产品列表（公开接口）

    - **merchant_id**: 商户ID（可选）
    - **keyword**: 搜索关键词（可选）
    - **status**: 状态过滤（可选）
    - **page**: 页码（默认1）
    - **page_size**: 每页数量（默认20）
    """
    skip = (page - 1) * page_size
    products, total = product_service.get_products(
        db=db,
        merchant_id=merchant_id,
        keyword=keyword,
        status=status,
        skip=skip,
        limit=page_size
    )

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": jsonable_encoder(products)
    }


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    获取产品详情（公开接口）
    """
    product = product_service.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_merchant)
):
    """
    更新产品（仅商户，且只能更新自己的产品）
    """
    # 获取商户信息
    merchant = db.query(Merchant).filter(Merchant.user_id == current_user.id).first()
    if not merchant:
        raise HTTPException(status_code=400, detail="商户信息不存在")

    try:
        # 只传递非None的字段
        update_data = product_update.dict(exclude_unset=True)
        updated_product = product_service.update_product(
            db=db,
            product_id=product_id,
            merchant_id=merchant.id,
            **update_data
        )
        return updated_product
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e.detail))
    except AuthorizationException as e:
        raise HTTPException(status_code=403, detail=str(e.detail))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_merchant)
):
    """
    删除产品（仅商户，且只能删除自己的产品）
    """
    # 获取商户信息
    merchant = db.query(Merchant).filter(Merchant.user_id == current_user.id).first()
    if not merchant:
        raise HTTPException(status_code=400, detail="商户信息不存在")

    try:
        product_service.delete_product(db=db, product_id=product_id, merchant_id=merchant.id)
        return None
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e.detail))
    except AuthorizationException as e:
        raise HTTPException(status_code=403, detail=str(e.detail))


@router.post("/{product_id}/upload-image", response_model=ProductResponse)
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_merchant)
):
    """
    上传产品图片（仅商户）

    支持格式: jpg, jpeg, png
    最大大小: 5MB
    """
    # 获取商户信息
    merchant = db.query(Merchant).filter(Merchant.user_id == current_user.id).first()
    if not merchant:
        raise HTTPException(status_code=400, detail="商户信息不存在")

    # 验证文件类型
    allowed_types = ["image/jpeg", "image/jpg", "image/png"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="不支持的图片格式，仅支持 jpg, jpeg, png")

    # 验证文件大小（5MB）
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="图片大小不能超过5MB")

    # 生成唯一文件名
    file_ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_ext}"

    # 创建上传目录
    upload_dir = Path("static/uploads/products") / str(merchant.id)
    upload_dir.mkdir(parents=True, exist_ok=True)

    # 保存文件
    file_path = upload_dir / filename
    with open(file_path, "wb") as f:
        f.write(contents)

    # 更新产品图片URL
    image_url = f"/static/uploads/products/{merchant.id}/{filename}"

    try:
        updated_product = product_service.update_product_image(
            db=db,
            product_id=product_id,
            merchant_id=merchant.id,
            image_url=image_url
        )
        return updated_product
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e.detail))
    except AuthorizationException as e:
        raise HTTPException(status_code=403, detail=str(e.detail))
