# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding='utf-8')

PATH = r'C:\Users\39930\.qclaw\workspace-agent-2de6b33c\weather-dashboard\index.html'
with open(PATH, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# ──────────────────────────────────────────────────────────────
# Fix 1: init() 缺少 DOMContentLoaded，改为 DOMContentLoaded 包裹
# ──────────────────────────────────────────────────────────────
old1 = "window.addEventListener('load', () => {\n    const firstCity = Object.keys(WEATHER_DATA)[0];"
new1 = "window.addEventListener('DOMContentLoaded', () => {\n    init();\n});\nwindow.addEventListener('load', () => {\n    const firstCity = Object.keys(WEATHER_DATA)[0];"

if old1 in content:
    content = content.replace(old1, new1, 1)
    print('Fix 1 OK: wrapped init() in DOMContentLoaded')
else:
    print('Fix 1 FAILED: pattern not found')
    # 看看实际内容
    idx = content.find("window.addEventListener('load'")
    if idx >= 0:
        print(repr(content[idx:idx+300]))

# ──────────────────────────────────────────────────────────────
# Fix 2: loadCity - d 声明顺序错误（我的 patch 写的顺序反了）
# 行 709 引用 d，行 710 才声明 const d = ...
# 修复：把 const d 声明移到行 709 之前
# ──────────────────────────────────────────────────────────────
old2 = """    document.getElementById('headerTitle').textContent = '>>> ' + name + ' data OK yr=' + yearKeys[2] + ' len=' + (d ? d.time.length : 'N/A');
    const d = cityData[yearKeys[2]];
    if (!d || !d.time || d.time.length === 0) {
        showToast('⚠️ 今年数据尚未更新，请等待下次采集');
        return;
    }

    const today = new Date().toISOString().split('T')[0];
    const idx = d.time.findIndex(t => t === today);"""

new2 = """    const d = cityData[yearKeys[2]];
    if (!d || !d.time || d.time.length === 0) {
        showToast('⚠️ 今年数据尚未更新，请等待下次采集');
        return;
    }
    // DEBUG: 更新状态栏显示
    document.getElementById('dataStatusText').textContent = '[loadCity] yr=' + yearKeys[2] + ' d.len=' + d.time.length;

    const today = new Date().toISOString().split('T')[0];
    const idx = d.time.findIndex(t => t === today);"""

if old2 in content:
    content = content.replace(old2, new2, 1)
    print('Fix 2 OK: d declaration order fixed')
else:
    print('Fix 2 FAILED: pattern not found')
    idx = content.find("cityData[yearKeys[2]]")
    if idx >= 0:
        print(repr(content[idx-200:idx+400]))

# ──────────────────────────────────────────────────────────────
# Fix 3: initMainSearch 中的 headerTitle → 改用 dataStatusText
# ──────────────────────────────────────────────────────────────
old3 = """    mainSearchCtrl = createCitySearch(inp, drop, (name) => {
        // visible debug: write state to header title so user can see
        const yk = WEATHER_DATA[name] ? Object.keys(WEATHER_DATA[name]).sort().slice(-3) : [];
        document.getElementById('headerTitle').textContent = '>>> ' + name + ' yearKeys=' + yk.join(',') + ' LOADING...';
        loadCity(name);
    }, clr);"""

new3 = """    mainSearchCtrl = createCitySearch(inp, drop, (name) => {
        // DEBUG: 更新状态栏显示选中的城市
        const yk = WEATHER_DATA[name] ? Object.keys(WEATHER_DATA[name]).sort().slice(-3) : [];
        document.getElementById('dataStatusText').textContent = '[select] ' + name + ' yr=' + yk.join(',') + ' LOADING...';
        loadCity(name);
    }, clr);"""

if old3 in content:
    content = content.replace(old3, new3, 1)
    print('Fix 3 OK: headerTitle → dataStatusText')
else:
    print('Fix 3 FAILED: pattern not found')

# ──────────────────────────────────────────────────────────────
# Fix 4: loadCity k3 赋值区 — headerTitle → dataStatusText
# ──────────────────────────────────────────────────────────────
old4 = """        // DEBUG: visible output - user can see this directly on the page
        const wmoStatus = window.WMO_TEXT_MAP ? (window.WMO_TEXT_MAP[wc] || '? NO_MAP_ENTRY(wc='+wc+')') : 'ERR_MAP_UNDEFINED';
        const debugInfo = `[k3] wc=${wc} map=${window.WMO_TEXT_MAP ? 'OK' : 'MISSING'} result=${wmoStatus} idx=${idx} yearKeys2=${yearKeys[2]} dtime=${d ? d.time.length : 'N/A'}`;
        document.getElementById('headerTitle').textContent = debugInfo;
        document.getElementById('k3').textContent = 'W' + wc + '=' + wmoStatus;"""

new4 = """        // DEBUG: 显示在状态栏，用户可见
        const wmoStatus = window.WMO_TEXT_MAP ? (window.WMO_TEXT_MAP[wc] || '? NO_MAP(wc='+wc+')') : 'ERR_MAP_UNDEF';
        document.getElementById('dataStatusText').textContent = '[k3] wc=' + wc + ' map=' + (window.WMO_TEXT_MAP ? 'OK' : 'MISSING') + ' result=' + wmoStatus;
        document.getElementById('k3').textContent = (wc !== null && wc !== undefined && window.WMO_TEXT_MAP) ? window.WMO_TEXT_MAP[wc] : '--';"""

if old4 in content:
    content = content.replace(old4, new4, 1)
    print('Fix 4 OK: k3 headerTitle → dataStatusText')
else:
    print('Fix 4 FAILED: pattern not found')
    idx4 = content.find('const wmoStatus')
    if idx4 >= 0:
        print(repr(content[idx4-100:idx4+300]))

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)
print('All done')
