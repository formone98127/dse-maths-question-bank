# MC 伏位卡組（源檔）

> 格式：`## id | 課題 tag | trap|true | 難度 1–3 | source_ref(可選)`
> body 係卡面陳述（LaTeX 用 `$…$` / `$$…$$`），之後一行 `hint:` 廣東話精警提示。
> 課題 tag 必須屬於 docs/hub/data.js TOPICS.math 嘅 20 個 tag。
> 由 scripts/build_trap_cards.py 產生 docs/trap/cards.js。

## EXP-001 | 指數與對數 | trap | 1

對任意實數 $a$，都有 $a^0 = 0$。

hint: 喂！任何非零數嘅 0 次方係 1，唔係 0 啊！

## EXP-002 | 指數與對數 | trap | 2

$$\log(x+y) = \log x + \log y$$

hint: log 只拆得乘除，加減拆唔開㗎！

## NUM-003 | 數系 | true | 1

$$1.\overline{3} = \frac{4}{3}$$

hint: 冇伏！設 $x=1.333\ldots$，$10x-x=12$，$x=\frac43$。

## PER-004 | 百分法 | trap | 2

一件貨標價 \$100，先加 10%，再減 10%，就會返返原價 \$100。

hint: 110 減 10% 係 99 啊——加減嘅基數唔同！

## STA-005 | 集中趨勢與離差 | trap | 2

一組數據每項同時加 5，標準差會增加 5。

hint: 全體一齊移，離散度冇變，SD 唔會變！

## PROB-006 | 概率 | true | 1

若事件 $A$ 與 $B$ 獨立，則 $P(A \cap B) = P(A) \times P(B)$。

hint: 冇伏！呢句正正係獨立事件嘅定義。

## TRI-007 | 三角學與解三角形 | trap | 2

$$\sin 2\theta = 2\sin\theta$$

hint: $\sin 2\theta = 2\sin\theta\cos\theta$，唔可以就咁乘大兩倍！

## GEO-008 | 圓形幾何 | true | 2

同一弧上，圓周角的度數是圓心角的一半。

hint: 冇伏！圓心角 = 2 × 圓周角（同弧）。

## COD-009 | 坐標幾何：直線 | trap | 3 | 2012P2Q25

兩條互相垂直的直線，其斜率的乘積等於 1。

hint: 垂直係 $m_1 m_2 = -1$，乘 1 係平行先啱！

## MEN-010 | 求積法 | trap | 3

圓錐的體積是同底同高圓柱的一半。

hint: 係 $\frac{1}{3}$，唔係 $\frac{1}{2}$——錐體係三分一！
