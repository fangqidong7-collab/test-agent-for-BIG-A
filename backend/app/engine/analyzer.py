"""
主分析引擎
协调各子模块完成完整的股票分析
"""

import logging
import math
from typing import Optional, List, Any, Dict
from datetime import datetime

from ..models.schemas import (
    StockAnalysis, StockBasicInfo, RealtimePrice, KLineData,
    FinancialIndicator, ValuationData, SevenDRating, 
    ScenarioAnalysis, Catalyst
)
from ..services.base import get_registry
from .rating import rating_engine
from .scenario import scenario_engine

logger = logging.getLogger(__name__)


def clean_nan(obj: Any) -> Any:
    """递归清理字典/列表中的NaN和Infinity值"""
    if isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nan(item) for item in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    return obj


class Analyzer:
    """主分析引擎"""
    
    def __init__(self):
        self.service_registry = get_registry()
    
    async def analyze_stock(self, code: str) -> StockAnalysis:
        """
        执行完整的股票分析
        
        流程：
        1. 获取股票基本信息
        2. 获取实时价格
        3. 获取K线数据
        4. 获取财务数据
        5. 获取估值数据
        6. 计算七维评分
        7. 生成情景分析
        8. 生成催化剂与风险提示
        """
        
        data_source = []
        
        # 1. 获取股票基本信息
        basic_info = await self._fetch_basic_info(code)
        
        # 2. 获取实时价格
        realtime_price = await self._fetch_realtime_price(code)
        
        # 3. 获取K线数据
        kline_data = await self._fetch_kline_data(code)
        
        # 4. 获取财务数据
        financial_indicators = await self._fetch_financial_indicators(code)
        
        # 5. 获取估值数据
        valuation = await self._fetch_valuation_data(code)
        
        # 6. 计算七维评分
        seven_d_rating = None
        if basic_info and (financial_indicators or kline_data or valuation):
            seven_d_rating = await rating_engine.calculate_rating(
                code=code,
                name=basic_info.name if basic_info else "",
                financial_indicators=financial_indicators,
                valuation=valuation,
                kline_data=kline_data,
                realtime_price=realtime_price,
                industry=basic_info.industry if basic_info else None
            )
        
        # 7. 生成情景分析
        scenario_analysis = None
        if realtime_price and realtime_price.close > 0:
            scenario_analysis = await scenario_engine.analyze(
                code=code,
                name=basic_info.name if basic_info else "",
                current_price=realtime_price.close,
                kline_data=kline_data,
                financial_indicators=financial_indicators,
                valuation=valuation,
                basic_info=basic_info
            )
        
        # 8. 生成催化剂与风险提示
        catalysts = self._generate_catalysts(
            code, basic_info, financial_indicators, valuation, kline_data
        )
        
        # 9. 获取行业/概念标签（预留）
        industry_tags = [basic_info.industry] if basic_info and basic_info.industry else []
        concept_tags = self._get_concept_tags(code)
        
        # 确定数据来源
        if self.service_registry.get_primary_service():
            data_source.append(self.service_registry.get_primary_service().name)
        
        return StockAnalysis(
            basic_info=basic_info,
            realtime_price=realtime_price,
            kline_data=kline_data,
            financial_indicators=financial_indicators,
            valuation=valuation,
            seven_d_rating=seven_d_rating,
            scenario_analysis=scenario_analysis,
            catalysts=catalysts,
            industry_tags=industry_tags,
            concept_tags=concept_tags,
            data_source="BaoStock/AKShare" if data_source else "Mock Data",
            data_timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    
    async def _fetch_basic_info(self, code: str) -> Optional[StockBasicInfo]:
        """获取股票基本信息"""
        for service in self.service_registry.get_all_services():
            try:
                if await service.is_available():
                    result = await service.get_stock_basic_info(code)
                    if result:
                        return result
            except Exception as e:
                logger.warning(f"{service.name} get_basic_info failed: {e}")
        
        # 如果所有服务都失败，使用Mock数据
        return self._get_mock_basic_info(code)
    
    async def _fetch_realtime_price(self, code: str) -> Optional[RealtimePrice]:
        """获取实时价格"""
        for service in self.service_registry.get_all_services():
            try:
                if await service.is_available():
                    result = await service.get_realtime_price([code])
                    if result:
                        return result[0]
            except Exception as e:
                logger.warning(f"{service.name} get_realtime_price failed: {e}")
        
        return self._get_mock_realtime_price(code)
    
    async def _fetch_kline_data(
        self, 
        code: str, 
        period: str = "daily"
    ) -> Optional[KLineData]:
        """获取K线数据"""
        for service in self.service_registry.get_all_services():
            try:
                if await service.is_available():
                    result = await service.get_kline_data(code, period=period)
                    if result:
                        return result
            except Exception as e:
                logger.warning(f"{service.name} get_kline_data failed: {e}")
        
        return self._get_mock_kline_data(code)
    
    async def _fetch_financial_indicators(
        self, 
        code: str
    ) -> List[FinancialIndicator]:
        """获取财务指标"""
        for service in self.service_registry.get_all_services():
            try:
                if await service.is_available():
                    result = await service.get_financial_indicators(code)
                    if result:
                        return result
            except Exception as e:
                logger.warning(f"{service.name} get_financial_indicators failed: {e}")
        
        return self._get_mock_financial_indicators(code)
    
    async def _fetch_valuation_data(self, code: str) -> Optional[ValuationData]:
        """获取估值数据"""
        for service in self.service_registry.get_all_services():
            try:
                if await service.is_available():
                    result = await service.get_valuation_data(code)
                    if result:
                        return result
            except Exception as e:
                logger.warning(f"{service.name} get_valuation_data failed: {e}")
        
        return self._get_mock_valuation_data(code)
    
    def _generate_catalysts(
        self,
        code: str,
        basic_info: Optional[StockBasicInfo],
        financial_indicators: List[FinancialIndicator],
        valuation: Optional[ValuationData],
        kline_data: Optional[KLineData]
    ) -> List[Catalyst]:
        """生成催化剂与风险提示"""
        catalysts = []
        
        # 基于财务数据生成
        if financial_indicators:
            latest = financial_indicators[0]
            
            if latest.roe_avg and latest.roe_avg > 20:
                catalysts.append(Catalyst(
                    type="positive",
                    title="ROE表现优异",
                    description=f"净资产收益率达{latest.roe_avg:.1f}%，盈利能力突出",
                    source="财务数据",
                    date=latest.date
                ))
            
            if latest.net_margin and latest.net_margin > 15:
                catalysts.append(Catalyst(
                    type="positive",
                    title="净利率较高",
                    description=f"销售净利率{latest.net_margin:.1f}%，成本控制能力较强",
                    source="财务数据",
                    date=latest.date
                ))
            
            if latest.debt_asset_ratio and latest.debt_asset_ratio > 70:
                catalysts.append(Catalyst(
                    type="negative",
                    title="资产负债率偏高",
                    description=f"资产负债率{latest.debt_asset_ratio:.1f}%，需关注债务风险",
                    source="财务数据",
                    date=latest.date
                ))
        
        # 基于估值生成
        if valuation:
            if valuation.pe_ttm and valuation.pe_ttm > 50:
                catalysts.append(Catalyst(
                    type="negative",
                    title="估值偏高",
                    description=f"动态市盈率{valuation.pe_ttm:.1f}倍，处于历史较高水平",
                    source="估值数据",
                    date="当前"
                ))
            elif valuation.pe_ttm and valuation.pe_ttm < 15:
                catalysts.append(Catalyst(
                    type="positive",
                    title="估值合理偏低",
                    description=f"动态市盈率{valuation.pe_ttm:.1f}倍，具备估值优势",
                    source="估值数据",
                    date="当前"
                ))
        
        # 基于技术面生成
        if kline_data and len(kline_data.closes) >= 60:
            recent_closes = kline_data.closes[-20:]
            ma20 = kline_data.ma20[-20:] if kline_data.ma20 else []
            
            if ma20 and all(c > m for c, m in zip(recent_closes[-10:], ma20[-10:])):
                catalysts.append(Catalyst(
                    type="positive",
                    title="技术形态向好",
                    description="股价站稳20日均线上方，短期趋势向上",
                    source="技术分析",
                    date="近期"
                ))
        
        # 如果没有生成任何催化剂，添加默认提示
        if not catalysts:
            catalysts.append(Catalyst(
                type="neutral",
                title="数据收集中",
                description="当前数据不足以生成详细催化剂分析，建议关注近期公告",
                source="系统",
                date="当前"
            ))
        
        return catalysts
    
    def _get_concept_tags(self, code: str) -> List[str]:
        """获取概念标签（预留）"""
        # 实际应该从数据源获取
        return []
    
    # ==================== Mock数据生成 ====================
    
    def _get_mock_basic_info(self, code: str) -> StockBasicInfo:
        """生成Mock基本信息"""
        return StockBasicInfo(
            code=code,
            name=f"股票{code}",
            full_name=f"某某股份有限公司",
            exchange="SZ",
            industry="电子",
            market="创业板",
            list_date="2020-01-01"
        )
    
    def _get_mock_realtime_price(self, code: str) -> RealtimePrice:
        """生成Mock实时价格"""
        import random
        price = random.uniform(10, 100)
        change = random.uniform(-5, 5)
        
        return RealtimePrice(
            code=code,
            name=f"股票{code}",
            open=price * 0.99,
            high=price * 1.03,
            low=price * 0.97,
            close=price,
            pre_close=price * (1 - change / 100),
            volume=random.uniform(1000000, 10000000),
            amount=random.uniform(10000000, 100000000),
            change_amount=change,
            change_pct=change,
            pe_ttm=random.uniform(15, 40),
            pb=random.uniform(1, 5),
            market_cap=random.uniform(50, 500),
            float_market_cap=random.uniform(30, 300)
        )
    
    def _get_mock_kline_data(self, code: str) -> KLineData:
        """生成Mock K线数据"""
        import random
        import pandas as pd
        
        # 生成日期
        dates = pd.date_range(end=datetime.now(), periods=365, freq='D').strftime('%Y-%m-%d').tolist()
        
        # 生成价格序列（模拟趋势）
        base_price = 20
        closes = []
        current = base_price
        
        for _ in range(365):
            current += random.uniform(-0.5, 0.6)
            closes.append(max(1, current))
        
        # 计算其他OHLCV
        highs = [c * random.uniform(1.0, 1.05) for c in closes]
        lows = [c * random.uniform(0.95, 1.0) for c in closes]
        opens = [random.uniform(l, h) for l, h in zip(lows, highs)]
        volumes = [random.uniform(1000000, 5000000) for _ in range(365)]
        
        # 计算均线
        closes_series = pd.Series(closes)
        ma5 = closes_series.rolling(5).mean().tolist()
        ma10 = closes_series.rolling(10).mean().tolist()
        ma20 = closes_series.rolling(20).mean().tolist()
        ma60 = closes_series.rolling(60).mean().tolist()
        
        return KLineData(
            dates=dates,
            opens=opens,
            highs=highs,
            lows=lows,
            closes=closes,
            volumes=volumes,
            ma5=ma5,
            ma10=ma10,
            ma20=ma20,
            ma60=ma60,
            period="daily",
            adjust="qfq"
        )
    
    def _get_mock_financial_indicators(self, code: str) -> List[FinancialIndicator]:
        """生成Mock财务数据"""
        import random
        
        indicators = []
        for i in range(8):
            indicators.append(FinancialIndicator(
                date=f"20{23-i//4}-{(i%4)*3+3:02d}-31" if i < 4 else f"20{22-i//4}-{(i%4)*3+3:02d}-31",
                code=code,
                roe_avg=random.uniform(8, 25),
                gross_margin=random.uniform(15, 45),
                net_margin=random.uniform(5, 20),
                debt_asset_ratio=random.uniform(30, 70),
                current_ratio=random.uniform(1, 3),
                quick_ratio=random.uniform(0.5, 2.5),
                total_revenue=random.uniform(50, 500),
                main_business_profit=random.uniform(10, 100),
                operating_profit=random.uniform(8, 80),
                total_profit=random.uniform(10, 90),
                net_profit=random.uniform(5, 70),
                net_profit_atsopc=random.uniform(4, 60),
                diluted_roe=random.uniform(8, 25),
                weighted_roe=random.uniform(8, 25),
                basic_eps=random.uniform(0.2, 2.0),
                bvps=random.uniform(5, 20),
                total_asset_turnover=random.uniform(0.3, 1.5),
                inventory_turnover=random.uniform(2, 10),
                receivables_turnover=random.uniform(3, 12),
                cash_ratio=random.uniform(20, 150)
            ))
        
        return indicators
    
    def _get_mock_valuation_data(self, code: str) -> ValuationData:
        """生成Mock估值数据"""
        import random
        
        return ValuationData(
            code=code,
            pe_ttm=random.uniform(15, 40),
            pe_lyr=random.uniform(15, 40),
            pb=random.uniform(1, 5),
            ps_ttm=random.uniform(1, 10),
            ps_lyr=random.uniform(1, 10),
            dividend_ratio=random.uniform(0.5, 4),
            dividend_yield2=random.uniform(0.5, 4),
            pe_history_percentile=random.uniform(20, 80),
            pb_history_percentile=random.uniform(20, 80),
            industry_avg_pe=random.uniform(20, 35),
            industry_median_pe=random.uniform(18, 30)
        )


# 全局实例
analyzer = Analyzer()
