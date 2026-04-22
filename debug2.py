# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 找 WMO_TEXT 所有出现位置
print('=== WMO_TEXT 相关代码 ===')
for i, line in enumerate(content.split('\n')):
    if 'WMO_TEXT' in line:
        print(f'行 {i+1}: {line}')

print('\n=== 查找 loadCity 中 k3 相关代码 ===')
idx = content.find('loadCity')
if idx >= 0:
    chunk = content[idx:idx+1000]
    for line in chunk.split('\n')[:40]:
        if any(k in line for k in ['k3', 'k4', 'wc', 'dress', 'WMO']):
            print(line)