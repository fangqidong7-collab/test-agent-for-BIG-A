'use client';

import { useEffect, useState, use } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { ArrowLeft, ExternalLink, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { OverviewCards } from '@/components/overview/OverviewCards';
import { KLineChart } from '@/components/charts/KLineChart';
import { FinancialAnalysis } from '@/components/analysis/FinancialAnalysis';
import { SevenDRatingCard } from '@/components/rating/SevenDRatingCard';
import { ScenarioAnalysisCard } from '@/components/analysis/ScenarioAnalysisCard';
import { CatalystCard } from '@/components/analysis/CatalystCard';
import { api } from '@/services/api';
import type { StockAnalysis } from '@/types/stock';

interface StockPageProps {
  params: Promise<{ code: string }>;
}

export default function StockPage({ params }: StockPageProps) {
  const { code } = use(params);
  const router = useRouter();
  const [data, setData] = useState<StockAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await api.getStockAnalysis(code);
      setData(result);
    } catch (err) {
      console.error('Failed to fetch stock data:', err);
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [code]);

  return (
    <div className="min-h-screen bg-slate-900">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/">
              <Button variant="ghost" size="sm" className="text-slate-400 hover:text-slate-100">
                <ArrowLeft className="w-4 h-4 mr-2" />
                返回首页
              </Button>
            </Link>
            {data?.basic_info && (
              <div className="flex items-center gap-3">
                <h1 className="text-xl font-bold text-slate-100">
                  {data.basic_info.name}
                </h1>
                <span className="text-slate-400">({data.basic_info.code})</span>
                {data.basic_info.industry && (
                  <span className="px-2 py-0.5 bg-blue-500/20 text-blue-400 text-sm rounded">
                    {data.basic_info.industry}
                  </span>
                )}
              </div>
            )}
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={fetchData}
              disabled={loading}
              className="border-slate-700 text-slate-400 hover:text-slate-100"
            >
              <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
              刷新
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6">
        {loading && !data ? (
          <div className="space-y-6">
            {/* Loading Skeleton */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {[...Array(4)].map((_, i) => (
                <Skeleton key={i} className="h-48 bg-slate-800" />
              ))}
            </div>
            <Skeleton className="h-[400px] bg-slate-800" />
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Skeleton className="h-[400px] bg-slate-800" />
              <Skeleton className="h-[400px] bg-slate-800" />
            </div>
          </div>
        ) : error ? (
          <div className="flex flex-col items-center justify-center py-20">
            <div className="text-red-400 text-lg mb-4">{error}</div>
            <Button onClick={fetchData} className="bg-blue-600 hover:bg-blue-700">
              <RefreshCw className="w-4 h-4 mr-2" />
              重试
            </Button>
          </div>
        ) : data ? (
          <div className="space-y-6">
            {/* 概览卡片 */}
            <OverviewCards
              basicInfo={data.basic_info}
              price={data.realtime_price}
              rating={data.seven_d_rating}
              valuation={data.valuation}
            />

            {/* K线与成交量 */}
            <KLineChart data={data.kline_data} />

            {/* 行业/概念标签 */}
            {(data.industry_tags.length > 0 || data.concept_tags.length > 0) && (
              <div className="flex flex-wrap gap-2">
                {data.industry_tags.map((tag) => (
                  <span
                    key={`ind-${tag}`}
                    className="px-3 py-1 bg-blue-500/20 text-blue-400 text-sm rounded-full"
                  >
                    {tag}
                  </span>
                ))}
                {data.concept_tags.map((tag) => (
                  <span
                    key={`con-${tag}`}
                    className="px-3 py-1 bg-purple-500/20 text-purple-400 text-sm rounded-full"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            )}

            {/* 财务分析 */}
            <FinancialAnalysis data={data.financial_indicators} />

            {/* 估值分析 */}
            {data.valuation && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* 七维评分 */}
                <SevenDRatingCard rating={data.seven_d_rating} />
                
                {/* 情景分析 */}
                <ScenarioAnalysisCard analysis={data.scenario_analysis} />
              </div>
            )}

            {/* 催化剂与风险提示 */}
            <CatalystCard catalysts={data.catalysts} />

            {/* 数据来源 */}
            <div className="text-center text-sm text-slate-500 py-4 border-t border-slate-800">
              <p>数据来源: {data.data_source}</p>
              <p>更新时间: {data.data_timestamp}</p>
            </div>
          </div>
        ) : null}
      </main>
    </div>
  );
}
