# -*- coding: utf-8 -*-
import re

PATH = r'C:\Users\39930\.qclaw\workspace-agent-2de6b33c\weather-dashboard\index.html'
with open(PATH, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# ── Patch 1: initMainSearch — 在页面顶部写入调试信息 ─────────────
OLD = "    mainSearchCtrl = createCitySearch(inp, drop, (name) => { loadCity(name); }, clr);"
NEW = """    mainSearchCtrl = createCitySearch(inp, drop, (name) => {
        // visible debug: write state to header title so user can see
        const yk = WEATHER_DATA[name] ? Object.keys(WEATHER_DATA[name]).sort().slice(-3) : [];
        document.getElementById('headerTitle').textContent = '>>> ' + name + ' yearKeys=' + yk.join(',') + ' LOADING...';
        loadCity(name);
    }, clr);"""

if OLD not in content:
    print('ERROR: patch target 1 not found')
    with open(r'C:\Users\39930\.qclaw\workspace-agent-2de6b33c\weather-dashboard\_patch1.txt','w',encoding='utf-8') as f:
        f.write(content[content.find('mainSearchCtrl'):content.find('mainSearchCtrl')+400])
else:
    content = content.replace(OLD, NEW, 1)
    print('Patched initMainSearch')

# ── Patch 2: loadCity — 替换 k3 赋值，加入可见调试信息 ──────────
# 找到并替换 k3 那行
OLD2 = "        document.getElementById('k3').textContent = (wc !== null && wc !== undefined) ? (window.WMO_TEXT_MAP[wc] || '?') : '--';\n        // DEBUG: 直接覆盖 k3 显示调试信息（上线后删除此行）\n        document.getElementById('k3').textContent = `W${wc}=${window.WMO_TEXT_MAP ? window.WMO_TEXT_MAP[wc] : 'ERR_MAP_UNDEF'}`;"
NEW2 = """        // DEBUG: visible output - user can see this directly on the page
        const wmoStatus = window.WMO_TEXT_MAP ? (window.WMO_TEXT_MAP[wc] || '? NO_MAP_ENTRY(wc='+wc+')') : 'ERR_MAP_UNDEFINED';
        const debugInfo = `[k3] wc=${wc} map=${window.WMO_TEXT_MAP ? 'OK' : 'MISSING'} result=${wmoStatus} idx=${idx} yearKeys2=${yearKeys[2]} dtime=${d ? d.time.length : 'N/A'} days`;
        document.getElementById('headerTitle').textContent = debugInfo;
        document.getElementById('k3').textContent = 'W' + wc + '=' + wmoStatus;"""

if OLD2 not in content:
    print('ERROR: patch target 2 not found')
    # 尝试找k3相关代码
    idx2 = content.find("getElementById('k3')")
    if idx2 >= 0:
        with open(r'C:\Users\39930\.qclaw\workspace-agent-2de6b33c\weather-dashboard\_patch2.txt','w',encoding='utf-8') as f:
            f.write(content[idx2-100:idx2+300])
else:
    content = content.replace(OLD2, NEW2, 1)
    print('Patched loadCity k3')

# ── Patch 3: loadCity 开头 - 显示 yearKeys ──────────────────────
OLD3 = "    const d = cityData[yearKeys[2]];\n    if (!d || !d.time || d.time.length === 0) {"
NEW3 = """    document.getElementById('headerTitle').textContent = '>>> ' + name + ' data OK yr=' + yearKeys[2] + ' len=' + (d ? d.time.length : 'N/A');
    const d = cityData[yearKeys[2]];
    if (!d || !d.time || d.time.length === 0) {"""

if OLD3 not in content:
    print('ERROR: patch target 3 not found')
else:
    content = content.replace(OLD3, NEW3, 1)
    print('Patched yearKeys header')

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
