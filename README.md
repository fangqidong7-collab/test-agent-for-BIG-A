# A股智能分析平台

专业、客观的A股股票分析Web应用，基于基本面分析，提供七维评分、K线图表、财务分析、情景分析等专业工具。

## 功能特性

- **首页搜索**：支持股票代码、名称、公司全名模糊搜索
- **股票详情页**：完整的股票分析报告
- **概览卡片**：价格、估值、评分、基本信息一目了然
- **K线图表**：日/周/月K线，前复权/后复权，MA均线叠加
- **财务分析**：盈利能力、成长能力、偿债能力、运营能力
- **估值分析**：PE/PB/PS历史分位，与行业对比
- **七维评分**：盈利能力、成长能力、估值水平、财务健康、技术走势、行业前景、机构关注
- **情景分析**：乐观/中性/悲观三种情景下的目标价分析
- **催化剂追踪**：利好/风险因素及时追踪

## 技术栈

### 前端
- Next.js 16 (App Router)
- React 19
- TypeScript 5
- Tailwind CSS 4
- shadcn/ui
- Recharts
- ECharts

### 后端
- Python FastAPI
- BaoStock
- AKShare
- AKTools

## 项目结构

```
/workspace/projects/
├── frontend/                    # Next.js 前端
│   ├── src/
│   │   ├── app/                # 页面路由
│   │   ├── components/         # 组件
│   │   │   ├── ui/            # shadcn/ui 组件
│   │   │   ├── search/        # 搜索组件
│   │   │   ├── overview/      # 概览卡片
│   │   │   ├── charts/        # 图表组件
│   │   │   ├── analysis/      # 分析模块
│   │   │   └── rating/        # 评分组件
│   │   ├── hooks/             # 自定义 hooks
│   │   ├── lib/               # 工具函数
│   │   ├── services/          # API 服务
│   │   └── types/             # TypeScript 类型
│   └── package.json
│
├── backend/                     # FastAPI 后端
│   ├── app/
│   │   ├── api/               # API 路由
│   │   ├── services/          # 数据服务
│   │   ├── engine/             # 分析引擎
│   │   ├── models/            # 数据模型
│   │   └── main.py             # FastAPI 入口
│   └── requirements.txt
│
├── SPEC.md                      # 项目规范
└── README.md                    # 本文档
```

## 快速开始

### 前端

```bash
cd /workspace/projects

# 安装依赖
pnpm install

# 开发模式
pnpm dev

# 构建
pnpm build

# 生产模式
pnpm start
```

前端服务运行在 http://localhost:5000

### 后端

```bash
cd /workspace/projects/backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端服务运行在 http://localhost:8000

API文档: http://localhost:8000/docs

## 环境变量

### 前端 (.env.local)
```
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

### 后端 (.env)
```
# BaoStock (可选，已内置免费接口)
# BAOSTOCK_USERNAME=your_username
# BAOSTOCK_PASSWORD=your_password

# AKTools (可选，需要Token)
# AKTOOLS_TOKEN=your_token
```

## 数据服务架构

项目采用可替换的数据服务架构，支持多个数据源：

1. **BaoStock** (主数据源) - 优先级最高
2. **AKTools** (补充数据源) - 需要Token
3. **AKShare** (备选数据源) - 开源库

当主数据源不可用时，会自动切换到备选数据源。

## 分析逻辑

### 七维评分体系

| 维度 | 权重 | 说明 |
|------|------|------|
| 盈利能力 | 25% | ROE、毛利率、净利率等 |
| 成长能力 | 20% | 营收增长、利润增长等 |
| 估值水平 | 15% | PE、PB、PS等指标 |
| 财务健康 | 15% | 资产负债率、流动比率等 |
| 技术走势 | 10% | 趋势、动量、波动率 |
| 行业前景 | 10% | 行业景气度 |
| 机构关注 | 5% | 机构持仓、分析师覆盖 |

### 投资标签

| 标签 | 评分范围 | 说明 |
|------|----------|------|
| 重点关注 | >=75 | 多维度向好，可考虑建仓 |
| 回调关注 | 60-74 | 长期看好，等待买点 |
| 中性观察 | 45-59 | 无明显方向，需更多信息 |
| 谨慎参与 | 30-44 | 风险大于机会 |
| 暂不参与 | <30 | 风险显著 |

### 分析原则

- 先结论，后论证
- 区分短期、中期、长期判断
- 技术面只作辅助参考
- 中长期结论更多依赖基本面和估值
- 数据不足时必须明确说明
- 不允许夸张喊单式表达

## 数据说明

本项目的数据主要来源于公开数据源：
- BaoStock (http://www.baostock.com)
- AKShare (https://akshare.akun.com)

所有数据仅供投资参考，不构成投资建议。投资有风险，入市需谨慎。

## 许可证

MIT License
