# Math skills schema（本地基礎）

## 檔案

- `math_skill_book.json` — 固定技能冊（課題／知識點／公式／能力）
- `math_tag_crosswalk.json` — 題庫 tag → 技能冊 20 課題（不改網站既有 tag）
- `math_question_cards.json` — 統一題卡（由 `scripts/build_question_cards.py` 產生）
- `math_error_tags.json` — 錯法短標籤目錄（同上腳本產生）
- `math_cards_index.json` — 按課題／錯法索引題卡 id（同上腳本產生）

## 統一題卡（`math_question_cards.json`）

每題一張卡，合併題庫、逐題頁、分析檔：

| 欄位 | 說明 |
|---|---|
| `id` | `math-{year}-p{paper}-q{qno}` |
| `bank_tags` | 網站原本課題字串（不變） |
| `hub_topics` | 經 crosswalk 歸入嘅 20 大課題 |
| `primary_hub_topic` | 第一個成功對上嘅大課題 |
| `answer` / `answer_pct` | 官方答案、全港答對率 |
| `option_errors` | 錯選項 → `error_tags`（短標籤）+ `detail` |
| `report_errors` | 考評報告抽出嘅常見錯法 |
| `skills` | 若分析檔有 skills 就附上（而家 2012 P2 試點） |
| `stream` | `compulsory`（必修卷一／二）或 `m1`（延伸部分） |

備註：20 大課題只覆蓋必修。M1 標籤（微分法、正態分佈等）暫時留喺 `unmapped_tags`，唔強迫歸入必修課題。

重建：

```text
python scripts/build_math_skill_foundation.py
python scripts/build_question_cards.py
```

## 每題 `skills` 欄位（分析檔）

加喺 `docs/analysis/.../qN.json` 頂層（同 `analysis` 並列）：

```json
{
  "skills": {
    "topic_id": "T-EXP",
    "knowledge_point_ids": ["K-EXP-01"],
    "formula_ids": ["F-EXP-03"],
    "ability_ids": ["A-ALG"],
    "option_faults": {
      "A": {
        "knowledge_point_id": "K-EXP-02",
        "formula_id": "F-EXP-03",
        "ability_id": "A-ALG"
      }
    }
  }
}
```

規則：

1. 所有 id 必須存在於技能冊。
2. 正確選項唔寫入 `option_faults`。
3. 每個錯選項恰好一個 `ability_id`；`knowledge_point_id` 或 `formula_id` 至少一個非 null。
4. `formula_id` 若有，其 `knowledge_point_id` 應屬於同一課題網絡（可跨課題引用先備知識）。

## 驗證

```text
python scripts/validate_skills.py
python scripts/validate_skills.py --path docs/analysis/math/2012/paper-2
python scripts/build_question_cards.py --check
```
