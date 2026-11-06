# freebuff 本輪任務：第 2 層掃卷（化學 2018 中文）— OCR＋清洗＋crop

你係本機 Free AI coding assistant。跟 `OCR_WORKFLOW.md` §0.1 做 **第 2 層文字交貨**。

## 已完成（唔使重做）
- 化學 2019 三卷已上線（`化學\2019_*`）。

## 你要做
1. 由源 PDF 渲染 300dpi 頁圖（可放 `_work_chem2018\pages_300\`），跑 OCR（easyocr ch_tra+en／GPU）。
2. 清洗成三份題庫 MD（零答案；化學式 Unicode 下標；去頁眉頁碼雜訊）：
   - `化學\2018_P1A_QU(CHI).md`（甲部 MC，通常 36 題）
   - `化學\2018_P1B_QU(CHI).md`（乙部結構題）
   - `化學\2018_P2_QU(CHI).md`（卷二）
3. 有圖：由 `pages_300` 做 300dpi crop，放入對應 `化學\2018_*_crops\`，並嵌入 MD。**唔做**向量重繪／§9。截唔到標圖待補。
4. 檔頭寫「本檔為第 2 層文字交貨（圖用原卷截圖；精修重繪另開第 3 層）。」
5. 格式對照 `化學\2019_*_QU(CHI).md`／`2020_*`。
6. `python qa_md_format.py` 要 exit 0。
7. **唔** build_index／commit／push。
8. 完成後寫 `_work_chem2018\FREEBUFF_DONE.txt`：一行 `chem2018 layer2 done` + 題數／截圖數摘要，然後停。

## 源 PDF（只用中文卷）
- `dsepaper_hk\化學\2018\文憑試 DSE 化學 Chemistry 2018 歷屆試題 Past Paper 卷一.pdf`
- `dsepaper_hk\化學\2018\文憑試 DSE 化學 Chemistry 2018 歷屆試題 Past Paper 卷二.pdf`

**唔用：** Model Answers／參考答案／考生表現／英文 Paper 1／Paper 2。
