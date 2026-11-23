# -*- coding: utf-8 -*-
"""Build local math skill foundation: skill book, tag crosswalk, 2012 P2 pilot hooks.

Outputs:
  docs/skills/math_skill_book.json
  docs/skills/math_tag_crosswalk.json
  docs/skills/SCHEMA.md
  patches skills onto docs/analysis/math/2012/paper-2/q*.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "docs" / "skills"
ANALYSIS_P2 = ROOT / "docs" / "analysis" / "math" / "2012" / "paper-2"

ABILITIES = [
    {"id": "A-SUB", "name": "代入數值", "desc": "把已知數值代入式子或公式"},
    {"id": "A-ALG", "name": "代數變形", "desc": "搬項、展開、因式、合併同類項"},
    {"id": "A-COND", "name": "睇條件", "desc": "注意單位、範圍、正負、非零、定義域"},
    {"id": "A-GRAPH", "name": "讀圖", "desc": "從圖像讀出斜率、截距、頂點、週期等"},
    {"id": "A-BACK", "name": "由答案倒推", "desc": "用選項反推或驗證"},
    {"id": "A-CHAIN", "name": "多步串連", "desc": "多步解題，中間一步錯會帶歪後續"},
    {"id": "A-ELIM", "name": "排除錯選項", "desc": "用性質或邊界情況剔除不合理選項"},
    {"id": "A-CALC", "name": "計算仔細度", "desc": "符號、係數、口算與代數操作準確"},
]

# topic_id -> (hub_name, group, knowledge_points[(id,name,prereqs)], formulas[(id,name,latex,kp)])
TOPICS_SPEC = {
    "T-PCT": (
        "百分法",
        "數與代數",
        [
            ("K-PCT-01", "百分率換算", []),
            ("K-PCT-02", "百分增減與新值", ["K-PCT-01"]),
            ("K-PCT-03", "利息與增長", ["K-PCT-02"]),
            ("K-PCT-04", "盈虧與折扣", ["K-PCT-02"]),
            ("K-PCT-05", "人口／群體比例混合", ["K-PCT-01"]),
        ],
        [
            ("F-PCT-01", "百分率", r"p\% = \frac{p}{100}", "K-PCT-01"),
            ("F-PCT-02", "新值", r"新值 = 原值 \times (1 \pm r)", "K-PCT-02"),
            ("F-PCT-03", "單利", r"利息 = 本金 \times 利率 \times 期數", "K-PCT-03"),
        ],
    ),
    "T-EXP": (
        "指數與對數",
        "數與代數",
        [
            ("K-EXP-01", "同底乘除：指數加減", []),
            ("K-EXP-02", "冪的冪：指數相乘", ["K-EXP-01"]),
            ("K-EXP-03", "零指數與負指數", ["K-EXP-01"]),
            ("K-EXP-04", "分數指數與根式", ["K-EXP-02", "K-EXP-03"]),
            ("K-EXP-05", "對數定義與換底", ["K-EXP-03"]),
            ("K-EXP-06", "對數運算法則", ["K-EXP-05"]),
            ("K-EXP-07", "指數／對數方程與圖像", ["K-EXP-06"]),
        ],
        [
            ("F-EXP-01", "乘法則", r"a^m \cdot a^n = a^{m+n}", "K-EXP-01"),
            ("F-EXP-02", "除法則", r"\frac{a^m}{a^n} = a^{m-n}", "K-EXP-01"),
            ("F-EXP-03", "冪的冪", r"(a^m)^n = a^{mn}", "K-EXP-02"),
            ("F-EXP-04", "積的冪", r"(ab)^n = a^n b^n", "K-EXP-02"),
            ("F-EXP-05", "零指數", r"a^0 = 1\ (a\neq 0)", "K-EXP-03"),
            ("F-EXP-06", "負指數", r"a^{-n} = \frac{1}{a^n}", "K-EXP-03"),
            ("F-EXP-07", "對數定義", r"\log_b a = c \iff b^c = a", "K-EXP-05"),
            ("F-EXP-08", "對數積", r"\log_b(xy)=\log_b x+\log_b y", "K-EXP-06"),
            ("F-EXP-09", "對數冪", r"\log_b(a^k)=k\log_b a", "K-EXP-06"),
        ],
    ),
    "T-RAT": (
        "比、率與比例",
        "數與代數",
        [
            ("K-RAT-01", "比的化簡", []),
            ("K-RAT-02", "率與單位", ["K-RAT-01"]),
            ("K-RAT-03", "正比與反比", ["K-RAT-01"]),
            ("K-RAT-04", "比例式交叉相乘", ["K-RAT-03"]),
            ("K-RAT-05", "比例分配", ["K-RAT-04"]),
        ],
        [
            ("F-RAT-01", "比", r"a:b = \frac{a}{b}", "K-RAT-01"),
            ("F-RAT-02", "正比", r"y = kx", "K-RAT-03"),
            ("F-RAT-03", "反比", r"y = \frac{k}{x}", "K-RAT-03"),
            ("F-RAT-04", "交叉相乘", r"\frac{a}{b}=\frac{c}{d}\Rightarrow ad=bc", "K-RAT-04"),
        ],
    ),
    "T-POL": (
        "多項式（續）",
        "數與代數",
        [
            ("K-POL-01", "展開與合併同類項", []),
            ("K-POL-02", "完全平方與平方差", ["K-POL-01"]),
            ("K-POL-03", "因式分解", ["K-POL-02"]),
            ("K-POL-04", "餘式定理", ["K-POL-01"]),
            ("K-POL-05", "因式定理", ["K-POL-04"]),
            ("K-POL-06", "恆等式與比較係數", ["K-POL-01"]),
            ("K-POL-07", "主項變換", ["K-POL-01"]),
        ],
        [
            ("F-POL-01", "完全平方", r"(a\pm b)^2=a^2\pm 2ab+b^2", "K-POL-02"),
            ("F-POL-02", "平方差", r"a^2-b^2=(a-b)(a+b)", "K-POL-02"),
            ("F-POL-03", "兩平方差展開差", r"(a+b)^2-(a-b)^2=4ab", "K-POL-02"),
            ("F-POL-04", "餘式定理", r"P(x)\div(x-a)\Rightarrow 餘數=P(a)", "K-POL-04"),
            ("F-POL-05", "因式定理", r"x-a\ 為因式 \iff P(a)=0", "K-POL-05"),
            ("F-POL-06", "二次展開", r"(x+a)(x+b)=x^2+(a+b)x+ab", "K-POL-01"),
        ],
    ),
    "T-NUM": (
        "數系",
        "數與代數",
        [
            ("K-NUM-01", "整數／有理／無理／實數", []),
            ("K-NUM-02", "H.C.F. 與 L.C.M.", []),
            ("K-NUM-03", "進位制換算", []),
            ("K-NUM-04", "有效數字與小數位", []),
            ("K-NUM-05", "近似與絕對誤差", ["K-NUM-04"]),
            ("K-NUM-06", "複數基本運算", ["K-NUM-01"]),
        ],
        [
            ("F-NUM-01", "HCF×LCM", r"\mathrm{HCF}(a,b)\times\mathrm{LCM}(a,b)=|ab|", "K-NUM-02"),
            ("F-NUM-02", "進位展開", r"\sum d_i b^i", "K-NUM-03"),
            ("F-NUM-03", "誤差半單位", r"x\pm\frac{1}{2}u", "K-NUM-05"),
            ("F-NUM-04", "虛數單位", r"i^2=-1", "K-NUM-06"),
        ],
    ),
    "T-EQN": (
        "方程與不等式",
        "數與代數",
        [
            ("K-EQN-01", "一次方程與移項", []),
            ("K-EQN-02", "聯立一次方程", ["K-EQN-01"]),
            ("K-EQN-03", "二次方程解法", ["K-EQN-01"]),
            ("K-EQN-04", "判別式與根的性質", ["K-EQN-03"]),
            ("K-EQN-05", "一元一次不等式", ["K-EQN-01"]),
            ("K-EQN-06", "線性不等式區域", ["K-EQN-05"]),
            ("K-EQN-07", "線性規劃初步", ["K-EQN-06"]),
        ],
        [
            ("F-EQN-01", "求根公式", r"x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}", "K-EQN-03"),
            ("F-EQN-02", "判別式", r"\Delta=b^2-4ac", "K-EQN-04"),
            ("F-EQN-03", "不等式同號", r"a>0\Rightarrow ax>c-b\ \text{同向}", "K-EQN-05"),
            ("F-EQN-04", "斜截式", r"y=mx+c", "K-EQN-06"),
        ],
    ),
    "T-FUN": (
        "函數與圖像",
        "數與代數",
        [
            ("K-FUN-01", "函數值與定義域", []),
            ("K-FUN-02", "一次函數圖像", ["K-FUN-01"]),
            ("K-FUN-03", "二次函數頂點與開口", ["K-FUN-01"]),
            ("K-FUN-04", "圖像平移與反射", ["K-FUN-02", "K-FUN-03"]),
            ("K-FUN-05", "圖像讀取與參數意義", ["K-FUN-03"]),
        ],
        [
            ("F-FUN-01", "頂點式", r"y=a(x-h)^2+k", "K-FUN-03"),
            ("F-FUN-02", "水平平移", r"y=f(x-h)\Rightarrow 右移 h", "K-FUN-04"),
            ("F-FUN-03", "垂直平移", r"y=f(x)+k\Rightarrow 上移 k", "K-FUN-04"),
            ("F-FUN-04", "二次通式", r"y=ax^2+bx+c", "K-FUN-03"),
        ],
    ),
    "T-SEQ": (
        "數列",
        "數與代數",
        [
            ("K-SEQ-01", "數列通項與規律", []),
            ("K-SEQ-02", "等差數列", ["K-SEQ-01"]),
            ("K-SEQ-03", "等比數列", ["K-SEQ-01"]),
            ("K-SEQ-04", "求和公式", ["K-SEQ-02", "K-SEQ-03"]),
            ("K-SEQ-05", "圖形／圖案遞迴", ["K-SEQ-01"]),
        ],
        [
            ("F-SEQ-01", "等差通項", r"a_n=a_1+(n-1)d", "K-SEQ-02"),
            ("F-SEQ-02", "等差求和", r"S_n=\frac{n}{2}[2a_1+(n-1)d]", "K-SEQ-04"),
            ("F-SEQ-03", "等比通項", r"a_n=a_1 r^{n-1}", "K-SEQ-03"),
            ("F-SEQ-04", "三角數", r"T_n=\frac{n(n+1)}{2}", "K-SEQ-05"),
        ],
    ),
    "T-VAR": (
        "變分",
        "數與代數",
        [
            ("K-VAR-01", "正變", []),
            ("K-VAR-02", "反變", []),
            ("K-VAR-03", "聯變／混合變", ["K-VAR-01", "K-VAR-02"]),
            ("K-VAR-04", "由已知點求常數", ["K-VAR-03"]),
        ],
        [
            ("F-VAR-01", "正變", r"y=kx", "K-VAR-01"),
            ("F-VAR-02", "反變", r"y=\frac{k}{x}", "K-VAR-02"),
            ("F-VAR-03", "混合變例", r"y=k_1 x^2+\frac{k_2}{x}", "K-VAR-03"),
        ],
    ),
    "T-TRI": (
        "三角學與解三角形",
        "度量、圖形與空間",
        [
            ("K-TRI-01", "銳角三角比定義", []),
            ("K-TRI-02", "特殊角值", ["K-TRI-01"]),
            ("K-TRI-03", "餘角／誘導公式", ["K-TRI-01"]),
            ("K-TRI-04", "正弦／餘弦定理", ["K-TRI-01"]),
            ("K-TRI-05", "三角方程與圖像", ["K-TRI-03"]),
            ("K-TRI-06", "方位角與應用", ["K-TRI-01"]),
        ],
        [
            ("F-TRI-01", "sin", r"\sin\theta=\frac{\text{對}}{\text{斜}}", "K-TRI-01"),
            ("F-TRI-02", "cos", r"\cos\theta=\frac{\text{鄰}}{\text{斜}}", "K-TRI-01"),
            ("F-TRI-03", "餘角", r"\cos(90^\circ-\theta)=\sin\theta", "K-TRI-03"),
            ("F-TRI-04", "餘弦定理", r"c^2=a^2+b^2-2ab\cos C", "K-TRI-04"),
            ("F-TRI-05", "餘弦週期", r"y=A+B\cos(kx),\ T=\frac{360^\circ}{k}", "K-TRI-05"),
        ],
    ),
    "T-MEN": (
        "求積法",
        "度量、圖形與空間",
        [
            ("K-MEN-01", "平面圖形面積", []),
            ("K-MEN-02", "弧長與扇形", ["K-MEN-01"]),
            ("K-MEN-03", "相似面積比", ["K-MEN-01"]),
            ("K-MEN-04", "立體表面積與體積", ["K-MEN-01"]),
            ("K-MEN-05", "立體角與二面角", ["K-MEN-04"]),
        ],
        [
            ("F-MEN-01", "三角形面積", r"\frac12 bh", "K-MEN-01"),
            ("F-MEN-02", "弧長", r"L=r\theta", "K-MEN-02"),
            ("F-MEN-03", "扇形面積", r"\frac{n}{360}\pi r^2", "K-MEN-02"),
            ("F-MEN-04", "三角面積公式", r"\frac12 ab\sin C", "K-MEN-01"),
            ("F-MEN-05", "二面角餘弦", r"\cos\theta=\frac{\vec n_1\cdot\vec n_2}{|\vec n_1||\vec n_2|}", "K-MEN-05"),
        ],
    ),
    "T-LIN": (
        "坐標幾何：直線",
        "度量、圖形與空間",
        [
            ("K-LIN-01", "距離與中點", []),
            ("K-LIN-02", "斜率與截距", []),
            ("K-LIN-03", "直線方程形式", ["K-LIN-02"]),
            ("K-LIN-04", "平行與垂直", ["K-LIN-02"]),
            ("K-LIN-05", "點到直線距離", ["K-LIN-03"]),
        ],
        [
            ("F-LIN-01", "距離", r"d=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}", "K-LIN-01"),
            ("F-LIN-02", "斜率", r"m=\frac{y_2-y_1}{x_2-x_1}", "K-LIN-02"),
            ("F-LIN-03", "斜截式", r"y=mx+c", "K-LIN-03"),
            ("F-LIN-04", "點到線", r"d=\frac{|Ax_0+By_0+C|}{\sqrt{A^2+B^2}}", "K-LIN-05"),
        ],
    ),
    "T-CIR": (
        "坐標幾何：圓",
        "度量、圖形與空間",
        [
            ("K-CIR-01", "圓的標準方程", []),
            ("K-CIR-02", "圓心半徑判讀", ["K-CIR-01"]),
            ("K-CIR-03", "圓與直線相交", ["K-CIR-01", "K-LIN-05"]),
            ("K-CIR-04", "圓與點的位置", ["K-CIR-02"]),
        ],
        [
            ("F-CIR-01", "標準方程", r"(x-h)^2+(y-k)^2=r^2", "K-CIR-01"),
            ("F-CIR-02", "一般式半徑", r"r=\sqrt{g^2+f^2-c}", "K-CIR-02"),
        ],
    ),
    "T-GEO": (
        "圓形幾何",
        "度量、圖形與空間",
        [
            ("K-GEO-01", "圓心角與圓周角", []),
            ("K-GEO-02", "切線與半徑垂直", ["K-GEO-01"]),
            ("K-GEO-03", "弦、弧與對稱", ["K-GEO-01"]),
            ("K-GEO-04", "多邊形內外角", []),
            ("K-GEO-05", "相似／全等三角形", []),
        ],
        [
            ("F-GEO-01", "圓周角", r"圓周角=\frac12 同弧圓心角", "K-GEO-01"),
            ("F-GEO-02", "切線垂直", r"切線 \perp 半徑", "K-GEO-02"),
            ("F-GEO-03", "外角和", r"正 n 邊形外角=\frac{360^\circ}{n}", "K-GEO-04"),
            ("F-GEO-04", "內角和", r"(n-2)\times 180^\circ", "K-GEO-04"),
        ],
    ),
    "T-LOC": (
        "軌跡",
        "度量、圖形與空間",
        [
            ("K-LOC-01", "到定點等距（圓）", []),
            ("K-LOC-02", "到兩點等距（垂直平分線）", []),
            ("K-LOC-03", "到定直線等距", []),
            ("K-LOC-04", "軌跡方程描述", ["K-LOC-01", "K-LOC-02"]),
        ],
        [
            ("F-LOC-01", "圓軌跡", r"\{P: |PA|=r\}", "K-LOC-01"),
            ("F-LOC-02", "垂直平分線", r"\{P: |PA|=|PB|\}", "K-LOC-02"),
        ],
    ),
    "T-TRF": (
        "幾何變換",
        "度量、圖形與空間",
        [
            ("K-TRF-01", "平移", []),
            ("K-TRF-02", "反射", []),
            ("K-TRF-03", "旋轉", []),
            ("K-TRF-04", "極坐標與直角坐標", []),
            ("K-TRF-05", "圖像變換綜合", ["K-TRF-01", "K-TRF-02", "K-TRF-03"]),
        ],
        [
            ("F-TRF-01", "逆時針 90°", r"(x,y)\mapsto(-y,x)", "K-TRF-03"),
            ("F-TRF-02", "極徑", r"r=\sqrt{x^2+y^2}", "K-TRF-04"),
        ],
    ),
    "T-CHR": (
        "統計圖表",
        "數據處理",
        [
            ("K-CHR-01", "棒形／圓形圖讀取", []),
            ("K-CHR-02", "幹葉圖", []),
            ("K-CHR-03", "框線圖與四分位", []),
            ("K-CHR-04", "散點圖與趨勢", []),
            ("K-CHR-05", "頻數分佈表", []),
        ],
        [
            ("F-CHR-01", "圓形圖角", r"扇形角 = 比例 \times 360^\circ", "K-CHR-01"),
            ("F-CHR-02", "四分位距", r"IQR=Q_3-Q_1", "K-CHR-03"),
        ],
    ),
    "T-STA": (
        "集中趨勢與離差",
        "數據處理",
        [
            ("K-STA-01", "平均數", []),
            ("K-STA-02", "中位數與眾數", []),
            ("K-STA-03", "加權平均", ["K-STA-01"]),
            ("K-STA-04", "分佈域（極差）", []),
            ("K-STA-05", "方差與標準差", ["K-STA-01"]),
            ("K-STA-06", "數據增刪對統計量影響", ["K-STA-01", "K-STA-04", "K-STA-05"]),
        ],
        [
            ("F-STA-01", "平均數", r"\bar x=\frac{\sum x}{n}", "K-STA-01"),
            ("F-STA-02", "加權平均", r"\bar x=\frac{\sum f_i x_i}{\sum f_i}", "K-STA-03"),
            ("F-STA-03", "極差", r"R=\max-\min", "K-STA-04"),
            ("F-STA-04", "標準差", r"\sigma=\sqrt{\frac{\sum(x_i-\bar x)^2}{n}}", "K-STA-05"),
            ("F-STA-05", "加入新數據平均", r"\bar x_{new}=\frac{n\bar x+x_{new}}{n+1}", "K-STA-06"),
        ],
    ),
    "T-PROB": (
        "概率",
        "數據處理",
        [
            ("K-PROB-01", "古典概率", []),
            ("K-PROB-02", "互斥與加法", ["K-PROB-01"]),
            ("K-PROB-03", "獨立事件乘法", ["K-PROB-01"]),
            ("K-PROB-04", "條件概率", ["K-PROB-03"]),
            ("K-PROB-05", "與計數結合", ["K-PROB-01"]),
        ],
        [
            ("F-PROB-01", "古典", r"P(E)=\frac{n(E)}{n(S)}", "K-PROB-01"),
            ("F-PROB-02", "互斥加", r"P(A\cup B)=P(A)+P(B)", "K-PROB-02"),
            ("F-PROB-03", "條件", r"P(A\cap B)=P(A)P(B|A)", "K-PROB-04"),
        ],
    ),
    "T-COM": (
        "排列與組合",
        "數據處理",
        [
            ("K-COM-01", "計數基本原理", []),
            ("K-COM-02", "排列", ["K-COM-01"]),
            ("K-COM-03", "組合", ["K-COM-01"]),
            ("K-COM-04", "組合恒等式", ["K-COM-03"]),
        ],
        [
            ("F-COM-01", "排列", r"P(n,r)=\frac{n!}{(n-r)!}", "K-COM-02"),
            ("F-COM-02", "組合", r"\binom{n}{k}=\frac{n!}{k!(n-k)!}", "K-COM-03"),
            ("F-COM-03", "二項式和", r"\sum_{k=0}^n\binom{n}{k}=2^n", "K-COM-04"),
        ],
    ),
}


def build_skill_book() -> dict:
    topics = []
    for tid, (name, group, kps, formulas) in TOPICS_SPEC.items():
        topics.append(
            {
                "id": tid,
                "name": name,
                "group": group,
                "knowledge_points": [
                    {"id": kid, "name": kn, "prereqs": pr} for kid, kn, pr in kps
                ],
                "formulas": [
                    {"id": fid, "name": fn, "latex": lx, "knowledge_point_id": kid}
                    for fid, fn, lx, kid in formulas
                ],
            }
        )
    return {
        "version": 1,
        "subject": "math",
        "subject_name": "數學（必修部分）",
        "abilities": ABILITIES,
        "topics": topics,
        "notes": [
            "所有分析 skills 欄位只准使用本冊 id。",
            "課題名與 docs/hub/data.js TOPICS.math 的 20 個葉節點一致。",
            "學生報告／自動出題稍後再做；本冊是計分基礎。",
        ],
    }


# bank tag (Chinese / English / mapping name) -> topic_id
# Keep website tags unchanged; this is lookup only.
CROSSWALK_RULES: list[tuple[str, str]] = [
    # hub 20
    ("百分法", "T-PCT"),
    ("指數與對數", "T-EXP"),
    ("比、率與比例", "T-RAT"),
    ("多項式（續）", "T-POL"),
    ("數系", "T-NUM"),
    ("方程與不等式", "T-EQN"),
    ("函數與圖像", "T-FUN"),
    ("數列", "T-SEQ"),
    ("變分", "T-VAR"),
    ("三角學與解三角形", "T-TRI"),
    ("求積法", "T-MEN"),
    ("坐標幾何：直線", "T-LIN"),
    ("坐標幾何：圓", "T-CIR"),
    ("圓形幾何", "T-GEO"),
    ("軌跡", "T-LOC"),
    ("幾何變換", "T-TRF"),
    ("統計圖表", "T-CHR"),
    ("集中趨勢與離差", "T-STA"),
    ("概率", "T-PROB"),
    ("排列與組合", "T-COM"),
    # common bank tags
    ("百分比", "T-PCT"),
    ("百分數", "T-PCT"),
    ("百分數／利息", "T-PCT"),
    ("百分變化", "T-PCT"),
    ("利息與增長", "T-PCT"),
    ("複利息", "T-PCT"),
    ("Percentages", "T-PCT"),
    ("Discount", "T-PCT"),
    ("Profit", "T-PCT"),
    ("Profit and Loss", "T-PCT"),
    ("Investment", "T-PCT"),
    ("指數定律", "T-EXP"),
    ("指數比較", "T-EXP"),
    ("指數函數", "T-EXP"),
    ("對數", "T-EXP"),
    ("對數方程", "T-EXP"),
    ("Laws of Indices", "T-EXP"),
    ("Positive Indices", "T-EXP"),
    ("比率與比例", "T-RAT"),
    ("比與比例", "T-RAT"),
    ("比例", "T-RAT"),
    ("比例與相似", "T-RAT"),
    ("Rate and Ratio", "T-RAT"),
    ("Ratio", "T-RAT"),
    ("平均速率", "T-RAT"),
    ("Average Speed", "T-RAT"),
    ("多項式", "T-POL"),
    ("因式分解", "T-POL"),
    ("因式定理", "T-POL"),
    ("餘式定理", "T-POL"),
    ("代數化簡", "T-POL"),
    ("恆等式", "T-POL"),
    ("比較係數", "T-POL"),
    ("主項變換", "T-POL"),
    ("配方法", "T-POL"),
    ("Polynomials", "T-POL"),
    ("Factorisation", "T-POL"),
    ("Factor Theorem", "T-POL"),
    ("Algebraic Expressions", "T-POL"),
    ("Quadratic Expressions", "T-POL"),
    ("Algebra", "T-POL"),
    ("Change of Subject", "T-POL"),
    ("H.C.F.", "T-NUM"),
    ("L.C.M.", "T-NUM"),
    ("數制", "T-NUM"),
    ("二進位", "T-NUM"),
    ("十六進位", "T-NUM"),
    ("十六進制", "T-NUM"),
    ("複數", "T-NUM"),
    ("Complex Numbers", "T-NUM"),
    ("近似與誤差", "T-NUM"),
    ("誤差上限", "T-NUM"),
    ("Errors", "T-NUM"),
    ("Significant Figures", "T-NUM"),
    ("一元方程", "T-EQN"),
    ("一元一次方程", "T-EQN"),
    ("一元二次方程", "T-EQN"),
    ("一元一次不等式", "T-EQN"),
    ("不等式", "T-EQN"),
    ("複合不等式", "T-EQN"),
    ("聯立方程", "T-EQN"),
    ("二元一次方程組", "T-EQN"),
    ("二次方程", "T-EQN"),
    ("判別式", "T-EQN"),
    ("根與係數", "T-EQN"),
    ("線性規劃", "T-EQN"),
    ("Equations", "T-EQN"),
    ("Quadratic Equations", "T-EQN"),
    ("Linear Inequalities", "T-EQN"),
    ("Simultaneous Equations", "T-EQN"),
    ("Real Roots", "T-EQN"),
    ("二次函數", "T-FUN"),
    ("函數", "T-FUN"),
    ("圖像", "T-FUN"),
    ("拋物線", "T-FUN"),
    ("頂點", "T-FUN"),
    ("線性關係", "T-FUN"),
    ("圖像變換", "T-FUN"),
    ("Functions and Graphs", "T-FUN"),
    ("Quadratic Functions", "T-FUN"),
    ("Graph Reading", "T-FUN"),
    ("Variables", "T-FUN"),
    ("等差數列", "T-SEQ"),
    ("等比數列", "T-SEQ"),
    ("圖案規律", "T-SEQ"),
    ("Sequences", "T-SEQ"),
    ("Geometric Sequence", "T-SEQ"),
    ("Variation", "T-VAR"),
    ("三角學", "T-TRI"),
    ("三角比", "T-TRI"),
    ("三角比／角", "T-TRI"),
    ("三角函數", "T-TRI"),
    ("三角恆等式", "T-TRI"),
    ("三角方程", "T-TRI"),
    ("餘弦定理", "T-TRI"),
    ("畢氏定理", "T-TRI"),
    ("方位角", "T-TRI"),
    ("弧度", "T-TRI"),
    ("Trigonometry", "T-TRI"),
    ("面積", "T-MEN"),
    ("面積比", "T-MEN"),
    ("多邊形面積", "T-MEN"),
    ("梯形面積", "T-MEN"),
    ("扇形", "T-MEN"),
    ("扇形面積", "T-MEN"),
    ("弧長", "T-MEN"),
    ("體積", "T-MEN"),
    ("表面積", "T-MEN"),
    ("容量", "T-MEN"),
    ("立體圖形", "T-MEN"),
    ("立體幾何", "T-MEN"),
    ("圓柱", "T-MEN"),
    ("圓錐", "T-MEN"),
    ("半球", "T-MEN"),
    ("角柱體", "T-MEN"),
    ("角錐", "T-MEN"),
    ("四面體", "T-MEN"),
    ("兩面角", "T-MEN"),
    ("Mensuration", "T-MEN"),
    ("Solids", "T-MEN"),
    ("3-D Geometry", "T-MEN"),
    ("Capacity", "T-MEN"),
    ("Cube", "T-MEN"),
    ("Tetrahedron", "T-MEN"),
    ("Angle between Planes", "T-MEN"),
    ("直線方程", "T-LIN"),
    ("坐標幾何", "T-LIN"),
    ("Equations of Straight Lines", "T-LIN"),
    ("圓的方程", "T-CIR"),
    ("圓與直線", "T-CIR"),
    ("直線與圓", "T-CIR"),
    ("Equations of Circles", "T-CIR"),
    ("圓的性質", "T-GEO"),
    ("圓的幾何", "T-GEO"),
    ("圓形性質", "T-GEO"),
    ("圓形", "T-GEO"),
    ("圓周角", "T-GEO"),
    ("切線", "T-GEO"),
    ("交弦定理", "T-GEO"),
    ("平面幾何", "T-GEO"),
    ("三角形", "T-GEO"),
    ("相似三角形", "T-GEO"),
    ("全等三角形", "T-GEO"),
    ("直角三角形", "T-GEO"),
    ("四邊形", "T-GEO"),
    ("平行線", "T-GEO"),
    ("多邊形", "T-GEO"),
    ("菱形", "T-GEO"),
    ("正方形", "T-GEO"),
    ("角", "T-GEO"),
    ("內心", "T-GEO"),
    ("外心", "T-GEO"),
    ("幾何中心", "T-GEO"),
    ("垂直平分線", "T-GEO"),
    ("Circle Properties", "T-GEO"),
    ("Similar Triangles", "T-GEO"),
    ("Tangents", "T-GEO"),
    ("Geometry", "T-GEO"),
    ("Angles", "T-GEO"),
    ("Isosceles Triangle", "T-GEO"),
    ("Locus", "T-LOC"),
    ("變換", "T-TRF"),
    ("變換與對稱", "T-TRF"),
    ("變換／對稱", "T-TRF"),
    ("對稱", "T-TRF"),
    ("對稱軸", "T-TRF"),
    ("反射", "T-TRF"),
    ("極坐標", "T-TRF"),
    ("Reflection", "T-TRF"),
    ("Rotation", "T-TRF"),
    ("Polar Coordinates", "T-TRF"),
    ("幹葉圖", "T-CHR"),
    ("框線圖", "T-CHR"),
    ("散點圖", "T-CHR"),
    ("圓形圖", "T-CHR"),
    ("棒形圖", "T-CHR"),
    ("頻數分佈表", "T-CHR"),
    ("Bar Chart", "T-CHR"),
    ("Pie Chart", "T-CHR"),
    ("Box-and-whisker Diagram", "T-CHR"),
    ("統計", "T-STA"),
    ("集中趨勢", "T-STA"),
    ("離差", "T-STA"),
    ("平均數", "T-STA"),
    ("平均值", "T-STA"),
    ("中位數", "T-STA"),
    ("眾數", "T-STA"),
    ("四分位數", "T-STA"),
    ("分佈域", "T-STA"),
    ("方差", "T-STA"),
    ("標準差", "T-STA"),
    ("標準分", "T-STA"),
    ("Statistics", "T-STA"),
    ("Mean", "T-STA"),
    ("Median", "T-STA"),
    ("Standard Score", "T-STA"),
    ("Interquartile Range", "T-STA"),
    ("Data Distribution", "T-STA"),
    ("Change in Data", "T-STA"),
    ("條件概率", "T-PROB"),
    ("獨立事件", "T-PROB"),
    ("Probability", "T-PROB"),
    ("Conditional Probability", "T-PROB"),
    ("組合", "T-COM"),
    ("Permutations and Combinations", "T-COM"),
    ("Combinations", "T-COM"),
    # leftovers from topics/_mapping + questions/_index
    ("應用題", "T-EQN"),
    ("Cost Function", "T-FUN"),
    ("三角形的心", "T-GEO"),
    ("Division", "T-POL"),
    ("幾何", "T-GEO"),
    ("三角形內心", "T-GEO"),
    ("Area of Triangle", "T-TRI"),
    ("Revenue", "T-FUN"),
]


def build_crosswalk(book: dict) -> dict:
    id_to_name = {t["id"]: t["name"] for t in book["topics"]}
    mapping = {}
    for tag, tid in CROSSWALK_RULES:
        mapping[tag] = {"topic_id": tid, "topic_name": id_to_name[tid]}
    return {
        "version": 1,
        "note": "題庫 tags 對照到技能冊 20 課題；不改網站既有 tag 字串。",
        "map": mapping,
    }


# Manual pilot hooks for 2012 Paper 2 Q1–Q45
# option_faults: wrong options only; each maps to one kp OR formula + one ability
PILOT_2012_P2: dict[int, dict] = {
    1: {
        "topic_id": "T-EXP",
        "knowledge_point_ids": ["K-EXP-01", "K-EXP-02"],
        "formula_ids": ["F-EXP-02", "F-EXP-03", "F-EXP-04"],
        "ability_ids": ["A-ALG", "A-CALC"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-EXP-02", "formula_id": "F-EXP-03", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-EXP-01", "formula_id": "F-EXP-04", "ability_id": "A-CALC"},
            "D": {"knowledge_point_id": "K-EXP-01", "formula_id": "F-EXP-02", "ability_id": "A-ALG"},
        },
    },
    2: {
        "topic_id": "T-POL",
        "knowledge_point_ids": ["K-POL-01", "K-POL-02"],
        "formula_ids": ["F-POL-01", "F-POL-03"],
        "ability_ids": ["A-ALG", "A-CALC"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-POL-02", "formula_id": "F-POL-03", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-POL-01", "formula_id": "F-POL-01", "ability_id": "A-CALC"},
            "C": {"knowledge_point_id": "K-POL-01", "formula_id": "F-POL-01", "ability_id": "A-CALC"},
        },
    },
    3: {
        "topic_id": "T-POL",
        "knowledge_point_ids": ["K-POL-01", "K-POL-06"],
        "formula_ids": ["F-POL-06"],
        "ability_ids": ["A-ALG", "A-CALC"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-POL-01", "formula_id": "F-POL-06", "ability_id": "A-CALC"},
            "B": {"knowledge_point_id": "K-POL-06", "formula_id": "F-POL-06", "ability_id": "A-ALG"},
            "C": {"knowledge_point_id": "K-POL-01", "formula_id": "F-POL-06", "ability_id": "A-CALC"},
        },
    },
    4: {
        "topic_id": "T-POL",
        "knowledge_point_ids": ["K-POL-04", "K-POL-05"],
        "formula_ids": ["F-POL-04", "F-POL-05"],
        "ability_ids": ["A-SUB", "A-ALG"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-POL-04", "formula_id": "F-POL-04", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-POL-04", "formula_id": "F-POL-04", "ability_id": "A-CALC"},
            "C": {"knowledge_point_id": "K-POL-05", "formula_id": "F-POL-05", "ability_id": "A-ALG"},
        },
    },
    5: {
        "topic_id": "T-EQN",
        "knowledge_point_ids": ["K-EQN-01", "K-EQN-02"],
        "formula_ids": [],
        "ability_ids": ["A-ALG", "A-CHAIN"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-EQN-02", "formula_id": None, "ability_id": "A-CHAIN"},
            "B": {"knowledge_point_id": "K-EQN-01", "formula_id": None, "ability_id": "A-CALC"},
            "C": {"knowledge_point_id": "K-EQN-01", "formula_id": None, "ability_id": "A-COND"},
        },
    },
    6: {
        "topic_id": "T-FUN",
        "knowledge_point_ids": ["K-FUN-03", "K-FUN-05"],
        "formula_ids": ["F-FUN-01"],
        "ability_ids": ["A-GRAPH", "A-COND"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-FUN-03", "formula_id": "F-FUN-01", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-FUN-05", "formula_id": "F-FUN-01", "ability_id": "A-GRAPH"},
            "C": {"knowledge_point_id": "K-FUN-03", "formula_id": "F-FUN-01", "ability_id": "A-COND"},
        },
    },
    7: {
        "topic_id": "T-EQN",
        "knowledge_point_ids": ["K-EQN-05"],
        "formula_ids": ["F-EQN-03"],
        "ability_ids": ["A-ALG", "A-ELIM"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-EQN-05", "formula_id": "F-EQN-03", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-EQN-05", "formula_id": "F-EQN-03", "ability_id": "A-ELIM"},
            "C": {"knowledge_point_id": "K-EQN-05", "formula_id": "F-EQN-03", "ability_id": "A-ELIM"},
        },
    },
    8: {
        "topic_id": "T-PCT",
        "knowledge_point_ids": ["K-PCT-05", "K-PCT-01"],
        "formula_ids": ["F-PCT-01"],
        "ability_ids": ["A-CALC", "A-COND"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-PCT-05", "formula_id": "F-PCT-01", "ability_id": "A-CALC"},
            "B": {"knowledge_point_id": "K-PCT-05", "formula_id": None, "ability_id": "A-ALG"},
            "C": {"knowledge_point_id": "K-PCT-05", "formula_id": "F-PCT-01", "ability_id": "A-COND"},
        },
    },
    9: {
        "topic_id": "T-RAT",
        "knowledge_point_ids": ["K-RAT-04", "K-EQN-01"],
        "formula_ids": ["F-RAT-04"],
        "ability_ids": ["A-ALG", "A-CALC"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-RAT-04", "formula_id": "F-RAT-04", "ability_id": "A-CALC"},
            "B": {"knowledge_point_id": "K-RAT-04", "formula_id": "F-RAT-04", "ability_id": "A-ALG"},
            "C": {"knowledge_point_id": "K-RAT-03", "formula_id": "F-RAT-04", "ability_id": "A-ALG"},
        },
    },
    10: {
        "topic_id": "T-VAR",
        "knowledge_point_ids": ["K-VAR-03", "K-VAR-04"],
        "formula_ids": ["F-VAR-03"],
        "ability_ids": ["A-SUB", "A-ALG", "A-CHAIN"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-VAR-03", "formula_id": "F-VAR-03", "ability_id": "A-CALC"},
            "B": {"knowledge_point_id": "K-VAR-04", "formula_id": "F-VAR-03", "ability_id": "A-ALG"},
            "C": {"knowledge_point_id": "K-VAR-03", "formula_id": "F-VAR-03", "ability_id": "A-COND"},
        },
    },
    11: {
        "topic_id": "T-STA",
        "knowledge_point_ids": ["K-STA-01", "K-STA-03"],
        "formula_ids": ["F-STA-01", "F-STA-02"],
        "ability_ids": ["A-CALC", "A-COND"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-STA-01", "formula_id": "F-STA-01", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-STA-03", "formula_id": "F-STA-02", "ability_id": "A-COND"},
            "C": {"knowledge_point_id": "K-STA-03", "formula_id": "F-STA-02", "ability_id": "A-CALC"},
        },
    },
    12: {
        "topic_id": "T-SEQ",
        "knowledge_point_ids": ["K-SEQ-05", "K-SEQ-01"],
        "formula_ids": ["F-SEQ-04"],
        "ability_ids": ["A-CHAIN", "A-CALC"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-SEQ-05", "formula_id": "F-SEQ-04", "ability_id": "A-CALC"},
            "B": {"knowledge_point_id": "K-SEQ-01", "formula_id": "F-SEQ-04", "ability_id": "A-ALG"},
            "C": {"knowledge_point_id": "K-SEQ-05", "formula_id": None, "ability_id": "A-COND"},
        },
    },
    13: {
        "topic_id": "T-NUM",
        "knowledge_point_ids": ["K-NUM-04"],
        "formula_ids": [],
        "ability_ids": ["A-COND", "A-CALC"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-NUM-04", "formula_id": None, "ability_id": "A-COND"},
            "B": {"knowledge_point_id": "K-NUM-04", "formula_id": None, "ability_id": "A-CALC"},
            "C": {"knowledge_point_id": "K-NUM-04", "formula_id": None, "ability_id": "A-COND"},
        },
    },
    14: {
        "topic_id": "T-NUM",
        "knowledge_point_ids": ["K-NUM-05"],
        "formula_ids": ["F-NUM-03"],
        "ability_ids": ["A-COND", "A-CHAIN"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-NUM-05", "formula_id": "F-NUM-03", "ability_id": "A-COND"},
            "B": {"knowledge_point_id": "K-NUM-05", "formula_id": "F-NUM-03", "ability_id": "A-CALC"},
            "C": {"knowledge_point_id": "K-NUM-05", "formula_id": "F-NUM-03", "ability_id": "A-CHAIN"},
        },
    },
    15: {
        "topic_id": "T-MEN",
        "knowledge_point_ids": ["K-MEN-01"],
        "formula_ids": ["F-MEN-01"],
        "ability_ids": ["A-ALG", "A-CALC"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-MEN-01", "formula_id": "F-MEN-01", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-MEN-01", "formula_id": "F-MEN-01", "ability_id": "A-CALC"},
            "C": {"knowledge_point_id": "K-MEN-01", "formula_id": "F-MEN-01", "ability_id": "A-COND"},
        },
    },
    16: {
        "topic_id": "T-MEN",
        "knowledge_point_ids": ["K-MEN-02", "K-MEN-03"],
        "formula_ids": ["F-MEN-02"],
        "ability_ids": ["A-ALG", "A-CHAIN"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-MEN-02", "formula_id": "F-MEN-02", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-MEN-03", "formula_id": "F-MEN-02", "ability_id": "A-ALG"},
            "C": {"knowledge_point_id": "K-MEN-02", "formula_id": "F-MEN-02", "ability_id": "A-CALC"},
        },
    },
    17: {
        "topic_id": "T-MEN",
        "knowledge_point_ids": ["K-MEN-01", "K-MEN-03", "K-GEO-05"],
        "formula_ids": ["F-MEN-01"],
        "ability_ids": ["A-CHAIN", "A-ALG"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-MEN-03", "formula_id": "F-MEN-01", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-MEN-01", "formula_id": "F-MEN-01", "ability_id": "A-CALC"},
            "C": {"knowledge_point_id": "K-GEO-05", "formula_id": None, "ability_id": "A-CHAIN"},
        },
    },
    18: {
        "topic_id": "T-TRI",
        "knowledge_point_ids": ["K-TRI-01", "K-TRI-02"],
        "formula_ids": ["F-TRI-01", "F-TRI-02"],
        "ability_ids": ["A-SUB", "A-CALC"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-TRI-01", "formula_id": "F-TRI-01", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-TRI-01", "formula_id": "F-TRI-02", "ability_id": "A-CALC"},
            "C": {"knowledge_point_id": "K-TRI-02", "formula_id": "F-TRI-01", "ability_id": "A-SUB"},
        },
    },
    19: {
        "topic_id": "T-TRI",
        "knowledge_point_ids": ["K-TRI-03", "K-TRI-02"],
        "formula_ids": ["F-TRI-03"],
        "ability_ids": ["A-ALG", "A-COND"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-TRI-03", "formula_id": "F-TRI-03", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-TRI-03", "formula_id": "F-TRI-03", "ability_id": "A-COND"},
            "C": {"knowledge_point_id": "K-TRI-02", "formula_id": None, "ability_id": "A-CALC"},
        },
    },
    20: {
        "topic_id": "T-GEO",
        "knowledge_point_ids": ["K-GEO-01", "K-GEO-04"],
        "formula_ids": ["F-GEO-01", "F-GEO-04"],
        "ability_ids": ["A-CHAIN", "A-ALG"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-GEO-01", "formula_id": "F-GEO-01", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-GEO-04", "formula_id": "F-GEO-04", "ability_id": "A-CALC"},
            "C": {"knowledge_point_id": "K-GEO-01", "formula_id": "F-GEO-01", "ability_id": "A-CHAIN"},
        },
    },
    21: {
        "topic_id": "T-GEO",
        "knowledge_point_ids": ["K-MEN-02", "K-GEO-01"],
        "formula_ids": ["F-MEN-03", "F-MEN-04"],
        "ability_ids": ["A-CALC", "A-CHAIN"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-MEN-02", "formula_id": "F-MEN-03", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-MEN-01", "formula_id": "F-MEN-04", "ability_id": "A-CALC"},
            "C": {"knowledge_point_id": "K-MEN-02", "formula_id": "F-MEN-03", "ability_id": "A-CHAIN"},
        },
    },
    22: {
        "topic_id": "T-GEO",
        "knowledge_point_ids": ["K-GEO-04"],
        "formula_ids": ["F-GEO-03", "F-GEO-04"],
        "ability_ids": ["A-ALG", "A-COND"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-GEO-04", "formula_id": "F-GEO-03", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-GEO-04", "formula_id": "F-GEO-04", "ability_id": "A-COND"},
            "C": {"knowledge_point_id": "K-GEO-04", "formula_id": "F-GEO-03", "ability_id": "A-CALC"},
        },
    },
    23: {
        "topic_id": "T-TRF",
        "knowledge_point_ids": ["K-TRF-03", "K-TRF-04"],
        "formula_ids": ["F-TRF-01", "F-TRF-02"],
        "ability_ids": ["A-ALG", "A-CHAIN"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-TRF-04", "formula_id": "F-TRF-02", "ability_id": "A-CALC"},
            "B": {"knowledge_point_id": "K-TRF-03", "formula_id": "F-TRF-01", "ability_id": "A-ALG"},
            "C": {"knowledge_point_id": "K-TRF-03", "formula_id": "F-TRF-01", "ability_id": "A-COND"},
        },
    },
    24: {
        "topic_id": "T-LIN",
        "knowledge_point_ids": ["K-LIN-01"],
        "formula_ids": ["F-LIN-01"],
        "ability_ids": ["A-CALC", "A-ALG"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-LIN-01", "formula_id": "F-LIN-01", "ability_id": "A-CALC"},
            "B": {"knowledge_point_id": "K-LIN-01", "formula_id": "F-LIN-01", "ability_id": "A-ALG"},
            "C": {"knowledge_point_id": "K-LIN-01", "formula_id": "F-LIN-01", "ability_id": "A-COND"},
        },
    },
    25: {
        "topic_id": "T-LIN",
        "knowledge_point_ids": ["K-LIN-02", "K-LIN-03"],
        "formula_ids": ["F-LIN-03"],
        "ability_ids": ["A-GRAPH", "A-COND"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-LIN-02", "formula_id": "F-LIN-03", "ability_id": "A-COND"},
            "B": {"knowledge_point_id": "K-LIN-02", "formula_id": "F-LIN-03", "ability_id": "A-GRAPH"},
            "C": {"knowledge_point_id": "K-LIN-03", "formula_id": "F-LIN-03", "ability_id": "A-ALG"},
        },
    },
    26: {
        "topic_id": "T-CIR",
        "knowledge_point_ids": ["K-CIR-01", "K-CIR-02"],
        "formula_ids": ["F-CIR-01"],
        "ability_ids": ["A-ALG", "A-COND"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-CIR-02", "formula_id": "F-CIR-01", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-CIR-02", "formula_id": "F-CIR-01", "ability_id": "A-COND"},
            "C": {"knowledge_point_id": "K-CIR-01", "formula_id": "F-CIR-01", "ability_id": "A-CALC"},
        },
    },
    27: {
        "topic_id": "T-PROB",
        "knowledge_point_ids": ["K-PROB-01", "K-PROB-05"],
        "formula_ids": ["F-PROB-01"],
        "ability_ids": ["A-COND", "A-CALC"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-PROB-01", "formula_id": "F-PROB-01", "ability_id": "A-COND"},
            "B": {"knowledge_point_id": "K-PROB-05", "formula_id": "F-PROB-01", "ability_id": "A-CALC"},
            "C": {"knowledge_point_id": "K-PROB-01", "formula_id": "F-PROB-01", "ability_id": "A-ALG"},
        },
    },
    28: {
        "topic_id": "T-PROB",
        "knowledge_point_ids": ["K-PROB-01", "K-CHR-02"],
        "formula_ids": ["F-PROB-01"],
        "ability_ids": ["A-GRAPH", "A-CALC"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-CHR-02", "formula_id": None, "ability_id": "A-GRAPH"},
            "B": {"knowledge_point_id": "K-PROB-01", "formula_id": "F-PROB-01", "ability_id": "A-CALC"},
            "C": {"knowledge_point_id": "K-PROB-01", "formula_id": "F-PROB-01", "ability_id": "A-COND"},
        },
    },
    29: {
        "topic_id": "T-STA",
        "knowledge_point_ids": ["K-STA-05", "K-STA-01"],
        "formula_ids": ["F-STA-02", "F-STA-04"],
        "ability_ids": ["A-CALC", "A-CHAIN"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-STA-01", "formula_id": "F-STA-02", "ability_id": "A-CALC"},
            "B": {"knowledge_point_id": "K-STA-05", "formula_id": "F-STA-04", "ability_id": "A-ALG"},
            "C": {"knowledge_point_id": "K-STA-05", "formula_id": "F-STA-04", "ability_id": "A-CHAIN"},
        },
    },
    30: {
        "topic_id": "T-STA",
        "knowledge_point_ids": ["K-STA-01", "K-STA-02"],
        "formula_ids": ["F-STA-01"],
        "ability_ids": ["A-CALC", "A-COND"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-STA-01", "formula_id": "F-STA-01", "ability_id": "A-CALC"},
            "B": {"knowledge_point_id": "K-STA-02", "formula_id": None, "ability_id": "A-COND"},
            "C": {"knowledge_point_id": "K-STA-02", "formula_id": None, "ability_id": "A-ALG"},
        },
    },
    31: {
        "topic_id": "T-NUM",
        "knowledge_point_ids": ["K-NUM-02"],
        "formula_ids": ["F-NUM-01"],
        "ability_ids": ["A-ALG", "A-CALC"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-NUM-02", "formula_id": "F-NUM-01", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-NUM-02", "formula_id": "F-NUM-01", "ability_id": "A-CALC"},
            "C": {"knowledge_point_id": "K-NUM-02", "formula_id": None, "ability_id": "A-COND"},
        },
    },
    32: {
        "topic_id": "T-EXP",
        "knowledge_point_ids": ["K-EXP-06", "K-EXP-07"],
        "formula_ids": ["F-EXP-09"],
        "ability_ids": ["A-ALG", "A-CHAIN"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-EXP-06", "formula_id": "F-EXP-09", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-EXP-07", "formula_id": "F-EXP-09", "ability_id": "A-CHAIN"},
            "C": {"knowledge_point_id": "K-EXP-06", "formula_id": "F-EXP-08", "ability_id": "A-COND"},
        },
    },
    33: {
        "topic_id": "T-NUM",
        "knowledge_point_ids": ["K-NUM-03"],
        "formula_ids": ["F-NUM-02"],
        "ability_ids": ["A-CALC", "A-SUB"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-NUM-03", "formula_id": "F-NUM-02", "ability_id": "A-CALC"},
            "B": {"knowledge_point_id": "K-NUM-03", "formula_id": "F-NUM-02", "ability_id": "A-SUB"},
            "C": {"knowledge_point_id": "K-NUM-03", "formula_id": "F-NUM-02", "ability_id": "A-COND"},
        },
    },
    34: {
        "topic_id": "T-FUN",
        "knowledge_point_ids": ["K-FUN-03"],
        "formula_ids": ["F-FUN-01"],
        "ability_ids": ["A-ALG", "A-GRAPH"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-FUN-03", "formula_id": "F-FUN-01", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-FUN-03", "formula_id": "F-FUN-01", "ability_id": "A-GRAPH"},
            "C": {"knowledge_point_id": "K-FUN-03", "formula_id": "F-FUN-01", "ability_id": "A-CALC"},
        },
    },
    35: {
        "topic_id": "T-NUM",
        "knowledge_point_ids": ["K-NUM-06"],
        "formula_ids": ["F-NUM-04"],
        "ability_ids": ["A-ALG", "A-CALC"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-NUM-06", "formula_id": "F-NUM-04", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-NUM-06", "formula_id": "F-NUM-04", "ability_id": "A-CALC"},
            "C": {"knowledge_point_id": "K-NUM-06", "formula_id": "F-NUM-04", "ability_id": "A-COND"},
        },
    },
    36: {
        "topic_id": "T-EQN",
        "knowledge_point_ids": ["K-EQN-06"],
        "formula_ids": ["F-EQN-04"],
        "ability_ids": ["A-GRAPH", "A-BACK"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-EQN-06", "formula_id": "F-EQN-04", "ability_id": "A-GRAPH"},
            "B": {"knowledge_point_id": "K-EQN-06", "formula_id": "F-EQN-04", "ability_id": "A-BACK"},
            "C": {"knowledge_point_id": "K-EQN-05", "formula_id": "F-EQN-03", "ability_id": "A-ALG"},
        },
    },
    37: {
        "topic_id": "T-SEQ",
        "knowledge_point_ids": ["K-SEQ-02", "K-SEQ-04"],
        "formula_ids": ["F-SEQ-01", "F-SEQ-02"],
        "ability_ids": ["A-SUB", "A-CALC"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-SEQ-02", "formula_id": "F-SEQ-01", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-SEQ-04", "formula_id": "F-SEQ-02", "ability_id": "A-CALC"},
            "C": {"knowledge_point_id": "K-SEQ-02", "formula_id": "F-SEQ-01", "ability_id": "A-SUB"},
        },
    },
    38: {
        "topic_id": "T-FUN",
        "knowledge_point_ids": ["K-FUN-04"],
        "formula_ids": ["F-FUN-02", "F-FUN-03"],
        "ability_ids": ["A-GRAPH", "A-COND"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-FUN-04", "formula_id": "F-FUN-02", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-FUN-04", "formula_id": "F-FUN-03", "ability_id": "A-GRAPH"},
            "C": {"knowledge_point_id": "K-FUN-04", "formula_id": "F-FUN-02", "ability_id": "A-COND"},
        },
    },
    39: {
        "topic_id": "T-TRI",
        "knowledge_point_ids": ["K-TRI-05"],
        "formula_ids": ["F-TRI-05"],
        "ability_ids": ["A-GRAPH", "A-COND"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-TRI-05", "formula_id": "F-TRI-05", "ability_id": "A-GRAPH"},
            "B": {"knowledge_point_id": "K-TRI-05", "formula_id": "F-TRI-05", "ability_id": "A-COND"},
            "C": {"knowledge_point_id": "K-TRI-05", "formula_id": "F-TRI-05", "ability_id": "A-ALG"},
        },
    },
    40: {
        "topic_id": "T-MEN",
        "knowledge_point_ids": ["K-MEN-05"],
        "formula_ids": ["F-MEN-05", "F-TRI-04"],
        "ability_ids": ["A-CHAIN", "A-ALG"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-MEN-05", "formula_id": "F-MEN-05", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-MEN-05", "formula_id": "F-TRI-04", "ability_id": "A-CHAIN"},
            "C": {"knowledge_point_id": "K-MEN-05", "formula_id": "F-MEN-05", "ability_id": "A-COND"},
        },
    },
    41: {
        "topic_id": "T-GEO",
        "knowledge_point_ids": ["K-GEO-02", "K-GEO-01"],
        "formula_ids": ["F-GEO-02", "F-GEO-01"],
        "ability_ids": ["A-CHAIN", "A-ALG"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-GEO-02", "formula_id": "F-GEO-02", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-GEO-01", "formula_id": "F-GEO-01", "ability_id": "A-CHAIN"},
            "C": {"knowledge_point_id": "K-GEO-02", "formula_id": "F-GEO-02", "ability_id": "A-COND"},
        },
    },
    42: {
        "topic_id": "T-CIR",
        "knowledge_point_ids": ["K-CIR-03", "K-LIN-05"],
        "formula_ids": ["F-CIR-01", "F-LIN-04"],
        "ability_ids": ["A-CHAIN", "A-COND"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-CIR-03", "formula_id": "F-LIN-04", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-CIR-03", "formula_id": "F-CIR-01", "ability_id": "A-COND"},
            "C": {"knowledge_point_id": "K-LIN-05", "formula_id": "F-LIN-04", "ability_id": "A-CHAIN"},
        },
    },
    43: {
        "topic_id": "T-COM",
        "knowledge_point_ids": ["K-COM-03", "K-COM-04"],
        "formula_ids": ["F-COM-02", "F-COM-03"],
        "ability_ids": ["A-ALG", "A-CALC"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-COM-03", "formula_id": "F-COM-02", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-COM-04", "formula_id": "F-COM-03", "ability_id": "A-CALC"},
            "C": {"knowledge_point_id": "K-COM-03", "formula_id": "F-COM-02", "ability_id": "A-COND"},
        },
    },
    44: {
        "topic_id": "T-PROB",
        "knowledge_point_ids": ["K-PROB-04", "K-COM-03"],
        "formula_ids": ["F-PROB-03", "F-COM-02"],
        "ability_ids": ["A-CHAIN", "A-CALC"],
        "option_faults": {
            "A": {"knowledge_point_id": "K-PROB-04", "formula_id": "F-PROB-03", "ability_id": "A-ALG"},
            "B": {"knowledge_point_id": "K-COM-03", "formula_id": "F-COM-02", "ability_id": "A-CALC"},
            "C": {"knowledge_point_id": "K-PROB-04", "formula_id": "F-PROB-03", "ability_id": "A-CHAIN"},
        },
    },
    45: {
        "topic_id": "T-STA",
        "knowledge_point_ids": ["K-STA-06", "K-STA-04", "K-STA-05"],
        "formula_ids": ["F-STA-05", "F-STA-03", "F-STA-04"],
        "ability_ids": ["A-ELIM", "A-COND"],
        "option_faults": {
            "B": {"knowledge_point_id": "K-STA-04", "formula_id": "F-STA-03", "ability_id": "A-COND"},
            "C": {"knowledge_point_id": "K-STA-05", "formula_id": "F-STA-04", "ability_id": "A-ALG"},
            "D": {"knowledge_point_id": "K-STA-06", "formula_id": "F-STA-05", "ability_id": "A-ELIM"},
        },
    },
}


SCHEMA_MD = """# Math skills schema（本地基礎）

## 檔案

- `math_skill_book.json` — 固定技能冊（課題／知識點／公式／能力）
- `math_skill_book.md` — 同上，方便逐條睇
- `math_tag_crosswalk.json` — 題庫 tag → 技能冊 20 課題（不改網站既有 tag）
- `math_tag_crosswalk.md` — 同上對照表
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
python scripts/export_skill_book_md.py
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
"""


def index_book(book: dict):
    topics = {t["id"]: t for t in book["topics"]}
    kps = {}
    formulas = {}
    for t in book["topics"]:
        for k in t["knowledge_points"]:
            kps[k["id"]] = {**k, "topic_id": t["id"]}
        for f in t["formulas"]:
            formulas[f["id"]] = {**f, "topic_id": t["id"]}
    abilities = {a["id"]: a for a in book["abilities"]}
    return topics, kps, formulas, abilities


def validate_skills_block(skills: dict, book_idx, wrong_options: set[str]) -> list[str]:
    topics, kps, formulas, abilities = book_idx
    errs = []
    if not isinstance(skills, dict):
        return ["skills 不是物件"]
    tid = skills.get("topic_id")
    if tid not in topics:
        errs.append(f"未知 topic_id {tid!r}")
    for kid in skills.get("knowledge_point_ids") or []:
        if kid not in kps:
            errs.append(f"未知 knowledge_point_id {kid!r}")
    for fid in skills.get("formula_ids") or []:
        if fid not in formulas:
            errs.append(f"未知 formula_id {fid!r}")
    for aid in skills.get("ability_ids") or []:
        if aid not in abilities:
            errs.append(f"未知 ability_id {aid!r}")
    faults = skills.get("option_faults") or {}
    if not isinstance(faults, dict):
        errs.append("option_faults 須為物件")
        return errs
    for opt in faults:
        if opt not in "ABCD":
            errs.append(f"option_faults 鍵非法 {opt!r}")
        if opt not in wrong_options:
            errs.append(f"option_faults 含非錯選項或不存在選項 {opt}")
    for opt in wrong_options:
        if opt not in faults:
            errs.append(f"錯選項 {opt} 缺 option_faults")
            continue
        f = faults[opt]
        if not isinstance(f, dict):
            errs.append(f"{opt} fault 不是物件")
            continue
        kid, fid, aid = f.get("knowledge_point_id"), f.get("formula_id"), f.get("ability_id")
        if aid not in abilities:
            errs.append(f"{opt} 未知 ability_id {aid!r}")
        if kid is None and fid is None:
            errs.append(f"{opt} 須有 knowledge_point_id 或 formula_id")
        if kid is not None and kid not in kps:
            errs.append(f"{opt} 未知 knowledge_point_id {kid!r}")
        if fid is not None and fid not in formulas:
            errs.append(f"{opt} 未知 formula_id {fid!r}")
    return errs


def wrong_options_from_analysis(doc: dict) -> set[str]:
    oa = (doc.get("analysis") or {}).get("options_analysis") or {}
    return {k for k, v in oa.items() if isinstance(v, dict) and not v.get("is_correct")}


def remap_option_faults(raw_faults: dict, wrong: set[str]) -> dict:
    """Assign fault payloads to actual wrong options by sorted letter order.

    Pilot tables may list A/B/C even when the real wrong set is e.g. A/B/D;
    we keep three (or N) fault payloads and re-key them to the real wrong letters.
    """
    payloads = [raw_faults[k] for k in sorted(raw_faults)]
    targets = sorted(wrong)
    if len(payloads) != len(targets):
        raise ValueError(f"fault count {len(payloads)} != wrong count {len(targets)}")
    return {opt: payloads[i] for i, opt in enumerate(targets)}


def annotate_pilot(book: dict) -> tuple[int, list[str]]:
    idx = index_book(book)
    errors = []
    n = 0
    for qno, skills in PILOT_2012_P2.items():
        path = ANALYSIS_P2 / f"q{qno}.json"
        if not path.is_file():
            errors.append(f"缺檔 {path}")
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        wrong = wrong_options_from_analysis(doc)
        cleaned = dict(skills)
        try:
            cleaned["option_faults"] = remap_option_faults(skills.get("option_faults") or {}, wrong)
        except ValueError as e:
            errors.append(f"Q{qno}: {e}")
            continue
        ve = validate_skills_block(cleaned, idx, wrong)
        if ve:
            errors.append(f"Q{qno}: " + "; ".join(ve))
            continue
        doc["skills"] = cleaned
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        n += 1
    return n, errors


def coverage_report(book: dict) -> str:
    kps = sum(len(t["knowledge_points"]) for t in book["topics"])
    formulas = sum(len(t["formulas"]) for t in book["topics"])
    return (
        f"topics={len(book['topics'])} "
        f"knowledge_points={kps} "
        f"formulas={formulas} "
        f"abilities={len(book['abilities'])}"
    )


def main():
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    book = build_skill_book()
    crosswalk = build_crosswalk(book)

    book_path = SKILLS_DIR / "math_skill_book.json"
    cw_path = SKILLS_DIR / "math_tag_crosswalk.json"
    schema_path = SKILLS_DIR / "SCHEMA.md"

    book_path.write_text(json.dumps(book, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cw_path.write_text(json.dumps(crosswalk, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    schema_path.write_text(SCHEMA_MD, encoding="utf-8")

    # human-readable copies
    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "export_skill_book_md", ROOT / "scripts" / "export_skill_book_md.py"
        )
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)
        mod.export_book()
        mod.export_crosswalk()
    except Exception as e:
        print(f"warn: markdown export skipped ({e})")

    n, errors = annotate_pilot(book)
    print(coverage_report(book))
    print(f"wrote {book_path.relative_to(ROOT)}")
    print(f"wrote {cw_path.relative_to(ROOT)} ({len(crosswalk['map'])} tags)")
    print(f"annotated {n} / {len(PILOT_2012_P2)} pilot questions")
    if errors:
        print("ERRORS:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("ok")


if __name__ == "__main__":
    main()
