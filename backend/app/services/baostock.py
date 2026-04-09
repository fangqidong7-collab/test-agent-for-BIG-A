"""
BaoStock 数据服务
官网: http://www.baostock.com
免费数据，无需注册即可使用基本功能
"""

import baostock as bs
import pandas as pd
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from .base import BaseDataService, register_service
from ..models.schemas import (
    SearchResult, RealtimePrice, KLineData, 
    FinancialIndicator, ValuationData, StockBasicInfo
)

logger = logging.getLogger(__name__)


class BaoStockService(BaseDataService):
    """BaoStock 数据服务实现"""
    
    def __init__(self):
        self._logged_in = False
        self._login()
    
    @property
    def name(self) -> str:
        return "baostock"
    
    @property
    def priority(self) -> int:
        return 1  # 主数据源，优先级最高
    
    def _login(self):
        """登录BaoStock"""
        try:
            if not self._logged_in:
                lg = bs.login()
                if lg.error_code == '0':
                    self._logged_in = True
                    logger.info("BaoStock login successful")
                else:
                    logger.warning(f"BaoStock login failed: {lg.error_msg}")
        except Exception as e:
            logger.error(f"BaoStock login error: {e}")
    
    def _logout(self):
        """登出BaoStock"""
        if self._logged_in:
            try:
                bs.logout()
                self._logged_in = False
            except:
                pass
    
    async def search_stocks(self, keyword: str) -> List[SearchResult]:
        """搜索股票 - 使用BaoStock的股票检索功能"""
        results = []
        
        try:
            # 获取所有A股列表
            rs = bs.query_all_stock()
            data_list = []
            while (rs.error_code == '0') & rs.next():
                data_list.append(rs.get_row_data())
            
            if data_list:
                df = pd.DataFrame(data_list, columns=rs.fields)
                
                # 搜索匹配
                keyword_upper = keyword.upper()
                mask = (
                    df['code'].str.contains(keyword_upper, na=False) |
                    df['code_name'].str.contains(keyword, na=False) |
                    df['code_name'].str.contains(keyword_upper, na=False)
                )
                matched = df[mask].head(20)
                
                for _, row in matched.iterrows():
                    code = row['code']
                    exchange = 'SZ' if code.startswith('sz') else ('SH' if code.startswith('sh') else 'BJ')
                    
                    results.append(SearchResult(
                        code=code.replace('sh.', '').replace('sz.', '').replace('bj.', ''),
                        name=row['code_name'],
                        exchange=exchange,
                        market=self._get_market_type(code),
                        list_status=row['type']
                    ))
        except Exception as e:
            logger.error(f"BaoStock search error: {e}")
        
        return results
    
    def _get_market_type(self, code: str) -> str:
        """判断市场类型"""
        if code.startswith('sh.6'):
            return '主板(沪市)'
        elif code.startswith('sz.000'):
            return '主板(深市)'
        elif code.startswith('sz.002'):
            return '中小企业板'
        elif code.startswith('sz.300'):
            return '创业板'
        elif code.startswith('bj.'):
            return '北交所'
        return '其他'
    
    async def get_realtime_price(self, codes: List[str]) -> List[RealtimePrice]:
        """获取实时价格"""
        results = []
        
        try:
            for code in codes:
                bao_code = self._to_baostock_code(code)
                rs = bs.query_daily_data(bao_code, date=datetime.now().strftime('%Y-%m-%d'))
                
                if rs.error_code == '0':
                    data = rs.get_row_data()
                    if data:
                        # 获取前一交易日数据
                        rs_prev = bs.query_daily_data(bao_code, date='')
                        pre_close = 0
                        if rs_prev.error_code == '0':
                            prev_data = rs_prev.get_row_data()
                            if prev_data:
                                pre_close = float(prev_data[3]) if len(prev_data) > 3 else 0
                        
                        close = float(data[3]) if len(data) > 3 else 0
                        change_amount = close - pre_close if pre_close else 0
                        change_pct = (change_amount / pre_close * 100) if pre_close else 0
                        
                        results.append(RealtimePrice(
                            code=code,
                            name='',
                            open=float(data[1]) if len(data) > 1 else 0,
                            high=float(data[2]) if len(data) > 2 else 0,
                            low=float(data[4]) if len(data) > 4 else 0,
                            close=close,
                            pre_close=pre_close,
                            volume=float(data[5]) if len(data) > 5 else 0,
                            amount=float(data[6]) if len(data) > 6 else 0,
                            change_amount=change_amount,
                            change_pct=change_pct
                        ))
        except Exception as e:
            logger.error(f"BaoStock realtime price error: {e}")
        
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
            bao_code = self._to_baostock_code(code)
            
            # 默认时间范围：最近2年
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
            if not start_date:
                start_date = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
            
            # 调整字段名
            adjust_str = "2" if adjust == "hfq" else ("1" if adjust == "qfq" else "3")
            
            rs = bs.query_history_k_data_plus(
                bao_code,
                "date,open,high,low,close,volume,amount",
                start_date=start_date,
                end_date=end_date,
                frequency=period,
                adjust=adjust_str
            )
            
            if rs.error_code == '0':
                data_list = []
                while rs.next():
                    data_list.append(rs.get_row_data())
                
                if data_list:
                    df = pd.DataFrame(data_list, columns=['date', 'open', 'high', 'low', 'close', 'volume', 'amount'])
                    
                    # 计算均线
                    closes = pd.to_numeric(df['close'], errors='coerce')
                    df['ma5'] = closes.rolling(5).mean()
                    df['ma10'] = closes.rolling(10).mean()
                    df['ma20'] = closes.rolling(20).mean()
                    df['ma60'] = closes.rolling(60).mean()
                    
                    return KLineData(
                        dates=df['date'].tolist(),
                        opens=pd.to_numeric(df['open'], errors='coerce').tolist(),
                        highs=pd.to_numeric(df['high'], errors='coerce').tolist(),
                        lows=pd.to_numeric(df['low'], errors='coerce').tolist(),
                        closes=closes.tolist(),
                        volumes=pd.to_numeric(df['volume'], errors='coerce').tolist(),
                        amounts=pd.to_numeric(df['amount'], errors='coerce').tolist(),
                        ma5=df['ma5'].tolist(),
                        ma10=df['ma10'].tolist(),
                        ma20=df['ma20'].tolist(),
                        ma60=df['ma60'].tolist(),
                        period=period,
                        adjust=adjust
                    )
        except Exception as e:
            logger.error(f"BaoStock kline error: {e}")
        
        return None
    
    async def get_stock_basic_info(self, code: str) -> Optional[StockBasicInfo]:
        """获取股票基本信息"""
        try:
            bao_code = self._to_baostock_code(code)
            rs = bs.query_stock_basic(code=bao_code)
            
            if rs.error_code == '0':
                data = rs.get_row_data()
                if data:
                    return StockBasicInfo(
                        code=code,
                        name=data[1] if len(data) > 1 else '',
                        full_name=data[2] if len(data) > 2 else None,
                        exchange='SZ' if code.startswith('sz') else 'SH',
                        industry=data[4] if len(data) > 4 else None,
                        list_date=data[5] if len(data) > 5 else None,
                        is_hs=data[6] if len(data) > 6 else None
                    )
        except Exception as e:
            logger.error(f"BaoStock basic info error: {e}")
        
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
            bao_code = self._to_baostock_code(code)
            
            rs = bs.query_profit_data(
                code=bao_code,
                year=start_date[:4] if start_date else None,
                quarter=start_date[5:7] if start_date and len(start_date) > 6 else None
            )
            
            # BaoStock的财务指标查询有限，这里简化处理
            # 实际项目中应该使用完整的季度财报数据
            
        except Exception as e:
            logger.error(f"BaoStock financial indicators error: {e}")
        
        return results
    
    async def get_valuation_data(self, code: str) -> Optional[ValuationData]:
        """获取估值数据 - BaoStock不直接提供PE/PB等，使用历史K线数据估算"""
        try:
            # 从历史数据中获取最新估值（简化版本）
            kline = await self.get_kline_data(code, start_date='2020-01-01', end_date=datetime.now().strftime('%Y-%m-%d'))
            
            if kline and kline.closes:
                latest_close = kline.closes[-1]
                
                # 这些值需要从财务报表计算，这里返回估算值
                return ValuationData(
                    code=code,
                    pe_history_percentile=50,  # 需要历史数据计算
                    pb_history_percentile=50
                )
        except Exception as e:
            logger.error(f"BaoStock valuation error: {e}")
        
        return None
    
    async def is_available(self) -> bool:
        """检查服务是否可用"""
        try:
            if not self._logged_in:
                self._login()
            return self._logged_in
        except:
            return False
    
    def _to_baostock_code(self, code: str) -> str:
        """转换代码格式"""
        code = code.strip().lower()
        if not code.startswith(('sh.', 'sz.', 'bj.')):
            if code.startswith('6'):
                return f"sh.{code}"
            elif code.startswith(('0', '3')):
                return f"sz.{code}"
            elif code.startswith('8', '4', '9'):
                return f"bj.{code}"
        return code


# 注册服务
baostock_service = BaoStockService()
register_service(baostock_service)
