# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\39930\.qclaw\workspace-agent-2de6b33c\weather-dashboard\index.html', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
print('=== data.js ===')
for i,l in enumerate(lines):
    if 'data.js' in l: print(f'{i+1}: {repr(l[:200])}')
print('=== DOMContentLoaded ===')
for i,l in enumerate(lines):
    if 'DOMContentLoaded' in l: print(f'{i+1}: {repr(l[:200])}')
print('=== k3 area (lines 718-738) ===')
for i in range(717, min(len(lines), 738)):
    print(f'{i+1}: {repr(lines[i][:200])}')
