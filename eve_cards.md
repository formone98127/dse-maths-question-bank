# 開考倒數卡組（源檔）

> 格式：`## id | kind | speaker | [trap|true] | [min_days] | [belief_of]`
> kind：life | urgent | belief | exam
> speaker：self | parents | classmate | tutor | exam
> body 係對白（LaTeX 用 `$…$`），之後：
> - `left:` / `right:` — 標籤 `|` 橫條加減（brain/time/score/mood）
> - `correct:` — 正確一句（belief / exam 用；死亡畫面顯示）
> - `exam:` — belief 卡對應嘅考試局卡 id
> - `timeout:` — urgent 卡唔滑嘅橫條加減
> 由 scripts/build_eve_cards.py 產生 docs/eve/cards.js。

## LIFE-01 | life | parents

今晚做到十二點，聽日就唔使急。

left: 做到十二點 | brain:-2,score:+2,mood:-1
right: 早瞓 | mood:+2,brain:+1,score:-1

## LIFE-02 | life | self

先睇五分鐘電話。

left: 睇 | mood:+2,time:-2
right: 收起 | time:+1,mood:-1

## LIFE-03 | life | classmate

落去茶記坐陣，陣間再溫。

left: 去 | mood:+2,time:-2
right: 唔去 | time:+1,mood:-1

## LIFE-04 | life | parents

再幫你報多一科補習。

left: 報 | score:+1,time:-2,mood:-1
right: 唔報 | time:+1,mood:+1,score:-1

## LIFE-05 | life | self

今晚溫熟的，定係溫最憎的？

left: 溫熟的 | mood:+1,brain:+1,score:-1
right: 溫最憎的 | brain:-2,score:+2,mood:-1

## LIFE-06 | life | classmate

筆記借你抄，快過自己寫。

left: 抄 | time:+1,mood:+1,score:-1
right: 自己寫 | time:-2,brain:-1,score:+1

## LIFE-07 | life | self

而家對答案，定係遲啲先對？

left: 而家對 | brain:-1,score:+1
right: 遲啲先 | mood:+1,time:-1

## LIFE-08 | life | self

聽歌先溫得落去。

left: 聽 | mood:+2,brain:-1
right: 靜音 | brain:+1,mood:-1

## LIFE-09 | life | tutor

這課題很少出，跳過啦。

left: 跳過 | time:+2,mood:+1,score:-2
right: 照溫 | time:-2,score:+2,brain:-1

## LIFE-10 | life | parents

星期日一齊去飲茶。

left: 去 | mood:+2,time:-2
right: 留屋企 | time:+1,mood:-2

## LIFE-11 | life | self

做錯的再做一次，定係做新題？

left: 再做一次 | brain:-2,score:+2
right: 做新題 | mood:+1,score:-1

## LIFE-12 | life | classmate | | 6

群組話今屆必考圓形，其他不用理。

left: 全溫圓 | time:-2,score:+1
right: 當沒看見 | mood:+1,score:-1

## URG-13 | urgent | self

鬧鐘響了。好眼瞓。

left: 瞓多陣 | mood:+1,time:-2
right: 起身 | brain:-1,time:+1
timeout: time:-2

## URG-14 | urgent | parents

而家出廳食飯。

left: 去食 | mood:+1,brain:+1,time:-1
right: 話遲啲 | time:+1,mood:-2
timeout: time:-2

## URG-15 | urgent | classmate

小測提前到下一節。

left: 狂溫 | brain:-2,score:+1
right: 這科算了 | mood:+1,score:-2
timeout: time:-2

## URG-16 | urgent | self

電話得返 5% 電。

left: 去借充電器 | time:-1,mood:-1
right: 做到沒電 | brain:-1,time:+1
timeout: time:-2

## BEL-17 | belief | classmate | trap

$\log(x+y) = \log x + \log y$

left: 信 | score:0
right: 唔信 | score:0
correct: log 只拆得開乘同除，加減拆唔開。
exam: EXAM-29

## BEL-18 | belief | tutor | true

$\log_a(xy) = \log_a x + \log_a y$（$x>0,\,y>0$）

left: 信 | score:0
right: 唔信 | score:0
correct: 括號裡係乘，先可以拆成相加。
exam: EXAM-30

## BEL-19 | belief | classmate | trap

$(x+y)^2 = x^2 + y^2$

left: 信 | score:0
right: 唔信 | score:0
correct: 仲有 $2xy$，完整係 $x^2+2xy+y^2$。
exam: EXAM-31

## BEL-20 | belief | tutor | true

$x^2 - y^2 = (x-y)(x+y)$

left: 信 | score:0
right: 唔信 | score:0
correct: 平方差公式就係咁。
exam: EXAM-32

## BEL-21 | belief | tutor | trap

對任意實數 $a$，都有 $a^0 = 0$。

left: 信 | score:0
right: 唔信 | score:0
correct: 任何非零數嘅 0 次方係 1，唔係 0。
exam: EXAM-33

## BEL-22 | belief | classmate | trap

$(a^m)^n = a^{m+n}$

left: 信 | score:0
right: 唔信 | score:0
correct: 外層冪係乘指數：$(a^m)^n=a^{mn}$。
exam: EXAM-34

## BEL-23 | belief | classmate | trap

件衫 \$100，先加 10%，再減 10%，就返原價。

left: 信 | score:0
right: 唔信 | score:0
correct: 110 再減 10% 係 99，加減嘅底數唔同。
exam: EXAM-35

## BEL-24 | belief | tutor | trap

解不等式時，兩邊同乘 $-1$，不等號方向唔使轉。

left: 信 | score:0
right: 唔信 | score:0
correct: 乘／除負數，不等號一定要轉。
exam: EXAM-36

## BEL-25 | belief | classmate | trap

$y=f(x-2)$ 的圖像是 $y=f(x)$ 向左平移 2 單位。

left: 信 | score:0
right: 唔信 | score:0
correct: $x-2$ 係向右移 2，符號同直覺相反。
exam: EXAM-37

## BEL-26 | belief | self | trap

若 $y$ 與 $x$ 成正比，則 $y=\dfrac{k}{x}$。

left: 信 | score:0
right: 唔信 | score:0
correct: 正比係 $y=kx$；$k/x$ 係反比。
exam: EXAM-38

## BEL-27 | belief | tutor | true

若 $y$ 與 $x$ 成反比，則 $xy$ 為常數。

left: 信 | score:0
right: 唔信 | score:0
correct: 反比即 $y=k/x$，所以 $xy=k$。
exam: EXAM-39

## BEL-28 | belief | tutor | true

圓面積公式是 $\pi r^2$。

left: 信 | score:0
right: 唔信 | score:0
correct: $\pi r^2$ 係面積，$2\pi r$ 係圓周。
exam: EXAM-40

## EXAM-29 | exam | exam | | | BEL-17

第 7 題：$\log(x+y)$ 可唔可以拆？

left: 睇卷 | score:0
right: 睇卷 | score:0
correct: log 只拆得開乘同除，加減拆唔開。

## EXAM-30 | exam | exam | | | BEL-18

第 8 題：$\log_a(xy)$ 點拆？

left: 睇卷 | score:0
right: 睇卷 | score:0
correct: 括號裡係乘，先可以拆成相加。

## EXAM-31 | exam | exam | | | BEL-19

第 3 題：展開 $(x+y)^2$。

left: 睇卷 | score:0
right: 睇卷 | score:0
correct: 仲有 $2xy$，完整係 $x^2+2xy+y^2$。

## EXAM-32 | exam | exam | | | BEL-20

第 4 題：化簡 $x^2-y^2$。

left: 睇卷 | score:0
right: 睇卷 | score:0
correct: 平方差公式就係咁。

## EXAM-33 | exam | exam | | | BEL-21

第 1 題：$a^0$ 等於幾多？

left: 睇卷 | score:0
right: 睇卷 | score:0
correct: 任何非零數嘅 0 次方係 1，唔係 0。

## EXAM-34 | exam | exam | | | BEL-22

第 2 題：$(a^m)^n$ 等於？

left: 睇卷 | score:0
right: 睇卷 | score:0
correct: 外層冪係乘指數：$(a^m)^n=a^{mn}$。

## EXAM-35 | exam | exam | | | BEL-23

應用題：加 10% 再減 10%。

left: 睇卷 | score:0
right: 睇卷 | score:0
correct: 110 再減 10% 係 99，加減嘅底數唔同。

## EXAM-36 | exam | exam | | | BEL-24

第 5 題：不等式兩邊乘 $-1$。

left: 睇卷 | score:0
right: 睇卷 | score:0
correct: 乘／除負數，不等號一定要轉。

## EXAM-37 | exam | exam | | | BEL-25

第 6 題：$y=f(x-2)$ 移去邊？

left: 睇卷 | score:0
right: 睇卷 | score:0
correct: $x-2$ 係向右移 2，符號同直覺相反。

## EXAM-38 | exam | exam | | | BEL-26

第 9 題：$y$ 同 $x$ 成正比？

left: 睇卷 | score:0
right: 睇卷 | score:0
correct: 正比係 $y=kx$；$k/x$ 係反比。

## EXAM-39 | exam | exam | | | BEL-27

第 10 題：$y$ 同 $x$ 成反比？

left: 睇卷 | score:0
right: 睇卷 | score:0
correct: 反比即 $y=k/x$，所以 $xy=k$。

## EXAM-40 | exam | exam | | | BEL-28

第 11 題：圓面積公式？

left: 睇卷 | score:0
right: 睇卷 | score:0
correct: $\pi r^2$ 係面積，$2\pi r$ 係圓周。
