"""
股票详情API
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional, List
import logging
import math
import json

from ..models.schemas import StockAnalysis, KLineData
from ..engine.analyzer import analyzer
from ..services.base import get_registry

router = APIRouter(prefix="/api/stock", tags=["stock"])
logger = logging.getLogger(__name__)


def clean_nan_for_json(obj):
    """清理NaN和Infinity值用于JSON序列化"""
    if isinstance(obj, dict):
        return {k: clean_nan_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nan_for_json(item) for item in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    return obj


@router.get("/{code}")
async def get_stock_analysis(code: str):
    """
    获取股票完整分析报告
    
    返回包含基本信息、实时价格、K线数据、财务指标、
    估值数据、七维评分、情景分析、催化剂与风险提示等
    """
    # 验证股票代码格式
    if not code or len(code) < 6:
        raise HTTPException(status_code=400, detail="股票代码格式不正确")
    
    # 清理代码
    code = code.strip().upper()
    
    try:
        analysis = await analyzer.analyze_stock(code)
        # 转换为dict并清理NaN
        data = analysis.model_dump()
        data = clean_nan_for_json(data)
        return JSONResponse(content=data)
    except Exception as e:
        logger.error(f"Analysis failed for {code}: {e}")
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@router.get("/{code}/kline")
async def get_kline(
    code: str,
    period: str = Query("daily", description="周期: daily/weekly/monthly"),
    adjust: str = Query("qfq", description="复权: qfq/hfq/none"),
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD")
):
    """
    获取K线数据
    """
    if not code:
        raise HTTPException(status_code=400, detail="股票代码不能为空")
    
    registry = get_registry()
    
    for service in registry.get_all_services():
        try:
            if await service.is_available():
                kline_data = await service.get_kline_data(
                    code=code,
                    period=period,
                    adjust=adjust,
                    start_date=start_date,
                    end_date=end_date
                )
                
                if kline_data:
                    return JSONResponse(content={
                        "code": 200,
                        "data": kline_data.model_dump(),
                        "source": service.name
                    })
        except Exception as e:
            logger.warning(f"{service.name} kline failed: {e}")
    
    raise HTTPException(status_code=404, detail="未找到K线数据")


@router.get("/{code}/financial")
async def get_financial(
    code: str,
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM")
):
    """
    获取财务数据
    """
    if not code:
        raise HTTPException(status_code=400, detail="股票代码不能为空")
    
    registry = get_registry()
    
    for service in registry.get_all_services():
        try:
            if await service.is_available():
                data = await service.get_financial_indicators(
                    code=code,
                    start_date=start_date,
                    end_date=end_date
                )
                
                if data:
                    return JSONResponse(content={
                        "code": 200,
                        "data": [item.model_dump() for item in data],
                        "source": service.name,
                        "total": len(data)
                    })
        except Exception as e:
            logger.warning(f"{service.name} financial failed: {e}")
    
    raise HTTPException(status_code=404, detail="未找到财务数据")


@router.get("/{code}/valuation")
async def get_valuation(code: str):
    """
    获取估值数据
    """
    if not code:
        raise HTTPException(status_code=400, detail="股票代码不能为空")
    
    registry = get_registry()
    
    for service in registry.get_all_services():
        try:
            if await service.is_available():
                data = await service.get_valuation_data(code)
                
                if data:
                    return JSONResponse(content={
                        "code": 200,
                        "data": data.model_dump(),
                        "source": service.name
                    })
        except Exception as e:
            logger.warning(f"{service.name} valuation failed: {e}")
    
    raise HTTPException(status_code=404, detail="未找到估值数据")


@router.get("/batch/realtime")
async def get_batch_realtime(codes: str = Query(..., description="股票代码，多个用逗号分隔")):
    """
    批量获取实时价格
    """
    code_list = [c.strip() for c in codes.split(",") if c.strip()]
    
    if not code_list:
        raise HTTPException(status_code=400, detail="股票代码不能为空")
    
    if len(code_list) > 50:
        raise HTTPException(status_code=400, detail="最多支持50个股票代码")
    
    registry = get_registry()
    
    for service in registry.get_all_services():
        try:
            if await service.is_available():
                prices = await service.get_realtime_price(code_list)
                
                if prices:
                    return JSONResponse(content={
                        "code": 200,
                        "data": [item.model_dump() for item in prices],
                        "source": service.name,
                        "total": len(prices)
                    })
        except Exception as e:
            logger.warning(f"{service.name} batch realtime failed: {e}")
    
    raise HTTPException(status_code=404, detail="未找到实时价格数据")
