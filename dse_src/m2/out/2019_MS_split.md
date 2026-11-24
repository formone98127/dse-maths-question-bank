# 2019 M2 Paper 1 — 評卷參考（分題）

> 分題依據：MS 題號行 + marks 對題目卷分數 [4, 5, 6, 6, 7, 7, 7, 8, 12, 13, 12, 13]｜合計 100

## 第 1 題  <!-- 頁 [2]｜4/4（題目卷為準；MS 讀到 subtotals=無 cells=6） -->

Marks: 1 1M 1M 1A 1M 1A

1. f(1+h) - f(1)
$$= \frac{10(1+h)}{7+3(1+h)^2} - \frac{10}{7+3}$$
$$= \frac{10+10h}{10+6h+3h^2} - 1$$
$$= \frac{10+10h-10-6h-3h^2}{10+6h+3h^2}$$
$$= \frac{4h-3h^2}{10+6h+3h^2}$$
f'(1)
$$= \lim_{h \to 0} \frac{f(1+h) - f(1)}{h}$$
$$= \lim_{h \to 0} \frac{1}{h} \left( \frac{4h-3h^2}{10+6h+3h^2} \right)
$$= \lim_{h \to 0} \frac{4-3h}{10+6h+3h^2}$$
$$= \frac{4-3(0)}{10+6(0)+3(0)^2}$$
$$= \frac{2}{5}$$

## 第 2 題  <!-- 頁 [2]｜5/5（題目卷為準；MS 讀到 subtotals=無 cells=3） -->

Marks: 1M 1M 1A

2. (a) P(x)
$$= (x+\lambda)(x+\lambda)^2(x+\lambda)^3 - (3)(5)(x+\lambda) + (1)(3)(4) - (2)(4)(x+\lambda)^2$$
$$= (x+\lambda)^6 - 8(x+\lambda)^2 - 15(x+\lambda) + 12$$
Note that the coefficient of $x^3$ in the expansion of P(x) is 160. So, we have $C_3^6\lambda^3 = 160$. Thus, we have $\lambda = 2$.
(b) Note that P'(0) is the coefficient of $x$ in the expansion of P(x). Also note that the coefficient of $x$ is $6\lambda^5 - 16\lambda - 15$. By (a), we have P'(0) = 145.
1A
(5)

## 第 3 題  <!-- 頁 [3]｜6/6（題目卷為準；MS 讀到 subtotals=無 cells=7） -->

Marks: 1M 1M 1A 1M 1M 1M 1A

3. (a) $V = \int -2t \, dt$ $= -t^2 + C$, where $C$ is a constant
Since $V = 580$ when $t = 0$, we have $C = 580$.
So, we have $V = 580 - t^2$.
When $t = 24$, we have $V = 4 > 0$.
Thus, the claim is correct.
(b) Let $p$ cm be the depth of liquid $X$ in the vessel when $t = 18$.
Since $V \bigg|_{t=18} = 580 - 18^2 = 256$, we have $p^2 + 24p = 256$.
So, we have $p^2 + 24p - 256 = 0$.
Solving, we have $p = 8$ or $p = -32$ (rejected).
Note that $\frac{dV}{dt} = (2h + 24)\frac{dh}{dt}$.
Since $\frac{dV}{dt} \bigg|_{t=18} = -36$, we have $-36 = (2(8) + 24)\frac{dh}{dt} \bigg|_{t=18}$.
Thus, we have $\frac{dh}{dt} \bigg|_{t=18} = \frac{-9}{10}$.

## 第 4 題  <!-- 頁 [3]｜6/6（題目卷為準；MS 讀到 subtotals=無 cells=6） -->

Marks: 1M 1M 1 1M 1M 1A

4. (a) $g'(x)$
$= \frac{\sqrt{x}\left(\frac{1}{x}\right) - (\ln x)\left(\frac{1}{2\sqrt{x}}\right)}{x}$
$= \frac{2 - \ln x}{2\sqrt{x^3}}$
So, we have $g'(x) = 0 \iff x = e^2$.
$x \quad (0, e^2) \quad e^2 \quad (e^2, 99)$
$g'(x) \quad + \quad 0 \quad -$
Therefore, $G$ attains its maximum value only when $x = e^2$.
Thus, $G$ has only one maximum point.
(b) Note that $g(x) 0$ for all $x \in (1, 99)$.
So, we have $g(x) = 0 \iff x = 1$.
The required volume
$= \int_1^{e^2} \pi \left(\frac{\ln x}{\sqrt{x}}\right)^2 \, dx$
$= \pi \int_0^2 u^2 \, du$ (by letting $u = \ln x$)
$= \pi \left[ \frac{u^3}{3} \right]_0^2$
$= \frac{8\pi}{3}$

## 第 5 題  <!-- 頁 [4]｜7/7（題目卷為準；MS 讀到 subtotals=無 cells=3） -->

Marks: 1 1M 1A

5. (a) Note that $\frac{1}{(1)(2)} + \frac{1}{(2)(3)} = \frac{2}{3} = \frac{1+1}{(1)(2+1)}$. Therefore, the statement is true for $n=1$. Assume that $\sum_{k=m}^{2m} \frac{1}{k(k+1)} = \frac{m+1}{m(2m+1)}$, where $m$ is a positive integer. $\sum_{k=m+1}^{2m+2} \frac{1}{k(k+1)}$ $= \sum_{k=m}^{2m} \frac{1}{k(k+1)} - \frac{1}{m(m+1)} + \frac{1}{(2m+1)(2m+2)} + \frac{1}{(2m+2)(2m+3)}$ $= \frac{m+1}{m(2m+1)} - \frac{1}{m(m+1)} + \frac{1}{(2m+1)(2m+2)} + \frac{1}{(2m+2)(2m+3)}$ $= \frac{(m+1)^2 - (2m+1)}{m(m+1)(2m+1)} + \frac{(2m+3) + (2m+1)}{(2m+1)(2m+2)(2m+3)}$ $= \frac{m}{(m+1)(2m+1)} + \frac{2}{(2m+1)(2m+3)}$ $= \frac{(2m+1)(m+2)}{(m+1)(2m+1)(2m+3)}$ $= \frac{m+2}{(m+1)(2m+3)}$ So, the statement is true for $n=m+1$ if it is true for $n=m$. By mathematical induction, the statement is true for all positive integers $n$.
(b) Putting $n=50$ in (a), we have $\sum_{k=50}^{100} \frac{1}{k(k+1)} = \frac{51}{(50)(101)} = \frac{51}{5050}$. Putting $n=100$ in (a), we have $\sum_{k=100}^{200} \frac{1}{k(k+1)} = \frac{101}{(100)(201)} = \frac{101}{20100}$. So, we have $\sum_{k=50}^{200} \frac{1}{k(k+1)} = \frac{51}{5050} + \frac{101}{20100} - \frac{1}{(100)(101)}$. Thus, we have $\sum_{k=50}^{200} \frac{1}{k(k+1)} = \frac{151}{10050}$.

## 第 6 題  <!-- 頁 [5]｜7/7（題目卷為準；MS 讀到 subtotals=無 cells=7） -->

Marks: 1A 1M 1M 1A 1M 1M 1A

6. (a) (i) Note that $$\begin{vmatrix} 1 & -2 & -2 \\ 5 & \alpha & \alpha \\ 7 & \alpha - 3 & 2\alpha + 1 \end{vmatrix} = (\alpha)(2\alpha + 1) + (-2)(\alpha)(7) + (-2)(5)(\alpha - 3) - (\alpha)(\alpha - 3) - (-2)(5)(2\alpha + 1) - (-2)(\alpha)(7) = (\alpha + 4)(\alpha + 10)$$
Since ($E$) has a unique solution, we have $\begin{vmatrix} 1 & -2 & -2 \\ 5 & \alpha & \alpha \\ 7 & \alpha - 3 & 2\alpha + 1 \end{vmatrix} \neq 0$. Hence, we have $(\alpha + 4)(\alpha + 10) \neq 0$. So, we have $\alpha \neq -4$ and $\alpha \neq -10$. Thus, we have $\alpha -4$.
The augmented matrix of ($E$) is $$\begin{pmatrix} 1 & -2 & -2 & \beta \\ 5 & \alpha & \alpha & 5\beta \\ 7 & \alpha - 3 & 2\alpha + 1 & 8\beta \end{pmatrix} \sim \begin{pmatrix} 1 & -2 & -2 & \beta \\ 0 & \alpha + 10 & \alpha + 10 & 0 \\ 0 & \alpha + 11 & 2\alpha + 15 & \beta \end{pmatrix}$$
Since ($E$) has a unique solution, we have $(\alpha + 4)(\alpha + 10) \neq 0$. So, we have $\alpha \neq -4$ and $\alpha \neq -10$. Thus, we have $\alpha -4$.
(ii) Since ($E$) has a unique solution, we have $$y = \frac{1}{(\alpha + 4)(\alpha + 10)} \begin{vmatrix} 1 & \beta & -2 \\ 5 & 5\beta & \alpha \\ 7 & 8\beta & 2\alpha + 1 \end{vmatrix}$$
$(b)$ When $\alpha = -4$, the augmented matrix of ($E$) is $$\begin{pmatrix} 1 & -2 & -2 & \beta \\ 5 & -4 & -4 & 5\beta \\ 7 & -7 & -7 & 8\beta \end{pmatrix} \sim \begin{pmatrix} 1 & -2 & -2 & \beta \\ 0 & 1 & 1 & 0 \\ 0 & 0 & 0 & \beta \end{pmatrix}$$
Since ($E$) is inconsistent, we have $\beta \neq 0$. Thus, we have $\beta 0$.

## 第 7 題  <!-- 頁 [6]｜7/7（MS 小計） -->

Marks: 1M 1M 1A

7. (a) $\int e^x \sin \pi x \, dx$ $= \int \sin \pi x \, de^x$ $= e^x \sin \pi x - \pi \int e^x \cos \pi x \, dx$ $= e^x \sin \pi x - \pi \int \cos \pi x \, de^x$ $= e^x \sin \pi x - \pi \left( e^x \cos \pi x - \pi \int -e^x \sin \pi x \, dx \right)$ $\int e^x \sin \pi x \, dx = e^x \sin \pi x - \pi e^x \cos \pi x - \pi^2 \int e^x \sin \pi x \, dx$ $\pi^2 \int e^x \sin \pi x \, dx + \int e^x \sin \pi x \, dx = e^x \sin \pi x - \pi e^x \cos \pi x + \text{constant}$ $(\pi^2 + 1) \int e^x \sin \pi x \, dx = e^x (\sin \pi x - \pi \cos \pi x) + \text{constant}$ $\int e^x \sin \pi x \, dx = \frac{1}{\pi^2 + 1} \left( e^x (\sin \pi x - \pi \cos \pi x) \right) + \text{constant}$
(b) $\int_0^3 e^{3-x} \sin \pi x \, dx$ $= \int_0^3 -e^u \sin \pi (3-u) \, du$ (by letting $u = 3-x$) $= \int_0^3 e^u \sin \pi u \, du$ $= \int_0^3 e^x \sin \pi x \, dx$ $= \frac{1}{\pi^2 + 1} \left[ e^x (\sin \pi x - \pi \cos \pi x) \right]_0^3$ (by (a)) $= \frac{\pi(e^3 + 1)}{\pi^2 + 1}$

## 第 8 題  <!-- 頁 [7]｜8/8（題目卷為準；MS 讀到 subtotals=無 cells=8） -->

Marks: 1M 1A 1M 1M 1A 1M 1M 1A

8. (a) For all $x > 0$, $h'(x)$
$$= \frac{2}{x} \left( \left( x^2 - \frac{7}{2}x + \left( \frac{7}{4} \right)^2 - \left( \frac{7}{4} \right)^2 \right) + 4 \right)$$
$$= \frac{2}{x} \left( \left( x - \frac{7}{4} \right)^2 + \frac{15}{16} \right).$$
&gt; 0
Thus, $h(x)$ is an increasing function.
(b) (i) $y$
$$= \int \left( 2x - 7 + \frac{8}{x} \right) dx$$
$$= x^2 - 7x + 8 \ln x + C$, where $C$ is a constant
Note that $y = 3$ when $x = 1$.
So, we have $1^2 - 7(1) + 8 \ln 1 + C = 3$.
Therefore, we have $C = 9$.
Thus, the equation of $H$ is $y = x^2 - 7x + 8 \ln x + 9$.
(ii) $h''(x)$
$$= \frac{x(4x - 7) - (2x^2 - 7x + 8)}{x^2}$$
$$= \frac{2x^2 - 8}{x^2}$$
$$= \frac{2(x - 2)(x + 2)}{x^2}$$
Since $x > 0$, we have $h''(x) = 0 \iff x = 2$.
Thus, the point of inflexion of $H$ is $(2, 8 \ln 2 - 1)$.

## 第 9 題  <!-- 頁 [8]｜12/12（題目卷為準；MS 讀到 subtotals=無 cells=5） -->

Marks: 1M 1M 1A 1M+1A

9. (a) $\frac{dy}{dx}$ $= \left(\frac{1}{3}\right)\left(\frac{1}{2}\right)(12 - x^2)^{\frac{-1}{2}}(-2x)$ $= \frac{-x}{3\sqrt{12 - x^2}}$ So, we have $\left. \frac{dy}{dx} \right|_{x=3} = \frac{-1}{\sqrt{3}}$. The equation of $L$ is $y - \frac{\sqrt{3}}{3} = \frac{-1}{\sqrt{3}}(x - 3)$ $x + \sqrt{3}y - 4 = 0$
(b) (i) Putting $y = \frac{1}{\sqrt{3}}(4 - x)$ in $y = \sqrt{4 - x^2}$, we have $\frac{1}{\sqrt{3}}(4 - x) = \sqrt{4 - x^2}$ $x^2 - 2x + 1 = 0$ So, we have $x = 1$ and $y = \sqrt{3}$. Thus, the point of contact of $L$ and $C$ is $(1, \sqrt{3})$.
(ii) When $\sqrt{4 - x^2} = \frac{1}{3}\sqrt{12 - x^2}$, we have $36 - 9x^2 = 12 - x^2$. So, we have $8x^2 - 24 = 0$. Since $0 Thus, the point of intersection of $C$ and $\Gamma$ is $(\sqrt{3}, 1)$.
(iii) The required area $= \int_{1}^{\sqrt{3}} \left( \frac{1}{\sqrt{3}}(4 - x) - \sqrt{4 - x^2} \right) dx + \int_{\sqrt{3}}^{3} \left( \frac{1}{\sqrt{3}}(4 - x) - \frac{1}{3}\sqrt{12 - x^2} \right) dx$ $= \int_{1}^{3} \frac{1}{\sqrt{3}}(4 - x) dx - \int_{1}^{\sqrt{3}} \sqrt{4 - u^2} du - \int_{\sqrt{3}}^{3} \frac{1}{3}\sqrt{12 - v^2} dv$ $= \frac{4\sqrt{3}}{3} - \int_{\frac{\pi}{6}}^{\frac{\pi}{3}} 4\cos^2\alpha d\alpha - \int_{\frac{\pi}{6}}^{\frac{\pi}{3}} \frac{12\cos^2\beta}{3} d\beta$ (by letting $u = 2\sin\alpha$ and $\nu = \sqrt{12}\sin\beta$) $= \frac{4\sqrt{3}}{3} - 8\int_{\frac{\pi}{6}}^{\frac{\pi}{3}} \frac{\cos 2\theta + 1}{2} d\theta$ $= \frac{4\sqrt{3}}{3} - 8\left[ \frac{\sin 2\theta}{4} + \frac{\theta}{2} \right]_{\frac{\pi}{6}}^{\frac{\pi}{3}}$ $= \frac{4\sqrt{3}}{3} - \frac{2\pi}{3}$

## 第 10 題  <!-- 頁 [9, 10]｜13/13（題目卷為準；MS 讀到 subtotals=無 cells=20） -->

Marks: 1 1M 1M 1M 1A 1A 1A 1M 1M 1M 1M 1M 1 1 1 1M 1M 1M 1M 1A

10. (a) $\frac{1}{2 + \cos 2x}$ $= \frac{1}{2 + 2\cos^2x - 1}$ $= \frac{1}{2\cos^2x + 1}$ $= \frac{\sec^2x}{2 + \sec^2x}$
(b) $\int_0^{\frac{\pi}{4}} \frac{1}{2 + \cos 2x} \, dx$
$= \int_0^{\frac{\pi}{4}} \frac{\sec^2x}{2 + \sec^2x} \, dx$ (by (a))
$= \int_0^{\frac{\pi}{4}} \frac{\sec^2x}{3 + \tan^2x} \, dx$
$= \int_0^{1} \frac{1}{3 + t^2} \, dt$ (by letting $t = \tan x$)
$= \left[ \frac{1}{\sqrt{3}} \tan^{-1}\left( \frac{t}{\sqrt{3}} \right) \right]_0^1$
$= \frac{\sqrt{3}\pi}{18}$
(c) By letting $u = -x$, we have $\int_-a^0 f(x) \ln(1 + e^x) \, dx = \int_a^0 -f(-u) \ln(1 + e^{-u}) \, du$.
So, we have $\int_-a^0 f(x) \ln(1 + e^x) \, dx = \int_0^a f(-x) \ln(1 + e^{-x}) \, dx$.
$\int_-a^a f(x) \ln(1 + e^x) \, dx$
$= \int_0^a f(x) \ln(1 + e^{-x}) \, dx + \int_0^a f(x) \ln(1 + e^x) \, dx$
$= -\int_0^a f(x) \ln(1 + e^{-x}) \, dx + \int_0^a f(x) \ln(1 + e^x) \, dx$
$= -\int_0^a f(x) \ln\left( \frac{e^x + 1}{e^x} \right) \, dx + \int_0^a f(x) \ln(1 + e^x) \, dx$
$= -\int_0^a f(x) \ln(e^x + 1) \, dx + \int_0^a x f(x) \, dx + \int_0^a f(x) \ln(1 + e^x) \, dx$
$= \int_0^a x f(x) \, dx$
(d) Note that $\frac{\sin 2(-x)}{(2 + \cos 2(-x))^2} = \frac{-\sin 2x}{(2 + \cos 2x)^2}$ for all $x \in \mathbf{R}$.
By (c), we have $\int_{-\frac{\pi}{4}}^{\frac{\pi}{4}} \frac{\sin 2x}{(2 + \cos 2x)^2} \ln(1 + e^x) \, \mathrm{d}x = \int_{0}^{\frac{\pi}{4}} \frac{x \sin 2x}{(2 + \cos 2x)^2} \, \mathrm{d}x$.
Also note that $\frac{\mathrm{d}}{\mathrm{d}x}\left(\frac{1}{2(2 + \cos 2x)}\right) = \frac{\sin 2x}{(2 + \cos 2x)^2}$.
$\int_{0}^{\frac{\pi}{4}} \frac{x \sin 2x}{(2 + \cos 2x)^2} \, \mathrm{d}x$
$= \left[ \frac{x}{2(2 + \cos 2x)} \right]_{0}^{\frac{\pi}{4}} - \int_{0}^{\frac{\pi}{4}} \frac{1}{2(2 + \cos 2x)} \, \mathrm{d}x$
$= \frac{1}{2}\left(\frac{\pi}{4}\right)\left(\frac{1}{2 + 0}\right) - \frac{1}{2}\left(\frac{\sqrt{3}\pi}{18}\right)$ (by (b))
$= \frac{(9 - 4\sqrt{3})\pi}{144}$
Thus, we have $\int_{-\frac{\pi}{4}}^{\frac{\pi}{4}} \frac{\sin 2x}{(2 + \cos 2x)^2} \ln(1 + e^x) \, \mathrm{d}x = \frac{(9 - 4\sqrt{3})\pi}{144}$.

## 第 11 題  <!-- 頁 [11, 12]｜12/12（題目卷為準；MS 讀到 subtotals=無 cells=38） -->

Marks: 1M 1M 1M 1A 1M 1M 1M 1M 1M 1M 1M 1M 1 1M 1M 1M 1M 1M 1M 1M 1M 1M 1M 1 1M 1M 1M 1M 1M 1M 1A 1M 1M 1M 1M 1M 1M 1A

11. (a) $M^2 = \begin{pmatrix} 2 & 7 \\ -1 & -6 \end{pmatrix} \begin{pmatrix} 2 & 7 \\ -1 & -6 \end{pmatrix} = \begin{pmatrix} -3 & -28 \\ 4 & 29 \end{pmatrix}$
$M^2 = aM + bI$
$\begin{pmatrix} -3 & -28 \\ 4 & 29 \end{pmatrix} = \begin{pmatrix} 2a & 7a \\ -a & -6a \end{pmatrix} + \begin{pmatrix} b & 0 \\ 0 & b \end{pmatrix}$
$\begin{cases} -3 = 2a + b \\ -28 = 7a \\ 4 = -a \\ 29 = -6a + b \end{cases}$
Thus, we have $a = -4$ and $b = 5$.
(b) Note that $(1 - (-5))M + (5 + (-5))I = 6M$.
Therefore, the statement is true for $n = 1$.
Assume that $6M^k = (1 - (-5)^k)M + (5 + (-5)^k)I$, where $k$ is a positive integer.
$6M^{k+1} = M(6M^k)$
$= M((1 - (-5)^k)M + (5 + (-5)^k)I)$
$= (1 - (-5)^k)M^2 + (5 + (-5)^k)M$
$= (1 - (-5)^k)((1 + (-5))M + 5I) + (5 + (-5)^k)M$
$= (1 + (-5) - (-5)^k - (-5)^{k+1})M + (5 + (-5)^{k+1})I + (5 + (-5)^k)M$
$= (1 - (-5)^{k+1})M + (5 + (-5)^{k+1})I$
So, the statement is true for $n = k + 1$ if it is true for $n = k$.
By mathematical induction, we have $6M^n = (1 - (-5)^n)M + (5 + (-5)^n)I$.
$6M = (1 - (-5))M + (5 + (-5))I$
$6M^2 = (1 - (-5))M^2$
$= (1 - (-5))((1 + (-5))M + 5I)$
$= (1 - (-5)^2)M + (5 + (-5)^2)I$
$= M(6M^2)$
$= M((1 - (-5)^2)M + (5 + (-5)^2)I)$
$= (1 - (-5)^2)M^2 + (5 + (-5)^2)M$
$= (1 - (-5)^2)((1 + (-5))M + 5I) + (5 + (-5)^2)M$
$= (1 + (-5) - (-5)^2 - (-5)^3)M + (5 + (-5)^3)I + (5 + (-5)^2)M$
$= (1 - (-5)^3)M + (5 + (-5)^3)I$
Thus, we have $6M^n = (1 - (-5)^n)M + (5 + (-5)^n)I$.
$(c) \text{ By (b), we have } 6M^n = (1 - (-5)^n)M + (5 + (-5)^n)I \text{ and } 6M^{n+1} = (1 - (-5)^{n+1})M + (5 + (-5)^{n+1})I.$
$6(1 - (-5)^n)M^{n+1} - 6(1 - (-5)^{n+1})M^n = ((1 - (-5)^n)(5 + (-5)^{n+1}) - (1 - (-5)^{n+1})(5 + (-5)^{n}))I$
$M^n \left( \frac{(1 - (-5)^n)M - (1 - (-5)^{n+1})I}{-6(-5)^n} \right) = \left( \frac{(1 - (-5)^n)M - (1 - (-5)^{n+1})I}{-6(-5)^n} \right)M^n = I$
So, we have $(M^n)^{-1} = \frac{(1 - (-5)^n)M - (1 - (-5)^{n+1})I}{-6(-5)^n}.$
$(M^n)^{-1} = \frac{(-5)^n - 1}{6(-5)^n}M + \frac{-(-5)^{n+1} + 1}{6(-5)^n}I$
$= \left( \frac{1}{6}M + \frac{5}{6}I \right) + \frac{1}{(-5)^n} \left( \frac{-1}{6}M + \frac{1}{6}I \right)$
Letting $A = \frac{1}{6}M + \frac{5}{6}I = \frac{1}{6} \left( \begin{array}{cc} 7 & 7 \\ -1 & -1 \end{array} \right)$ and $B = \frac{-1}{6}M + \frac{1}{6}I = \frac{1}{6} \left( \begin{array}{cc} -1 & -7 \\ 1 & 7 \end{array} \right)$, we have $(M^n)^{-1} = A + \frac{1}{(-5)^n}B.$
Thus, there exists a pair of $2 \times 2$ real matrices $A$ and $B$ such that $(M^n)^{-1} = A + \frac{1}{(-5)^n}B$ for all positive integers $n$.
$(6M^n = (1 - (-5)^n)M + (5 + (-5)^n)I \text{ (by (b))}$
$M^n = \frac{1}{6}(1 - (-5)^n) \left( \begin{array}{cc} 2 & 7 \\ -1 & -6 \end{array} \right) + \frac{1}{6}(5 + (-5)^n) \left( \begin{array}{cc} 1 & 0 \\ 0 & 1 \end{array} \right)$
$= \left( \frac{(-5)^n + 7}{6} \frac{-7(-5)^n + 7}{6} \right)$
$\det(M^n) = \left( \frac{-(-5)^n + 7}{6} \right) \left( \frac{7(-5)^n - 1}{6} \right) - \left( \frac{-7(-5)^n + 7}{6} \right) \left( \frac{(-5)^n - 1}{6} \right)$
$= (-5)^n$
$(M^n)^{-1} = \frac{1}{\det(M^n)} \left( \frac{7(-5)^n - 1}{6} \frac{7(-5)^n - 7}{6} \right)$
$= \left( \frac{\frac{7}{6}}{\frac{-1}{6}} \frac{\frac{7}{6}}{\frac{-1}{6}} \right) + \frac{1}{(-5)^n} \left( \frac{\frac{-1}{6}}{\frac{1}{6}} \frac{\frac{-7}{6}}{\frac{1}{6}} \right)$
Letting $A = \left( \frac{\frac{7}{6}}{\frac{-1}{6}} \frac{\frac{7}{6}}{\frac{-1}{6}} \right)$ and $B = \left( \frac{\frac{-1}{6}}{\frac{1}{6}} \frac{\frac{-7}{6}}{\frac{1}{6}} \right)$, we have $(M^n)^{-1} = A + \frac{1}{(-5)^n}B.$
Thus, there exists a pair of $2 \times 2$ real matrices $A$ and $B$ such that $(M^n)^{-1} = A + \frac{1}{(-5)^n}B$ for all positive integers $n$.

## 第 12 題  <!-- 頁 [13, 14]｜13/13（題目卷為準；MS 讀到 subtotals=[3, 2] cells=17） -->

Marks: 1M 1M 1M 1A 1M 1M 1A 1M 1A 1M 1A 1 1M 1A 1A 1A 1A

12. (a) $\left| \overrightarrow{AC} \right| = \left| \overrightarrow{BC} \right|$
$\left| \overrightarrow{OC} - \overrightarrow{OA} \right| = \left| \overrightarrow{OC} - \overrightarrow{OB} \right|$
$\left| -6\mathbf{i} - 8\mathbf{j} + (t - 2)\mathbf{k} \right| = \left| -8\mathbf{j} + (t - 8)\mathbf{k} \right|$
$\sqrt{(-6)^2 + (-8)^2 + (t - 2)^2} = \sqrt{(-8)^2 + (t - 8)^2}$
$t^2 - 4t + 104 = t^2 - 16t + 128$
$12t = 24$
$t = 2$
(b) $\overrightarrow{AB} \times \overrightarrow{AC}$
$= (-6\mathbf{i} + 6\mathbf{k}) \times (-6\mathbf{i} - 8\mathbf{j})$
$= \begin{vmatrix} \mathbf{i} & \mathbf{j} & \mathbf{k} \\ -6 & 0 & 6 \\ -6 & -8 & 0 \end{vmatrix}$
$= ((0)(0) - (6)(-8))\mathbf{i} + ((6)(-6) - (6)(0))\mathbf{j} + ((-6)(-8) - (0)(-6))\mathbf{k}$
$= 48\mathbf{i}^2 - 36\mathbf{j} + 48\mathbf{k}$
---------(2)
(c) The volume of the pyramid $OABC$
$= \frac{1}{6} \left| \overrightarrow{OA} \cdot (\overrightarrow{AB} \times \overrightarrow{AC}) \right|$
$= \frac{1}{6} \left| (i - 4\mathbf{j} + 2\mathbf{k}) \cdot (48\mathbf{i} - 36\mathbf{j} + 48\mathbf{k}) \right|$
$= \frac{1}{6} \left| (1)(48) + (-4)(-36) + (2)(48) \right|$
$= 48$
The volume of the pyramid $OABC$
$= \frac{1}{6} \left| \overrightarrow{OA} \cdot (\overrightarrow{OB} \times \overrightarrow{OC}) \right|$
$= \frac{1}{6} \left\| \begin{array}{ccc} 1 & -4 & 2 \\ -5 & -4 & 8 \\ -5 & -12 & 2 \end{array} \right\|$
$= \frac{1}{6} \left| (1)(-4)(2) + (-4)(8)(-5) + (2)(-5)(-12) - (1)(8)(-12) - (-4)(-5)(2) - (2)(-4)(-5) \right|$
$= 48$
(d) (i) By (c), the volume of the pyramid $OABC$ is not equal to 0 .
So, $O$ does not lie on $\Pi$ .
Therefore, $\overrightarrow{OP}, \overrightarrow{OQ}$ and $\overrightarrow{OR}$ are non-zero vectors.
Hence, we have $p \neq 0, q \neq 0$ and $r \neq 0$ .
Thus, we have $pqr \neq 0$ .
(ii) $\overrightarrow{OD}$ $= \overrightarrow{OA} \cdot \frac{\overrightarrow{AB} \times \overrightarrow{AC}}{\left| \overrightarrow{AB} \times \overrightarrow{AC} \right|^2} (\overrightarrow{AB} \times \overrightarrow{AC})$ $= \frac{(6)(48)}{48^2 + (-36)^2 + 48^2} (48\mathbf{i} - 36\mathbf{j} + 48\mathbf{k})$ $= \frac{288}{5904} (48\mathbf{i} - 36\mathbf{j} + 48\mathbf{k})$ $= \frac{96}{41} \mathbf{i} - \frac{72}{41} \mathbf{j} + \frac{96}{41} \mathbf{k}$
(iii) $\overrightarrow{AP} \cdot (\overrightarrow{AB} \times \overrightarrow{AC}) = 0$ $((p-1)\mathbf{i} + 4\mathbf{j} - 2\mathbf{k}) \cdot (48\mathbf{i} - 36\mathbf{j} + 48\mathbf{k}) = 0$ $48p - 48 - 144 - 96 = 0$ $p = 6$
$\overrightarrow{AQ} \cdot (\overrightarrow{AB} \times \overrightarrow{AC}) = 0$ $(-\mathbf{i} + (q+4)\mathbf{j} - 2\mathbf{k}) \cdot (48\mathbf{i} - 36\mathbf{j} + 48\mathbf{k}) = 0$ $-48 - 36q - 144 - 96 = 0$ $q = -8$
$\overrightarrow{AR} \cdot (\overrightarrow{AB} \times \overrightarrow{AC}) = 0$ $(-\mathbf{i} + 4\mathbf{j} + (r-2)\mathbf{k}) \cdot (48\mathbf{i} - 36\mathbf{j} + 48\mathbf{k}) = 0$ $-48 - 144 + 48r - 96 = 0$ $r = 6$
So, we have $\overrightarrow{OE} = \frac{1}{6} \mathbf{i} - \frac{1}{8} \mathbf{j} + \frac{1}{6} \mathbf{k}$.
By (b)(ii), we have $\overrightarrow{OE} = \frac{41}{576} \overrightarrow{OD}$.
Thus, $D, E$ and $O$ are collinear.


**合計 100 / 100**
