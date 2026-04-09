"""
情景分析引擎
分析三种情景下的股价区间和概率
"""

import numpy as np
from typing import Dict, Optional, Any, List
from datetime import datetime
import logging

from ..models.schemas import (
    ScenarioAnalysis, KLineData, FinancialIndicator, 
    ValuationData, RealtimePrice, StockBasicInfo
)

logger = logging.getLogger(__name__)


class ScenarioEngine:
    """情景分析引擎"""
    
    def __init__(self):
        # 情景概率权重（可配置）
        self.probability_weights = {
            "optimistic": 0.20,
            "neutral": 0.55,
            "pessimistic": 0.25
        }
    
    async def analyze(
        self,
        code: str,
        name: str,
        current_price: float,
        kline_data: Optional[KLineData],
        financial_indicators: List[FinancialIndicator],
        valuation: Optional[ValuationData],
        basic_info: Optional[StockBasicInfo]
    ) -> ScenarioAnalysis:
        """执行情景分析"""
        
        # 计算历史波动率
        volatility = self._calculate_volatility(kline_data)
        
        # 计算估值区间
        valuation_range = self._calculate_valuation_range(
            current_price, valuation, financial_indicators
        )
        
        # 生成三种情景
        scenarios = {}
        
        # 乐观情景
        scenarios["optimistic"] = {
            "probability": self.probability_weights["optimistic"],
            "target_price": round(current_price * (1 + volatility * 1.5), 2),
            "upside_pct": round(volatility * 150, 1),
            "conditions": self._get_optimistic_conditions(
                financial_indicators, valuation, basic_info
            ),
            "time_horizon": "6-12个月",
            "description": "在乐观假设下（业绩超预期、估值提升、市场情绪高涨）的目标价"
        }
        
        # 中性情景
        scenarios["neutral"] = {
            "probability": self.probability_weights["neutral"],
            "target_price": round(
                scenarios["optimistic"]["target_price"] * 0.5 + 
                current_price * 0.5 * (1 + volatility * 0.5), 2
            ),
            "upside_pct": round(volatility * 50, 1),
            "conditions": self._get_neutral_conditions(
                financial_indicators, valuation
            ),
            "time_horizon": "6-12个月",
            "description": "在基准假设下（业绩平稳增长、市场估值稳定）的合理目标价"
        }
        
        # 悲观情景
        scenarios["pessimistic"] = {
            "probability": self.probability_weights["pessimistic"],
            "target_price": round(current_price * (1 - volatility), 2),
            "downside_pct": round(volatility * 100, 1),
            "conditions": self._get_pessimistic_conditions(
                financial_indicators, valuation
            ),
            "time_horizon": "3-6个月",
            "description": "在悲观假设下（业绩不及预期、市场情绪低迷、估值收缩）的支撑位"
        }
        
        # 生成综合摘要
        summary = self._generate_summary(
            current_price, scenarios, volatility
        )
        
        return ScenarioAnalysis(
            current_price=current_price,
            currency="CNY",
            scenarios=scenarios,
            summary=summary
        )
    
    def _calculate_volatility(self, kline_data: Optional[KLineData]) -> float:
        """计算历史波动率（年化）"""
        if kline_data and len(kline_data.closes) >= 60:
            closes = np.array(kline_data.closes[-60:])
            returns = np.diff(np.log(closes))
            daily_volatility = np.std(returns)
            annual_volatility = daily_volatility * np.sqrt(252)
            return min(annual_volatility, 0.5)  # 限制最大波动率50%
        return 0.25  # 默认25%年化波动率
    
    def _calculate_valuation_range(
        self,
        current_price: float,
        valuation: Optional[ValuationData],
        financial_indicators: List[FinancialIndicator]
    ) -> Dict[str, float]:
        """计算估值区间"""
        range_info = {
            "current_pe": None,
            "historical_low_pe": None,
            "historical_high_pe": None,
            "historical_low_price": None,
            "historical_high_price": None
        }
        
        if valuation:
            range_info["current_pe"] = valuation.pe_ttm
            range_info["historical_low_pe"] = valuation.pe_ttm * 0.7 if valuation.pe_ttm else None
            range_info["historical_high_pe"] = valuation.pe_ttm * 1.3 if valuation.pe_ttm else None
        
        return range_info
    
    def _get_optimistic_conditions(
        self,
        financial_indicators: List[FinancialIndicator],
        valuation: Optional[ValuationData],
        basic_info: Optional[StockBasicInfo]
    ) -> List[str]:
        """乐观情景触发条件"""
        conditions = []
        
        if financial_indicators:
            latest = financial_indicators[0]
            
            # 业绩超预期
            if latest.net_margin and latest.net_margin > 15:
                conditions.append("业绩持续超预期")
            
            # 高增长
            if latest.roe_avg and latest.roe_avg > 20:
                conditions.append("ROE持续保持20%以上")
            
            # 市场份额提升
            if latest.total_revenue and len(financial_indicators) >= 4:
                growth = (latest.total_revenue - financial_indicators[3].total_revenue) / \
                         financial_indicators[3].total_revenue * 100 if financial_indicators[3].total_revenue else 0
                if growth > 30:
                    conditions.append("营收快速增长，市场份额提升")
        
        # 行业因素
        if basic_info and basic_info.industry:
            conditions.append(f"行业景气度提升（{basic_info.industry}）")
        
        # 估值扩张
        if valuation and valuation.pe_history_percentile and valuation.pe_history_percentile < 50:
            conditions.append("估值有望向历史均值回归")
        
        if not conditions:
            conditions = ["业绩持续增长", "市场情绪回暖", "估值适度扩张"]
        
        return conditions[:4]  # 最多4个条件
    
    def _get_neutral_conditions(
        self,
        financial_indicators: List[FinancialIndicator],
        valuation: Optional[ValuationData]
    ) -> List[str]:
        """中性情景假设"""
        conditions = []
        
        if financial_indicators:
            latest = financial_indicators[0]
            
            if latest.roe_avg and 10 <= latest.roe_avg <= 20:
                conditions.append("ROE保持10-20%区间")
            
            if latest.net_margin and latest.net_margin > 5:
                conditions.append("净利率保持稳定")
        
        if valuation and valuation.pe_ttm:
            conditions.append(f"PE维持在{valuation.pe_ttm:.0f}倍左右")
        
        if not conditions:
            conditions = ["业绩平稳增长", "估值保持稳定", "市场整体平稳"]
        
        return conditions[:4]
    
    def _get_pessimistic_conditions(
        self,
        financial_indicators: List[FinancialIndicator],
        valuation: Optional[ValuationData]
    ) -> List[str]:
        """悲观情景风险因素"""
        risks = []
        
        if financial_indicators:
            latest = financial_indicators[0]
            
            if latest.roe_avg and latest.roe_avg < 10:
                risks.append("ROE低于10%，盈利能力下降")
            
            if latest.debt_asset_ratio and latest.debt_asset_ratio > 70:
                risks.append("资产负债率偏高，财务风险")
            
            if latest.net_margin and latest.net_margin < 0:
                risks.append("净利润为负，亏损扩大")
        
        if valuation and valuation.pe_ttm and valuation.pe_ttm > 50:
            risks.append("估值处于历史高位，回调压力大")
        
        if not risks:
            risks = ["市场整体回调", "业绩增速放缓", "估值面临收缩"]
        
        return risks[:4]
    
    def _generate_summary(
        self,
        current_price: float,
        scenarios: Dict[str, Any],
        volatility: float
    ) -> str:
        """生成分析摘要"""
        optimistic_price = scenarios["optimistic"]["target_price"]
        neutral_price = scenarios["neutral"]["target_price"]
        pessimistic_price = scenarios["pessimistic"]["target_price"]
        
        upside = (optimistic_price - current_price) / current_price * 100
        downside = (current_price - pessimistic_price) / current_price * 100
        
        summary = f"""基于当前价格 {current_price:.2f} 元和历史波动率 {volatility*100:.1f}%，情景分析如下：

• 乐观情景（概率{scenarios["optimistic"]["probability"]*100:.0f}%）：目标价 {optimistic_price:.2f} 元，上涨空间约 {upside:.1f}%
• 中性情景（概率{scenarios["neutral"]["probability"]*100:.0f}%）：目标价 {neutral_price:.2f} 元
• 悲观情景（概率{scenarios["pessimistic"]["probability"]*100:.0f}%）：支撑位 {pessimistic_price:.2f} 元，下跌风险约 {downside:.1f}%

风险收益比（R/R）约为 {upside/downside:.2f}，投资者可根据自身风险偏好评估配置价值。
"""
        
        return summary.strip()


# 全局实例
scenario_engine = ScenarioEngine()
