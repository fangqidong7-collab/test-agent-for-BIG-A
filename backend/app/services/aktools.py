"""
AKTools 数据服务
官网: https://aktools.com
需要API Token
"""

import httpx
import json
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from .base import BaseDataService, register_service
from ..models.schemas import (
    SearchResult, RealtimePrice, KLineData, 
    FinancialIndicator, ValuationData, StockBasicInfo
)

logger = logging.getLogger(__name__)


class AKToolsService(BaseDataService):
    """AKTools 数据服务实现"""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or ""
        self.base_url = "https://aktools.com"
    
    @property
    def name(self) -> str:
        return "aktools"
    
    @property
    def priority(self) -> int:
        return 2  # 补充数据源
    
    async def search_stocks(self, keyword: str) -> List[SearchResult]:
        """搜索股票"""
        results = []
        
        try:
            async with httpx.AsyncClient() as client:
                # 使用AKTools的股票列表接口
                url = f"{self.base_url}/api/stock/search"
                params = {"keyword": keyword}
                if self.token:
                    params["token"] = self.token
                
                response = await client.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("code") == 200 and "data" in data:
                        for item in data["data"]:
                            results.append(SearchResult(
                                code=item.get("code", ""),
                                name=item.get("name", ""),
                                full_name=item.get("fullname"),
                                exchange=item.get("exchange", ""),
                                market=item.get("market"),
                                list_status=item.get("status", "上市")
                            ))
        except Exception as e:
            logger.error(f"AKTools search error: {e}")
        
        return results
    
    async def get_realtime_price(self, codes: List[str]) -> List[RealtimePrice]:
        """获取实时价格"""
        results = []
        
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/api/stock/quote"
                params = {"codes": ",".join(codes)}
                if self.token:
                    params["token"] = self.token
                
                response = await client.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("code") == 200 and "data" in data:
                        for item in data["data"]:
                            results.append(RealtimePrice(
                                code=item.get("code", ""),
                                name=item.get("name", ""),
                                open=float(item.get("open", 0)),
                                high=float(item.get("high", 0)),
                                low=float(item.get("low", 0)),
                                close=float(item.get("close", 0)),
                                pre_close=float(item.get("pre_close", 0)),
                                volume=float(item.get("volume", 0)),
                                amount=float(item.get("amount", 0)),
                                change_amount=float(item.get("change", 0)),
                                change_pct=float(item.get("change_pct", 0)),
                                pe_ttm=float(item.get("pe_ttm")) if item.get("pe_ttm") else None,
                                pb=float(item.get("pb")) if item.get("pb") else None,
                                market_cap=float(item.get("market_cap")) if item.get("market_cap") else None
                            ))
        except Exception as e:
            logger.error(f"AKTools realtime price error: {e}")
        
        return results
    
    async def get_kline_data(
        self, 
        code: str, 
        period: str = "daily",
        adjust: str = "qfq",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Optional[KLineData]:
        """获取K线数据"""
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/api/stock/kline"
                params = {
                    "code": code,
                    "period": period,
                    "adjust": adjust
                }
                if start_date:
                    params["start_date"] = start_date
                if end_date:
                    params["end_date"] = end_date
                if self.token:
                    params["token"] = self.token
                
                response = await client.get(url, params=params, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("code") == 200 and "data" in data:
                        kline_data = data["data"]
                        
                        # 计算均线
                        import pandas as pd
                        closes = pd.Series(kline_data.get("close", []))
                        
                        return KLineData(
                            dates=kline_data.get("date", []),
                            opens=kline_data.get("open", []),
                            highs=kline_data.get("high", []),
                            lows=kline_data.get("low", []),
                            closes=kline_data.get("close", []),
                            volumes=kline_data.get("volume", []),
                            amounts=kline_data.get("amount"),
                            ma5=closes.rolling(5).mean().tolist(),
                            ma10=closes.rolling(10).mean().tolist(),
                            ma20=closes.rolling(20).mean().tolist(),
                            ma60=closes.rolling(60).mean().tolist(),
                            period=period,
                            adjust=adjust
                        )
        except Exception as e:
            logger.error(f"AKTools kline error: {e}")
        
        return None
    
    async def get_stock_basic_info(self, code: str) -> Optional[StockBasicInfo]:
        """获取股票基本信息"""
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/api/stock/info"
                params = {"code": code}
                if self.token:
                    params["token"] = self.token
                
                response = await client.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("code") == 200 and "data" in data:
                        info = data["data"]
                        return StockBasicInfo(
                            code=info.get("code", code),
                            name=info.get("name", ""),
                            full_name=info.get("full_name"),
                            exchange=info.get("exchange", ""),
                            industry=info.get("industry"),
                            market=info.get("market"),
                            list_date=info.get("list_date")
                        )
        except Exception as e:
            logger.error(f"AKTools basic info error: {e}")
        
        return None
    
    async def get_financial_indicators(
        self, 
        code: str, 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[FinancialIndicator]:
        """获取财务指标"""
        # AKTools提供财务数据接口，需要Token
        return []
    
    async def get_valuation_data(self, code: str) -> Optional[ValuationData]:
        """获取估值数据"""
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/api/stock/valuation"
                params = {"code": code}
                if self.token:
                    params["token"] = self.token
                
                response = await client.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("code") == 200 and "data" in data:
                        val = data["data"]
                        return ValuationData(
                            code=code,
                            pe_ttm=val.get("pe_ttm"),
                            pe_lyr=val.get("pe_lyr"),
                            pb=val.get("pb"),
                            ps_ttm=val.get("ps_ttm"),
                            dividend_ratio=val.get("dividend_ratio")
                        )
        except Exception as e:
            logger.error(f"AKTools valuation error: {e}")
        
        return None
    
    async def is_available(self) -> bool:
        """检查服务是否可用"""
        # AKTools作为补充源，即使没有token也返回True（部分功能可用）
        return True


# 注册服务
# 注意：需要Token才能使用完整功能
# aktools_service = AKToolsService()
# register_service(aktools_service)
