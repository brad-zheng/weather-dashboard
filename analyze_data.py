# -*- coding: utf-8 -*-
import re

DATA_PATH = r'C:\Users\39930\.qclaw\workspace-agent-2de6b33c\weather-dashboard\data.js'
with open(DATA_PATH, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# DATA_DATE
m = re.search(r'DATA_DATE\s*=\s*"(.*?)"', content)
print('DATA_DATE:', m.group(1) if m else 'not found')

# yearKeys 逻辑：Object.keys(cityData).sort().slice(-3)
# 所以即使 25/26 是 null，只要 key 存在就排在前面
wd_start = content.find('WEATHER_DATA = {')

for city in ['北京', '上海', '广州']:
    ci = content.find('"' + city + '"', wd_start)
    if ci < 0:
        continue
    chunk = content[ci:ci+2000]
    # 找该城市所有年份 key
    yr_entries = re.findall(r'"(\d+)":\s*(?:\{|null)', chunk)
    print('\n' + city + ' year keys:', yr_entries)

    all_yrs = sorted(yr_entries)
    year_keys = all_yrs[-3:]
    print('  yearKeys:', year_keys)
    print('  yearKeys[2]:', year_keys[2] if len(year_keys) > 2 else 'N/A')

    for yr in year_keys:
        yr_start = chunk.find('"' + yr + '":')
        if yr_start >= 0:
            t_start = chunk.find('time:', yr_start)
            if t_start >= 0:
                dates = re.findall(r'"(20\d{2}-\d{2}-\d{2})"', content[t_start:t_start+500])
                if dates:
                    print(f'  {yr}: {dates[0]} ~ {dates[-1]} ({len(dates)} days)')
