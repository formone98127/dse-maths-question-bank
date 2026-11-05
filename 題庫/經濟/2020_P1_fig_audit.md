# 2020 經濟 P1 ENG — 圖核對表

**狀態（2026-11-05）**：12 張圖檔凍結（PNG／SVG／MD embed **唔准改**）。MD 已按 2014 式重洗（原文對頁；圖序跟原卷；檔頭誠實：**7 張有 §9.4 check 數字 + 5 張語義／樣板核**）。

## A. 7 張有 §9.4 雙向 check.json

| 題號 | dir1% | dir2% | maxdev | p99.9 | 依據檔 |
|---|---:|---:|---:|---:|---|
| Q16 | 99.996 | 99.695 | 2.24 | 2.00 | `fig_2020P1_q16_check.json` |
| Q18 | 99.616 | 100.000 | 2.83 | 2.24 | `fig_2020P1_q18_check.json` |
| Q20 | 99.762 | 99.765 | 2.24 | 2.24 | `fig_2020P1_q20_check.json` |
| Q28 | 100.000 | 100.000 | 2.00 | 1.41 | `fig_2020P1_q28_check.json` |
| Q31 | 99.992 | 100.000 | 2.24 | 1.41 | `fig_2020P1_q31_check.json` |
| Q36 | 99.944 | 99.912 | 2.24 | 2.00 | `fig_2020P1_q36_check.json` |
| Q43 | 99.868 | 99.917 | 2.83 | 2.24 | `fig_2020P1_q43_check.json` |

## B. 5 張語義／樣板核（無完整 §9.4 雙向 check.json）

| 題號 | 核對類型 | 依據（磁碟） | 要點 |
|---|---|---|---|
| Q6 | 語義核（Nightmare 收樣板） | `fig_2020P1_q6_meta.json` | method=`semantic_geometry`；SVG image=0／base64=0／path=33／text=10 |
| Q14 | 樣板核（skeleton §9） | `fig_2020P1_q14_meta.json` | maxdev_px=1.40；coverage=100%；pass=true；SVG 真向量 |
| Q21 | 語義核（Nightmare 收 UI） | `fig_2020P1_q21_meta.json` | method=`semantic_ui`；SVG image=0／base64=0／path=16／text=15 |
| Q22 | 語義量度核（Nightmare 收 Lorenz） | `fig_2020P1_q22_meta.json` | method=`semantic_lorenz_measured`；curve_a maxdev_px=1；Country A/B 每 2% ink-snap |
| Q26 | 樣板核（skeleton §9） | `fig_2020P1_q26_meta.json` | maxdev_px=1.40；coverage=100%；pass=true；SVG 真向量 |

路徑前綴：`_work_econ_ocr\2020_fig_diff\`。
