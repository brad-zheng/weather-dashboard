#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天气数据抓取脚本
从 Open-Meteo API 拉取全国城市天气数据，输出 data.js
每天自动执行，由 GitHub Actions 调用
"""
import json
import os
import sys
import time
import subprocess
from datetime import datetime, date

# ── 配置 ──────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CITIES_FILE = os.path.join(SCRIPT_DIR, "cities.json")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "data.js")

# 默认抓取的城市列表（留空则抓全部，支持按需减少加快速度）
TARGET_CITIES = []  # 例如 ["北京","上海","广州"] 留空=全部城市

# Open-Meteo API 地址
ARCHIVE_API = "https://archive-api.open-meteo.com/v1/archive"
FORECAST_API = "https://api.open-meteo.com/v1/forecast"

# 和风天气 API（从环境变量读取）
QWEATHER_API = "https://devapi.qweather.com/v7/indices/1d"
QWEATHER_KEY = os.environ.get("QWEATHER_KEY", "")
# ─────────────────────────────────────────────────────

def rt(v):
    """四舍五入到整数"""
    return round(float(v)) if v is not None else None

def date_str(d):
    """date → ISO字符串 YYYY-MM-DD"""
    return d.strftime("%Y-%m-%d")

def fmt_date(d):
    """date → M/D 格式"""
    return f"{d.month}/{d.day}"

def build_date_range(year):
    """构建历史数据日期范围（今天±14天，同一季节对比）"""
    today = date.today()
    start = date(year, today.month, today.day)
    end = date(year, today.month, today.day)
    # ±14天
    s = date(start.year, today.month, today.day) - __import__("datetime").timedelta(days=14)
    e = date(end.year, today.month, today.day) + __import__("datetime").timedelta(days=14)
    return date_str(s), date_str(e)

def fetch_json(url, params=None):
    """带重试的 HTTP GET"""
    import urllib.request, urllib.parse, urllib.error
    if params:
        url += "?" + urllib.parse.urlencode(params)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"  [警告] 请求失败（第{attempt+1}次）: {e}")
            time.sleep(3)
    return None

def fetch_weather_history(city_name, lat, lng, year):
    """抓取某城市某年的历史天气（今天±14天）"""
    s, e = build_date_range(year)
    params = {
        "latitude": lat,
        "longitude": lng,
        "start_date": s,
        "end_date": e,
        "daily": "temperature_2m_max,temperature_2m_min,weather_code,wind_speed_10m_max",
        "timezone": "Asia/Shanghai"
    }
    data = fetch_json(ARCHIVE_API, params)
    if not data or data.get("error"):
        return None
    daily = data.get("daily")
    if not daily:
        return None
    return {
        "time": daily.get("time", []),
        "max": [rt(v) for v in daily.get("temperature_2m_max", [])],
        "min": [rt(v) for v in daily.get("temperature_2m_min", [])],
        "wc": daily.get("weather_code", []),
        "ws": [rt(v) for v in daily.get("wind_speed_10m_max", [])]
    }

def fetch_dressing_index(lat, lng):
    """从和风天气抓取穿衣指数（type=3），返回 {date: category} 映射"""
    if not QWEATHER_KEY:
        print("  [警告] 未配置 QWEATHER_KEY，跳过穿衣指数")
        return {}
    params = {
        "location": f"{lng},{lat}",
        "type": "3",
        "key": QWEATHER_KEY
    }
    data = fetch_json(QWEATHER_API, params)
    if not data or data.get("code") != "200":
        print(f"  [警告] 和风天气请求失败: {data}")
        return {}
    result = {}
    for item in data.get("daily", []):
        result[item["date"]] = item.get("category", "")
    print(f"  穿衣指数: {result}")
    return result

def fetch_weather_current_year(city_name, lat, lng):
    """抓取当前年数据：历史部分用 archive + 未来部分用 forecast，合并"""
    today = date.today()
    past14 = today - __import__("datetime").timedelta(days=14)
    future14 = today + __import__("datetime").timedelta(days=14)
    yesterday = today - __import__("datetime").timedelta(days=1)

    archive_s = date_str(past14)
    archive_e = date_str(yesterday)
    fore_s = date_str(today)
    fore_e = date_str(future14)

    # 并行请求（urllib 不支持并发，顺序请求）
    arch_params = {
        "latitude": lat, "longitude": lng,
        "start_date": archive_s, "end_date": archive_e,
        "daily": "temperature_2m_max,temperature_2m_min,weather_code,wind_speed_10m_max",
        "timezone": "Asia/Shanghai"
    }
    fore_params = {
        "latitude": lat, "longitude": lng,
        "start_date": fore_s, "end_date": fore_e,
        "daily": "temperature_2m_max,temperature_2m_min,weather_code,wind_speed_10m_max",
        "timezone": "Asia/Shanghai"
    }

    arch_data = fetch_json(ARCHIVE_API, arch_params)
    fore_data = fetch_json(FORECAST_API, fore_params)

    arch_daily = (arch_data.get("daily") or {}) if arch_data and not arch_data.get("error") else {}
    fore_daily = (fore_data.get("daily") or {}) if fore_data and not fore_data.get("error") else {}

    merged = {
        "time": list(arch_daily.get("time", [])) + list(fore_daily.get("time", [])),
        "max": [rt(v) for v in list(arch_daily.get("temperature_2m_max", [])) + list(fore_daily.get("temperature_2m_max", []))],
        "min": [rt(v) for v in list(arch_daily.get("temperature_2m_min", [])) + list(fore_daily.get("temperature_2m_min", []))],
        "wc": list(arch_daily.get("weather_code", [])) + list(fore_daily.get("weather_code", [])),
        "ws": [rt(v) for v in list(arch_daily.get("wind_speed_10m_max", [])) + list(fore_daily.get("wind_speed_10m_max", []))]
    }

    # 和风天气穿衣指数（只查一次，复用到当年数据所有日期）
    dress_map = fetch_dressing_index(lng, lat)
    if dress_map:
        merged["dress"] = [dress_map.get(t, "") for t in merged["time"]]

    return merged if merged["time"] else None

def fetch_city(city_name, lat, lng, current_year):
    """抓取一个城市三年数据"""
    d24 = fetch_weather_history(city_name, lat, lng, current_year - 2)
    d25 = fetch_weather_history(city_name, lat, lng, current_year - 1)
    d26 = fetch_weather_current_year(city_name, lat, lng)
    # 礼貌限速
    time.sleep(0.5)
    return {"24": d24, "25": d25, "26": d26}

def generate_js(data, timestamp):
    """生成 data.js 文件内容"""
    lines = [
        "// ============================================",
        "// 天气数据文件 - 自动生成，请勿手动编辑",
        f"// 生成时间: {timestamp}",
        "// 数据来源: Open-Meteo API + 和风天气生活指数",
        "// ============================================",
        "",
        "// 城市列表（含经纬度）",
        f"const CITIES = {json.dumps(data['cities'], ensure_ascii=False, indent=2)};",
        "",
        "// 各城市天气数据",
        "const WEATHER_DATA = {",
    ]

    for city, info in data["weather"].items():
        lines.append(f'  "{city}": {{')
        for year_key, year_data in info.items():
            if year_data:
                lines.append(f'    "{year_key}": {{')
                lines.append(f'      time: {json.dumps(year_data["time"])},')
                lines.append(f'      max:  {json.dumps(year_data["max"])},')
                lines.append(f'      min:  {json.dumps(year_data["min"])},')
                lines.append(f'      wc:   {json.dumps(year_data.get("wc", []))},')
                lines.append(f'      ws:   {json.dumps(year_data.get("ws", []))},')
                lines.append(f'      dress: {json.dumps(year_data.get("dress", []))},')
                lines.append('    },')
            else:
                lines.append(f'    "{year_key}": null,')
        lines.append('  },')

    lines.append("};")
    lines.append("")
    lines.append("// 数据更新日期")
    lines.append(f"const DATA_DATE = \"{timestamp}\";")
    lines.append("")

    return "\n".join(lines)

def main():
    print("=" * 50)
    print("  天气数据抓取脚本")
    print("=" * 50)
    print()

    # 1. 加载城市列表
    if not os.path.exists(CITIES_FILE):
        print(f"[错误] 找不到 cities.json: {CITIES_FILE}")
        sys.exit(1)

    with open(CITIES_FILE, "r", encoding="utf-8") as f:
        cities = json.load(f)

    # 按需筛选
    if TARGET_CITIES:
        cities = {k: v for k, v in cities.items() if k in TARGET_CITIES}

    print(f"[1/2] 加载了 {len(cities)} 个城市，开始抓取数据...")
    print()

    current_year = date.today().year
    weather = {}
    total = len(cities)
    success = 0
    failed = []

    for i, (city_name, info) in enumerate(cities.items(), 1):
        print(f"  [{i}/{total}] 正在抓取: {city_name} ({info['province']})", end=" ... ")
        try:
            result = fetch_city(city_name, info["lat"], info["lng"], current_year)
            weather[city_name] = result
            if result.get("26"):
                success += 1
                print("✓")
            else:
                failed.append(city_name)
                print("⚠ 无当年数据")
        except Exception as e:
            failed.append(city_name)
            print(f"✗ {e}")

    print()
    print(f"[2/2] 生成 data.js ...")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "cities": cities,
        "weather": weather
    }

    js_content = generate_js(data, timestamp)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"      输出文件: {OUTPUT_FILE}")
    print(f"      文件大小: {os.path.getsize(OUTPUT_FILE) / 1024:.1f} KB")
    print()
    print(f"  成功: {success}/{total} 个城市")
    if failed:
        print(f"  失败: {', '.join(failed[:10])}{'...' if len(failed) > 10 else ''}")

    print()
    print("=" * 50)
    print("  完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()
