# 2020 M2 Paper 1 — 評卷參考（分題）

> 分題依據：MS 題號行 + marks 對題目卷分數 [4, 4, 6, 6, 7, 7, 8, 8, 12, 13, 13, 12]｜合計 100

## 第 1 題  <!-- 頁 [2]｜4/4（MS 小計） -->

Marks: 1A 1M 1A

1. (a) $(1-x)^4 = 1-4x+6x^2-4x^3+x^4$
(b) Note that $(1+kx)^9 = 1+C_1^9 kx+C_2^9 (kx)^2+\cdots+(kx)^9$. $C_2^9 k^2-4 C_1^9 k+6=-3$ $36 k^2-36 k+9=0$ $(2k-1)^2=0$
Thus, we have $k=\frac{1}{2}$.

## 第 2 題  <!-- 頁 [2]｜4/4（MS 小計） -->

Marks: 1M 1M 1M 1A 1M 1M 1M 1A

2. $f'(2)$
$= \lim_{h \to 0} \frac{f(2+h)-f(2)}{h}$
$= \lim_{h \to 0} \frac{2+h-\sqrt{4+h}}{h\sqrt{4+h}}$
$= \lim_{h \to 0} \frac{(2+h)^2-(4+h)}{h\sqrt{4+h}(2+h+\sqrt{4+h})}$
$= \lim_{h \to 0} \frac{h(h+3)}{h\sqrt{4+h}(2+h+\sqrt{4+h})}$
$= \lim_{h \to 0} \frac{h+3}{\sqrt{4+h}(2+h+\sqrt{4+h})}$
$= \frac{3}{8}$
$f'(x)$
$= \lim_{h \to 0} \frac{f(x+h)-f(x)}{h}$
$= \lim_{h \to 0} \frac{\frac{x+h}{\sqrt{2+x+h}}-\frac{x}{\sqrt{2+x}}}{h}$
$= \lim_{h \to 0} \frac{(x+h)\sqrt{2+x}-x\sqrt{2+x+h}}{h\sqrt{2+x}\sqrt{2+x+h}}$
$= \lim_{h \to 0} \frac{(2+x)(x+h)^2-x^2(2+x+h)}{h\sqrt{2+x}\sqrt{2+x+h}((x+h)\sqrt{2+x}+x\sqrt{2+x+h})}$
$= \lim_{h \to 0} \frac{h(x^2+4x+hx+2h)}{h\sqrt{2+x}\sqrt{2+x+h}((x+h)\sqrt{2+x}+x\sqrt{2+x+h})}$
$= \lim_{h \to 0} \frac{x^2+4x+hx+2h}{\sqrt{2+x}\sqrt{2+x+h}((x+h)\sqrt{2+x}+x\sqrt{2+x+h})}$
$= \frac{x^2+4x}{2x(2+x)\sqrt{2+x}}$
Thus, we have $f'(2)=\frac{3}{8}$.

## 第 3 題  <!-- 頁 [3]｜6/6（題目卷為準；MS 讀到 subtotals=無 cells=8） -->

Marks: 1M 1M 1M 1 1 1M 1M 1M

3. (a) (i) tan 3x = tan(2x+x) = $\frac{\tan 2x + \tan x}{1 - \tan 2x \tan x}$ = $\frac{\frac{2 \tan x}{1 - \tan^2 x} + \tan x}{1 - \left(\frac{2 \tan x}{1 - \tan^2 x}\right) \tan x}$ = $\frac{2 \tan x + \tan x - \tan^3 x}{1 - \tan^2 x - 2 \tan^2 x}$ = $\frac{3 \tan x - \tan^3 x}{1 - 3 \tan^2 x}$
(ii) tan x tan (60° - x) tan (60° + x) = tan x $\left(\frac{\tan 60° - \tan x}{1 + \tan 60^\circ \tan x}\right)\left(\frac{\tan 60^\circ + \tan x}{1 - \tan 60^\circ \tan x}\right)$
= tan x $\left(\frac{\sqrt{3} - \tan x}{1 + \sqrt{3} \tan x}\right)\left(\frac{\sqrt{3} + \tan x}{1 - \sqrt{3} \tan x}\right)$
= $\frac{3 \tan x - \tan^3 x}{1 - 3 \tan^2 x}$
= tan 3x
(b) Putting x = 5° in (a)(ii), we have tan 5° tan (60° - 5°) tan (60° + 5°) = tan 3(5°) tan 5° tan 55° tan 65° = tan 15° $\left(\frac{1}{\tan 85^\circ}\right) \tan 55^\circ \tan 65^\circ = \frac{1}{\tan 75^\circ}$ tan 55° tan 65° tan 75° = tan 85°
Putting x = 25° in (a)(ii), we have tan 25° tan (60° - 25°) tan (60° + 25°) = tan 3(25°) tan 25° tan 35° tan 85° = tan 75° $\left(\frac{1}{\tan 65^\circ}\right)\left(\frac{1}{\tan 55^\circ}\right) \tan 85^\circ = \tan 75^\circ$ tan 55° tan 65° tan 75° = tan 85°
Putting x = 95° in (a)(ii), we have tan 95° tan (60° - 95°) tan (60° + 95°) = tan 3(95°) tan 95° tan (-35°) tan 155° = tan 285° $\tan 85^\circ\left(\frac{1}{\tan 55^\circ}\right)\left(\frac{1}{\tan 65^\circ}\right) = \tan 75^\circ$ tan 55° tan 65° tan 75° = tan 85°

## 第 4 題  <!-- 頁 [4]｜6/6（題目卷為準；MS 讀到 subtotals=無 cells=6） -->

Marks: 1M 1A 1M 1M 1M 1A

4. (a) $\int \sin^2\theta \mathrm{d}\theta$
$= \int \frac{1-\cos 2\theta}{2} \mathrm{d}\theta$
$= \frac{\theta}{2} - \frac{1}{2} \int \cos 2\theta \mathrm{d}\theta$
$= \frac{\theta}{2} - \frac{\sin 2\theta}{4} + \mathrm{constant}$
(b) The required volume
$= \pi \int_0^1 \left( 4x(1-x^2)^{\frac{1}{4}} \right)^2 \mathrm{d}x$
$= \pi \int_0^{\frac{\pi}{2}} 16 \sin^2 u \cos^2 u \mathrm{d}u$ (by letting $x = \sin u$)
$= \pi \int_0^{\frac{\pi}{2}} 4 \sin^2 2u \mathrm{d}u$
$= 2\pi \int_0^{\pi} \sin^2\theta \mathrm{d}\theta$ (by letting $\theta = 2u$)
$= \pi \left[ \theta - \frac{\sin 2\theta}{2} \right]_0^{\pi}$ (by (a))
$= \pi^2$

## 第 5 題  <!-- 頁 [5]｜7/7（題目卷為準；MS 讀到 subtotals=無 cells=2） -->

Marks: 1 1M

5. (a) Note that $\frac{1}{(1)(2)(3)} = \frac{(1)(4)}{4(2)(3)}$. Therefore, the statement is true for $n = 1$. Assume that $\sum_{k=1}^{m} \frac{1}{k(k+1)(k+2)} = \frac{m(m+3)}{4(m+1)(m+2)}$, where $m$ is a positive integer. $$\sum_{k=1}^{m+1} \frac{1}{k(k+1)(k+2)} = \sum_{k=1}^{m} \frac{1}{k(k+1)(k+2)} + \frac{1}{(m+1)(m+2)(m+3)} = \frac{m(m+3)}{4(m+1)(m+2)} + \frac{1}{(m+1)(m+2)(m+3)} \quad (\text{by induction assumption})$$ $$= \frac{m(m+3)^2 + 4}{4(m+1)(m+2)(m+3)} = \frac{m^3 + 6m^2 + 9m + 4}{4(m+1)(m+2)(m+3)} = \frac{(m+1)^2(m+4)}{4(m+1)(m+2)(m+3)} = \frac{(m+1)(m+4)}{4(m+2)(m+3)}$$ So, the statement is true for $n = m+1$ if it is true for $n = m$. By mathematical induction, the statement is true for all positive integers $n$.
(b) $\sum_{k=4}^{123} \frac{50}{k(k+1)(k+2)} = 50 \sum_{k=4}^{123} \frac{1}{k(k+1)(k+2)} = 50 \left( \sum_{k=1}^{123} \frac{1}{k(k+1)(k+2)} - \sum_{k=1}^{3} \frac{1}{k(k+1)(k+2)} \right) = 50 \left( \frac{(123)(123+3)}{4(123+1)(123+2)} - \frac{1}{6} - \frac{1}{24} - \frac{1}{60} \right) \quad (\text{by (a)})$ $$= 50 \left( \frac{(123)(126)}{4(124)(125)} - \frac{9}{40} \right) = \frac{387}{310}$$

## 第 6 題  <!-- 頁 [6]｜7/7（題目卷為準；MS 讀到 subtotals=無 cells=7） -->

Marks: 1M 1A 1M 1M 1M 1M 1A

6. (a) Let $A$ square units be the area of the circle with $OP$ as a diameter. $A = \pi \left( \frac{\sqrt{u^2 + v^2}}{2} \right)^2 = \frac{\pi}{4} (u^2 + v^2)$
Therefore, we have $u^2 + v^2 = \frac{4A}{\pi}$.
Hence, we have $S = \frac{4A}{\pi}$.
At time $t$ s, we have $\frac{dS}{dt} = \frac{4}{\pi} \left( \frac{dA}{dt} \right) = \frac{4}{\pi} (5\pi) = 20$.
Note that 20 is a positive constant.
Thus, $S$ increases at a constant rate.
(b) Let $R$ square units be the area of $\Delta OPQ$.
Note that $R = \frac{1}{2} u (2^u - 2^{u-1}) = u 2^{u-2}$.
At time $t$ s, we have $\frac{dR}{dt} = (1 + u \ln 2) 2^{u-2} \frac{du}{dt}$.
Since $\frac{d}{dt} (u^2 + v^2) = 20$ (by (a)), we have $2u \frac{du}{dt} + 2v \frac{dv}{dt} = 20$.
Therefore, we have $2u \frac{du}{dt} + 2 (2^{u-1})^2 \ln 2 \frac{du}{dt} = 20$.
Hence, we have $\frac{du}{dt} = \frac{10}{u + 2^{2u-2} \ln 2}$.
$\left. \frac{du}{dt} \right|_{u=2} = \frac{10}{2 + 4 \ln 2}$
$= \frac{5}{1 + 2 \ln 2}$
$\left. \frac{dR}{dt} \right|_{u=2} = (1 + 2 \ln 2) \frac{du}{dt} \left|_{u=2} \right.$
$= (1 + 2 \ln 2) \frac{5}{1 + 2 \ln 2}$
$= 5$
Thus, the required rate of change is 5 square units per second.

## 第 7 題  <!-- 頁 [7]｜8/8（題目卷為準；MS 讀到 subtotals=無 cells=9） -->

Marks: 1M 1M 1A 1M 1A 1M 1M 1M 1A

7. (a) $f(x) = \int (-2x+8) \, dx$ $= -x^2+8x+C$, where $C$ is a constant
Since $f(1)=2$, we have $-1^2+8(1)+C=2$.
Solving, we have $C=-5$.
Thus, the equation of $\Gamma$ is $y=-x^2+8x-5$.
(b) (i) Let $(a,b)$ be the coordinates of $P$.
Therefore, we have $\frac{b-14}{a-5}=-2a+8$ and $b=-a^2+8a-5$. $-2a^2+18a-26=-a^2+8a-5$ $a^2-10a+21=0$ $a=7$ or $a=3$
Since $f'(7)=-6 0$, we have $a=7$.
Thus, the coordinates of $P$ are $(7,2)$.
(ii) The slope of the tangent to $\Gamma$ at $P$
$=f'(7)$ $=-6$
The slope of the normal to $\Gamma$ at $P$
The equation of the normal to $\Gamma$ at $P$ is
$y-2=\frac{1}{6}(x-7)$
$x-6y+5=0$

## 第 8 題  <!-- 頁 [8]｜8/8（題目卷為準；MS 讀到 subtotals=無 cells=14） -->

Marks: 1M 1M 1M 1M 1A 1M 1M 1M 1M 1M 1M 1M 1 1

8. (a) $\begin{pmatrix} -5 & -2 \\ 15 & 6 \end{pmatrix} \begin{pmatrix} 1 & a \\ b & c \end{pmatrix} = \begin{pmatrix} 1 & a \\ b & c \end{pmatrix} \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$ $\begin{pmatrix} -5 - 2b & -5a - 2c \\ 15 + 6b & 15a + 6c \end{pmatrix} = \begin{pmatrix} 1 & 0 \\ b & 0 \end{pmatrix}$
So, we have $-5 - 2b = 1$, $-5a - 2c = 0$, $15 + 6b = b$ and $15a + 6c = 0$. Therefore, we have $b = -3$ and $c = \frac{-5}{2}a$. Since $|M| = 1$, we have $c - ab = 1$. Hence, we have $\frac{-5a}{2} + 3a = 1$. Thus, we have $a = 2$, $b = -3$ and $c = -5$.
(b) (i) By (a), we have $M = \begin{pmatrix} 1 & 2 \\ -3 & -5 \end{pmatrix}$.
$M^{-1} = \frac{1}{1} \begin{pmatrix} -5 & -2 \\ 3 & 1 \end{pmatrix}$ $= \begin{pmatrix} -5 & -2 \\ 3 & 1 \end{pmatrix}$
$M^{-1}RM = \begin{pmatrix} -5 & -2 \\ 3 & 1 \end{pmatrix} \begin{pmatrix} 6 & 2 \\ -15 & -5 \end{pmatrix} \begin{pmatrix} 1 & 2 \\ -3 & -5 \end{pmatrix}$ $= \begin{pmatrix} 0 & 0 \\ 3 & 1 \end{pmatrix} \begin{pmatrix} 1 & 2 \\ -3 & -5 \end{pmatrix}$ $= \begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix}$
(ii) Note that $P = M \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} M^{-1}$.
By (b)(i), we have $R = M \begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix} M^{-1}$.
$(\alpha P + \beta R)^{99}$
$= \left[ \alpha M \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} M^{-1} + \beta M \begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix} M^{-1} \right]^{99}$
$= \left[ M \begin{pmatrix} \alpha & 0 \\ 0 & \beta \end{pmatrix} M^{-1} \right]^{99}$
$= M \begin{pmatrix} \alpha & 0 \\ 0 & \beta \end{pmatrix} M^{-1}$
$= M \begin{pmatrix} \alpha^{99} & 0 \\ 0 & \beta^{99} \end{pmatrix} M^{-1}$
$= \alpha^{99} M \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} M^{-1} + \beta^{99} M \begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix} M^{-1}$
$= \alpha^{99} P + \beta^{99} R$

## 第 9 題  <!-- 頁 [9]｜12/12（題目卷為準；MS 讀到 subtotals=無 cells=8） -->

Marks: 1A 1M 1A 1M 1A 1M 1M 1M

9. (a) The equation of the vertical asymptote is $x - 4 = 0$.
Note that $\frac{(x + 4)^3}{(x - 4)^2} = x + 20 + \frac{192x - 256}{(x - 4)^2}$.
Thus, the equation of the oblique asymptote is $y = x + 20$.
(b) $f'(x)$
$= \frac{(x - 4)^2(3(x + 4)^2) - (x + 4)^3(2(x - 4))}{(x - 4)^4}$
$= \frac{(x + 4)^2(x - 20)}{(x - 4)^3}$
$f''(x)$
$= \frac{384(x + 4)}{(x - 4)^4}$
(c) By (b), we have $f'(x) = \frac{(x + 4)^2(x - 20)}{(x - 4)^3}$.
So, we have $f'(x) = 0 \iff x = -4$ or $x = 20$.
$x \quad (-\infty, -4) \quad -4 \quad (-4, 4) \quad (4, 20) \quad 20 \quad (20, \infty)$
$f'(x) \quad + \quad 0 \quad + \quad - \quad 0 \quad +$
$f(x) \quad \neq \quad 0 \quad \neq \quad \neq \quad 54 \quad \neq$
Therefore, there is only one turning point of $H$.
Thus, the claim is disagreed.
(d) By (b), we have $f''(x) = \frac{384(x + 4)}{(x - 4)^4}$.
So, we have $f''(x) = 0 \iff x = -4$.
$x \quad (-\infty, -4) \quad -4 \quad (-4, 4)$
$f''(x) \quad - \quad 0 \quad +$
Thus, the point of inflexion of $H$ is $(-4, 0)$.
(e) The required area
$= \int_{-4}^{0} \frac{(x + 4)^3}{(x - 4)^2} \mathrm{d}x$
$= \int_{-8}^{-4} \frac{(u + 8)^3}{u^2} \mathrm{d}u$
$= \int_{-8}^{-4} \left( u + 24 + \frac{192}{u} + \frac{512}{u^2} \right) \mathrm{d}u$
$= \left[ \frac{u^2}{2} + 24u + 192 \ln|u| - \frac{512}{u} \right]_{-8}^{-4}$
$= 136 - 192 \ln 2$

## 第 10 題  <!-- 頁 [10, 11]｜13/13（題目卷為準；MS 讀到 subtotals=無 cells=21） -->

Marks: 1M 1M 1 1M 1M 1M 1A 1M 1 1M 1 1M 1M 1M 1M 1M 1 1 1 1 1

10. (a) Let $u = \frac{\pi}{4} - x$. Then, we have $\frac{du}{dx} = -1$.
$$\int_{\frac{\pi}{12}}^{\frac{\pi}{6}} \ln \left( \sin \left( \frac{\pi}{4} - x \right) \right) dx$$
$= -\int_{\frac{\pi}{6}}^{\frac{\pi}{12}} \ln(\sin u) du$
$= \int_{\frac{\pi}{12}}^{\frac{\pi}{6}} \ln(\sin u) du$
$= \int_{\frac{\pi}{12}}^{\frac{\pi}{6}} \ln(\sin x) dx$
(b) $\int_{\frac{\pi}{12}}^{\frac{\pi}{6}} \ln \left( \sin \left( \frac{\pi}{4} - x \right) \right) dx = \int_{\frac{\pi}{12}}^{\frac{\pi}{6}} \ln(\sin x) dx$ (by (a))
$$\int_{\frac{\pi}{12}}^{\frac{\pi}{6}} \ln \left( \sin \frac{\pi}{4} \cos x - \cos \frac{\pi}{4} \sin x \right) dx = \int_{\frac{\pi}{12}}^{\frac{\pi}{6}} \ln(\sin x) dx$
$$\int_{\frac{\pi}{12}}^{\frac{\pi}{6}} \ln \left( \frac{1}{\sqrt{2}} (\cos x - \sin x) \right) dx = \int_{\frac{\pi}{12}}^{\frac{\pi}{6}} \ln(\sin x) dx$
$$\int_{\frac{\pi}{12}}^{\frac{\pi}{6}} \left( \ln \left( \frac{1}{\sqrt{2}} \right) + \ln(\cos x - \sin x) \right) dx = \int_{\frac{\pi}{12}}^{\frac{\pi}{6}} \ln(\sin x) dx$
$$\int_{\frac{\pi}{12}}^{\frac{\pi}{6}} \ln \left( \frac{\cos x - \sin x}{\sin x} \right) dx = \int_{\frac{\pi}{12}}^{\frac{\pi}{6}} \ln \sqrt{2} dx$
$$\int_{\frac{\pi}{12}}^{\frac{\pi}{6}} \ln(\cot x - 1) dx = \frac{\pi \ln 2}{24}$
(c) (i) $\cot \frac{\pi}{12}$
$= \cot \left( \frac{\pi}{4} - \frac{\pi}{6} \right)$
$= \frac{\cot \frac{\pi}{4} \cot \frac{\pi}{6} + 1}{\cot \frac{\pi}{6} - \cot \frac{\pi}{4}}$
$= \frac{(\sqrt{3} + 1)(\sqrt{3} + 1)}{(\sqrt{3} - 1)(\sqrt{3} + 1)}$
$= \frac{3 + 2\sqrt{3} + 1}{2}$
$= 2 + \sqrt{3}$
$$\cot \left( \frac{\pi}{12} - \left( \frac{-\pi}{12} \right) \right) = \cot \frac{\pi}{6}$$ $$\frac{\cot \frac{\pi}{12} \cot \left( \frac{-\pi}{12} \right) + 1}{\cot \left( \frac{-\pi}{12} \right) - \cot \frac{\pi}{12}} = \cot \frac{\pi}{6}$$ $$-\cot^2 \frac{\pi}{12} + 1 - 2 \cot \frac{\pi}{12} = \sqrt{3}$$ $$\cot^2 \frac{\pi}{12} - 2\sqrt{3} \cot \frac{\pi}{12} - 1 = 0$$ $$\cot \frac{\pi}{12} = \frac{2\sqrt{3} \pm \sqrt{(-2\sqrt{3})^2 - 4(1)(-1)}}{2}$$ $$\cot \frac{\pi}{12} = 2 + \sqrt{3} \text{ or } \cot \frac{\pi}{12} = -2 + \sqrt{3} \text{ (rejected)}$$
Thus, we have $\cot \frac{\pi}{12} = 2 + \sqrt{3}$.
(ii) $$\int_{\frac{\pi}{12}}^{\frac{\pi}{6}} \frac{x \csc^2 x}{\cot x - 1} \, dx$$
= $-\left[ x \ln(\cot x - 1) \right]_{\frac{\pi}{12}}^{\frac{\pi}{6}} + \int_{\frac{\pi}{12}}^{\frac{\pi}{6}} \ln(\cot x - 1) \, dx$
= $-\left( \frac{\pi}{6} \ln\left( \cot \frac{\pi}{6} - 1 \right) - \frac{\pi}{12} \ln\left( \cot \frac{\pi}{12} - 1 \right) \right) + \frac{\pi \ln 2}{24}$ (by (b))
= $\frac{\pi}{12} \left( \ln(\sqrt{3} + 1) - 2 \ln(\sqrt{3} - 1) \right) + \frac{\pi \ln 2}{24}$ (by (c)(i))
= $\frac{\pi}{12} \ln\left( \frac{\sqrt{3} + 1}{(\sqrt{3} - 1)^2} \right) + \frac{\pi \ln 2}{24}$
= $\frac{\pi}{12} \ln\left( \frac{(\sqrt{3} + 1)^3}{4} \right) + \frac{\pi \ln 2}{24}$
= $\frac{\pi}{24} \ln\left( 2 \left( \frac{(\sqrt{3} + 1)^3}{4} \right)^2 \right)$
= $\frac{\pi}{24} \ln\left( \frac{(\sqrt{3} + 1)^6}{8} \right)$
= $\frac{\pi}{8} \ln\left( \frac{(\sqrt{3} + 1)^2}{2} \right)$
= $\frac{\pi}{8} \ln\left( \frac{4 + 2\sqrt{3}}{2} \right)$
= $\frac{\pi}{8} \ln(2 + \sqrt{3})$

## 第 11 題  <!-- 頁 [12, 13]｜13/13（題目卷為準；MS 讀到 subtotals=無 cells=18） -->

Marks: 1A 1M 1M 1A 1M 1A+1A 1M 1A+1A 1M 1 1A 1A 1M 1A 1M 1A

11. (a) (i) (1) Note that $$\begin{vmatrix} 1 & -1 & -2 \\ 1 & -2 & h \\ 4 & h & -7 \end{vmatrix} = (-2)(-7) + (-1)(h)(4) + (-2)(h) - (-2)(-2)(4) - (h)(h) - (-1)(-7) = -(h+3)^2$$
Since ($E$) has a unique solution, we have $\begin{vmatrix} 1 & -1 & -2 \\ 1 & -2 & h \\ 4 & h & -7 \end{vmatrix} \neq 0$. So, we have $-(h+3)^2 \neq 0$. Thus, we have $h \neq -3$.
The augmented matrix of ($E$) is $$\begin{pmatrix} 1 & -1 & -2 & 1 \\ 1 & -2 & h & k \\ 4 & h & -7 & 7 \end{pmatrix} \sim \begin{pmatrix} 1 & -1 & -2 & 1 \\ 0 & -1 & h+2 & k-1 \\ 0 & h+4 & 1 & 3 \end{pmatrix}$$
Since ($E$) has a unique solution, we have $(h+3)^2 \neq 0$. Thus, we have $h \neq -3$.
(2) Since ($E$) has a unique solution, we have $$x = \frac{1}{-(h+3)^2} \cdot \begin{vmatrix} 1 & -1 & -2 \\ k & -2 & h \\ 7 & h & -7 \end{vmatrix} = \frac{h^2 + 2hk + 7h + 7k + 14}{(h+3)^2}$$
$$y = \frac{1}{-(h+3)^2} \cdot \begin{vmatrix} 1 & 1 & -2 \\ 1 & k & h \\ 4 & 7 & -7 \end{vmatrix} = \frac{3h-k+7}{(h+3)^2}$$
$$z = \frac{1}{-(h+3)^2} \cdot \begin{vmatrix} 1 & -1 & 1 \\ 1 & -2 & k \\ 4 & h & 7 \end{vmatrix} = \frac{hk-h+4k-1}{(h+3)^2}$$
Since $(E)$ has a unique solution, the augmented matrix of $(E)$ ~ $\begin{pmatrix} 1 & -1 & -2 \\ 0 & -1 & h+2 \\ 0 & 0 & (h+3)^2 \end{pmatrix} \mid \begin{array}{c} 1 \\ k-1 \\ hk-h+4k-1 \end{array}$
~ $\begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix} \mid \frac{h^2+2hk+7h+7k+14}{(h+3)^2} \mid \frac{3h-k+7}{(h+3)^2} \mid \frac{hk-h+4k-1}{(h+3)^2}$
Thus, we have $x = \frac{h^2+2hk+7h+7k+14}{(h+3)^2}$, $y = \frac{3h-k+7}{(h+3)^2}$ and $z = \frac{hk-h+4k-1}{(h+3)^2}$.
(ii) (1) When $h = -3$, the augmented matrix of $(E)$ is $\begin{pmatrix} 1 & -1 & -2 \\ 1 & -2 & -3 \\ 4 & -3 & -7 \end{pmatrix} \sim \begin{pmatrix} 1 & -1 & -2 \\ 0 & -1 & -1 \\ 0 & 0 & 0 \end{pmatrix}$
Since $(E)$ is consistent, we have $k = -2$.
(2) When $h = -3$ and $k = -2$, the augmented matrix of $(E)$ ~ $\begin{pmatrix} 1 & -1 & -2 \\ 0 & -1 & -1 \\ 0 & 0 & 0 \end{pmatrix}$
Thus, the solution set of $(E)$ is $\{(t+4,-t+3,t): t \in \mathbf{R}\}$.
(b) When $h = -3$, the solution set of $(F)$ is $\{(t+4,-t+3,t): t \in \mathbf{R}\}$. $3x^2+4y^2-7z^2 = 3(t+4)^2+4(-t+3)^2-7t^2 = 84 \neq 1$
When $h \neq -3$, $(F)$ does not have a real solution $(x,y,z)$ satisfying $3x^2+4y^2-7z^2 = 1$.
When $h \neq -3$, the solution of $(F)$ is $x = \frac{h}{h+3}$, $y = \frac{3}{h+3}$ and $z = \frac{-3}{h+3}$. $3x^2+4y^2-7z^2 = 3\left(\frac{h}{h+3}\right)^2+4\left(\frac{3}{h+3}\right)^2-7\left(\frac{-3}{h+3}\right)^2 = \frac{3(h-3)}{h+3}$
Hence, we have $3x^2+4y^2-7z^2 = 1 \iff \frac{3(h-3)}{h+3} = 1$.
Therefore, we have $3x^2+4y^2-7z^2 = 1 \iff h = 6$.
So, there is only one value of $h$ such that $(F)$ has a real solution $(x,y,z)$ satisfying $3x^2+4y^2-7z^2 = 1$.
Thus, the claim is disagreed.

## 第 12 題  <!-- 頁 [14]｜12/12（題目卷為準；MS 讀到 subtotals=無 cells=6） -->

Marks: 1M 1A 1M 1M 1M 1M

12. (a) Note that $\overrightarrow{OR} = \frac{3}{4}\overrightarrow{OP} + \frac{1}{4}\overrightarrow{OQ}$. So, we have $\overrightarrow{OR} = 2\mathbf{i} - \mathbf{j} + 2\mathbf{k}$. $\overrightarrow{OP} \times \overrightarrow{OR}$ = $\begin{vmatrix} \mathbf{i} & \mathbf{j} & \mathbf{k} \\ 1 & 1 & 4 \\ 2 & -1 & 2 \end{vmatrix}$ = $6\mathbf{i} + 6\mathbf{j} - 3\mathbf{k}$
(b) Note that the quadrilateral $OPSR$ is a parallelogram. The area of the quadrilateral $OPSR$
$\overrightarrow{OP} \times \overrightarrow{OR}$ = $\begin{vmatrix} 6\mathbf{i} + 6\mathbf{j} - 3\mathbf{k} \end{vmatrix}$ = $\sqrt{6^2 + 6^2 + (-3)^2}$ = 9
(c) (i) Note that $\overrightarrow{NR} = \overrightarrow{OR} - \overrightarrow{ON} = (2 - 6\lambda)\mathbf{i} - (1 + 6\lambda)\mathbf{j} + (2 + 3\lambda)\mathbf{k}$ and $\overrightarrow{PQ} = 4\mathbf{i} - 8\mathbf{j} - 8\mathbf{k}$. So, we have $\overrightarrow{NR} \cdot \overrightarrow{PQ} = 4(2 - 6\lambda) + 8(1 + 6\lambda) - 8(2 + 3\lambda) = 0$. Thus, $\overrightarrow{NR}$ is perpendicular to $\overrightarrow{PQ}$.
(ii) (1) Note that $\overrightarrow{NQ} = \overrightarrow{OQ} - \overrightarrow{ON} = (5 - 6\lambda)\mathbf{i} - (6\lambda + 7)\mathbf{j} + (3\lambda - 4)\mathbf{k}$. Also note that $\overrightarrow{NQ}$ is parallel to $11\mathbf{i} + \mu\mathbf{j} - 10\mathbf{k}$. Since $\mu \neq 0$, we have $\frac{6\lambda - 5}{11} = \frac{6\lambda + 7}{\mu} = \frac{3\lambda - 4}{10}$. Solving, we have $\lambda = \frac{2}{9}$ and $\mu = -25$.
(2) Note that $PQ$ is the line of intersection of $\Delta OPQ$ and $\Delta NPQ$. Since $\overrightarrow{OR} \cdot \overrightarrow{PQ} = 0$, $OR$ is perpendicular to $PQ$. By (c)(i), $NR$ is perpendicular to $PQ$. So, we have $\theta = \angle ORN$. Therefore, we have $\tan \theta = \tan \angle ORN = \frac{\left| \overrightarrow{ON} \right|}{\left| \overrightarrow{OR} \right|}$. By (c)(ii)(1), we have $\tan \theta = \frac{\frac{2}{9} \left| \overrightarrow{OP} \times \overrightarrow{OR} \right|}{\left| \overrightarrow{OR} \right|}$. By (b), we have $\tan \theta = \frac{\frac{2}{9} (9)}{\sqrt{2^2 + (-1)^2 + 2^2}} = \frac{2}{3}$.


**合計 100 / 100**
