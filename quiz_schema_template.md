# DSE Hub — Quiz Schema 範本（Google Practice Problems 富媒體）

> **已實現**：`scripts/build_quiz_pages.py` 會由逐題頁嘅 QAPage JSON-LD 自動抽取題目、選項同答案，生成全卷操練頁（而家有 `/math/2012/paper-2/quiz/` 同 `/math/2012/paper-2-en/quiz/`），每頁附完整 `Quiz` schema。
> 下面保留手動範本作參考；新增有逐題頁嘅卷，行一次 `python scripts/build_quiz_pages.py` 即可。

## 用途

喺每張 MC 卷頁（例如 `/math/2012/paper-2-en/`、`/math/2024/paper-2/`）加入 `Quiz` 結構化資料，令 Google 有機會喺搜尋結果直接顯示「操題」卡片（Practice Problems rich result）——對題庫站嚟講係最有價值嘅富媒體位。

## 先決條件（Google 會驗證，唔做會被當 spam）

1. 頁面上必須**可見**題目同答案——schema 內容要同頁面文字一致，用 CSS 收埋嘅答案唔可以入 schema。
2. 每張卷一個 `Quiz`；`hasPart` 放嗰卷全部題目（MC 卷 45 題 = 45 個 `Question`）。
3. 正確答案用 `acceptedAnswer`；其餘 3 個選項全部放 `suggestedAnswer`。
4. 卷頁已有答案／解析區塊先好用呢個範本（例如 paper-2-en 系列，q 頁有「正確答案＋深度解析」）。

## 範本（貼喺卷頁 `<head>`，或用 build script 由 `docs/data.js` 生成）

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Quiz",
  "name": "DSE 數學 2012 卷二（英文）MC 操卷",
  "description": "DSE 數學必修部分 2012 年卷二 45 題選擇題，附答案同逐題解析，即時核對。",
  "url": "https://hkdse.exampaper.cloud/math/2012/paper-2-en/",
  "inLanguage": "en-HK",
  "isAccessibleForFree": true,
  "dateModified": "2026-11-16",
  "educationalAlignment": {
    "@type": "AlignmentObject",
    "alignmentType": "educationalSubject",
    "targetName": "HKDSE Mathematics Compulsory Part",
    "targetUrl": "https://www.hkeaa.edu.hk/"
  },
  "hasPart": [
    {
      "@type": "Question",
      "position": 1,
      "eduQuestionType": "Multiple choice",
      "name": "DSE 數學 2012 卷二第 1 題（指數法則）",
      "text": "〔貼上題目全文，同頁面一字不差〕",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "〔正確選項字母＋答案文字〕"
      },
      "suggestedAnswer": [
        { "@type": "Answer", "text": "〔錯誤選項文字〕" },
        { "@type": "Answer", "text": "〔錯誤選項文字〕" },
        { "@type": "Answer", "text": "〔錯誤選項文字〕" }
      ]
    },
    {
      "@type": "Question",
      "position": 2,
      "eduQuestionType": "Multiple choice",
      "name": "DSE 數學 2012 卷二第 2 題",
      "text": "〔貼上題目全文〕",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "〔正確答案〕"
      },
      "suggestedAnswer": [
        { "@type": "Answer", "text": "〔錯誤選項〕" },
        { "@type": "Answer", "text": "〔錯誤選項〕" },
        { "@type": "Answer", "text": "〔錯誤選項〕" }
      ]
    }
  ]
}
</script>
```

## 部署檢查清單

- `text` 同頁面顯示嘅題目要**一字不差**（符號、LaTeX 格式都要一致）。
- `position` 由 1 開始順序排，唔好跳號。
- 卷一（長題目）唔啱用 `Quiz`——卷一頁可以考慮 `LearningResource`＋`MathSolver` 組合（進階方案，需要時另開一版）。
- 貼完去 https://search.google.com/test/rich-results 驗證，輸入卷頁 URL，應該出「Practice problems」結果。
- **唔建議人手維護 45 題 JSON**：已由 `scripts/build_quiz_pages.py` 自動生成（見上文）。要新增卷：確認逐題頁（`q*/index.html`）存在，喺 script 嘅 `PAPERS` 加入該卷，再行 `python scripts/build_quiz_pages.py`。

## 備註：同 Dataset schema 嘅分工

- `Dataset`（已加喺 `/math/` 頁）：描述成個題庫集合，幫 Google 理解站內有咩檔案（PDF 分佈、年份範圍、授權）。
- `Quiz`（本範本，放每張卷頁）：搶 Practice Problems 富媒體位，直接喺 SERP 顯示操題。
- 兩者唔衝突，可以並存喺唔同頁面。
