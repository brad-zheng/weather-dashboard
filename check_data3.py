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
    print(f"Beijing section length: {len(beijing_section)}")
    print(f"First 300 chars: {beijing_section[:300]}")

    # Find time array
    time_match = re.search(r'"time"\s*:\s*\[([^\]]+)\]', beijing_section)
    if time_match:
        times_str = time_match.group(1)
        times = [t.strip().strip('"') for t in times_str.split(',')]
        print(f"\nTotal dates: {len(times)}")
        print(f"First 5: {times[:5]}")
        print(f"Last 5: {times[-5:]}")
        # Check if 2026-04-29 exists
        if "2026-04-29" in times:
            idx = times.index("2026-04-29")
            print(f"2026-04-29 found at index {idx}")
        else:
            print("2026-04-29 NOT found")
            if "2026" in str(times):
                print("2026 dates found, showing last few:")
                dates_2026 = [t for t in times if "2026" in t]
                print(dates_2026[-5:] if dates_2026 else "none")
else:
    print("Beijing not found")
