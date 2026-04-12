# 天气数据看板

全国 300+ 城市天气数据可视化，支持三年同期温度对比与多城市横向对比。

## 在线访问

部署完成后访问：`https://brad-zheng.github.io/weather-dashboard/`

## 架构说明

```
weather-dashboard/
├── .github/workflows/daily-weather.yml  ← GitHub Actions 定时任务（每天自动抓取数据）
├── data_fetch.py                        ← Python 数据层脚本（从 Open-Meteo API 抓数据）
├── cities.json                          ← 全国城市经纬度数据
├── data.js                              ← 自动生成（勿手动编辑）
├── index.html                           ← 前端页面
└── README.md
```

## 数据层架构（方案 B）

- **定时任务**：GitHub Actions 每天凌晨 3:00（北京时间）自动运行 `data_fetch.py`
- **数据来源**：Open-Meteo API（免费，无需 API Key）
- **输出**：生成 `data.js`，包含全国城市 ±14 天历史 + 预报温度
- **前端**：纯静态 HTML，读取本地 `data.js` 渲染图表，无需服务器

**你的电脑不需要一直开着** — 定时任务在 GitHub 服务器上跑，数据部署到 GitHub Pages，全球可访问。

## 首次部署步骤

### 第一步：上传文件到 GitHub

1. 打开 https://github.com/brad-zheng/weather-dashboard
2. 点击 **Add file** → **Upload files**
3. 把本地 `weather-dashboard` 文件夹里的所有文件拖进去
4. 点击 **Commit changes**

### 第二步：开启 GitHub Pages

1. 在仓库页面点击 **Settings**（右上角 Settings）
2. 左侧菜单找到 **Pages**
3. **Source** 选 **Deploy from a branch**
4. **Branch** 选 **main**，目录选 **/ (root)**
5. 点击 **Save**
6. 等 1-2 分钟，页面显示 `Your site is published` 后即可访问

### 第三步：验证 Actions 自动任务

1. 进入仓库 → **Actions** 标签页
2. 看到 "每日天气数据更新" 工作流
3. 点击 **Run workflow** → **Run workflow** 可以手动触发一次
4. 任务完成后检查 `data.js` 是否有内容

> GitHub Actions 免费额度：每月 2000 分钟，对于这个项目（每次运行约 5-10 分钟）完全够用。

## 本地测试

如果你想在本地先跑一遍数据脚本：

```bash
pip install requests
python data_fetch.py
```

然后直接用浏览器打开 `index.html` 即可（本地测试需要先把 `data.js` 生成好）。

## 自定义城市

修改 `cities.json`，添加/删除城市即可。支持全国任意有经纬度的城市。

## 依赖技术

- [Tailwind CSS](https://tailwindcss.com/)（CDN）
- [Chart.js](https://www.chartjs.org/)（CDN）
- [chartjs-plugin-annotation](https://github.com/chartjs/chartjs-plugin-annotation)（CDN）
- [html2canvas](https://html2canvas.hertzen.com/)（CDN）
- [Open-Meteo API](https://open-meteo.com/)（免费天气数据）
