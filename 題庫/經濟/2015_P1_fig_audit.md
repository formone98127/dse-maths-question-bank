# 2015 經濟 P1 ENG — 圖核對表

**2026-11-05 重洗**：來源改對英文 `Paper 1.pdf`；頁影像 `_work_econ_ocr\2015_P1_ENG_pages_300\`；OCR `2015_P1_ENG_ocr_v2`（easyocr en）。舊 `2015_pages_300`／壞 OCR 係中文卷一，已棄用。

§9.4 含抗鋸齒容差（maxdev≤2.9、p99.9≤2.5；超標只限 ≤8px 孤立斑點）。`check.json` 的 `pass`＝`pass_dir1`∧`pass_dir2`∧`pass_aa`。

| 題號 | 頁 | dir1% | dir2% | maxdev | p99.9 | pass_aa | 狀態 |
|---|---|---:|---:|---:|---:|---|---|
| Q15 | p05 | 99.599 | 99.748 | **5.83** | **4.48** | false | **待重繪**（dir1 unmatched area=24 @ 9×5 塊，非孤立 AA）；已撤 embed |
| Q19 | p07 | 99.746 | 100.000 | **4.12** | **2.86** | false | **待重繪**（p99.9>2.5；標籤／線偏）；已撤 embed |
| Q22 | p08 | 99.872 | 100.000 | 2.24 | 2.24 | true | **過關**；MD 有 embed |
| Q27 | p10 | 99.888 | 100.000 | 2.83 | 2.24 | true | **過關**；MD 有 embed（A–D 圖選項） |
| Q28 | p10 | 99.967 | 100.000 | 2.24 | 2.00 | true | **過關**；MD 有 embed |
| Q37 | p13 | 99.912 | 100.000 | 2.24 | 2.00 | true | **過關**；MD 有 embed |

- MD 檔頭：**4/6**（唔寫「6 張已 100%」）。
- check：`_work_econ_ocr\2015_fig_diff\fig_2015P1_q{N}_check.json`。
- **Q45（p15）無圖**：原卷純文字 MC。
