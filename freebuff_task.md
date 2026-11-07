# freebuff 本輪任務：第 2 層掃卷（生物 2024）— OCR＋清洗＋crop

你係本機 Free AI coding assistant。跟 `OCR_WORKFLOW.md` §0.1 做 **第 2 層文字交貨**。只跑一輪就停。

## 已完成（唔使重做）
- 化學 2012～2025 中文三卷已上線（`化學\2012_*` … `2025_*`）。
- 生物 2023、物理 2024 已上線。
- 生物 2024 尚未開工。

## 你要做
1. 用 PyMuPDF 由源 PDF 渲染 300dpi 頁圖到 `_work_bio2024\pages_300\`（卷一／卷二分開前綴）。
2. 用 easyocr（ch_tra+en，GPU）做 OCR → `_work_bio2024\ocr_raw\`／`ocr_json\`。
3. 清洗成題庫 MD（零答案；去頁眉頁碼雜訊），格式對照 `生物\2023_P1_QU(CHI).md`／`2023_P2_QU(CHI).md`：
   - `生物\2024_P1_QU(CHI).md`
   - `生物\2024_P2_QU(CHI).md`
4. 有圖：由 `pages_300` 做 300dpi crop，放入對應 `生物\2024_*_crops\`，並嵌入 MD。**唔做**向量重繪／§9。截唔到標圖待補。
5. 檔頭寫「本檔為第 2 層文字交貨（圖用原卷截圖；精修重繪另開第 3 層）。」
6. `python qa_md_format.py` 要 exit 0。
7. **唔** build_index／commit／push。
8. 完成後寫 `_work_bio2024\FREEBUFF_DONE.txt`：一行 `bio2024 layer2 done` + 題數／截圖數摘要，然後停。

## 源 PDF
- `dsepaper_hk\生物\2024\文憑試 DSE 生物 Biology 2024 歷屆試題 Past Paper Paper 1.pdf`
- `dsepaper_hk\生物\2024\文憑試 DSE 生物 Biology 2024 歷屆試題 Past Paper Paper 2.pdf`

**唔用：** Model Answers／參考答案／考生表現／考評報告。

若 PDF 主要係英文卷而唔係中文，寫明喺 FREEBUFF_DONE 後停，唔硬做。
