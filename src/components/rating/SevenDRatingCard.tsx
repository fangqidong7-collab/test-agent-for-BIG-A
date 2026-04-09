'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { SevenDRating, DimensionScore } from '@/types/stock';
import { TAG_COLORS } from '@/types/stock';

interface SevenDRatingCardProps {
  rating?: SevenDRating;
  loading?: boolean;
}

// 维度配置
const DIMENSION_CONFIG: Record<string, { label: string; icon: string }> = {
  profitability: { label: '盈利能力', icon: '💰' },
  growth: { label: '成长能力', icon: '📈' },
  valuation: { label: '估值水平', icon: '⚖️' },
  financial_health: { label: '财务健康', icon: '🏥' },
  technical: { label: '技术走势', icon: '📊' },
  industry_outlook: { label: '行业前景', icon: '🏭' },
  institutional_attention: { label: '机构关注', icon: '🏛️' }
};

// 获取评分颜色
const getScoreColor = (score: number) => {
  if (score >= 75) return 'text-green-400';
  if (score >= 55) return 'text-blue-400';
  if (score >= 40) return 'text-yellow-400';
  return 'text-red-400';
};

// 获取评分背景
const getScoreBg = (score: number) => {
  if (score >= 75) return 'bg-green-500';
  if (score >= 55) return 'bg-blue-500';
  if (score >= 40) return 'bg-yellow-500';
  return 'bg-red-500';
};

export function SevenDRatingCard({ rating, loading }: SevenDRatingCardProps) {
  if (loading) {
    return (
      <Card className="bg-slate-800/50 border-slate-700">
        <CardHeader>
          <CardTitle className="text-lg text-slate-100">七维评分</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[300px] flex items-center justify-center">
            <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!rating) {
    return (
      <Card className="bg-slate-800/50 border-slate-700">
        <CardHeader>
          <CardTitle className="text-lg text-slate-100">七维评分</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[200px] flex items-center justify-center text-slate-400">
            暂无评分数据
          </div>
        </CardContent>
      </Card>
    );
  }

  const tagStyle = TAG_COLORS[rating.tag] || { bg: 'bg-slate-700', text: 'text-slate-300', border: 'border-slate-600' };

  return (
    <Card className="bg-slate-800/50 border-slate-700">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg text-slate-100">七维评分</CardTitle>
          <div className={`inline-flex items-center px-3 py-1.5 rounded-full ${
            tagStyle.bg
          } border ${tagStyle.border}`}>
            <span className={`text-sm font-medium ${tagStyle.text}`}>
              {rating.tag}
            </span>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* 总分展示 */}
        <div className="text-center">
          <div className="text-5xl font-bold text-slate-100">
            {rating.total_score.toFixed(1)}
          </div>
          <div className="text-sm text-slate-400 mt-1">综合评分 (满分100)</div>
        </div>

        {/* 雷达图 */}
        <div className="relative h-[200px]">
          <div className="absolute inset-0 flex items-center justify-center">
            {/* 雷达图简化版本 - 使用条形图替代 */}
            <div className="w-full grid grid-cols-7 gap-2">
              {rating.dimensions.map((dim) => {
                const config = DIMENSION_CONFIG[dim.dimension] || { label: dim.dimension, icon: '📊' };
                const heightPercent = dim.score;
                
                return (
                  <div key={dim.dimension} className="flex flex-col items-center">
                    <div className="relative w-full h-32 flex items-end justify-center">
                      <div 
                        className={`w-6 rounded-t-md transition-all ${getScoreBg(dim.score)}`}
                        style={{ height: `${heightPercent}%` }}
                      />
                    </div>
                    <div className="text-xs text-slate-400 mt-2 text-center leading-tight">
                      {config.label}
                    </div>
                    <div className={`text-sm font-semibold ${getScoreColor(dim.score)}`}>
                      {dim.score.toFixed(0)}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* 维度详情列表 */}
        <div className="space-y-3">
          {rating.dimensions.map((dim) => {
            const config = DIMENSION_CONFIG[dim.dimension] || { label: dim.dimension, icon: '📊' };
            
            return (
              <div key={dim.dimension} className="bg-slate-900/50 rounded-lg p-3">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{config.icon}</span>
                    <span className="text-sm text-slate-300">{config.label}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`text-lg font-bold ${getScoreColor(dim.score)}`}>
                      {dim.score.toFixed(0)}
                    </span>
                    <span className="text-xs text-slate-500">
                      (权重{(dim.weight * 100).toFixed(0)}%)
                    </span>
                  </div>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full transition-all ${getScoreBg(dim.score)}`}
                    style={{ width: `${dim.score}%` }}
                  />
                </div>
                {/* 指标详情 */}
                {Object.keys(dim.metrics).length > 0 && (
                  <div className="mt-2 flex flex-wrap gap-2">
                    {Object.entries(dim.metrics).slice(0, 3).map(([key, val]: [string, any]) => {
                      if (val.value === undefined || val.value === null) return null;
                      return (
                        <span key={key} className="inline-flex items-center gap-1 text-xs bg-slate-800 px-2 py-1 rounded">
                          <span className="text-slate-400">{key}:</span>
                          <span className={getScoreColor(typeof val.value === 'number' ? val.value : 50)}>
                            {typeof val.value === 'number' ? val.value.toFixed(2) : val.value}
                          </span>
                        </span>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* 时间维度判断 */}
        <div className="border-t border-slate-700 pt-4 space-y-3">
          <div className="text-sm font-medium text-slate-300 mb-2">时间维度判断</div>
          
          <div className="bg-slate-900/50 rounded-lg p-3">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs px-2 py-0.5 bg-orange-500/20 text-orange-400 rounded">短期</span>
              <span className="text-sm text-slate-300">{rating.short_term}</span>
            </div>
          </div>
          
          <div className="bg-slate-900/50 rounded-lg p-3">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs px-2 py-0.5 bg-blue-500/20 text-blue-400 rounded">中期</span>
              <span className="text-sm text-slate-300">{rating.mid_term}</span>
            </div>
          </div>
          
          <div className="bg-slate-900/50 rounded-lg p-3">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs px-2 py-0.5 bg-green-500/20 text-green-400 rounded">长期</span>
              <span className="text-sm text-slate-300">{rating.long_term}</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
