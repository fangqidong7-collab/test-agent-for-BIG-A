# AGENTS.md - A股智能分析平台

## 项目概述

**智投A股** 是一个专业、客观的A股股票分析Web应用，采用前后端分离架构。

### 技术栈

**前端**
- Next.js 16 (App Router)
- React 19
- TypeScript 5
- Tailwind CSS 4
- shadcn/ui
- Recharts
- ECharts

**后端**
- Python FastAPI
- BaoStock
- AKShare

## 目录结构

```
/workspace/projects/
├── frontend/                    # Next.js 前端 (在根目录)
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx        # 首页
│   │   │   ├── layout.tsx      # 布局
│   │   │   └── stock/[code]/   # 股票详情页
│   │   ├── components/
│   │   │   ├── search/         # 搜索组件
│   │   │   ├── overview/       # 概览卡片
│   │   │   ├── charts/        # K线图表
│   │   │   ├── analysis/       # 分析模块
│   │   │   └── rating/         # 七维评分
│   │   ├── services/api.ts     # API服务
│   │   └── types/stock.ts      # 类型定义
│   └── package.json
│
├── backend/                     # FastAPI 后端
│   ├── app/
│   │   ├── api/                # API路由
│   │   │   ├── search.py       # 搜索接口
│   │   │   └── stock.py        # 股票详情接口
│   │   ├── services/           # 数据服务层
│   │   │   ├── base.py         # 服务基类
│   │   │   ├── baostock.py     # BaoStock服务
│   │   │   ├── aktools.py      # AKTools服务
│   │   │   └── akshare.py      # AKShare服务
│   │   ├── engine/             # 分析引擎
│   │   │   ├── analyzer.py     # 主分析引擎
│   │   │   ├── rating.py       # 七维评分
│   │   │   └── scenario.py     # 情景分析
│   │   ├── models/             # 数据模型
│   │   │   └── schemas.py      # Pydantic模型
│   │   └── main.py             # FastAPI入口
│   └── requirements.txt
│
├── SPEC.md                      # 项目规范
└── README.md                    # 项目说明
```

## 开发命令

### 前端 (根目录)

```bash
# 开发模式 (端口5000)
pnpm dev

# 构建
pnpm build

# 生产模式
pnpm start
```

### 后端

```bash
cd /workspace/projects/backend

# 安装依赖
pip install -r requirements.txt

# 运行 (端口8000)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API 端点

### 搜索接口
```
GET /api/search?q={keyword}
```

### 股票详情
```
GET /api/stock/{code}
```

### K线数据
```
GET /api/stock/{code}/kline?period=daily&adjust=qfq
```

### 财务数据
```
GET /api/stock/{code}/financial
```

### 估值数据
```
GET /api/stock/{code}/valuation
```

## 核心功能

### 1. 七维评分
- 盈利能力 (25%)
- 成长能力 (20%)
- 估值水平 (15%)
- 财务健康 (15%)
- 技术走势 (10%)
- 行业前景 (10%)
- 机构关注 (5%)

### 2. 投资标签
- 重点关注 (>=75分)
- 回调关注 (60-74分)
- 中性观察 (45-59分)
- 谨慎参与 (30-44分)
- 暂不参与 (<30分)

### 3. 情景分析
- 乐观情景 (20%概率)
- 中性情景 (55%概率)
- 悲观情景 (25%概率)

## 环境变量

### 前端
```
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

### 后端 (backend/.env)
```
# 可选配置
BAOSTOCK_USERNAME=
BAOSTOCK_PASSWORD=
AKTOOLS_TOKEN=
```

## 数据源

1. **BaoStock** (主) - 免费数据，无需注册
2. **AKTools** (补) - 需要Token
3. **AKShare** (备) - 开源Python库

## 注意事项

1. 后端需要独立运行在端口8000
2. 前端API_BASE需配置正确指向后端
3. 数据服务采用可替换架构，失败时自动切换
4. 所有数据仅供投资参考，不构成投资建议

## 常见问题

**Q: 前端无法连接后端?**  
A: 检查后端是否运行在8000端口，确认NEXT_PUBLIC_API_BASE配置

**Q: 数据加载失败?**  
A: 外部数据源可能暂时不可用，系统会自动降级使用缓存数据

**Q: 如何添加新的数据源?**  
A: 实现BaseDataService接口，在services/__init__.py中注册
