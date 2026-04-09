"""
AKShare 数据服务
官网: https://akshare.akun.com
Python库形式提供，数据种类丰富
"""

import akshare as ak
import pandas as pd
import logging
from typing import List, Optional
from datetime import datetime, timedelta

from .base import BaseDataService, register_service
from ..models.schemas import (
    SearchResult, RealtimePrice, KLineData, 
    FinancialIndicator, ValuationData, StockBasicInfo
)

logger = logging.getLogger(__name__)


class AKShareService(BaseDataService):
    """AKShare 数据服务实现"""
    
    @property
    def name(self) -> str:
        return "akshare"
    
    @property
    def priority(self) -> int:
        return 3  # 备选数据源
    
    async def search_stocks(self, keyword: str) -> List[SearchResult]:
        """搜索股票"""
        results = []
        
        try:
            # 使用AKShare的A股列表接口
            df = ak.stock_info_a_code_name()
            
            # 搜索匹配
            mask = (
                df['code'].str.contains(keyword, na=False) |
                df['name'].str.contains(keyword, na=False)
            )
            matched = df[mask].head(20)
            
            for _, row in matched.iterrows():
                code = str(row['code'])
                exchange = 'SH' if code.startswith('6') else 'SZ'
                
                results.append(SearchResult(
                    code=code,
                    name=row['name'],
                    exchange=exchange,
                    market='主板',  # AKShare不直接提供板块信息
                    list_status='上市'
                ))
        except Exception as e:
            logger.error(f"AKShare search error: {e}")
        
        return results
    
    async def get_realtime_price(self, codes: List[str]) -> List[RealtimePrice]:
        """获取实时价格 - 使用AKShare实时行情接口"""
        results = []
        
        try:
            # 批量获取实时行情
            if len(codes) == 1:
                df = ak.stock_zh_a_spot_em()
            else:
                df = ak.stock_zh_a_spot_em()
            
            # 过滤目标股票
            df_filtered = df[df['代码'].isin(codes)]
            
            for _, row in df_filtered.iterrows():
                results.append(RealtimePrice(
                    code=str(row['代码']),
                    name=str(row['名称']),
                    open=float(row['今开']) if pd.notna(row['今开']) else 0,
                    high=float(row['最高']) if pd.notna(row['最高']) else 0,
                    low=float(row['最低']) if pd.notna(row['最低']) else 0,
                    close=float(row['最新价']) if pd.notna(row['最新价']) else 0,
                    pre_close=float(row['昨收']) if pd.notna(row['昨收']) else 0,
                    volume=float(row['成交量']) if pd.notna(row['成交量']) else 0,
                    amount=float(row['成交额']) if pd.notna(row['成交额']) else 0,
                    change_amount=float(row['涨跌额']) if pd.notna(row['涨跌额']) else 0,
                    change_pct=float(row['涨跌幅']) if pd.notna(row['涨跌幅']) else 0,
                    pe_ttm=float(row['市盈率-动态']) if pd.notna(row.get('市盈率-动态')) else None,
                    pb=float(row['市净率']) if pd.notna(row.get('市净率')) else None,
                    market_cap=float(row['总市值']) if pd.notna(row.get('总市值')) else None,
                    float_market_cap=float(row['流通市值']) if pd.notna(row.get('流通市值')) else None
                ))
        except Exception as e:
            logger.error(f"AKShare realtime price error: {e}")
        
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
            # 默认时间范围
            if not end_date:
                end_date = datetime.now().strftime('%Y%m%d')
            if not start_date:
                start_date = (datetime.now() - timedelta(days=730)).strftime('%Y%m%d')
            
            # AKShare的K线接口
            adjust_map = {"qfq": "qfq", "hfq": "hfq", "none": "None"}
            adj = adjust_map.get(adjust, "qfq")
            
            df = ak.stock_zh_a_hist(
                symbol=code,
                period=period,
                start_date=start_date,
                end_date=end_date,
                adjust=adj
            )
            
            if df is not None and not df.empty:
                # 转换日期格式
                df['日期'] = pd.to_datetime(df['日期']).dt.strftime('%Y-%m-%d')
                
                # 计算均线
                closes = pd.to_numeric(df['收盘'], errors='coerce')
                
                return KLineData(
                    dates=df['日期'].tolist(),
                    opens=pd.to_numeric(df['开盘'], errors='coerce').tolist(),
                    highs=pd.to_numeric(df['最高'], errors='coerce').tolist(),
                    lows=pd.to_numeric(df['最低'], errors='coerce').tolist(),
                    closes=closes.tolist(),
                    volumes=pd.to_numeric(df['成交量'], errors='coerce').tolist(),
                    amounts=pd.to_numeric(df['成交额'], errors='coerce').tolist(),
                    ma5=closes.rolling(5).mean().tolist(),
                    ma10=closes.rolling(10).mean().tolist(),
                    ma20=closes.rolling(20).mean().tolist(),
                    ma60=closes.rolling(60).mean().tolist(),
                    period=period,
                    adjust=adjust
                )
        except Exception as e:
            logger.error(f"AKShare kline error: {e}")
        
        return None
    
    async def get_stock_basic_info(self, code: str) -> Optional[StockBasicInfo]:
        """获取股票基本信息"""
        try:
            df = ak.stock_individual_info_em(symbol=code)
            
            if df is not None and not df.empty:
                info_dict = dict(zip(df['item'], df['value']))
                
                return StockBasicInfo(
                    code=code,
                    name=info_dict.get('股票简称', ''),
                    full_name=info_dict.get('公司全称'),
                    exchange='SH' if code.startswith('6') else 'SZ',
                    industry=info_dict.get('行业'),
                    market=info_dict.get('上市时间'),
                    list_date=info_dict.get('上市日期')
                )
        except Exception as e:
            logger.error(f"AKShare basic info error: {e}")
        
        return None
    
    async def get_financial_indicators(
        self, 
        code: str, 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[FinancialIndicator]:
        """获取财务指标"""
        results = []
        
        try:
            # 使用AKShare的财务指标接口
            df = ak.stock_financial_analysis_indicator(
                symbol=code,
                start_year=start_date[:4] if start_date else None,
                end_year=end_date[:4] if end_date else None
            )
            
            if df is not None and not df.empty:
                for _, row in df.iterrows():
                    results.append(FinancialIndicator(
                        date=str(row.get('日期', '')),
                        code=code,
                        roe_avg=float(row['净资产收益率(%)']) if pd.notna(row.get('净资产收益率(%)')) else None,
                        gross_margin=float(row['销售毛利率(%)']) if pd.notna(row.get('销售毛利率(%)')) else None,
                        net_margin=float(row['销售净利率(%)']) if pd.notna(row.get('销售净利率(%)')) else None,
                        debt_asset_ratio=float(row['资产负债率(%)']) if pd.notna(row.get('资产负债率(%)')) else None,
                        total_revenue=float(row['营业总收入(亿元)']) if pd.notna(row.get('营业总收入(亿元)')) else None,
                        net_profit=float(row['净利润(亿元)']) if pd.notna(row.get('净利润(亿元)')) else None,
                        basic_eps=float(row['基本每股收益(元)']) if pd.notna(row.get('基本每股收益(元)')) else None
                    ))
        except Exception as e:
            logger.error(f"AKShare financial indicators error: {e}")
        
        return results
    
    async def get_valuation_data(self, code: str) -> Optional[ValuationData]:
        """获取估值数据"""
        try:
            # 使用AKShare的历史PE/PB数据
            df_pe = ak.stock_a_pe_lrb(symbol=code)
            
            # 这是一个简化的实现，实际应该结合多个指标计算
            return ValuationData(
                code=code,
                pe_history_percentile=50,  # 需要历史数据计算
                pb_history_percentile=50
            )
        except Exception as e:
            logger.error(f"AKShare valuation error: {e}")
        
        return None
    
    async def is_available(self) -> bool:
        """检查服务是否可用"""
        try:
            # 简单检查AKShare是否可用
            ak.stock_info_a_code_name()
            return True
        except:
            return False


# 注册服务
akshare_service = AKShareService()
register_service(akshare_service)
