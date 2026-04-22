# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_loadcity = False
start = 0
for i, line in enumerate(lines):
    if 'function loadCity' in line:
        in_loadcity = True
        start = i
        break

if in_loadcity:
    print(f'loadCity 起始行: {start+1}')
    for i in range(start, min(start+100, len(lines))):
        ln = lines[i].rstrip('\r\n')
        if any(k in ln for k in ['k1','k2','k3','k4','wc','dress','WMO','max','min']):
            print(f'{i+1}: {ln[:120]}')