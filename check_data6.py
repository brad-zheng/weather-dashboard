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

    # Find "26" year data section
    idx26 = beijing_weather.find('"26":')
    if idx26 > 0:
        # Extract the "26" section
        section26 = beijing_weather[idx26:]
        # Find the closing brace by counting braces
        depth = 0
        end_idx = 0
        for i, c in enumerate(section26):
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    end_idx = i
                    break
        section26_data = section26[:end_idx+1]
        print(f"Section 26 length: {len(section26_data)}")
        print(f"First 300 chars: {section26_data[:300]}")

        # Find time array in section 26
        time_match = re.search(r'"time":\s*\[([^\]]+)\]', section26_data)
        if time_match:
            times_str = time_match.group(1)
            times = [t.strip().strip('"') for t in times_str.split(',')]
            print(f"\n2026 data - Total dates: {len(times)}")
            print(f"First 5: {times[:5]}")
            print(f"Last 5: {times[-5:]}")

            # Check if 2026-04-29 exists
            if "2026-04-29" in times:
                idx = times.index("2026-04-29")
                print(f"\n2026-04-29 found at index {idx}")
            else:
                print("\n2026-04-29 NOT found")
                print(f"Last 3 dates: {times[-3:]}")
