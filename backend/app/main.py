from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.api.v1.router import api_router
import os

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(
    title="街头地摊推广系统",
    description="支持商户和消费者的线上交易平台",
    version="1.0.0"
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    """根路径"""
    return {"message": "街头地摊推广系统API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "ok", "message": "服务运行正常"}


# 注册API路由
app.include_router(api_router, prefix="/api/v1")
