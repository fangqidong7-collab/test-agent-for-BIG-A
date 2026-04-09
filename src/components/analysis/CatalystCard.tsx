'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { AlertCircle, AlertTriangle, Info } from 'lucide-react';
import type { Catalyst } from '@/types/stock';

interface CatalystCardProps {
  catalysts: Catalyst[];
  loading?: boolean;
}

export function CatalystCard({ catalysts, loading }: CatalystCardProps) {
  if (loading) {
    return (
      <Card className="bg-slate-800/50 border-slate-700">
        <CardHeader>
          <CardTitle className="text-lg text-slate-100">催化剂与风险提示</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[200px] flex items-center justify-center">
            <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!catalysts || catalysts.length === 0) {
    return (
      <Card className="bg-slate-800/50 border-slate-700">
        <CardHeader>
          <CardTitle className="text-lg text-slate-100">催化剂与风险提示</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[200px] flex items-center justify-center text-slate-400">
            暂无催化剂与风险提示
          </div>
        </CardContent>
      </Card>
    );
  }

  // 分类
  const positive = catalysts.filter((c) => c.type === 'positive');
  const negative = catalysts.filter((c) => c.type === 'negative');
  const neutral = catalysts.filter((c) => c.type === 'neutral');

  return (
    <Card className="bg-slate-800/50 border-slate-700">
      <CardHeader>
        <CardTitle className="text-lg text-slate-100">催化剂与风险提示</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* 利好因素 */}
        {positive.length > 0 && (
          <div>
            <div className="flex items-center gap-2 mb-3">
              <div className="w-1 h-4 bg-green-500 rounded-full" />
              <span className="text-sm font-medium text-green-400">利好因素</span>
              <span className="text-xs text-slate-500">({positive.length})</span>
            </div>
            <div className="space-y-3">
              {positive.map((catalyst, idx) => (
                <div 
                  key={`pos-${idx}`}
                  className="bg-green-900/20 border border-green-800/50 rounded-lg p-4"
                >
                  <div className="flex items-start gap-3">
                    <AlertCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-medium text-slate-200">{catalyst.title}</span>
                        <span className="text-xs text-slate-500">{catalyst.date}</span>
                      </div>
                      <p className="text-sm text-slate-400">{catalyst.description}</p>
                      <div className="text-xs text-slate-500 mt-2">
                        数据来源: {catalyst.source}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 利空因素 */}
        {negative.length > 0 && (
          <div>
            <div className="flex items-center gap-2 mb-3">
              <div className="w-1 h-4 bg-red-500 rounded-full" />
              <span className="text-sm font-medium text-red-400">风险因素</span>
              <span className="text-xs text-slate-500">({negative.length})</span>
            </div>
            <div className="space-y-3">
              {negative.map((catalyst, idx) => (
                <div 
                  key={`neg-${idx}`}
                  className="bg-red-900/20 border border-red-800/50 rounded-lg p-4"
                >
                  <div className="flex items-start gap-3">
                    <AlertTriangle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-medium text-slate-200">{catalyst.title}</span>
                        <span className="text-xs text-slate-500">{catalyst.date}</span>
                      </div>
                      <p className="text-sm text-slate-400">{catalyst.description}</p>
                      <div className="text-xs text-slate-500 mt-2">
                        数据来源: {catalyst.source}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 中性信息 */}
        {neutral.length > 0 && (
          <div>
            <div className="flex items-center gap-2 mb-3">
              <div className="w-1 h-4 bg-yellow-500 rounded-full" />
              <span className="text-sm font-medium text-yellow-400">中性观察</span>
              <span className="text-xs text-slate-500">({neutral.length})</span>
            </div>
            <div className="space-y-3">
              {neutral.map((catalyst, idx) => (
                <div 
                  key={`neu-${idx}`}
                  className="bg-yellow-900/20 border border-yellow-800/50 rounded-lg p-4"
                >
                  <div className="flex items-start gap-3">
                    <Info className="w-5 h-5 text-yellow-400 flex-shrink-0 mt-0.5" />
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-medium text-slate-200">{catalyst.title}</span>
                        <span className="text-xs text-slate-500">{catalyst.date}</span>
                      </div>
                      <p className="text-sm text-slate-400">{catalyst.description}</p>
                      <div className="text-xs text-slate-500 mt-2">
                        数据来源: {catalyst.source}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 数据说明 */}
        <div className="border-t border-slate-700 pt-4">
          <div className="text-xs text-slate-500">
            <p className="mb-2">
              <strong>说明：</strong>以上分析基于公开数据和量化模型，仅供参考，不构成投资建议。
            </p>
            <p>
              投资有风险，入市需谨慎。投资者应根据自身风险承受能力做出投资决策。
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
