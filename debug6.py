# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('data.js', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# 找到北京当前年的数据
idx = content.find('"北京"')
# 跳过CITIES块，找到WEATHER_DATA
wd_idx = content.find('WEATHER_DATA = {')
if wd_idx < 0:
    print('WEATHER_DATA not found')
else:
    # 找到北京在WEATHER_DATA中的位置
    beijing_idx = content.find('"北京"', wd_idx)
    if beijing_idx < 0:
        print('北京 not found in WEATHER_DATA')
    else:
        # 找北京数据块的结束（下一个城市或者}）
        chunk = content[beijing_idx:beijing_idx+800]
        print('北京数据块前500字符:')
        print(chunk[:500])
        
        # 检查时间数组中是否包含今天
        import datetime
        today = datetime.date.today().strftime('%Y-%m-%d')
        print(f'\n今天日期: {today}')
        
        # 找"26"年份数据（今年）
        year_26_idx = content.find('"26":', beijing_idx)
        if year_26_idx > 0:
            yr_chunk = content[year_26_idx:year_26_idx+400]
            print(f'\n今年数据 (26):')
            print(yr_chunk[:400])
            
            # 检查是否包含今天
            if today in yr_chunk:
                print(f'\n✅ 今天({today})在数据中')
                # 找今天对应的索引
                time_idx = yr_chunk.find('time:')
                if time_idx >= 0:
                    time_chunk = yr_chunk[time_idx:]
                    dates = []
                    in_array = False
                    for ch in time_chunk:
                        if ch == '[': in_array = True
                        elif ch == ']': break
                        elif ch == '"' and in_array:
                            pass  # 简单检查
                    # 用正则
                    import re
                    dates_found = re.findall(r'"(2026-\d{2}-\d{2})"', yr_chunk[:300])
                    print(f'日期样例: {dates_found[:5]}')
            else:
                print(f'\n❌ 今天({today})不在数据中')
                # 找最后几个日期
                import re
                all_dates = re.findall(r'"(2026-\d{2}-\d{2})"', content[beijing_idx:beijing_idx+2000])
                if all_dates:
                    print(f'北京今年最近的日期: {all_dates[-5:]}')