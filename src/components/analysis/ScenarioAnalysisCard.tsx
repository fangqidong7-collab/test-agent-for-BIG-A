'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { TrendingUp, TrendingDown, Minus, Target } from 'lucide-react';
import type { ScenarioAnalysis } from '@/types/stock';

interface ScenarioAnalysisCardProps {
  analysis?: ScenarioAnalysis;
  loading?: boolean;
}

export function ScenarioAnalysisCard({ analysis, loading }: ScenarioAnalysisCardProps) {
  if (loading) {
    return (
      <Card className="bg-slate-800/50 border-slate-700">
        <CardHeader>
          <CardTitle className="text-lg text-slate-100">情景分析</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[300px] flex items-center justify-center">
            <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!analysis) {
    return (
      <Card className="bg-slate-800/50 border-slate-700">
        <CardHeader>
          <CardTitle className="text-lg text-slate-100">情景分析</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[200px] flex items-center justify-center text-slate-400">
            暂无情景分析数据
          </div>
        </CardContent>
      </Card>
    );
  }

  const { scenarios, current_price, summary } = analysis;

  return (
    <Card className="bg-slate-800/50 border-slate-700">
      <CardHeader>
        <CardTitle className="text-lg text-slate-100">情景分析</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* 当前价格 */}
        <div className="text-center py-4 bg-slate-900/50 rounded-lg">
          <div className="text-sm text-slate-400 mb-1">当前价格</div>
          <div className="text-4xl font-bold text-slate-100">
            ¥{current_price.toFixed(2)}
          </div>
        </div>

        {/* 三种情景 */}
        <div className="grid grid-cols-3 gap-4">
          {/* 乐观情景 */}
          {scenarios.optimistic && (
            <div className="bg-green-900/20 border border-green-800 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-3">
                <TrendingUp className="w-5 h-5 text-green-400" />
                <span className="text-sm font-medium text-green-400">乐观情景</span>
                <span className="ml-auto text-xs text-slate-400">
                  {(scenarios.optimistic.probability * 100).toFixed(0)}%
                </span>
              </div>
              <div className="text-2xl font-bold text-green-400 mb-2">
                ¥{scenarios.optimistic.target_price.toFixed(2)}
              </div>
              {scenarios.optimistic.upside_pct && (
                <div className="text-sm text-green-400/80 mb-3">
                  上涨空间 {scenarios.optimistic.upside_pct.toFixed(1)}%
                </div>
              )}
              <div className="text-xs text-slate-400 mb-2">{scenarios.optimistic.time_horizon}</div>
              <div className="space-y-1">
                {scenarios.optimistic.conditions.slice(0, 3).map((condition, idx) => (
                  <div key={idx} className="text-xs text-slate-400 flex items-start gap-1">
                    <span className="text-green-500">✓</span>
                    {condition}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 中性情景 */}
          {scenarios.neutral && (
            <div className="bg-blue-900/20 border border-blue-800 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-3">
                <Target className="w-5 h-5 text-blue-400" />
                <span className="text-sm font-medium text-blue-400">中性情景</span>
                <span className="ml-auto text-xs text-slate-400">
                  {(scenarios.neutral.probability * 100).toFixed(0)}%
                </span>
              </div>
              <div className="text-2xl font-bold text-blue-400 mb-2">
                ¥{scenarios.neutral.target_price.toFixed(2)}
              </div>
              {scenarios.neutral.upside_pct && (
                <div className="text-sm text-blue-400/80 mb-3">
                  上涨空间 {scenarios.neutral.upside_pct.toFixed(1)}%
                </div>
              )}
              <div className="text-xs text-slate-400 mb-2">{scenarios.neutral.time_horizon}</div>
              <div className="space-y-1">
                {scenarios.neutral.conditions.slice(0, 3).map((condition, idx) => (
                  <div key={idx} className="text-xs text-slate-400 flex items-start gap-1">
                    <span className="text-blue-500">•</span>
                    {condition}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 悲观情景 */}
          {scenarios.pessimistic && (
            <div className="bg-red-900/20 border border-red-800 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-3">
                <TrendingDown className="w-5 h-5 text-red-400" />
                <span className="text-sm font-medium text-red-400">悲观情景</span>
                <span className="ml-auto text-xs text-slate-400">
                  {(scenarios.pessimistic.probability * 100).toFixed(0)}%
                </span>
              </div>
              <div className="text-2xl font-bold text-red-400 mb-2">
                ¥{scenarios.pessimistic.target_price.toFixed(2)}
              </div>
              {scenarios.pessimistic.downside_pct && (
                <div className="text-sm text-red-400/80 mb-3">
                  下跌风险 {scenarios.pessimistic.downside_pct.toFixed(1)}%
                </div>
              )}
              <div className="text-xs text-slate-400 mb-2">{scenarios.pessimistic.time_horizon}</div>
              <div className="space-y-1">
                {scenarios.pessimistic.conditions.slice(0, 3).map((condition, idx) => (
                  <div key={idx} className="text-xs text-slate-400 flex items-start gap-1">
                    <span className="text-red-500">!</span>
                    {condition}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* 综合摘要 */}
        {summary && (
          <div className="border-t border-slate-700 pt-4">
            <div className="text-sm font-medium text-slate-300 mb-2">分析摘要</div>
            <div className="text-sm text-slate-400 leading-relaxed whitespace-pre-line">
              {summary}
            </div>
          </div>
        )}

        {/* 风险收益提示 */}
        <div className="bg-amber-900/20 border border-amber-800 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-amber-400">⚠️</span>
            <span className="text-sm font-medium text-amber-400">风险提示</span>
          </div>
          <div className="text-sm text-slate-400">
            情景分析仅供参考，实际股价受多种因素影响。投资有风险，决策需谨慎。
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
