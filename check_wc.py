# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 找北京的数据
idx = content.index('北京')
chunk = content[idx:idx+600]
print(chunk[:400])

# 检查data.js里的wc字段
print('\n\n--- 检查 wc 字段 ---')
# 找第一个有 wc 的地方
wc_idx = content.find('wc:')
if wc_idx >= 0:
    print(f'wc 首次出现位置: {wc_idx}')
    print(content[wc_idx:wc_idx+200])