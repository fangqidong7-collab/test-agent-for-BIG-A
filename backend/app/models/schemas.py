from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class StockBasicInfo(BaseModel):
    """股票基本信息"""
    code: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票简称")
    full_name: Optional[str] = Field(None, description="公司全名")
    exchange: str = Field(..., description="交易所: SZ/SH/BJ")
    industry: Optional[str] = Field(None, description="所属行业")
    market: Optional[str] = Field(None, description="市场板块")
    list_date: Optional[str] = Field(None, description="上市日期")
    is_hs: Optional[str] = Field(None, description="是否沪深港通: N/H/S")


class RealtimePrice(BaseModel):
    """实时价格数据"""
    code: str
    name: str
    open: float
    high: float
    low: float
    close: float
    pre_close: float
    volume: float
    amount: float
    change_pct: float
    change_amount: float
    turnover: Optional[float] = None
    amplitude: Optional[float] = None
    pe_ttm: Optional[float] = None
    pb: Optional[float] = None
    ps_ttm: Optional[float] = None
    market_cap: Optional[float] = None  # 市值(亿元)
    float_market_cap: Optional[float] = None  # 流通市值(亿元)


class KLineData(BaseModel):
    """K线数据"""
    dates: List[str]
    opens: List[float]
    highs: List[float]
    lows: List[float]
    closes: List[float]
    volumes: List[float]
    amounts: Optional[List[float]] = None
    ma5: Optional[List[float]] = None
    ma10: Optional[List[float]] = None
    ma20: Optional[List[float]] = None
    ma60: Optional[List[float]] = None
    period: str = "daily"  # daily, weekly, monthly
    adjust: str = "qfq"    # qfq, hfq, none


class FinancialIndicator(BaseModel):
    """财务指标"""
    date: str
    code: str
    roe_avg: Optional[float] = None  # 净资产收益率(%)
    gross_margin: Optional[float] = None  # 销售毛利率(%)
    net_margin: Optional[float] = None  # 销售净利率(%)
    debt_asset_ratio: Optional[float] = None  # 资产负债率(%)
    current_ratio: Optional[float] = None  # 流动比率
    quick_ratio: Optional[float] = None  # 速动比率
    total_revenue: Optional[float] = None  # 营业总收入(亿元)
    main_business_profit: Optional[float] = None  # 主营业务利润(亿元)
    operating_profit: Optional[float] = None  # 营业利润(亿元)
    investment_income: Optional[float] = None  # 投资收益(亿元)
    non_operating_profit: Optional[float] = None  # 营业外收支净额(亿元)
    total_profit: Optional[float] = None  # 利润总额(亿元)
    net_profit: Optional[float] = None  # 净利润(亿元)
    net_profit_atsopc: Optional[float] = None  # 归属母公司净利润(亿元)
    diluted_roe: Optional[float] = None  # 稀释净资产收益率(%)
    weighted_roe: Optional[float] = None  # 加权净资产收益率(%)
    basic_eps: Optional[float] = None  # 基本每股收益(元)
    diluted_eps: Optional[float] = None  # 稀释每股收益(元)
    total_asset_turnover: Optional[float] = None  # 总资产周转率(次)
    inventory_turnover: Optional[float] = None  # 存货周转率(次)
    receivables_turnover: Optional[float] = None  # 应收账款周转率(次)
    eps_yoy: Optional[float] = None  # 每股收益同比增长率(%)
    bvps: Optional[float] = None  # 每股净资产(元)
    operating_cash_flow_per_share: Optional[float] = None  # 每股经营现金流(元)
    cash_ratio: Optional[float] = None  # 现金比率(%)
    cash_flow_ratio: Optional[float] = None  # 经营现金净流量与负债比率(%)
    asset_to_liability: Optional[float] = None  # 资产与负债比率(%)
    property_ratio: Optional[float] = None  # 产权比率(%)
    net_asset_value_per_share: Optional[float] = None  # 每股净资产调整(元)


class ValuationData(BaseModel):
    """估值数据"""
    code: str
    pe_ttm: Optional[float] = None  # 市盈率TTM
    pe_lyr: Optional[float] = None  # 市盈率LYR
    pb: Optional[float] = None  # 市净率
    ps_ttm: Optional[float] = None  # 市销率TTM
    ps_lyr: Optional[float] = None  # 市销率LYR
    pcf_ncfttm: Optional[float] = None  # 市现率NCF
    pcf_ocfttm: Optional[float] = None  # 经营现金流市价
    ev_ebitda: Optional[float] = None  # 企业价值/EBITDA
    dividend_ratio: Optional[float] = None  # 股息率(%)
    dividend_yield2: Optional[float] = None  # 股息率(近一年)(%)
    pe_history_percentile: Optional[float] = None  # PE历史分位
    pb_history_percentile: Optional[float] = None  # PB历史分位
    industry_avg_pe: Optional[float] = None  # 行业平均PE
    industry_median_pe: Optional[float] = None  # 行业中位数PE


class DimensionScore(BaseModel):
    """单维度评分"""
    dimension: str
    score: float  # 0-100
    weight: float  # 权重
    description: str
    metrics: Dict[str, Any]


class SevenDRating(BaseModel):
    """七维评分"""
    total_score: float  # 总分 0-100
    tag: str  # 投资标签
    short_term: str  # 短期判断
    mid_term: str  # 中期判断
    long_term: str  # 长期判断
    dimensions: List[DimensionScore]
    updated_at: str


class ScenarioAnalysis(BaseModel):
    """情景分析"""
    current_price: float
    currency: str = "CNY"
    scenarios: Dict[str, Dict[str, Any]]  # {optimistic, neutral, pessimistic}
    summary: str


class Catalyst(BaseModel):
    """催化剂"""
    type: str  # positive, negative
    title: str
    description: str
    source: str
    date: str


class StockAnalysis(BaseModel):
    """完整股票分析"""
    basic_info: StockBasicInfo
    realtime_price: Optional[RealtimePrice] = None
    kline_data: Optional[KLineData] = None
    financial_indicators: List[FinancialIndicator] = []
    valuation: Optional[ValuationData] = None
    seven_d_rating: Optional[SevenDRating] = None
    scenario_analysis: Optional[ScenarioAnalysis] = None
    catalysts: List[Catalyst] = []
    industry_tags: List[str] = []
    concept_tags: List[str] = []
    data_source: str
    data_timestamp: str


class SearchResult(BaseModel):
    """搜索结果"""
    code: str
    name: str
    full_name: Optional[str] = None
    exchange: str
    market: Optional[str] = None
    list_status: str = "上市"


class SearchResponse(BaseModel):
    """搜索响应"""
    stocks: List[SearchResult]
    total: int
    query: str
