# -*- coding: utf-8 -*-
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('data.js', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# 找北京的 WEATHER_DATA
wd_idx = content.find('WEATHER_DATA = {')
if wd_idx < 0:
    print('WEATHER_DATA not found')
else:
    beijing_idx = content.find('"北京"', wd_idx)
    chunk = content[beijing_idx:beijing_idx+1200]
    
    # 找今年数据块
    year_26_idx = chunk.find('"26":')
    if year_26_idx > 0:
        yr_chunk = chunk[year_26_idx:year_26_idx+600]
        print('=== 北京今年数据块 ===')
        print(yr_chunk[:600])
        
        # 统计日期范围
        dates = re.findall(r'"(2026-\d{2}-\d{2})"', yr_chunk)
        if dates:
            print(f'\n日期范围: {dates[0]} ~ {dates[-1]}')
            print(f'共 {len(dates)} 天')
            print(f'今天 2026-04-22: {"存在" if "2026-04-22" in dates else "不存在"}')
    else:
        print('未找到今年数据 26')
        # 找所有年份key
        years = re.findall(r'"(\d+)":', chunk[:300])
        print(f'找到的年份: {years}')
        
        # 打印chunk前500字符
        print('\nchunk前500:')
        print(chunk[:500])