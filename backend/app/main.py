"""
FastAPI 应用入口
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import math

from .api import search_router, stock_router


def custom_json_encoder(obj):
    """自定义JSON编码器，处理NaN和Infinity值"""
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


class CustomJSONResponse(JSONResponse):
    """自定义JSON响应，处理NaN值"""
    def render(self, content) -> bytes:
        import json
        return json.dumps(
            content,
            default=custom_json_encoder,
            ensure_ascii=False,
            allow_nan=False
        ).encode("utf-8")

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="A股智能分析平台 API",
    description="提供A股股票搜索、实时行情、K线数据、财务分析、估值分析等功能",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("A股智能分析平台 API 启动中...")
    
    # 预加载数据服务
    try:
        from .services import baostock_service, akshare_service
        logger.info(f"已加载数据服务: baostock, akshare")
    except Exception as e:
        logger.warning(f"部分数据服务加载失败: {e}")
    
    logger.info("启动完成")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("应用关闭中...")
    
    # 登出数据服务
    try:
        from .services.baostock import BaoStockService
        service = BaoStockService()
        service._logout()
    except:
        pass


@app.get("/", tags=["root"])
async def root():
    """根路径"""
    return JSONResponse(content={
        "name": "A股智能分析平台 API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "search": "/api/search",
            "stock": "/api/stock/{code}",
            "kline": "/api/stock/{code}/kline",
            "financial": "/api/stock/{code}/financial",
            "valuation": "/api/stock/{code}/valuation"
        }
    })


@app.get("/health", tags=["health"])
async def health_check():
    """健康检查"""
    return JSONResponse(content={
        "status": "healthy",
        "service": "astock-analyzer-api"
    })


# 注册路由
app.include_router(search_router)
app.include_router(stock_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
