#!/usr/bin/env python3
"""為 docs/ 下欠缺 GA4 tag 的頁面注入 gtag（G-LTB27V0RGW）。
   只插 </head> 之前；已有 tag 的跳過。"""
import os, glob

TAG_ID = 'G-LTB27V0RGW'
SNIPPET = f'''<script async src="https://www.googletagmanager.com/gtag/js?id={TAG_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{TAG_ID}');
</script>
'''

ROOT = '/home/one/hub_repo/docs'

def inject(path):
    s = open(path, encoding='utf-8').read()
    if TAG_ID in s:
        return False
    i = s.lower().find('</head>')
    if i < 0:
        return False
    s = s[:i] + SNIPPET + s[i:]
    open(path, 'w', encoding='utf-8').write(s)
    return True

added = skipped = 0
for p in glob.glob(f'{ROOT}/**/*.html', recursive=True):
    if inject(p):
        added += 1
    else:
        skipped += 1
print(f'inject GA: 新增 {added} 頁，已有 {skipped} 頁')
