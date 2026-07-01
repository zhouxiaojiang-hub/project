from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""

    # 数据库配置
    DATABASE_URL: str = "sqlite:///./street_vendor.db"

    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # 平台配置
    COMMISSION_RATE: float = 0.10

    # 文件上传配置
    UPLOAD_DIR: str = "static/uploads"
    MAX_UPLOAD_SIZE: int = 5242880  # 5MB

    # 微信支付配置
    WECHAT_PAY_MCHID: Optional[str] = None
    WECHAT_PAY_PRIVATE_KEY: Optional[str] = None
    WECHAT_PAY_CERT_SERIAL_NO: Optional[str] = None
    WECHAT_PAY_APIV3_KEY: Optional[str] = None
    WECHAT_PAY_APPID: Optional[str] = None

    # 支付宝配置
    ALIPAY_APPID: Optional[str] = None
    ALIPAY_PRIVATE_KEY: Optional[str] = None
    ALIPAY_PUBLIC_KEY: Optional[str] = None
    ALIPAY_SANDBOX: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
