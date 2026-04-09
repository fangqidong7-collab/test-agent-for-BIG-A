// 股票分析平台类型定义

export interface StockBasicInfo {
  code: string;
  name: string;
  full_name?: string;
  exchange: string;
  industry?: string;
  market?: string;
  list_date?: string;
  is_hs?: string;
}

export interface RealtimePrice {
  code: string;
  name: string;
  open: number;
  high: number;
  low: number;
  close: number;
  pre_close: number;
  volume: number;
  amount: number;
  change_amount: number;
  change_pct: number;
  turnover?: number;
  amplitude?: number;
  pe_ttm?: number;
  pb?: number;
  ps_ttm?: number;
  market_cap?: number;
  float_market_cap?: number;
}

export interface KLineData {
  dates: string[];
  opens: number[];
  highs: number[];
  lows: number[];
  closes: number[];
  volumes: number[];
  amounts?: number[];
  ma5?: number[];
  ma10?: number[];
  ma20?: number[];
  ma60?: number[];
  period: string;
  adjust: string;
}

export interface FinancialIndicator {
  date: string;
  code: string;
  roe_avg?: number;
  gross_margin?: number;
  net_margin?: number;
  debt_asset_ratio?: number;
  current_ratio?: number;
  quick_ratio?: number;
  total_revenue?: number;
  main_business_profit?: number;
  operating_profit?: number;
  investment_income?: number;
  non_operating_profit?: number;
  total_profit?: number;
  net_profit?: number;
  net_profit_atsopc?: number;
  diluted_roe?: number;
  weighted_roe?: number;
  basic_eps?: number;
  diluted_eps?: number;
  total_asset_turnover?: number;
  inventory_turnover?: number;
  receivables_turnover?: number;
  eps_yoy?: number;
  bvps?: number;
  operating_cash_flow_per_share?: number;
  cash_ratio?: number;
  cash_flow_ratio?: number;
  asset_to_liability?: number;
  property_ratio?: number;
  net_asset_value_per_share?: number;
}

export interface ValuationData {
  code: string;
  pe_ttm?: number;
  pe_lyr?: number;
  pb?: number;
  ps_ttm?: number;
  ps_lyr?: number;
  pcf_ncfttm?: number;
  pcf_ocfttm?: number;
  ev_ebitda?: number;
  dividend_ratio?: number;
  dividend_yield2?: number;
  pe_history_percentile?: number;
  pb_history_percentile?: number;
  industry_avg_pe?: number;
  industry_median_pe?: number;
}

export interface DimensionScore {
  dimension: string;
  score: number;
  weight: number;
  description: string;
  metrics: Record<string, any>;
}

export interface SevenDRating {
  total_score: number;
  tag: string;
  short_term: string;
  mid_term: string;
  long_term: string;
  dimensions: DimensionScore[];
  updated_at: string;
}

export interface ScenarioAnalysis {
  current_price: number;
  currency: string;
  scenarios: {
    optimistic?: Scenario;
    neutral?: Scenario;
    pessimistic?: Scenario;
  };
  summary: string;
}

export interface Scenario {
  probability: number;
  target_price: number;
  upside_pct?: number;
  downside_pct?: number;
  conditions: string[];
  time_horizon: string;
  description: string;
}

export interface Catalyst {
  type: string;
  title: string;
  description: string;
  source: string;
  date: string;
}

export interface StockAnalysis {
  basic_info: StockBasicInfo;
  realtime_price?: RealtimePrice;
  kline_data?: KLineData;
  financial_indicators: FinancialIndicator[];
  valuation?: ValuationData;
  seven_d_rating?: SevenDRating;
  scenario_analysis?: ScenarioAnalysis;
  catalysts: Catalyst[];
  industry_tags: string[];
  concept_tags: string[];
  data_source: string;
  data_timestamp: string;
}

export interface SearchResult {
  code: string;
  name: string;
  full_name?: string;
  exchange: string;
  market?: string;
  list_status: string;
}

export interface SearchResponse {
  stocks: SearchResult[];
  total: number;
  query: string;
}

// 投资标签定义
export const TAG_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  '重点关注': { bg: 'bg-green-900/50', text: 'text-green-400', border: 'border-green-500' },
  '回调关注': { bg: 'bg-blue-900/50', text: 'text-blue-400', border: 'border-blue-500' },
  '中性观察': { bg: 'bg-yellow-900/50', text: 'text-yellow-400', border: 'border-yellow-500' },
  '谨慎参与': { bg: 'bg-orange-900/50', text: 'text-orange-400', border: 'border-orange-500' },
  '暂不参与': { bg: 'bg-red-900/50', text: 'text-red-400', border: 'border-red-500' }
};
