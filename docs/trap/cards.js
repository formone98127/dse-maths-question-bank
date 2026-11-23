/* 由 scripts/build_trap_cards.py 產生；源檔 trap_cards.md；唔好手改 */
window.TRAP_CARDS = {
 "generated": "2026-11-23 00:55",
 "deck_version": "trap-v1",
 "count": 61,
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
   "id": "EXP-011",
   "topic": "指數與對數",
   "strand": "數與代數",
   "statement": "$$\\log_a (xy) = \\log_a x + \\log_a y \\quad (x>0,\\,y>0)$$",
   "is_trap": false,
   "hint": "冇伏！乘積嘅 log 先至可以拆做和。",
   "difficulty": 2
  },
  {
   "id": "EXP-012",
   "topic": "指數與對數",
   "strand": "數與代數",
   "statement": "$$(a^m)^n = a^{m+n}$$",
   "is_trap": true,
   "hint": "外層冪係乘指數：$(a^m)^n=a^{mn}$，加指數係 $a^m\\cdot a^n$！",
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
   "id": "NUM-013",
   "topic": "數系",
   "strand": "數與代數",
   "statement": "$\\sqrt{2}$ 是有理數，因為它可以寫成不盡根的形式。",
   "is_trap": true,
   "hint": "有理數要寫成 $\\frac{p}{q}$；$\\sqrt{2}$ 係經典無理數！",
   "difficulty": 2
  },
  {
   "id": "NUM-014",
   "topic": "數系",
   "strand": "數與代數",
   "statement": "$0.\\overline{9} = 1$",
   "is_trap": false,
   "hint": "冇伏！$0.999\\ldots$ 同 1 係同一個實數。",
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
   "id": "PER-015",
   "topic": "百分法",
   "strand": "數與代數",
   "statement": "成本 \\$80 嘅貨，加價 25% 後再八折出售，利潤率係 5%。",
   "is_trap": true,
   "hint": "$80\\times1.25\\times0.8=80$，打回原價——利潤率係 0%！",
   "difficulty": 2
  },
  {
   "id": "PER-016",
   "topic": "百分法",
   "strand": "數與代數",
   "statement": "本金 \\$1000、年利率 5% 單利，兩年利息共 \\$100。",
   "is_trap": false,
   "hint": "冇伏！單利每年都用原本金：$1000\\times5\\%\\times2=100$。",
   "difficulty": 1
  },
  {
   "id": "RAT-017",
   "topic": "比、率與比例",
   "strand": "數與代數",
   "statement": "若 $a:b=2:3$，則 $a+b:a-b=5:1$。",
   "is_trap": true,
   "hint": "$a=2k,\\,b=3k$ → $a+b:a-b=5k:(-k)$，比要留意符號／絕對值！",
   "difficulty": 2
  },
  {
   "id": "RAT-018",
   "topic": "比、率與比例",
   "strand": "數與代數",
   "statement": "若 $\\dfrac{a}{b}=\\dfrac{c}{d}$（$bd\\neq0$），則 $ad=bc$。",
   "is_trap": false,
   "hint": "冇伏！呢句正正係比例嘅交叉相乘。",
   "difficulty": 1
  },
  {
   "id": "RAT-019",
   "topic": "比、率與比例",
   "strand": "數與代數",
   "statement": "甲速 60 km/h、乙速 40 km/h，平均速率一定係 50 km/h。",
   "is_trap": true,
   "hint": "唔一定！唔同時間／路程要用加權，唔好直接平均兩個速度。",
   "difficulty": 2
  },
  {
   "id": "POL-020",
   "topic": "多項式（續）",
   "strand": "數與代數",
   "statement": "$(x+y)^2 = x^2 + y^2$",
   "is_trap": true,
   "hint": "漏咗中間 $2xy$！完整係 $x^2+2xy+y^2$。",
   "difficulty": 2
  },
  {
   "id": "POL-021",
   "topic": "多項式（續）",
   "strand": "數與代數",
   "statement": "$x^2 - y^2 = (x-y)(x+y)$",
   "is_trap": false,
   "hint": "冇伏！平方差公式就係咁。",
   "difficulty": 1
  },
  {
   "id": "POL-022",
   "topic": "多項式（續）",
   "strand": "數與代數",
   "statement": "若 $(x-2)$ 是 $f(x)$ 的因式，則 $f(2)=2$。",
   "is_trap": true,
   "hint": "因式定理：$f(2)=0$，唔係等於 2！",
   "difficulty": 2
  },
  {
   "id": "EQN-023",
   "topic": "方程與不等式",
   "strand": "數與代數",
   "statement": "解不等式時，兩邊同乘 $-1$，不等號方向唔使轉。",
   "is_trap": true,
   "hint": "乘／除負數一定要轉符號——呢個係大伏！",
   "difficulty": 2
  },
  {
   "id": "EQN-024",
   "topic": "方程與不等式",
   "strand": "數與代數",
   "statement": "二次方程 $ax^2+bx+c=0$（$a\\neq0$）的判別式是 $\\Delta=b^2-4ac$。",
   "is_trap": false,
   "hint": "冇伏！$\\Delta>0$ 兩實根，$\\Delta=0$ 重根，$\\Delta<0$ 無實根。",
   "difficulty": 1
  },
  {
   "id": "EQN-025",
   "topic": "方程與不等式",
   "strand": "數與代數",
   "statement": "由 $x^2=9$ 可得 $x=3$。",
   "is_trap": true,
   "hint": "仲有 $x=-3$！平方方程通常有兩個解。",
   "difficulty": 2
  },
  {
   "id": "FUN-026",
   "topic": "函數與圖像",
   "strand": "數與代數",
   "statement": "$y=f(x-2)$ 的圖像是 $y=f(x)$ 向左平移 2 單位。",
   "is_trap": true,
   "hint": "$x-2$ 係向右移 2！符號同直覺相反。",
   "difficulty": 2
  },
  {
   "id": "FUN-027",
   "topic": "函數與圖像",
   "strand": "數與代數",
   "statement": "拋物線 $y=a(x-h)^2+k$ 的頂點是 $(h,k)$。",
   "is_trap": false,
   "hint": "冇伏！頂點式直接讀出頂點坐標。",
   "difficulty": 2
  },
  {
   "id": "FUN-028",
   "topic": "函數與圖像",
   "strand": "數與代數",
   "statement": "函數 $f(x)=x^2$ 的反函數是 $f^{-1}(x)=\\sqrt{x}$。",
   "is_trap": true,
   "hint": "$x^2$ 唔係一對一，要限域先有反函數；而且仲有 $-\\sqrt{x}$。",
   "difficulty": 2
  },
  {
   "id": "SEQ-029",
   "topic": "數列",
   "strand": "數與代數",
   "statement": "等差數列第 $n$ 項公式是 $a_n = a_1 \\cdot d^{n-1}$。",
   "is_trap": true,
   "hint": "嗰條係等比！等差係 $a_n=a_1+(n-1)d$。",
   "difficulty": 2
  },
  {
   "id": "SEQ-030",
   "topic": "數列",
   "strand": "數與代數",
   "statement": "等比數列公比 $r\\neq1$ 時，前 $n$ 項和 $S_n=\\dfrac{a_1(1-r^n)}{1-r}$。",
   "is_trap": false,
   "hint": "冇伏！呢條係標準等比求和公式。",
   "difficulty": 1
  },
  {
   "id": "SEQ-031",
   "topic": "數列",
   "strand": "數與代數",
   "statement": "等差數列前 $n$ 項和一定係 $S_n=\\dfrac{n}{2}(a_1+a_n)$，所以末項唔知就計唔到。",
   "is_trap": true,
   "hint": "仲有 $S_n=\\dfrac{n}{2}[2a_1+(n-1)d]$，唔一定要知 $a_n$。",
   "difficulty": 2
  },
  {
   "id": "VAR-032",
   "topic": "變分",
   "strand": "數與代數",
   "statement": "若 $y$ 與 $x$ 成正比，則 $y=\\dfrac{k}{x}$（$k$ 為常數）。",
   "is_trap": true,
   "hint": "正比係 $y=kx$；$\\frac{k}{x}$ 係反比啊！",
   "difficulty": 2
  },
  {
   "id": "VAR-033",
   "topic": "變分",
   "strand": "數與代數",
   "statement": "若 $y$ 與 $x$ 成反比，則 $xy$ 為常數。",
   "is_trap": false,
   "hint": "冇伏！反比即 $y=\\frac{k}{x}$，所以 $xy=k$。",
   "difficulty": 1
  },
  {
   "id": "VAR-034",
   "topic": "變分",
   "strand": "數與代數",
   "statement": "若 $z$ 與 $x$ 正變、與 $y$ 反變，則 $z=kxy$。",
   "is_trap": true,
   "hint": "應該係 $z=\\dfrac{kx}{y}$——$y$ 反變要放分母！",
   "difficulty": 3
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
   "id": "TRI-035",
   "topic": "三角學與解三角形",
   "strand": "度量、圖形與空間",
   "statement": "在直角三角形中，$\\sin\\theta=\\dfrac{\\text{對邊}}{\\text{斜邊}}$。",
   "is_trap": false,
   "hint": "冇伏！SOH-CAH-TOA 入面 S 就係對／斜。",
   "difficulty": 1
  },
  {
   "id": "TRI-036",
   "topic": "三角學與解三角形",
   "strand": "度量、圖形與空間",
   "statement": "$$\\sin(\\theta+90^\\circ)=\\sin\\theta$$",
   "is_trap": true,
   "hint": "$\\sin(\\theta+90^\\circ)=\\cos\\theta$，唔係原樣！",
   "difficulty": 2
  },
  {
   "id": "MEN-010",
   "topic": "求積法",
   "strand": "度量、圖形與空間",
   "statement": "圓錐的體積是同底同高圓柱的一半。",
   "is_trap": true,
   "hint": "係 $\\frac{1}{3}$，唔係 $\\frac{1}{2}$——錐體係三分一！",
   "difficulty": 3
  },
  {
   "id": "MEN-037",
   "topic": "求積法",
   "strand": "度量、圖形與空間",
   "statement": "圓面積公式是 $\\pi r^2$。",
   "is_trap": false,
   "hint": "冇伏！記住係 $r^2$，圓周先係 $2\\pi r$。",
   "difficulty": 1
  },
  {
   "id": "MEN-038",
   "topic": "求積法",
   "strand": "度量、圖形與空間",
   "statement": "球體表面積是 $\\dfrac{4}{3}\\pi r^3$。",
   "is_trap": true,
   "hint": "嗰條係體積！表面積係 $4\\pi r^2$。",
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
   "id": "COD-039",
   "topic": "坐標幾何：直線",
   "strand": "度量、圖形與空間",
   "statement": "兩點 $(x_1,y_1)$、$(x_2,y_2)$ 的中點是 $\\left(\\dfrac{x_1+x_2}{2},\\dfrac{y_1+y_2}{2}\\right)$。",
   "is_trap": false,
   "hint": "冇伏！中點就係各坐標取平均。",
   "difficulty": 1
  },
  {
   "id": "COD-040",
   "topic": "坐標幾何：直線",
   "strand": "度量、圖形與空間",
   "statement": "斜率公式是 $m=\\dfrac{x_2-x_1}{y_2-y_1}$。",
   "is_trap": true,
   "hint": "上下反咗！正確係 $\\dfrac{y_2-y_1}{x_2-x_1}$（升／跑）。",
   "difficulty": 2
  },
  {
   "id": "CIR-041",
   "topic": "坐標幾何：圓",
   "strand": "度量、圖形與空間",
   "statement": "圓方程 $x^2+y^2+Dx+Ey+F=0$ 的圓心是 $(D,E)$。",
   "is_trap": true,
   "hint": "圓心係 $\\left(-\\dfrac{D}{2},-\\dfrac{E}{2}\\right)$，唔好直接抄係數！",
   "difficulty": 2
  },
  {
   "id": "CIR-042",
   "topic": "坐標幾何：圓",
   "strand": "度量、圖形與空間",
   "statement": "圓心 $(h,k)$、半徑 $r$ 的方程是 $(x-h)^2+(y-k)^2=r^2$。",
   "is_trap": false,
   "hint": "冇伏！呢條係圓嘅標準式。",
   "difficulty": 1
  },
  {
   "id": "CIR-043",
   "topic": "坐標幾何：圓",
   "strand": "度量、圖形與空間",
   "statement": "直線與圓相交，圓心到直線的距離一定等於半徑。",
   "is_trap": true,
   "hint": "等於半徑係相切；相交係距離 $<$ 半徑。",
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
   "id": "GEO-044",
   "topic": "圓形幾何",
   "strand": "度量、圖形與空間",
   "statement": "半圓上的圓周角一定是 $60^\\circ$。",
   "is_trap": true,
   "hint": "半圓上嘅圓周角係直角 $90^\\circ$，唔係 60！",
   "difficulty": 2
  },
  {
   "id": "GEO-045",
   "topic": "圓形幾何",
   "strand": "度量、圖形與空間",
   "statement": "圓的切線與過切點的半徑互相平行。",
   "is_trap": true,
   "hint": "係垂直，唔係平行——切線 ⊥ 半徑。",
   "difficulty": 2
  },
  {
   "id": "LOC-046",
   "topic": "軌跡",
   "strand": "度量、圖形與空間",
   "statement": "到兩定點距離相等的點的軌跡是以該兩點為焦點的橢圓。",
   "is_trap": true,
   "hint": "到兩點等距係垂直平分線；橢圓係距離之和為常數。",
   "difficulty": 2
  },
  {
   "id": "LOC-047",
   "topic": "軌跡",
   "strand": "度量、圖形與空間",
   "statement": "到定點距離等於定值的點的軌跡是圓。",
   "is_trap": false,
   "hint": "冇伏！呢句正正係圓嘅定義。",
   "difficulty": 2
  },
  {
   "id": "LOC-048",
   "topic": "軌跡",
   "strand": "度量、圖形與空間",
   "statement": "到一定點與一定直線距離相等的點的軌跡是圓。",
   "is_trap": true,
   "hint": "嗰個係拋物線定義；圓係「到定點距離＝定值」。",
   "difficulty": 3
  },
  {
   "id": "TRF-049",
   "topic": "幾何變換",
   "strand": "度量、圖形與空間",
   "statement": "將圖形繞原點逆時針旋轉 $90^\\circ$，點 $(x,y)$ 變為 $(y,x)$。",
   "is_trap": true,
   "hint": "逆時針 90° 係 $(x,y)\\to(-y,x)$，唔係對調咁簡單！",
   "difficulty": 2
  },
  {
   "id": "TRF-050",
   "topic": "幾何變換",
   "strand": "度量、圖形與空間",
   "statement": "對 $x$ 軸反射時，點 $(x,y)$ 變為 $(x,-y)$。",
   "is_trap": false,
   "hint": "冇伏！$x$ 軸反射淨係 $y$ 變號。",
   "difficulty": 1
  },
  {
   "id": "TRF-051",
   "topic": "幾何變換",
   "strand": "度量、圖形與空間",
   "statement": "位似中心在原點、相似比 $k=2$ 時，面積比一定係 2。",
   "is_trap": true,
   "hint": "面積比係 $k^2=4$，長度比先係 $k$！",
   "difficulty": 2
  },
  {
   "id": "CHR-052",
   "topic": "統計圖表",
   "strand": "數據處理",
   "statement": "圓形圖中，某類佔 25% 對應的圓心角是 $25^\\circ$。",
   "is_trap": true,
   "hint": "成個圓 $360^\\circ$，25% 係 $90^\\circ$，唔係 $25^\\circ$！",
   "difficulty": 2
  },
  {
   "id": "CHR-053",
   "topic": "統計圖表",
   "strand": "數據處理",
   "statement": "直方圖的各長方形面積與該組的頻數成正比。",
   "is_trap": false,
   "hint": "冇伏！尤其組距唔同時，要睇面積唔好淨睇高度。",
   "difficulty": 1
  },
  {
   "id": "CHR-054",
   "topic": "統計圖表",
   "strand": "數據處理",
   "statement": "幹葉圖的「葉」可以是任意多位數字。",
   "is_trap": true,
   "hint": "標準幹葉圖每片葉通常係一位數，方便還原數據。",
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
   "id": "STA-055",
   "topic": "集中趨勢與離差",
   "strand": "數據處理",
   "statement": "一組數據每項同時乘 2，標準差會變為原來的 2 倍。",
   "is_trap": false,
   "hint": "冇伏！平移唔變 SD，縮放會跟住倍大。",
   "difficulty": 1
  },
  {
   "id": "STA-056",
   "topic": "集中趨勢與離差",
   "strand": "數據處理",
   "statement": "中位數一定等於眾數。",
   "is_trap": true,
   "hint": "三者可以完全唔同——對稱分佈先容易撞埋一齊。",
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
   "id": "PROB-057",
   "topic": "概率",
   "strand": "數據處理",
   "statement": "互斥事件 $A$、$B$ 一定滿足 $P(A\\cap B)=P(A)P(B)$。",
   "is_trap": true,
   "hint": "互斥係交為空，$P(A\\cap B)=0$；獨立先係乘積。",
   "difficulty": 2
  },
  {
   "id": "PROB-058",
   "topic": "概率",
   "strand": "數據處理",
   "statement": "$P(A\\cup B)=P(A)+P(B)$ 對任意兩事件都成立。",
   "is_trap": true,
   "hint": "要減返交集：$P(A)+P(B)-P(A\\cap B)$；互斥先唔使減。",
   "difficulty": 2
  },
  {
   "id": "COM-059",
   "topic": "排列與組合",
   "strand": "數據處理",
   "statement": "從 5 人中選 3 人排隊，方法數是 $\\mathrm{C}^5_3$。",
   "is_trap": true,
   "hint": "排隊講次序，要用排列 $\\mathrm{P}^5_3$，唔係組合！",
   "difficulty": 2
  },
  {
   "id": "COM-060",
   "topic": "排列與組合",
   "strand": "數據處理",
   "statement": "$\\mathrm{C}^n_r = \\dfrac{n!}{r!(n-r)!}$（$0\\le r\\le n$）",
   "is_trap": false,
   "hint": "冇伏！組合公式就係咁——唔計次序所以除 $r!$。",
   "difficulty": 1
  },
  {
   "id": "COM-061",
   "topic": "排列與組合",
   "strand": "數據處理",
   "statement": "$n$ 件相異物全排列是 $n$，因為每人一個位置。",
   "is_trap": true,
   "hint": "全排列係 $n!$，唔係 $n$——第一位 $n$ 揀，之後遞減相乘。",
   "difficulty": 2
  }
 ]
};
