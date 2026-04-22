# Weather Dashboard - 天气数据看板工程文档

> 项目地址: https://github.com/brad-zheng/weather-dashboard  
> 在线访问: https://brad-zheng.github.io/weather-dashboard/

---

## 项目概述

全国 300+ 城市天气数据可视化看板，支持：
- 今日天气 KPI（最高/最低气温、天气状况、穿衣建议）
- 近14日 × 3年温度曲线对比
- 多城市横向对比（最多5城）
- 详细数据表格
- 一键截图分享

---

## 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                      数据层 (Python)                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Open-Meteo  │  │  和风天气   │  │ cities.json │         │
│  │   API       │  │    API      │  │ (城市坐标)  │         │
│  └──────┬──────┘  └──────┬──────┘  └─────────────┘         │
│         └─────────────────┘                                 │
│                   │                                         │
│              data_fetch.py                                  │
│                   │                                         │
│              data.js (生成)                                 │
└───────────────────┬─────────────────────────────────────────┘
                    │
┌───────────────────┼─────────────────────────────────────────┐
│                   │         部署层 (GitHub)                  │
│              GitHub Actions                                 │
│         ┌─────────────────────┐                             │
│         │ 每日 03:00 自动运行 │                             │
│         │ workflow_dispatch   │                             │
│         └─────────────────────┘                             │
│                          │                                  │
│                   GitHub Pages                              │
│                          │                                  │
└──────────────────────────┼──────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────┐
│                   表现层 (前端)                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ TailwindCSS │  │  Chart.js   │  │ html2canvas │         │
│  │  (CDN)      │  │  (CDN)      │  │  (CDN)      │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                          │                                  │
│                     index.html                              │
│                   科技风 HUD 界面                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 文件结构

```
weather-dashboard/
├── .github/
│   └── workflows/
│       └── daily-weather.yml      # GitHub Actions 定时任务
├── cities.json                     # 全国城市经纬度数据
├── data.js                         # 自动生成的天气数据
├── data_fetch.py                   # Python 数据抓取脚本
├── index.html                      # 前端可视化页面
└── README.md                       # 项目说明文档
```

---

## 核心文件详解

### 1. index.html - 前端可视化页面

**功能**: 科技风 HUD 界面，纯静态 HTML，无需服务器。

**技术栈**:
- Tailwind CSS (CDN) - 原子化 CSS 框架
- Chart.js (CDN) - 图表渲染
- chartjs-plugin-annotation (CDN) - 图表标注（今日线）
- html2canvas (CDN) - 页面截图

**核心功能模块**:

| 模块 | 说明 |
|------|------|
| KPI 卡片 | 最高/最低气温、天气状况、穿衣建议 |
| 温度折线图 | 近14日 × 3年对比，红色虚线标注今日 |
| 多城市对比 | 最多5城横向对比 |
| 数据表格 | 详细历史数据，今日高亮 |
| 城市搜索 | 模糊搜索 + 键盘导航 |
| 截图分享 | 一键复制到剪贴板或下载 |

**WMO 天气码映射**:
```javascript
const WMO_TEXT = {
    0:'☀️ 晴',1:'🌤️ 少云',2:'⛅ 多云',3:'☁️ 阴',
    45:'🌫️ 雾',48:'🌫️ 冻雾',
    51:'🌦️ 小雨',53:'🌧️ 中雨',55:'🌧️ 大雨',
    61:'🌧️ 小雨',63:'🌧️ 中雨',65:'🌧️ 大雨',
    66:'🌧️ 冻雨',67:'🌧️ 大冻雨',
    71:'🌨️ 小雪',73:'🌨️ 中雪',75:'❄️ 大雪',
    77:'🌨️ 雪粒',
    80:'🌦️ 阵雨',81:'🌧️ 中阵雨',82:'⛈️ 大阵雨',
    85:'🌨️ 小阵雪',86:'❄️ 大阵雪',
    95:'⛈️ 雷暴',96:'⛈️ 雷暴+冰雹',99:'⛈️ 强雷暴+冰雹'
};
```

---

### 2. data_fetch.py - 数据抓取脚本

**功能**: 从 Open-Meteo API 和和风天气 API 抓取数据，生成 data.js。

**API 来源**:

| API | 用途 | 参数 |
|-----|------|------|
| Open-Meteo Archive | 历史天气数据 | `temperature_2m_max`, `temperature_2m_min`, `weather_code`, `wind_speed_10m_max` |
| Open-Meteo Forecast | 未来预报数据 | 同上 |
| 和风天气生活指数 | 穿衣建议 | `type=3` (穿衣指数) |

**数据结构**:
```python
{
    "北京": {
        "24": {  # 两年前
            "time": ["2024-04-05", ...],
            "max": [23, 25, ...],   # 最高温
            "min": [11, 13, ...],   # 最低温
            "wc": [0, 1, ...],      # 天气码
            "ws": [12, 15, ...],    # 最大风速
        },
        "25": { ... },  # 一年前
        "26": { ... }   # 当年（含预报）
    }
}
```

**运行方式**:
```bash
# 本地测试
python data_fetch.py

# 需要配置环境变量
export QWEATHER_KEY="your_api_key"  # 可选，用于穿衣指数
```

---

### 3. cities.json - 城市坐标数据

**格式**:
```json
{
  "北京": {"lat": 39.90, "lng": 116.40, "province": "北京"},
  "上海": {"lat": 31.23, "lng": 121.47, "province": "上海"},
  ...
}
```

**说明**:
- 包含全国 300+ 城市
- 坐标用于 Open-Meteo API 查询
- 可按需增删城市

---

### 4. data.js - 自动生成的天气数据

**说明**: 由 `data_fetch.py` 自动生成，**请勿手动编辑**。

**内容示例**:
```javascript
// ============================================
// 天气数据文件 - 自动生成，请勿手动编辑
// 生成时间: 2026-04-16 06:48:31
// 数据来源: Open-Meteo API + 和风天气生活指数
// ============================================

const CITIES = { ... };
const WEATHER_DATA = { ... };
const DATA_DATE = "2026-04-16 06:48:31";
```

---

### 5. .github/workflows/daily-weather.yml - GitHub Actions

**功能**: 每天自动抓取最新天气数据并部署。

**触发条件**:
- 定时触发: 每天 UTC 19:00 (北京时间 03:00)
- 手动触发: `workflow_dispatch`

**工作流步骤**:
1. 检出代码
2. 设置 Python 3.12
3. 安装依赖 (`requests`)
4. 执行数据抓取
5. 提交并推送 `data.js`

**配置**:
```yaml
env:
  TZ: Asia/Shanghai
  QWEATHER_KEY: ${{ secrets.QWEATHER_KEY }}  # 可选
```

---

## 部署步骤

### 第一步: 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名: `weather-dashboard`
3. 选择 Public（GitHub Pages 免费版需要）
4. 点击 Create repository

### 第二步: 上传文件

```bash
# 本地初始化并上传
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/weather-dashboard.git
git push -u origin main
```

或使用 GitHub 网页上传:
1. 打开仓库页面
2. 点击 **Add file** → **Upload files**
3. 拖入所有文件
4. 点击 **Commit changes**

### 第三步: 开启 GitHub Pages

1. 进入仓库 **Settings** → **Pages**
2. **Source**: Deploy from a branch
3. **Branch**: main / (root)
4. 点击 **Save**
5. 等待 1-2 分钟，访问显示的 URL

### 第四步: 配置定时任务（可选）

如需穿衣指数功能:
1. 进入仓库 **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**
3. Name: `QWEATHER_KEY`
4. Value: 你的和风天气 API Key
5. 点击 **Add secret**

---

## 本地开发

### 环境要求
- Python 3.8+
- 现代浏览器（Chrome/Firefox/Edge）

### 本地运行

```bash
# 1. 进入项目目录
cd weather-dashboard

# 2. 生成数据文件（可选，也可直接用线上 data.js）
python data_fetch.py

# 3. 用浏览器打开 index.html
# 或启动本地服务器:
python -m http.server 8000
# 然后访问 http://localhost:8000
```

---

## 界面预览

### 科技风 HUD 设计

- **背景**: 深炭黑 (#050810) + 科技网格纹理 + 扫描线效果
- **主色调**: 发光冰蓝色 (#38bdf8)
- **面板**: 半透明磨砂玻璃 (backdrop-filter: blur)
- **边框**: 辉光效果 (box-shadow)

### KPI 卡片

| 卡片 | 颜色 | 内容 |
|------|------|------|
| 最高气温 | 红色 | 今日最高温 + 单位 |
| 最低气温 | 蓝色 | 今日最低温 + 单位 |
| 天气状况 | 绿色 | WMO 天气码转中文 |
| 穿衣建议 | 紫色 | 和风天气穿衣指数 |

### 图表

- 3年温度曲线对比
- 红色虚线标注今日位置
- 悬停显示详细数值

---

## 常见问题

### Q: 数据多久更新一次？
A: GitHub Actions 每天北京时间 03:00 自动更新。

### Q: 可以添加更多城市吗？
A: 可以，修改 `cities.json` 添加城市名称和坐标即可。

### Q: 穿衣指数为什么不显示？
A: 需要配置 `QWEATHER_KEY` 环境变量。免费版仅支持当天查询。

### Q: 如何手动触发数据更新？
A: 进入仓库 Actions 页面，找到 "每日天气数据更新"，点击 Run workflow。

### Q: 截图功能怎么用？
A: 点击页面右上角「截图」按钮，自动复制到剪贴板或下载 PNG。

---

## 技术依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| Tailwind CSS | CDN | 样式框架 |
| Chart.js | 4.4.0 | 图表渲染 |
| chartjs-plugin-annotation | 3.0.1 | 图表标注 |
| html2canvas | 1.4.1 | 页面截图 |
| Open-Meteo API | - | 天气数据 |
| 和风天气 API | - | 穿衣指数 |

---

## 许可证

MIT License

---

## 更新日志

| 日期 | 版本 | 更新内容 |
|------|------|----------|
| 2026-04-12 | v1.0 | 初始版本，基础温度对比 |
| 2026-04-13 | v1.1 | 添加天气状况 KPI |
| 2026-04-15 | v1.2 | 接入和风天气穿衣指数 |
| 2026-04-16 | v2.0 | HUD 科技风界面重设计 |

---

*文档生成时间: 2026-04-19*
