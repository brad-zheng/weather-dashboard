# -*- coding: utf-8 -*-
import re

with open('data.js', 'r', encoding='utf-8') as f:
    data = f.read()

# Find WEATHER_DATA section
weather_start = data.find('WEATHER_DATA')
if weather_start > 0:
    # Get a larger section
    section = data[weather_start:weather_start+2000]
    print(f"First 500 chars of WEATHER_DATA: {section[:500]}")

    # Find first city
    first_city = re.search(r'"(\u5317\u4eac|\u4e0a\u6d77|BJ|SH)"', section)
    if first_city:
        print(f"\nFirst city match: {first_city.group()}")

    # Look for pattern like "北京": {"24": {"time":
    m = re.search(r'"[^"]+":\s*\{\s*"[^"]+":\s*\{\s*"time":', section)
    if m:
        print(f"\nFound nested structure: {m.group()}")
