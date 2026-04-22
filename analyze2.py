# -*- coding: utf-8 -*-
import re

DATA_PATH = r'C:\Users\39930\.qclaw\workspace-agent-2de6b33c\weather-dashboard\data.js'
with open(DATA_PATH, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

wd_start = content.find('WEATHER_DATA = {')

for city in ['北京', '上海']:
    ci = content.find('"' + city + '"', wd_start)
    if ci < 0:
        continue
    # 找26年数据块的范围
    chunk = content[ci:ci+5000]
    yr26_start = chunk.find('"26":')
    if yr26_start >= 0:
        yr26_end = chunk.find('},', yr26_start)
        yr26_chunk = chunk[yr26_start:yr26_end]
        print('\n' + city + ' 26年数据块:')
        print(yr26_chunk[:400])
        dates = re.findall(r'"(20\d{2}-\d{2}-\d{2})"', yr26_chunk)
        if dates:
            print('日期: ' + dates[0] + ' ~ ' + dates[-1] + ' (' + str(len(dates)) + ' days)')
            print('最后5个: ' + str(dates[-5:]))
            print('含今天(2026-04-22):', '2026-04-22' in dates)
        else:
            print('未找到日期')
    else:
        print(city + ' 无26年数据')
