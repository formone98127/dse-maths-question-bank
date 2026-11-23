#!/usr/bin/env python3
"""為 papers.js 內每個 PDF 生成 SEO 下載著陸頁 docs/download/<sid>/<stem>.html。
   stem = item.u 去 /papers/ 前綴同 .pdf 後綴。"""
import json, re, os
from xml.sax.saxutils import escape, quoteattr

ROOT = '/home/one/hub_repo/docs'
BASE = 'https://hkdse.exampaper.cloud'

# 讀 papers.js
s = open(f'{ROOT}/hub/papers.js', encoding='utf-8').read()
P = json.loads(s[s.index('{'):s.rindex('}')+1])

KIND = {'ms': '評卷參考', 'paper': '試卷', 'report': '考評報告', 'mock': '模擬試卷'}
KIND_FALLBACK = {'ms': 'Marking Scheme', 'paper': 'Paper', 'report': 'Report', 'mock': 'Mock'}
LANG = {'zh': '中文卷', 'en': '英文卷', 'na': ''}

def stem_of(u):
    return u.replace('/papers/', '').replace('.pdf', '')

def page_path(sid, u):
    return f'/download/{stem_of(u)}.html'

pages = []  # (url, title)

for sid, subj in P['subjects'].items():
    name = subj['name']
    for it in subj['items']:
        u = it['u']
        stem = stem_of(u)
        y = it['y']
        kind = it['k']
        paper = it.get('p', '')
        lang = it.get('l', 'na')
        kindzh = KIND.get(kind, kind)
        paperlbl = f' Paper {paper}' if paper else ''
        langlbl = LANG.get(lang, '')

        title = f"{name} {y} {kindzh}{paperlbl}{' '+langlbl if langlbl else ''} PDF 免費下載｜DSE Hub"
        desc = f"{name} {y} 年{kindzh}{paperlbl}（{langlbl or '中英文'}）官方歷屆試題 PDF 免費下載，含答案與評卷參考，即按即下載。"

        # 相關連結：hub 該科
        hub_href = f"/hub/?subject={sid}&mode=year&year={y}"
        dl_href = u  # 實際 PDF

        html = f'''<!DOCTYPE html>
<html lang="zh-Hant-HK">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{BASE}{page_path(sid, u)}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:type" content="website">
<script type="application/ld+json">{{
  "@context":"https://schema.org",
  "@type":"WebPage",
  "name":{quoteattr(title)},
  "description":{quoteattr(desc)}
}}</script>
<style>
body{{font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:0;color:#1a1a2e;background:#f5f6fa}}
main{{max-width:640px;margin:0 auto;padding:24px 16px}}
.breadcrumb{{font-size:13px;color:#666;margin-bottom:16px}}
.breadcrumb a{{color:#2d6cdf;text-decoration:none}}
h1{{font-size:24px;line-height:1.4;margin:0 0 8px}}
.desc{{color:#555;font-size:15px;margin:0 0 24px}}
.meta{{background:#fff;border:1px solid #e2e5ee;border-radius:10px;padding:16px;margin-bottom:24px}}
.meta .row{{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #f0f1f5;font-size:14px}}
.meta .row:last-child{{border:none}}
.meta .k{{color:#888}}
.dl{{display:block;text-align:center;background:#2d6cdf;color:#fff;font-size:17px;font-weight:600;padding:15px;border-radius:10px;text-decoration:none}}
.dl:hover{{background:#2458b8}}
.note{{font-size:12px;color:#999;text-align:center;margin-top:12px}}
</style>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-LTB27V0RGW"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-LTB27V0RGW');</script>
</head>
<body>
<main>
<nav class="breadcrumb"><a href="/">首頁</a> › <a href="/hub/">DSE Hub</a> › <a href="{hub_href}">{escape(name)} {y}</a></nav>
<h1>{escape(title)}</h1>
<p class="desc">{escape(desc)}</p>
<div class="meta">
  <div class="row"><span class="k">科目</span><span>{escape(name)}</span></div>
  <div class="row"><span class="k">年份</span><span>{y}</span></div>
  <div class="row"><span class="k">類型</span><span>{escape(kindzh)}</span></div>
  {f'<div class="row"><span class="k">卷別</span><span>{escape(paper)}</span></div>' if paper else ''}
  <div class="row"><span class="k">語言</span><span>{escape(langlbl or '—')}</span></div>
</div>
<a class="dl" href="{dl_href}" download>下載 PDF</a>
<p class="note">檔案為官方歷屆試題（PDF），版權屬香港考試及評核局。</p>
</main>
</body>
</html>
'''
        # 寫檔
        rel = f'download/{stem}.html'
        path = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        pages.append((page_path(sid, u), title))

print('生成下載頁', len(pages))
# 寫 manifest 供 sitemap / hub 參考
with open(f'{ROOT}/download/_manifest.json', 'w', encoding='utf-8') as f:
    json.dump(pages, f, ensure_ascii=False)

# 生成 sitemap-download.xml
lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for url, _ in pages:
    lines.append(f'  <url><loc>{escape(BASE + url)}</loc></url>')
lines.append('</urlset>')
with open(f'{ROOT}/sitemap-download.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')
print('sitemap-download.xml 寫入', len(pages), 'URL')
