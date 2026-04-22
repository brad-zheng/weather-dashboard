# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding='utf-8')

PATH = r'C:\Users\39930\.qclaw\workspace-agent-2de6b33c\weather-dashboard\index.html'
with open(PATH, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# ──────────────────────────────────────────────────────────────
# Fix A: 外部脚本加 defer — 确保 DOM 完全解析后再执行
# ──────────────────────────────────────────────────────────────
# 先把 <script src="data.js"> 改成 defer
OLD_SCRIPT_DATA = '<script src="data.js">'
NEW_SCRIPT_DATA = '<script src="data.js" defer>'
if OLD_SCRIPT_DATA in content:
    content = content.replace(OLD_SCRIPT_DATA, NEW_SCRIPT_DATA, 1)
    print('Fix A OK: data.js +defer')
else:
    print('Fix A FAILED')

# 把内联脚本也加上 defer，确保在 defer data.js 之后执行
# 找到 <script>（行560的内联脚本开头），改成 defer
# 由于有多个 <script>，找包含 "let yearKeys" 或 "const currentYear" 的那个
OLD_SCRIPT_INLINE = '<script>\n// ── 年份常量'
NEW_SCRIPT_INLINE = '<script defer>\n// ── 年份常量'
if OLD_SCRIPT_INLINE in content:
    content = content.replace(OLD_SCRIPT_INLINE, NEW_SCRIPT_INLINE, 1)
    print('Fix A2 OK: inline script +defer')
else:
    print('Fix A2 FAILED')

# ──────────────────────────────────────────────────────────────
# Fix B: IIFE → DOMContentLoaded
# init() 现在在 DOM 完全解析后才执行，TDZ 不再是问题
# ──────────────────────────────────────────────────────────────
OLD_IIFE = "})();\n\n// ── 数据状态 ─"
NEW_IIFE = """    initMainSearch();
    renderPickerList(cityList);
});
\n// ── 数据状态 ─"""

if OLD_IIFE in content:
    content = content.replace(OLD_IIFE, NEW_IIFE, 1)
    print('Fix B OK: IIFE → DOMContentLoaded')
else:
    print('Fix B FAILED')
    idx = content.find('})();')
    if idx >= 0:
        print(repr(content[idx-50:idx+200]))

# ──────────────────────────────────────────────────────────────
# Fix C: loadCity - k3 调试代码替换为正确版本
# 移除旧调试代码，恢复正确逻辑
# ──────────────────────────────────────────────────────────────
# 找到 k3 相关代码块（多行）
import re
# 匹配 k3 调试代码块
old_k3 = """        // DEBUG: visible output - user can see this directly on the page
        const wmoStatus = window.WMO_TEXT_MAP ? (window.WMO_TEXT_MAP[wc] || '? NO_MAP_ENTRY(wc='+wc+')') : 'ERR_MAP_UNDEFINED';
        const debugInfo = `[k3] wc=${wc} map=${window.WMO_TEXT_MAP ? 'OK' : 'MISSING'} result=${wmoStatus} idx=${idx} yearKeys2=${yearKeys[2]} dtime=${d ? d.time.length : 'N/A'} days`;
        document.getElementById('headerTitle').textContent = debugInfo;
        document.getElementById('k3').textContent = 'W' + wc + '=' + wmoStatus;"""
new_k3 = """        // k3: 天气状况（使用 WMO_TEXT_MAP 显示中文）
        const wmoText = window.WMO_TEXT_MAP ? (window.WMO_TEXT_MAP[wc] || '--') : '--';
        document.getElementById('dataStatusText').textContent = '[k3] wc=' + wc + ' → ' + wmoText;
        document.getElementById('k3').textContent = (wc !== null && wc !== undefined && window.WMO_TEXT_MAP) ? window.WMO_TEXT_MAP[wc] : '--';"""
if old_k3 in content:
    content = content.replace(old_k3, new_k3, 1)
    print('Fix C OK: k3 debug → correct')
else:
    print('Fix C FAILED')
    # 尝试另一种匹配
    idx_c = content.find("const wmoStatus")
    if idx_c >= 0:
        print('Found wmoStatus at:', repr(content[idx_c-50:idx_c+300]))

# ──────────────────────────────────────────────────────────────
# Fix D: initMainSearch - headerTitle → dataStatusText
# ──────────────────────────────────────────────────────────────
old_is = """    document.getElementById('headerTitle').textContent = '>>> ' + name + ' yearKeys=' + yk.join(',') + ' LOADING...';"""
new_is = """    document.getElementById('dataStatusText').textContent = '[select] ' + name + ' yr=' + yk.join(',') + ' LOADING...';"""
if old_is in content:
    content = content.replace(old_is, new_is, 1)
    print('Fix D OK: headerTitle → dataStatusText')
else:
    print('Fix D FAILED - already patched?')

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)
print('All done')
