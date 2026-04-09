"""
七维评分引擎
评估维度：
1. 盈利能力 (25%权重)
2. 成长能力 (20%权重)
3. 估值水平 (15%权重)
4. 财务健康 (15%权重)
5. 技术走势 (10%权重)
6. 行业前景 (10%权重)
7. 机构关注 (5%权重)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from ..models.schemas import (
    DimensionScore, SevenDRating, KLineData, 
    FinancialIndicator, ValuationData, RealtimePrice
)

logger = logging.getLogger(__name__)


class RatingEngine:
    """七维评分引擎"""
    
    # 评分维度定义
    DIMENSIONS = {
        "profitability": {
            "name": "盈利能力",
            "weight": 0.25,
            "metrics": ["roe", "gross_margin", "net_margin", "eps"]
        },
        "growth": {
            "name": "成长能力",
            "weight": 0.20,
            "metrics": ["revenue_growth", "profit_growth", "eps_growth"]
        },
        "valuation": {
            "name": "估值水平",
            "weight": 0.15,
            "metrics": ["pe", "pb", "ps", "dividend_yield"]
        },
        "financial_health": {
            "name": "财务健康",
            "weight": 0.15,
            "metrics": ["debt_ratio", "current_ratio", "quick_ratio"]
        },
        "technical": {
            "name": "技术走势",
            "weight": 0.10,
            "metrics": ["trend", "momentum", "volatility"]
        },
        "industry_outlook": {
            "name": "行业前景",
            "weight": 0.10,
            "metrics": ["industry_growth", "market_share"]
        },
        "institutional_attention": {
            "name": "机构关注",
            "weight": 0.05,
            "metrics": ["institutional_holding", "analyst_coverage"]
        }
    }
    
    def __init__(self):
        self.industry_scores = self._load_industry_scores()
    
    def _load_industry_scores(self) -> Dict[str, float]:
        """加载行业前景评分（简化版本）"""
        # 实际项目中应从外部数据源获取
        return {
            "银行": 60,
            "证券": 65,
            "保险": 62,
            "房地产": 45,
            "医药生物": 75,
            "电子": 70,
            "计算机": 72,
            "通信": 68,
            "食品饮料": 70,
            "家用电器": 68,
            "汽车": 60,
            "机械设备": 62,
            "化工": 58,
            "电气设备": 65,
            "新能源": 78,
            "半导体": 75,
            "人工智能": 80,
            "云计算": 76,
            "大数据": 72,
            "5G": 70
        }
    
    async def calculate_rating(
        self,
        code: str,
        name: str,
        financial_indicators: List[FinancialIndicator],
        valuation: Optional[ValuationData],
        kline_data: Optional[KLineData],
        realtime_price: Optional[RealtimePrice],
        industry: Optional[str]
    ) -> SevenDRating:
        """计算七维评分"""
        
        dimensions = []
        
        # 1. 盈利能力评分
        profitability_score = await self._score_profitability(financial_indicators)
        dimensions.append(profitability_score)
        
        # 2. 成长能力评分
        growth_score = await self._score_growth(financial_indicators)
        dimensions.append(growth_score)
        
        # 3. 估值水平评分
        valuation_score = await self._score_valuation(valuation)
        dimensions.append(valuation_score)
        
        # 4. 财务健康评分
        health_score = await self._score_financial_health(financial_indicators)
        dimensions.append(health_score)
        
        # 5. 技术走势评分
        technical_score = await self._score_technical(kline_data, realtime_price)
        dimensions.append(technical_score)
        
        # 6. 行业前景评分
        industry_score = await self._score_industry_outlook(industry)
        dimensions.append(industry_score)
        
        # 7. 机构关注评分（简化）
        institutional_score = await self._score_institutional_attention(financial_indicators)
        dimensions.append(institutional_score)
        
        # 计算总分
        total_score = sum(d.score * d.weight for d in dimensions)
        
        # 确定投资标签
        tag = self._determine_tag(total_score)
        
        # 生成时间维度判断
        short_term, mid_term, long_term = self._generate_term_judgments(
            total_score, dimensions, kline_data
        )
        
        return SevenDRating(
            total_score=round(total_score, 1),
            tag=tag,
            short_term=short_term,
            mid_term=mid_term,
            long_term=long_term,
            dimensions=dimensions,
            updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    
    async def _score_profitability(
        self, 
        financial_indicators: List[FinancialIndicator]
    ) -> DimensionScore:
        """评估盈利能力"""
        metrics = {}
        score = 50  # 默认中等
        
        if financial_indicators:
            latest = financial_indicators[0]
            
            # ROE评分 (最优区间 10-25%)
            if latest.roe_avg is not None:
                roe = latest.roe_avg
                if roe >= 20:
                    metrics["roe"] = {"value": roe, "rating": "优秀"}
                    score = max(score, 90)
                elif roe >= 15:
                    metrics["roe"] = {"value": roe, "rating": "良好"}
                    score = max(score, 80)
                elif roe >= 10:
                    metrics["roe"] = {"value": roe, "rating": "中等"}
                    score = max(score, 65)
                elif roe >= 5:
                    metrics["roe"] = {"value": roe, "rating": "较差"}
                    score = max(score, 45)
                else:
                    metrics["roe"] = {"value": roe, "rating": "差"}
            
            # 毛利率评分
            if latest.gross_margin is not None:
                gm = latest.gross_margin
                if gm >= 40:
                    metrics["gross_margin"] = {"value": gm, "rating": "优秀"}
                    score += 5
                elif gm >= 20:
                    metrics["gross_margin"] = {"value": gm, "rating": "良好"}
                    score += 3
                elif gm >= 10:
                    metrics["gross_margin"] = {"value": gm, "rating": "中等"}
                    score += 1
            
            # 净利率评分
            if latest.net_margin is not None:
                nm = latest.net_margin
                if nm >= 15:
                    metrics["net_margin"] = {"value": nm, "rating": "优秀"}
                    score += 5
                elif nm >= 8:
                    metrics["net_margin"] = {"value": nm, "rating": "良好"}
                    score += 3
                elif nm >= 3:
                    metrics["net_margin"] = {"value": nm, "rating": "中等"}
                    score += 1
        
        return DimensionScore(
            dimension="profitability",
            score=min(score, 100),
            weight=self.DIMENSIONS["profitability"]["weight"],
            description=self.DIMENSIONS["profitability"]["name"],
            metrics=metrics
        )
    
    async def _score_growth(
        self, 
        financial_indicators: List[FinancialIndicator]
    ) -> DimensionScore:
        """评估成长能力"""
        metrics = {}
        score = 50
        
        if len(financial_indicators) >= 2:
            latest = financial_indicators[0]
            previous = financial_indicators[1]
            
            # 营收增长
            if latest.total_revenue and previous.total_revenue:
                rev_growth = (latest.total_revenue - previous.total_revenue) / previous.total_revenue * 100
                if rev_growth >= 20:
                    metrics["revenue_growth"] = {"value": rev_growth, "rating": "高增长"}
                    score = max(score, 85)
                elif rev_growth >= 10:
                    metrics["revenue_growth"] = {"value": rev_growth, "rating": "稳定增长"}
                    score = max(score, 70)
                elif rev_growth >= 0:
                    metrics["revenue_growth"] = {"value": rev_growth, "rating": "低速增长"}
                    score = max(score, 55)
                else:
                    metrics["revenue_growth"] = {"value": rev_growth, "rating": "负增长"}
            
            # 利润增长
            if latest.net_profit and previous.net_profit:
                profit_growth = (latest.net_profit - previous.net_profit) / previous.net_profit * 100
                if profit_growth >= 30:
                    metrics["profit_growth"] = {"value": profit_growth, "rating": "高增长"}
                    score = max(score, 90)
                elif profit_growth >= 15:
                    metrics["profit_growth"] = {"value": profit_growth, "rating": "稳定增长"}
                    score = max(score, 75)
                elif profit_growth >= 0:
                    metrics["profit_growth"] = {"value": profit_growth, "rating": "低速增长"}
                    score = max(score, 55)
                else:
                    metrics["profit_growth"] = {"value": profit_growth, "rating": "负增长"}
        
        return DimensionScore(
            dimension="growth",
            score=min(score, 100),
            weight=self.DIMENSIONS["growth"]["weight"],
            description=self.DIMENSIONS["growth"]["name"],
            metrics=metrics
        )
    
    async def _score_valuation(
        self, 
        valuation: Optional[ValuationData]
    ) -> DimensionScore:
        """评估估值水平"""
        metrics = {}
        score = 50
        
        if valuation:
            # PE评分 (参考银行利率和风险溢价)
            if valuation.pe_ttm is not None:
                pe = valuation.pe_ttm
                if 10 <= pe <= 20:
                    metrics["pe"] = {"value": pe, "rating": "合理"}
                    score = max(score, 80)
                elif 20 < pe <= 30:
                    metrics["pe"] = {"value": pe, "rating": "略高"}
                    score = max(score, 65)
                elif 30 < pe <= 50:
                    metrics["pe"] = {"value": pe, "rating": "偏高"}
                    score = max(score, 45)
                elif pe > 50:
                    metrics["pe"] = {"value": pe, "rating": "高估"}
                    score = max(score, 25)
                elif pe < 10:
                    metrics["pe"] = {"value": pe, "rating": "低估"}
                    score = max(score, 90)
            
            # PB评分
            if valuation.pb is not None:
                pb = valuation.pb
                if pb <= 1:
                    metrics["pb"] = {"value": pb, "rating": "低估"}
                    score = max(score, 90)
                elif pb <= 3:
                    metrics["pb"] = {"value": pb, "rating": "合理"}
                    score = max(score, 75)
                elif pb <= 5:
                    metrics["pb"] = {"value": pb, "rating": "略高"}
                    score = max(score, 55)
                else:
                    metrics["pb"] = {"value": pb, "rating": "偏高"}
                    score = max(score, 35)
            
            # 股息率
            if valuation.dividend_ratio is not None:
                dy = valuation.dividend_ratio
                if dy >= 3:
                    metrics["dividend_yield"] = {"value": dy, "rating": "高息"}
                    score += 5
                elif dy >= 1.5:
                    metrics["dividend_yield"] = {"value": dy, "rating": "中等"}
                    score += 2
        
        return DimensionScore(
            dimension="valuation",
            score=min(score, 100),
            weight=self.DIMENSIONS["valuation"]["weight"],
            description=self.DIMENSIONS["valuation"]["name"],
            metrics=metrics
        )
    
    async def _score_financial_health(
        self, 
        financial_indicators: List[FinancialIndicator]
    ) -> DimensionScore:
        """评估财务健康"""
        metrics = {}
        score = 50
        
        if financial_indicators:
            latest = financial_indicators[0]
            
            # 资产负债率 (不同行业标准不同)
            if latest.debt_asset_ratio is not None:
                debt = latest.debt_asset_ratio
                if debt <= 40:
                    metrics["debt_ratio"] = {"value": debt, "rating": "低负债"}
                    score = max(score, 85)
                elif debt <= 60:
                    metrics["debt_ratio"] = {"value": debt, "rating": "中等"}
                    score = max(score, 65)
                elif debt <= 75:
                    metrics["debt_ratio"] = {"value": debt, "rating": "较高"}
                    score = max(score, 45)
                else:
                    metrics["debt_ratio"] = {"value": debt, "rating": "高负债"}
            
            # 流动比率
            if latest.current_ratio is not None:
                cr = latest.current_ratio
                if cr >= 2:
                    metrics["current_ratio"] = {"value": cr, "rating": "优秀"}
                    score = max(score, 85)
                elif cr >= 1.5:
                    metrics["current_ratio"] = {"value": cr, "rating": "良好"}
                    score = max(score, 70)
                elif cr >= 1:
                    metrics["current_ratio"] = {"value": cr, "rating": "及格"}
                    score = max(score, 55)
                else:
                    metrics["current_ratio"] = {"value": cr, "rating": "不足"}
        
        return DimensionScore(
            dimension="financial_health",
            score=min(score, 100),
            weight=self.DIMENSIONS["financial_health"]["weight"],
            description=self.DIMENSIONS["financial_health"]["name"],
            metrics=metrics
        )
    
    async def _score_technical(
        self,
        kline_data: Optional[KLineData],
        realtime_price: Optional[RealtimePrice]
    ) -> DimensionScore:
        """评估技术走势"""
        metrics = {}
        score = 50
        
        if kline_data and len(kline_data.closes) >= 60:
            closes = np.array(kline_data.closes[-60:])
            
            # 趋势评分
            ma20 = kline_data.ma20[-20:] if kline_data.ma20 else []
            ma60 = kline_data.ma60[-60:] if kline_data.ma60 else []
            
            if ma20 and ma60:
                latest_price = closes[-1]
                ma20_current = np.nanmean(ma20[-5:])
                ma60_current = np.nanmean(ma60[-5:])
                
                if latest_price > ma20_current > ma60_current:
                    metrics["trend"] = {"value": "上升趋势", "rating": "多头"}
                    score = max(score, 80)
                elif latest_price > ma20_current:
                    metrics["trend"] = {"value": "震荡偏强", "rating": "偏多"}
                    score = max(score, 65)
                elif latest_price < ma20_current < ma60_current:
                    metrics["trend"] = {"value": "下降趋势", "rating": "空头"}
                    score = max(score, 30)
                else:
                    metrics["trend"] = {"value": "震荡", "rating": "中性"}
            
            # 动量评分
            returns = (closes[-1] - closes[-20]) / closes[-20] * 100 if len(closes) >= 20 else 0
            if returns >= 15:
                metrics["momentum"] = {"value": returns, "rating": "强势"}
                score = max(score, 85)
            elif returns >= 5:
                metrics["momentum"] = {"value": returns, "rating": "偏强"}
                score = max(score, 70)
            elif returns >= -5:
                metrics["momentum"] = {"value": returns, "rating": "中性"}
                score = max(score, 55)
            else:
                metrics["momentum"] = {"value": returns, "rating": "偏弱"}
            
            # 波动率评分
            volatility = np.std(closes[-20:]) / np.mean(closes[-20:]) * 100
            if volatility <= 10:
                metrics["volatility"] = {"value": volatility, "rating": "低波动"}
                score = max(score, 75)
            elif volatility <= 20:
                metrics["volatility"] = {"value": volatility, "rating": "中等波动"}
                score = max(score, 60)
            else:
                metrics["volatility"] = {"value": volatility, "rating": "高波动"}
        
        return DimensionScore(
            dimension="technical",
            score=min(score, 100),
            weight=self.DIMENSIONS["technical"]["weight"],
            description=self.DIMENSIONS["technical"]["name"],
            metrics=metrics
        )
    
    async def _score_industry_outlook(
        self,
        industry: Optional[str]
    ) -> DimensionScore:
        """评估行业前景"""
        metrics = {}
        score = 50
        
        if industry:
            base_score = self.industry_scores.get(industry, 60)
            metrics["industry_name"] = {"value": industry, "rating": ""}
            score = max(score, base_score)
        else:
            metrics["industry_name"] = {"value": "未知", "rating": "数据不足"}
        
        return DimensionScore(
            dimension="industry_outlook",
            score=min(score, 100),
            weight=self.DIMENSIONS["industry_outlook"]["weight"],
            description=self.DIMENSIONS["industry_outlook"]["name"],
            metrics=metrics
        )
    
    async def _score_institutional_attention(
        self,
        financial_indicators: List[FinancialIndicator]
    ) -> DimensionScore:
        """评估机构关注（简化版本）"""
        metrics = {}
        score = 50
        
        # 实际应该从机构持仓数据获取
        metrics["institutional_holding"] = {"value": None, "rating": "数据不足"}
        metrics["analyst_coverage"] = {"value": None, "rating": "数据不足"}
        
        return DimensionScore(
            dimension="institutional_attention",
            score=score,
            weight=self.DIMENSIONS["institutional_attention"]["weight"],
            description=self.DIMENSIONS["institutional_attention"]["name"],
            metrics=metrics
        )
    
    def _determine_tag(self, total_score: float) -> str:
        """根据总分确定投资标签"""
        if total_score >= 75:
            return "重点关注"
        elif total_score >= 60:
            return "回调关注"
        elif total_score >= 45:
            return "中性观察"
        elif total_score >= 30:
            return "谨慎参与"
        else:
            return "暂不参与"
    
    def _generate_term_judgments(
        self,
        total_score: float,
        dimensions: List[DimensionScore],
        kline_data: Optional[KLineData]
    ) -> tuple:
        """生成短期、中期、长期判断"""
        # 提取各维度分数
        profitability = next((d.score for d in dimensions if d.dimension == "profitability"), 50)
        growth = next((d.score for d in dimensions if d.dimension == "growth"), 50)
        valuation = next((d.score for d in dimensions if d.dimension == "valuation"), 50)
        technical = next((d.score for d in dimensions if d.dimension == "technical"), 50)
        
        # 短期判断（技术面为主）
        if technical >= 70:
            short_term = "技术形态向好，短期或有表现"
        elif technical >= 55:
            short_term = "技术形态中性，短期方向不明"
        else:
            short_term = "技术形态偏弱，短期谨慎"
        
        # 中期判断（基本面+估值）
        if total_score >= 70 and valuation >= 60:
            mid_term = "基本面改善，估值合理，中期值得关注"
        elif total_score >= 55:
            mid_term = "基本面平稳，估值中性，中期可跟踪观察"
        else:
            mid_term = "基本面承压，估值偏高，中期风险需关注"
        
        # 长期判断（成长+行业）
        growth_score = next((d.score for d in dimensions if d.dimension == "growth"), 50)
        industry_score = next((d.score for d in dimensions if d.dimension == "industry_outlook"), 50)
        
        if growth_score >= 65 and industry_score >= 65:
            long_term = "行业前景广阔，成长性良好，长期具备配置价值"
        elif growth_score >= 50:
            long_term = "成长性一般，长期需关注行业变化"
        else:
            long_term = "成长性存疑，长期配置需谨慎"
        
        return short_term, mid_term, long_term


# 全局实例
rating_engine = RatingEngine()
