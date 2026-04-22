# -*- coding: utf-8 -*-
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('data.js', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# 找北京的完整数据块
wd_idx = content.find('WEATHER_DATA = {')
beijing_idx = content.find('"北京"', wd_idx)
# 找北京数据块的结尾
end_idx = content.find('},', beijing_idx + 50)
chunk = content[beijing_idx:end_idx+2]

print('=== 北京完整数据块 ===')
print(chunk[:1500])

# 找所有年份key
years = re.findall(r'"(\d+)":', chunk)
print(f'\n年份列表: {years}')

# 检查最近更新的日期
all_dates = re.findall(r'"(202\d-\d{2}-\d{2})"', chunk)
if all_dates:
    print(f'\n所有日期范围: {all_dates[0]} ~ {all_dates[-1]}')
    print(f'共 {len(all_dates)} 条')
    print(f'最新日期: {all_dates[-1]}')