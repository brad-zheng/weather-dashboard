# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Read HEAD version from git
with open('git_head.html', 'r', encoding='utf-8', errors='replace') as f:
    head_content = f.read()

# Read local version
with open('index.html', 'r', encoding='utf-8', errors='replace') as f:
    local_content = f.read()

print('=== HEAD (remote pushed) version: 行 678-720 ===')
for i, ln in enumerate(head_content.split('\n')):
    if 677 <= i <= 719:
        print(f'{i+1}: {ln[:100]}')

print('\n=== 本地 index.html: 行 678-720 ===')
for i, ln in enumerate(local_content.split('\n')):
    if 677 <= i <= 719:
        print(f'{i+1}: {ln[:100]}')