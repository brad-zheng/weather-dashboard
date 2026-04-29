# -*- coding: utf-8 -*-
import re

with open('data.js', 'r', encoding='utf-8') as f:
    data = f.read()

# Find Beijing's 2026 data section
beijing_start = data.find('"北京"')
next_city = data.find('"上海"', beijing_start)
beijing_section = data[beijing_start:next_city]

# Find the "26" year data
m = re.search(r'"26"\s*:\s*\{[^}]*"time"\s*:\s*\[([^\]]+)\]', beijing_section)
if m:
    times_str = m.group(1)
    times = [t.strip().strip('"') for t in times_str.split(',')]
    print(f"Total dates: {len(times)}")
    print(f"First 5: {times[:5]}")
    print(f"Last 10: {times[-10:]}")
    # Check if 2026-04-29 exists
    if "2026-04-29" in times:
        idx = times.index("2026-04-29")
        print(f"2026-04-29 found at index {idx}")
    else:
        print("2026-04-29 NOT found in data")
        print(f"Closest dates: {times[-3:]}")
else:
    print("Could not find 2026 time data")
