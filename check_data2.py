# -*- coding: utf-8 -*-
import re

with open('data.js', 'r', encoding='utf-8') as f:
    data = f.read()

# Find Beijing's data
beijing_start = data.find('"北京"')
if beijing_start > 0:
    # Find the next city to limit search
    next_city = data.find('"上海"', beijing_start)
    beijing_section = data[beijing_start:next_city]

    # Find all year keys (24, 25, 26)
    year_keys = re.findall(r'"(24|25|26)"\s*:', beijing_section)
    print(f"Year keys found: {year_keys}")

    # Find first occurrence of each year
    for yk in ['26', '25', '24']:
        idx = beijing_section.find(f'"{yk}"')
        if idx > 0:
            # Get context around this year
            context = beijing_section[idx:idx+200]
            print(f"\n{yk} context: ...{context[:150]}...")

    # Find time arrays for year 26
    idx26 = beijing_section.find('"26"')
    if idx26 > 0:
        section26 = beijing_section[idx26:idx26+500]
        # Find max array (has numbers)
        max_match = re.search(r'"max"\s*:\s*\[([^\]]+)\]', section26)
        if max_match:
            max_vals = max_match.group(1)[:200]
            print(f"\n26 max values (first 200 chars): {max_vals}...")
        time_match = re.search(r'"time"\s*:\s*\[([^\]]+)\]', section26)
        if time_match:
            time_vals = time_match.group(1)[:300]
            print(f"\n26 time values (first 300 chars): {time_vals}...")
else:
    print("Beijing not found")
