# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\39930\.qclaw\workspace-agent-2de6b33c\weather-dashboard\index.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

checks = [
    ('data.js defer', 'defer' in content[content.find('data.js'):content.find('data.js')+30] if 'data.js' in content else False),
    ('DOMContentLoaded', 'DOMContentLoaded' in content),
    ('IIFE定义', '})();' in content),
    ('headerTitle已删除', 'headerTitle' not in content),
    ('d顺序正确', 'const d = cityData[yearKeys[2]]' in content),
    ('wmoText正确', 'const wmoText = window.WMO_TEXT_MAP' in content),
    ('k3直接赋值', "document.getElementById('k3').textContent" in content),
]
for name, ok in checks:
    print(('OK' if ok else 'FAIL') + ' - ' + name)
