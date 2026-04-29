# 天气数据看板

> 全国 337 城市天气数据可视化，支持三年同期温度对比与多城市横向对比。

**在线访问**: https://brad-zheng.github.io/weather-dashboard/

---

## 功能概览

| 模块 | 说明 | 联动 |
|------|------|:----:|
| Header | 搜索栏（337城模糊搜索）+ 12城快捷标签 | ✅ |
| KPI 卡片 | 最高温 / 最低温 / 天气状况 / 穿衣建议 + 昨日温差 | ✅ |
| 天气日历 | 未来15天 · 三年对比，含天气小结统计 | ✅ |
| 最高气温对比 | ±15天 · 三年折线图 + 今年均值/历史均值/偏差 | ✅ |
| 最低气温对比 | ±15天 · 三年折线图 | ✅ |
| 温差对比 | ±15天 · 三年折线图 | ✅ |
| 多城市对比 | 模态对话框（搜索+省份分组）+ 动态图表，最多3城 | ❌ |
| 气温数据表 | 两层表头 + sticky + hover高亮 + Excel导出 | ✅ |

> 联动说明：Header 搜索/快捷标签切换城市时，除多城市对比外所有模块同步更新。

---

## 技术架构

```
┌─────────────────────────────────────────────────────────┐
│  数据层 (Python)                                         │
│  Open-Meteo API (历史+预报) ──► data_fetch.py ──► data.js│
│  和风天气 API (穿衣指数，可选)                            │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────┐
│  部署层 (GitHub)         │                              │
│  Actions 每天 03:00 CST ─► data.js 自动提交 ─► Pages 托管 │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────┐
│  表现层 (纯静态前端)     │                              │
│  Chart.js + xlsx + html2canvas (CDN) ──► index.html     │
│  无 Tailwind / 无构建工具                               │
└─────────────────────────────────────────────────────────┘
```

**你的电脑不需要一直开着** — 全部运行在 GitHub 上。

---

## 文件结构

```
weather-dashboard/
├── .github/
│   └── workflows/
│       └── daily-weather.yml   # GitHub Actions 定时任务
├── cities.json                 # 337城市经纬度+省份
├── data_fetch.py               # Python 数据抓取脚本
├── data.js                     # ⚠️ 自动生成，勿手动编辑
├── index.html                  # 主页面（v6.0 数据驱动）
├── screenshot-preview.html     # 静态截图用预览版（不依赖 data.js）
├── README.md                   # 本文件
└── PROJECT.md                  # 详细工程文档
```

---

## CDN 依赖

| 库 | 版本 | 用途 |
|----|------|------|
| Chart.js | 4.4.7 | 图表渲染 |
| chartjs-plugin-annotation | 3.1.0 | 图表「今天」竖线标注 |
| html2canvas | 1.4.1 | 页面截图 |
| xlsx (SheetJS) | 0.18.5 | Excel 导出 |

> 无 Tailwind CSS，无构建工具，纯手写 CSS。

---

## 部署

### 已部署

- **仓库**: https://github.com/brad-zheng/weather-dashboard
- **Pages**: https://brad-zheng.github.io/weather-dashboard/
- **Actions**: 每天 UTC 19:00（北京时间 03:00）自动更新

### 重新部署步骤

1. Fork 或创建仓库，推送代码到 `master` 分支
2. Settings → Pages → Source: `master` / `(root)` → Save
3. Settings → Secrets → 添加 `QWEATHER_KEY`（可选，用于穿衣指数）
4. Actions 标签页手动 Run workflow 验证

---

## 本地开发

```bash
# 生成数据
pip install requests
python data_fetch.py

# 启动本地服务器
python -m http.server 8000
# 访问 http://localhost:8000
```

---

## 已知限制

1. **年份硬编码**: `data_fetch.py` 第167行年份key为 `"24"/"25"/"26"`，**2027年会出 bug**
2. **时区问题**: `new Date().toISOString()` 使用 UTC，北京时间 00:00~08:00 访问时日期可能偏移一天
3. **和风天气**: 穿衣指数需要 API Key，免费版仅支持当天查询

---

## 版本历史

| 日期 | 版本 | 说明 |
|------|------|------|
| 2026-04-29 | v6.0 | 全面重构：v5.0 HUD视觉 + 数据驱动架构，八模块完整实现 |
| 2026-04-29 | v5.0 | 预览版：HUD风格设计稿，静态数据 |
| 2026-04-16 | v2.0 | 旧版科技风界面 |

详细版本记录见 [PROJECT.md](./PROJECT.md)。

---

*MIT License*
