/* 由 scripts/build_trap_cards.py 產生；源檔 trap_cards.md；唔好手改 */
window.TRAP_CARDS = {
 "generated": "2026-11-23 00:27",
 "deck_version": "trap-v1",
 "count": 10,
 "strands": {
  "數與代數": [
   "百分法",
   "指數與對數",
   "比、率與比例",
   "多項式（續）",
   "數系",
   "方程與不等式",
   "函數與圖像",
   "數列",
   "變分"
  ],
  "度量、圖形與空間": [
   "三角學與解三角形",
   "求積法",
   "坐標幾何：直線",
   "坐標幾何：圓",
   "圓形幾何",
   "軌跡",
   "幾何變換"
  ],
  "數據處理": [
   "統計圖表",
   "集中趨勢與離差",
   "概率",
   "排列與組合"
  ]
 },
 "cards": [
  {
   "id": "EXP-001",
   "topic": "指數與對數",
   "strand": "數與代數",
   "statement": "對任意實數 $a$，都有 $a^0 = 0$。",
   "is_trap": true,
   "hint": "喂！任何非零數嘅 0 次方係 1，唔係 0 啊！",
   "difficulty": 1
  },
  {
   "id": "EXP-002",
   "topic": "指數與對數",
   "strand": "數與代數",
   "statement": "$$\\log(x+y) = \\log x + \\log y$$",
   "is_trap": true,
   "hint": "log 只拆得乘除，加減拆唔開㗎！",
   "difficulty": 2
  },
  {
   "id": "NUM-003",
   "topic": "數系",
   "strand": "數與代數",
   "statement": "$$1.\\overline{3} = \\frac{4}{3}$$",
   "is_trap": false,
   "hint": "冇伏！設 $x=1.333\\ldots$，$10x-x=12$，$x=\\frac43$。",
   "difficulty": 1
  },
  {
   "id": "PER-004",
   "topic": "百分法",
   "strand": "數與代數",
   "statement": "一件貨標價 \\$100，先加 10%，再減 10%，就會返返原價 \\$100。",
   "is_trap": true,
   "hint": "110 減 10% 係 99 啊——加減嘅基數唔同！",
   "difficulty": 2
  },
  {
   "id": "STA-005",
   "topic": "集中趨勢與離差",
   "strand": "數據處理",
   "statement": "一組數據每項同時加 5，標準差會增加 5。",
   "is_trap": true,
   "hint": "全體一齊移，離散度冇變，SD 唔會變！",
   "difficulty": 2
  },
  {
   "id": "PROB-006",
   "topic": "概率",
   "strand": "數據處理",
   "statement": "若事件 $A$ 與 $B$ 獨立，則 $P(A \\cap B) = P(A) \\times P(B)$。",
   "is_trap": false,
   "hint": "冇伏！呢句正正係獨立事件嘅定義。",
   "difficulty": 1
  },
  {
   "id": "TRI-007",
   "topic": "三角學與解三角形",
   "strand": "度量、圖形與空間",
   "statement": "$$\\sin 2\\theta = 2\\sin\\theta$$",
   "is_trap": true,
   "hint": "$\\sin 2\\theta = 2\\sin\\theta\\cos\\theta$，唔可以就咁乘大兩倍！",
   "difficulty": 2
  },
  {
   "id": "GEO-008",
   "topic": "圓形幾何",
   "strand": "度量、圖形與空間",
   "statement": "同一弧上，圓周角的度數是圓心角的一半。",
   "is_trap": false,
   "hint": "冇伏！圓心角 = 2 × 圓周角（同弧）。",
   "difficulty": 2
  },
  {
   "id": "COD-009",
   "topic": "坐標幾何：直線",
   "strand": "度量、圖形與空間",
   "statement": "兩條互相垂直的直線，其斜率的乘積等於 1。",
   "is_trap": true,
   "hint": "垂直係 $m_1 m_2 = -1$，乘 1 係平行先啱！",
   "source_ref": "2012P2Q25",
   "difficulty": 3
  },
  {
   "id": "MEN-010",
   "topic": "求積法",
   "strand": "度量、圖形與空間",
   "statement": "圓錐的體積是同底同高圓柱的一半。",
   "is_trap": true,
   "hint": "係 $\\frac{1}{3}$，唔係 $\\frac{1}{2}$——錐體係三分一！",
   "difficulty": 3
  }
 ]
};
