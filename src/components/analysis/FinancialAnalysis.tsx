'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import type { FinancialIndicator } from '@/types/stock';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

interface FinancialAnalysisProps {
  data: FinancialIndicator[];
  loading?: boolean;
}

// 格式化数字
const formatNumber = (num: number | undefined, suffix: string = '') => {
  if (num === undefined || num === null) return '--';
  if (suffix === '%') return `${num.toFixed(2)}%`;
  if (suffix === '亿') return `${num.toFixed(2)}亿`;
  return `${num.toFixed(2)}${suffix}`;
};

export function FinancialAnalysis({ data, loading }: FinancialAnalysisProps) {
  if (loading) {
    return (
      <Card className="bg-slate-800/50 border-slate-700">
        <CardHeader>
          <CardTitle className="text-lg text-slate-100">财务分析</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[300px] flex items-center justify-center">
            <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!data || data.length === 0) {
    return (
      <Card className="bg-slate-800/50 border-slate-700">
        <CardHeader>
          <CardTitle className="text-lg text-slate-100">财务分析</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[200px] flex items-center justify-center text-slate-400">
            暂无财务数据
          </div>
        </CardContent>
      </Card>
    );
  }

  // 准备图表数据
  const chartData = [...data].reverse().map((item) => ({
    date: item.date.substring(0, 7),
    roe: item.roe_avg,
    grossMargin: item.gross_margin,
    netMargin: item.net_margin,
    revenue: item.total_revenue,
    profit: item.net_profit
  }));

  // 财务指标表格数据（取最新4期）
  const tableData = data.slice(0, 4);

  return (
    <Card className="bg-slate-800/50 border-slate-700">
      <CardHeader>
        <CardTitle className="text-lg text-slate-100">财务分析</CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="profitability" className="space-y-4">
          <TabsList className="bg-slate-900">
            <TabsTrigger value="profitability" className="data-[state=active]:bg-blue-600">
              盈利能力
            </TabsTrigger>
            <TabsTrigger value="growth" className="data-[state=active]:bg-blue-600">
              成长能力
            </TabsTrigger>
            <TabsTrigger value="debt" className="data-[state=active]:bg-blue-600">
              偿债能力
            </TabsTrigger>
            <TabsTrigger value="turnover" className="data-[state=active]:bg-blue-600">
              运营能力
            </TabsTrigger>
          </TabsList>

          {/* 盈利能力 */}
          <TabsContent value="profitability" className="space-y-4">
            <div className="h-[250px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis dataKey="date" stroke="#64748b" fontSize={12} />
                  <YAxis stroke="#64748b" fontSize={12} tickFormatter={(v) => `${v}%`} />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'rgba(30, 41, 59, 0.95)', 
                      border: '1px solid #475569',
                      borderRadius: '8px'
                    }}
                    labelStyle={{ color: '#f8fafc' }}
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="roe" 
                    name="ROE(%)" 
                    stroke="#3b82f6" 
                    strokeWidth={2}
                    dot={{ fill: '#3b82f6', r: 3 }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="grossMargin" 
                    name="毛利率(%)" 
                    stroke="#22c55e" 
                    strokeWidth={2}
                    dot={{ fill: '#22c55e', r: 3 }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="netMargin" 
                    name="净利率(%)" 
                    stroke="#f97316" 
                    strokeWidth={2}
                    dot={{ fill: '#f97316', r: 3 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <div className="grid grid-cols-4 gap-4">
              {tableData.map((item, idx) => (
                <div key={idx} className="bg-slate-900/50 rounded-lg p-3">
                  <div className="text-xs text-slate-500 mb-1">{item.date}</div>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-400">ROE</span>
                      <span className="text-slate-200">{formatNumber(item.roe_avg, '%')}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">毛利率</span>
                      <span className="text-slate-200">{formatNumber(item.gross_margin, '%')}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">净利率</span>
                      <span className="text-slate-200">{formatNumber(item.net_margin, '%')}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </TabsContent>

          {/* 成长能力 */}
          <TabsContent value="growth" className="space-y-4">
            <div className="h-[250px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis dataKey="date" stroke="#64748b" fontSize={12} />
                  <YAxis stroke="#64748b" fontSize={12} tickFormatter={(v) => `${v}亿`} />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'rgba(30, 41, 59, 0.95)', 
                      border: '1px solid #475569',
                      borderRadius: '8px'
                    }}
                    labelStyle={{ color: '#f8fafc' }}
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="revenue" 
                    name="营收(亿)" 
                    stroke="#3b82f6" 
                    strokeWidth={2}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="profit" 
                    name="净利润(亿)" 
                    stroke="#22c55e" 
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <div className="grid grid-cols-4 gap-4">
              {tableData.map((item, idx) => (
                <div key={idx} className="bg-slate-900/50 rounded-lg p-3">
                  <div className="text-xs text-slate-500 mb-1">{item.date}</div>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-400">营收</span>
                      <span className="text-slate-200">{formatNumber(item.total_revenue, '亿')}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">净利润</span>
                      <span className="text-slate-200">{formatNumber(item.net_profit, '亿')}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">EPS</span>
                      <span className="text-slate-200">{formatNumber(item.basic_eps)}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </TabsContent>

          {/* 偿债能力 */}
          <TabsContent value="debt" className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              {tableData.map((item, idx) => (
                <div key={idx} className="bg-slate-900/50 rounded-lg p-4">
                  <div className="text-xs text-slate-500 mb-2">{item.date}</div>
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    <div>
                      <div className="text-slate-400">资产负债率</div>
                      <div className={`text-lg font-semibold ${
                        item.debt_asset_ratio && item.debt_asset_ratio > 70 
                          ? 'text-red-400' 
                          : 'text-slate-200'
                      }`}>
                        {formatNumber(item.debt_asset_ratio, '%')}
                      </div>
                    </div>
                    <div>
                      <div className="text-slate-400">流动比率</div>
                      <div className={`text-lg font-semibold ${
                        item.current_ratio && item.current_ratio < 1 
                          ? 'text-yellow-400' 
                          : 'text-slate-200'
                      }`}>
                        {formatNumber(item.current_ratio)}
                      </div>
                    </div>
                    <div>
                      <div className="text-slate-400">速动比率</div>
                      <div className="text-lg font-semibold text-slate-200">
                        {formatNumber(item.quick_ratio)}
                      </div>
                    </div>
                    <div>
                      <div className="text-slate-400">现金比率</div>
                      <div className="text-lg font-semibold text-slate-200">
                        {formatNumber(item.cash_ratio, '%')}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </TabsContent>

          {/* 运营能力 */}
          <TabsContent value="turnover" className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              {tableData.map((item, idx) => (
                <div key={idx} className="bg-slate-900/50 rounded-lg p-4">
                  <div className="text-xs text-slate-500 mb-2">{item.date}</div>
                  <div className="grid grid-cols-3 gap-3 text-sm">
                    <div>
                      <div className="text-slate-400">总资产周转</div>
                      <div className="text-lg font-semibold text-slate-200">
                        {formatNumber(item.total_asset_turnover)}
                      </div>
                    </div>
                    <div>
                      <div className="text-slate-400">存货周转</div>
                      <div className="text-lg font-semibold text-slate-200">
                        {formatNumber(item.inventory_turnover)}
                      </div>
                    </div>
                    <div>
                      <div className="text-slate-400">应收账款周转</div>
                      <div className="text-lg font-semibold text-slate-200">
                        {formatNumber(item.receivables_turnover)}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}
