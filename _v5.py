# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\39930\.qclaw\workspace-agent-2de6b33c\weather-dashboard\index.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

idx_iife = content.find('})();')
idx_dcl = content.find('DOMContentLoaded')
print('IIFE at: ' + str(idx_iife))
print('DOMContentLoaded at: ' + str(idx_dcl))

if idx_iife >= 0:
    print('Around IIFE:')
    print(repr(content[idx_iife-100:idx_iife+100]))

if idx_dcl >= 0:
    print('Around DOMContentLoaded:')
    print(repr(content[idx_dcl-50:idx_dcl+200]))

print('data.js defer: ' + str('defer' in content[content.find('data.js'):content.find('data.js')+30] if 'data.js' in content else False))
print('d order: ' + str('const d = cityData[yearKeys[2]]' in content))
print('wmoText: ' + str('const wmoText = window.WMO_TEXT_MAP' in content))
