# Weather Dashboard - 工程文档

> 项目地址: https://github.com/brad-zheng/weather-dashboard
> GitHub Pages: https://brad-zheng.github.io/weather-dashboard/
> Netlify: https://brad-weatherdashboard.netlify.app/

---

## 一、项目概述

全国 337 城市天气数据可视化看板，核心能力：
- **三年同期对比**：同一日期的今年/去年/前年温度叠加
- **多城市横向对比**：最多3城，独立于主搜索联动
- **数据驱动**：所有模块从 `data.js` 动态读取，零硬编码
- **零服务器成本**：纯静态 HTML，GitHub Actions + Pages 全托管

---

## 二、技术栈

| 层 | 技术 | 说明 |
|----|------|------|
| 数据层 | Python 3.12 | `data_fetch.py`，标准库 urllib，无需第三方依赖 |
| 数据源 | Open-Meteo API | 免费、无需Key，提供历史+预报天气 |
| 数据源 | 和风天气 API | 可选，穿衣指数（需配置 `QWEATHER_KEY`） |
| 前端 | 原生 HTML/CSS/JS | 单文件 `index.html`，无框架 |
| 图表 | Chart.js 4.4.7 | 折线图渲染 |
| 导出 | SheetJS 0.18.5 | Excel 导出 |
| 截图 | html2canvas 1.4.1 | 页面截图功能 |
| 部署 | GitHub Actions | 每天 03:00 CST 自动运行 `data_fetch.py` |
| 托管 | GitHub Pages | 静态站点，零成本 |

**不使用的技术**：Tailwind CSS、React/Vue、Webpack/Vite、Node.js、数据库

---

## 三、数据流

```
cities.json (337城坐标)
        │
        ▼
data_fetch.py ─── Open-Meteo Archive API ───► 历史数据 (2024/2025)
             │── Open-Meteo Forecast API ───► 预报数据 (2026未来14天)
             │── 和风天气 API ─────────────► 穿衣指数 (可选)
        │
        ▼
data.js (自动生成)
        │
        ├── CITIES: { 城市名: { lat, lng, province } }
        ├── WEATHER_DATA: { 城市名: { "24": {...}, "25": {...}, "26": {...} } }
        │     └── 每年: { time, max, min, wc, ws, dress }
        └── DATA_DATE: "YYYY-MM-DD HH:MM:SS"
        │
        ▼
index.html (前端读取渲染)
```

### 数据范围

| 年份 | 日期范围 | 来源 |
|------|----------|------|
| 前年 (24) | 今天±14天（共29天） | Open-Meteo Archive |
| 去年 (25) | 今天±14天（共29天） | Open-Meteo Archive |
| 今年 (26) | 过去14天（Archive）+ 未来14天（Forecast） | 合并 |

### data.js 结构详解

```javascript
// 城市元数据
const CITIES = {
  "北京": { "lat": 39.90, "lng": 116.40, "province": "北京" },
  // ... 337个城市
};

// 天气数据
const WEATHER_DATA = {
  "北京": {
    "26": {
      time:  ["2026-04-15", "2026-04-16", ...],  // 29天日期
      max:   [25, 23, ...],                        // 最高温(整数)
      min:   [12, 11, ...],                        // 最低温(整数)
      wc:    [0, 1, ...],                          // WMO天气码
      ws:    [12, 15, ...],                        // 最大风速
      dress: ["舒适", "舒适", ...]                 // 穿衣建议(可选)
    },
    "25": { time, max, min, wc, ws, dress },
    "24": { time, max, min, wc, ws, dress }
  },
  // ... 每个城市
};

const DATA_DATE = "2026-04-29 03:00:00";
```

---

## 四、前端架构 (index.html)

### 4.1 视觉设计

- **风格**: 汽车 HUD 仪表盘风格
- **背景**: `#0c1018` 深色灰蓝
- **配色**: 低饱和度（红`#a86858`/蓝`#4a90b8`/绿`#3a9a62`/紫`#8068b0`）
- **无网格/无格纹**: 纯深色 + 微妙渐变光晕
- **CSS**: 全部内联，无外部框架

### 4.2 模块架构

```
index.html
├── <style>           — 全部 CSS（内联，约300行）
├── <body>
│   ├── Header        — 搜索栏 + 城市快捷标签
│   ├── KPI           — 4个数据卡片
│   ├── Calendar      — 天气日历（三年对比）
│   ├── Charts        — 最高温/最低温/温差 × Chart.js
│   ├── CityCompare   — 多城市对比（模态对话框）
│   └── TempTable     — 气温数据表 + Excel导出
└── <script>          — 全部 JS（内联，约800行）
    ├── 数据层
    │   ├── loadCity()           — 核心函数，加载城市数据并渲染所有模块
    │   ├── findDateByMMDD()     — 跨年日期查找（按 MM-DD 匹配）
    │   ├── alignByDate()        — 单字段跨年对齐
    │   └── alignRecord()        — 完整记录跨年对齐
    ├── 渲染层
    │   ├── renderCityGrid()     — Header 快捷标签
    │   ├── renderKPI()          — KPI 卡片
    │   ├── renderCalendar()     — 天气日历
    │   ├── renderCharts()       — 三个温度对比图
    │   ├── renderTempTable()    — 气温数据表
    │   └── 多城市对比相关函数
    └── 初始化
        └── init()              — 入口，加载第一个城市
```

### 4.3 核心函数说明

| 函数 | 作用 | 关键点 |
|------|------|--------|
| `loadCity(name)` | 加载城市，渲染所有联动模块 | 调用 renderKPI/renderCalendar/renderCharts/renderTempTable |
| `findDateByMMDD(data, mmdd)` | 在年份记录中按 MM-DD 查找索引 | 解决跨年数据对齐问题 |
| `alignByDate(ref, target, start, end, field)` | 返回对齐后的单字段数组 | 2024/2025 全年数据 → 截取对应日期 |
| `alignRecord(ref, target, start, end)` | 返回对齐后的完整记录 {max,min,wc,ws} | 用于日历和数据表 |
| `renderDialogList()` | 多城市对话框城市列表渲染 | 按省份分组，3列网格布局 |
| `initMainSearch()` | Header 搜索框逻辑 | 模糊匹配城市名+省份 |

### 4.4 联动机制

```
用户操作                    响应
─────────────────────────────────────────
搜索框选择城市     ──►  loadCity() ──►  KPI + 日历 + 图表 + 数据表 全部更新
快捷标签点击城市   ──►  loadCity() ──►  同上
多城市添加城市     ──►  对比模块内部更新（不影响其他模块）
```

### 4.5 WMO 天气码映射

| 码 | 描述 | 分类 |
|----|------|------|
| 0 | 晴 | ☀️ 晴好 |
| 1 | 少云 | ☀️ 晴好 |
| 2 | 多云 | ☀️ 晴好 |
| 3 | 阴 | ☁️ 阴天 |
| 45, 48 | 雾 | ☁️ 阴天 |
| 51-55, 61-67, 80-82 | 雨 | 🌧️ 有雨 |
| 71-77, 85-86 | 雪 | 🌨️ 有雪 |
| 95-99 | 雷暴 | ⛈️ 雷暴 |

前端分类规则：晴好(0,1,2,3不算)、有雨、阴天(3,45,48)、有雪、雷暴

### 4.6 多城市对比模块

- **独立于主搜索联动**：不受 Header 搜索影响
- **最多3城**：选满后自动关闭对话框
- **数据源**：直接读 `WEATHER_DATA`，支持全部 337 城
- **UI**：模态对话框（深色毛玻璃遮罩）+ 搜索框 + 按省份分组网格
- **图表**：Chart.js 折线图，显示当天±14天最高温对比
- **交互**：标签带删除按钮，可随时移除已选城市

---

## 五、数据抓取脚本 (data_fetch.py)

### 5.1 运行流程

```
main()
├── 加载 cities.json
├── 遍历每个城市:
│   ├── fetch_weather_history(year-2)   — 前年数据 (Archive API)
│   ├── fetch_weather_history(year-1)   — 去年数据 (Archive API)
│   ├── fetch_weather_current_year()    — 今年数据 (Archive + Forecast 合并)
│   │   └── fetch_dressing_index()      — 穿衣指数 (和风天气，可选)
│   └── time.sleep(0.5)                — 礼貌限速
└── generate_js() ──► data.js
```

### 5.2 API 详情

| API | URL | 参数 |
|-----|-----|------|
| 历史天气 | `archive-api.open-meteo.com/v1/archive` | lat, lng, start_date, end_date, daily=temperature_2m_max,min,weather_code,wind_speed_10m_max |
| 天气预报 | `api.open-meteo.com/v1/forecast` | 同上 |
| 穿衣指数 | `devapi.qweather.com/v7/indices/1d` | location, type=3, key |

### 5.3 配置项

```python
# data_fetch.py 顶部配置
TARGET_CITIES = []   # 留空=全部城市；可指定 ["北京","上海"] 加快测试
QWEATHER_KEY = os.environ.get("QWEATHER_KEY", "")  # 可选
```

### 5.4 本地运行

```bash
# 无需安装任何第三方库（使用标准库 urllib）
python data_fetch.py

# 或者用 pip 安装 requests 版本（data_fetch.py 未使用 requests）
pip install requests
python data_fetch.py
```

---

## 六、GitHub Actions

### 配置文件: `.github/workflows/daily-weather.yml`

```yaml
on:
  schedule:
    - cron: '0 19 * * *'    # UTC 19:00 = 北京时间 03:00
  workflow_dispatch:          # 支持手动触发

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install requests
      - run: python data_fetch.py
      - run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add data.js
          git diff --cached --quiet || git commit -m "auto: update weather data"
          git push
```

### Secrets 配置（可选）

| Key | 说明 | 是否必须 |
|-----|------|:--------:|
| `QWEATHER_KEY` | 和风天气 API Key | ❌ |

---

## 七、版本历史

### v7.0 (2026-04-29) — 当前版本

**文件**: `index.html` + `data_fetch.py`

**P0 修复**：
- 年份硬编码 → 动态计算 `str(year % 100).zfill(2)`
- UTC时区偏移 → today/currentYear 改用 DATA_DATE
- tableCache → 改为全局变量

**P1 改进**：
- 气温数据表恢复（tableCache定义在loadCity调用前）
- 多城市对比双图表（MAX TEMP + MIN TEMP）
- 数据更新时间展示（Footer显示DATA_DATE）
- 日历模块背景色统一为深色

**P2 优化**：
- localStorage记忆城市标签折叠状态
- 城市对话框高度460px→520px，显示更多城市
- 城市对话框显示数量统计（"337 城市" / "匹配数 / 337"）
- 穿衣建议改为"最大风速"（Open-Meteo ws字段）
- KPI卡片样式优化（数字居中32px，标签在数字上方）

### v6.0 (2026-04-29)

**文件**: `index.html`（完全重写，数据驱动）

**变更**：
- 正式版 `index.html` 完全重写，抛弃旧版亮蓝色科技网格样式
- 100% 沿用 v5.0 预览版 HUD 视觉风格（深色灰蓝 `#0c1018`、低饱和度配色）
- 所有硬编码静态数据替换为 `data.js` 动态读取
- 新增模块：最低气温对比图、温差对比图（原正式版缺失）
- 多城市对比：内嵌 12 城 cityDB → 读取 WEATHER_DATA（支持 337 城）
- 多城市对比：下拉菜单 → 模态对话框（搜索 + 省份分组网格）
- 气温数据表：升级为两层表头 + sticky 日期列 + hover 高亮 + Excel 导出
- KPI 卡片：增加昨日温差计算
- 不再依赖 Tailwind CSS

**Bug 修复**：
- v6.0.1: 所有温度数值统一 `Math.round()` 四舍五入（KPI/日历/图表tooltip/Y轴/数据表/Excel导出 共8处）
- v6.0.2: 修复跨年日期对齐 bug，新增 `findDateByMMDD()`/`alignByDate()`/`alignRecord()` 按MM-DD匹配

### v5.0 (2026-04-29)

**文件**: 仅 `screenshot-preview.html`（静态预览版，不依赖 data.js）

- 八面板 HUD 风格设计稿
- 模态对话框城市选择器（搜索+省份分组）
- 数据一致性修复（min2025/min2024 五处对齐）
- 气温数据表列宽优化（`table-layout: fixed` + `<colgroup>`）

### v4.0 (2026-04-29)

**文件**: 仅 `screenshot-preview.html`

- 新增气温数据表模块（第八板块）
- 两层表头、sticky 日期列、行 hover 高亮
- Excel 导出（SheetJS CDN）

### v3.0 (2026-04-29)

**文件**: 仅 `screenshot-preview.html`

- 七面板 HUD 风格（Header + KPI + 日历 + 最高温 + 最低温 + 温差 + 多城市对比）
- Chart.js 折线图、annotation 插件「今天」竖线
- 多城市对比动态交互（初始空状态 → 添加 → 图表）

### v2.0 (2026-04-29)

- 五面板：Header + KPI + 日历 + 最高温图 + 最低温图

### v1.0 (2026-04-29)

- 四面板：天气日历 + 最高气温对比 + 气温趋势 + 降水概率
- 汽车 HUD 风格深色界面

---

## 八、已知问题与技术债务

### ✅ 已全部修复（v7.0）

- ~~年份硬编码~~ → 动态计算 `str(year % 100)`
- ~~UTC时区偏移~~ → today/currentYear 改用 DATA_DATE
- ~~tableCache未定义~~ → 改为全局变量
- ~~气温数据表报错~~ → 恢复并修复合并问题
- ~~多城市对比缺最低温~~ → 双图表 MAX+MIN

### 🟢 P2（可选增强）

- 图表加载骨架屏（数据预加载，渲染快，暂不需要）
- 穿衣指数（和风天气免费版限制，仅当天可用）

---

## 九、自定义与扩展

### 添加/删除城市

编辑 `cities.json`，格式：
```json
{
  "城市名": { "lat": 纬度, "lng": 经度, "province": "省份" }
}
```

### 修改 Header 快捷标签

编辑 `index.html` 中的 `quickCities` 数组：
```javascript
var quickCities = ['北京','上海','广州','深圳','杭州','南京','成都','武汉','重庆','西安','长沙','哈尔滨'];
```

### 修改颜色方案

编辑 `index.html` `<style>` 中的 CSS 变量和 Chart.js 配色常量。

---

*文档更新时间: 2026-04-29*
