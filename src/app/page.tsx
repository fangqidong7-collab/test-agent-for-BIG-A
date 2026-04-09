'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { SearchBox } from '@/components/search/SearchBox';
import { TrendingUp, BarChart3, Shield, Zap, ChevronRight, BookOpen, LineChart, Globe } from 'lucide-react';
import Link from 'next/link';

const HOT_STOCKS = [
  { code: '000001', name: '平安银行' },
  { code: '600519', name: '贵州茅台' },
  { code: '000858', name: '五粮液' },
  { code: '601318', name: '中国平安' },
  { code: '600036', name: '招商银行' },
  { code: '300750', name: '宁德时代' },
  { code: '002594', name: '比亚迪' },
  { code: '000333', name: '美的集团' },
];

const FEATURES = [
  {
    icon: <BarChart3 className="w-8 h-8" />,
    title: '七维评分',
    description: '从盈利能力、成长能力、估值水平、财务健康、技术走势、行业前景、机构关注七个维度全面评估',
  },
  {
    icon: <TrendingUp className="w-8 h-8" />,
    title: 'K线分析',
    description: '支持日/周/月K线，前复权/后复权，MA均线叠加，专业的技术分析图表',
  },
  {
    icon: <Shield className="w-8 h-8" />,
    title: '财务分析',
    description: '盈利能力、成长能力、偿债能力、运营能力全方位财务数据展示',
  },
  {
    icon: <Zap className="w-8 h-8" />,
    title: '情景分析',
    description: '乐观/中性/悲观三种情景下的目标价和概率分析',
  },
  {
    icon: <LineChart className="w-8 h-8" />,
    title: '估值分析',
    description: 'PE/PB/PS历史分位，与行业平均对比，辅助判断估值高低',
  },
  {
    icon: <Globe className="w-8 h-8" />,
    title: '催化剂追踪',
    description: '及时追踪利好/风险因素，帮助把握投资机会',
  },
];

export default function HomePage() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-900 to-slate-950">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-slate-100">智投A股</span>
          </div>
          <nav className="flex items-center gap-6">
            <Link href="/" className="text-sm text-blue-400 hover:text-blue-300">
              首页
            </Link>
            <a href="#features" className="text-sm text-slate-400 hover:text-slate-300">
              功能介绍
            </a>
            <a href="#about" className="text-sm text-slate-400 hover:text-slate-300">
              关于我们
            </a>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto text-center max-w-4xl">
          <h1 className={`text-4xl md:text-6xl font-bold text-slate-100 mb-6 transition-opacity duration-1000 ${
            mounted ? 'opacity-100' : 'opacity-0'
          }`}>
            专业、客观的
            <span className="bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">
              A股分析平台
            </span>
          </h1>
          <p className={`text-lg text-slate-400 mb-10 max-w-2xl mx-auto transition-opacity duration-1000 delay-200 ${
            mounted ? 'opacity-100' : 'opacity-0'
          }`}>
            基于基本面分析，提供七维评分、K线图表、财务分析、情景分析等专业工具，
            帮助投资者做出更明智的投资决策。
          </p>

          {/* 搜索框 */}
          <div className={`max-w-2xl mx-auto transition-all duration-1000 delay-400 ${
            mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
          }`}>
            <SearchBox className="w-full" autoFocus />
          </div>

          {/* 热门股票 */}
          <div className={`mt-6 transition-opacity duration-1000 delay-500 ${
            mounted ? 'opacity-100' : 'opacity-0'
          }`}>
            <div className="text-sm text-slate-500 mb-3">热门股票</div>
            <div className="flex flex-wrap justify-center gap-2">
              {HOT_STOCKS.map((stock) => (
                <Link key={stock.code} href={`/stock/${stock.code}`}>
                  <Badge 
                    variant="outline" 
                    className="cursor-pointer hover:bg-slate-800 border-slate-700 hover:border-blue-500 transition-colors"
                  >
                    {stock.name} ({stock.code})
                  </Badge>
                </Link>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 bg-slate-900/50">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-slate-100 mb-4">核心功能</h2>
            <p className="text-slate-400">专业的股票分析工具，助力投资决策</p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {FEATURES.map((feature, idx) => (
              <Card 
                key={idx} 
                className="bg-slate-800/50 border-slate-700 hover:border-blue-500/50 transition-colors group"
              >
                <CardHeader>
                  <div className="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center mb-4 text-blue-400 group-hover:bg-blue-500/30 transition-colors">
                    {feature.icon}
                  </div>
                  <CardTitle className="text-lg text-slate-100">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-slate-400 leading-relaxed">
                    {feature.description}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-20 px-4">
        <div className="container mx-auto max-w-4xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-slate-100 mb-4">关于智投A股</h2>
          </div>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardContent className="p-8">
              <div className="flex items-start gap-4 mb-6">
                <BookOpen className="w-8 h-8 text-blue-400 flex-shrink-0" />
                <div>
                  <h3 className="text-lg font-medium text-slate-100 mb-2">分析方法论</h3>
                  <p className="text-slate-400 text-sm leading-relaxed">
                    智投A股采用"先结论，后论证"的分析框架，从七个维度综合评估股票价值。
                    技术面只作辅助参考，中长期判断更多依赖基本面和估值分析。
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-4 mb-6">
                <Shield className="w-8 h-8 text-green-400 flex-shrink-0" />
                <div>
                  <h3 className="text-lg font-medium text-slate-100 mb-2">客观中立</h3>
                  <p className="text-slate-400 text-sm leading-relaxed">
                    我们坚持客观中立的分析立场，数据不足时会明确说明，不夸大、不喊单。
                    所有结论都有数据支撑，分析逻辑可追溯。
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-4">
                <Zap className="w-8 h-8 text-amber-400 flex-shrink-0" />
                <div>
                  <h3 className="text-lg font-medium text-slate-100 mb-2">数据来源</h3>
                  <p className="text-slate-400 text-sm leading-relaxed">
                    数据主要来源于 BaoStock、AKShare 等公开数据源。我们采用可替换的数据服务架构，
                    确保数据获取的稳定性和可靠性。
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-800 py-8 px-4">
        <div className="container mx-auto max-w-6xl">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-gradient-to-br from-blue-500 to-blue-600 rounded flex items-center justify-center">
                <TrendingUp className="w-4 h-4 text-white" />
              </div>
              <span className="text-sm font-medium text-slate-400">智投A股</span>
            </div>
            <div className="text-sm text-slate-500">
              © 2024 智投A股. 仅供投资参考，不构成投资建议。
            </div>
            <div className="flex items-center gap-4 text-sm text-slate-500">
              <span>投资有风险</span>
              <span>•</span>
              <span>入市需谨慎</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
