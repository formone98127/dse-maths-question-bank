# DSE 數學題庫

DSE 數學必修部分電子題庫 — 題目清洗（Markdown + LaTeX）＋ 插圖 matplotlib 1:1 向量重繪（SVG）＋ 線上檢索。

**線上檢索**（官方網站）：https://hkdse.exampaper.cloud/ （Hub：https://hkdse.exampaper.cloud/hub/）。按關鍵字、年份、卷別、題目、解答同課題標籤篩選。GitHub Pages 亦有獨立複本，但對外請用官方網址。

## 內容

| 檔案 | 說明 |
|---|---|
| `2012_P1_題目中文卷.md` | 2012 卷一 19 題（題目庫，零答案） |
| `2013_P1_QU(CHI).md` | 2013 卷一 19 題（題目庫，零答案） |
| `2014_P1_QU(CHI).md` | 2014 卷一 19 題（題目庫，零答案） |
| `2012_II_解答.md` | 2012 卷二 45 題詳解 + 答案速查表 |
| `2013_II_解答.md` | 2013 卷二 45 題詳解 + 答案速查表 |
| `2012_P1_figs_svg/` `2013P1_figs_svg/` `2014P1_figs_svg/` | 重繪插圖（SVG + 200dpi PNG） |
| `make_2012P1_figs.py` `make_2013P1_figs.py` `make_2014P1_figs.py` | 插圖重繪腳本（matplotlib，座標數學反算 / 量度原卷 crop） |
| `build_index.py` | 檢索 index 產生器（MD → `docs/data.js`） |
| `docs/index.html` | 檢索網頁（GitHub Pages root） |

## 更新檢索 index

新增／修改 MD 題目後：

```bash
python build_index.py
```

自動 parse 所有題目／解答檔，重建 `docs/data.js`。commit + push 後 Pages 即時更新。

## 新增一年題庫

1. 原卷 PDF（掃描版）→ PyMuPDF render 頁面 → 逐頁影像轉寫清洗成 `<年>_P<n>_QU(CHI).md`（【建議標籤】+【題目內容】，零答案）
2. 插圖：原卷 crop 量度座標 → matplotlib 重繪 → `<年><卷>_figs_svg/`
3. `python build_index.py` → push

## 版權說明

本 repo **只含清洗後成品**（題目文字 + 重繪向量圖）。HKEAA 原卷 PDF、掃描頁、原卷裁圖已由 `.gitignore` 排除，不上網。內容僅供學習用途。
