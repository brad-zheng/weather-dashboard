# -*- coding: utf-8 -*-
import subprocess, sys
repo = r'C:\Users\39930\.qclaw\workspace-agent-2de6b33c\weather-dashboard'
result = subprocess.run(['git', 'status', '--short'], cwd=repo, capture_output=True, text=True, encoding='utf-8', errors='replace')
print(result.stdout)
print(result.stderr)
if result.returncode != 0:
    sys.exit(1)

# Stage all
subprocess.run(['git', 'add', '-A'], cwd=repo)

# Commit
msg = 'fix: resolve TDZ errors, add DOMContentLoaded, fix k3 WMO display'
result2 = subprocess.run(['git', 'commit', '-m', msg], cwd=repo, capture_output=True, text=True, encoding='utf-8', errors='replace')
print(result2.stdout)
print(result2.stderr)
if result2.returncode != 0:
    sys.exit(1)
print('COMMIT DONE')
