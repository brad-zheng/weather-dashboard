# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Read HEAD version from git
import subprocess
result = subprocess.run(['git', 'show', 'HEAD:index.html'], capture_output=True)
content = result.stdout.decode('utf-8', errors='replace')

for i, ln in enumerate(content.split('\n')):
    if i+1 in range(678, 720):
        print(f'{i+1}: {ln[:100]}')