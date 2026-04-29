# -*- coding: utf-8 -*-
import re

with open('data.js', 'r', encoding='utf-8') as f:
    data = f.read()

# Find WEATHER_DATA section
weather_start = data.find('WEATHER_DATA')
if weather_start > 0:
    # Find Beijing section
    beijing_start = data.find('"北京"', weather_start)
    # Find next city
    shanghai_start = data.find('"上海"', beijing_start)
    beijing_weather = data[beijing_start:shanghai_start]

    print(f"Beijing weather section length: {len(beijing_weather)}")

    # Find "26" year data
    idx26 = beijing_weather.find('"26"')
    if idx26 > 0:
        section26 = beijing_weather[idx26:idx26+100]
        print(f"\n'26' found at: {section26[:80]}")
    else:
        print("'26' not found in Beijing weather")

    # Find time array
    time_match = re.search(r'"time":\s*\[([^\]]+)\]', beijing_weather)
    if time_match:
        times_str = time_match.group(1)
        times = [t.strip().strip('"') for t in times_str.split(',')]
        print(f"\nTotal dates: {len(times)}")
        print(f"First 5: {times[:5]}")
        print(f"Last 5: {times[-5:]}")

        # Check if 2026-04-29 exists
        if "2026-04-29" in times:
            idx = times.index("2026-04-29")
            print(f"\n2026-04-29 found at index {idx}")
        else:
            print("\n2026-04-29 NOT found")
            # Show dates around 2026-04
            dates_2026 = [t for t in times if "2026" in t]
            print(f"Dates with 2026: {dates_2026[-10:] if dates_2026 else 'none'}")
