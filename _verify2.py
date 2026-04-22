# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\39930\.qclaw\workspace-agent-2de6b33c\weather-dashboard\index.html', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
for i,l in enumerate(lines):
    if 'DOMContentLoaded' in l or ('load' in l and 'Event' in l):
        print(f'{i+1}: {repr(l[:200])}')
for i in range(583, 592):
    print(f'{i+1}: {repr(lines[i][:200])}')
