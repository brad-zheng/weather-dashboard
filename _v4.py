# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\39930\.qclaw\workspace-agent-2de6b33c\weather-dashboard\index.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# 找到 IIFE 的 })(); 并在其前面添加 DOMContentLoaded 包装
# 原始结尾: });  (line 590)
# 目标结尾: window.addEventListener('DOMContentLoaded', () => { init(); });
old_end = '    initMainSearch();\n    renderPickerList(cityList);\n});'
new_end = '''    initMainSearch();
    renderPickerList(cityList);
});
window.addEventListener('DOMContentLoaded', () => { init(); });'''

if old_end in content:
    content = content.replace(old_end, new_end, 1)
    print('DOMContentLoaded wrapper added OK')
else:
    print('Pattern not found!')
    idx = content.find('renderPickerList')
    if idx >= 0:
        print(repr(content[idx-50:idx+200]))

with open(r'C:\Users\39930\.qclaw\workspace-agent-2de6b33c\weather-dashboard\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
