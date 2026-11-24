# 2022 M2 Paper 1 — 評卷參考（分題）

> 分題依據：MS 題號行 + marks 對題目卷分數 [4, 5, 7, 6, 6, 7, 8, 7, 13, 12, 13, 12]｜合計 100

## 第 1 題  <!-- 頁 [3]｜4/4（MS 小計） -->

Marks: 1 1M 1M 1A

1. g(1+h) - g(1)
= $\frac{1}{\sqrt{5(1+h)}+4} - \frac{1}{\sqrt{5(1)+4}}$
= $\frac{3 - \sqrt{5h+9}}{3\sqrt{5h+9}}$
= $\frac{3^2 - (5h+9)}{3\sqrt{5h+9}(3 + \sqrt{5h+9})}$
= $\frac{-5h}{3\sqrt{5h+9}(3 + \sqrt{5h+9})}$
g'(1)
= $\lim_{h \to 0} \frac{g(1+h) - g(1)}{h}$
= $\lim_{h \to 0} \frac{1}{h} \left( \frac{-5h}{3\sqrt{5h+9}(3 + \sqrt{5h+9})} \right)$
= $\lim_{h \to 0} \frac{-5}{3\sqrt{5h+9}(3 + \sqrt{5h+9})}$
= $\frac{-5}{54}$

## 第 2 題  <!-- 頁 [3]｜5/5（題目卷為準；MS 讀到 subtotals=無 cells=5） -->

Marks: 1M 1M 1 1M 1A

2. (a) $\frac{\tan \theta}{1 - \cot \theta} + \frac{\cot \theta}{1 - \tan \theta}$
= $\frac{\tan^2 \theta}{\tan \theta - 1} + \frac{1}{\tan \theta(1 - \tan \theta)}$
= $\frac{\tan^3 \theta - 1}{\tan \theta(\tan \theta - 1)}$
= $\frac{(\tan \theta - 1)(\tan^2 \theta + \tan \theta + 1)}{\tan \theta(\tan \theta - 1)}$
= $\frac{\sec^2 \theta + \tan \theta}{\tan \theta}$
= $1 + \frac{\sec^2 \theta}{\tan \theta}$
= $1 + \sec \theta \csc \theta$
(b) $\frac{\tan \theta}{1 - \cot \theta} + \frac{\cot \theta}{1 - \tan \theta} = 5$
$1 + \sec \theta \csc \theta = 5$
$\sin \theta \cos \theta = \frac{1}{4}$
$\sin 2\theta = \frac{1}{2}$
$2\theta = \frac{5\pi}{6}$
$\theta = \frac{5\pi}{12}$

## 第 3 題  <!-- 頁 [4]｜7/7（MS 小計） -->

Marks: 1 1M 1M 1 1M 1M 1A

3. (a) For $n = 1$, L.H.S. $= (-1)(1^2) + (-1)^2(2^2) = 3$ R.H.S. $= (1)(2+1) = 3$ Therefore, the statement is true for $n = 1$.
Assume that $\sum_{k=1}^{2m} (-1)^k k^2 = m(2m+1)$, where $m$ is a positive integer.
$\sum_{k=1}^{2(m+1)} (-1)^k k^2$ $= \sum_{k=1}^{2m} (-1)^k k^2 - (2m+1)^2 + (2m+2)^2$ $= m(2m+1) - (2m+1)^2 + (2m+2)^2$ (by induction assumption)
So, the statement is true for $n = m+1$ if it is true for $n = m$. By mathematical induction, the statement is true for all positive integers $n$.
(b) $\sum_{k=1}^{100} (-1)^k k^2$ $= \sum_{k=1}^{100} (-1)^k k^2 - \sum_{k=1}^{10} (-1)^k k^2$ $= 50(2(50)+1) - 5(2(5)+1)$ $= 4995$

## 第 4 題  <!-- 頁 [5]｜6/6（題目卷為準；MS 讀到 subtotals=無 cells=5） -->

Marks: 1M 1A 1A 1M 1M 0

4. (a) $\frac{dy}{dx}$
$= (7 - 4x)e^{-x} + (7x - 2x^2)(e^{-x})(-1)$
$= (2x^2 - 11x + 7)e^{-x}$
$\frac{d^2y}{dx^2}$
$= (4x - 11)e^{-x} + (2x^2 - 11x + 7)(e^{-x})(-1)$
$= (-2x^2 + 15x - 18)e^{-x}$
(b) $\frac{d^2y}{dx^2} = 0$
$(-2x^2 + 15x - 18)e^{-x} = 0$
$-2x^2 + 15x - 18 = 0$
$x = \frac{3}{2}$ or $x = 6$
$x \quad \left(-\infty, \frac{3}{2}\right) \quad \frac{3}{2} \quad \left(\frac{3}{2}, 6\right) \quad 6 \quad (6, \infty)$
$\frac{d^2y}{dx^2}$
-
0

## 第 5 題  <!-- 頁 [6]｜6/6（題目卷為準；MS 讀到 subtotals=無 cells=3） -->

Marks: 1M 1M 1

5. (a) $(a+x)^n$
$= a^n + C_1^n a^{n-1}x + C_2^n a^{n-2}x^2 + \cdots + x^n$
$= a^n + a^{n-1}nx + \frac{a^{n-2}n(n-1)}{2}x^2 + \cdots + x^n$
$\mu_2 = -10$
$\frac{a^{n-2}n(n-1)}{2} = -10$
$a^{n-2}n(n-1) = -20$
Since $n$ is greater than 1, $a^{n-2}$ is a negative number. Thus, $a$ is a negative number and $n$ is an odd number.

## 第 6 題  <!-- 頁 [6, 7]｜7/7（題目卷為準；MS 讀到 subtotals=無 cells=11） -->

Marks: 1A 1A 1A 1M 1M 1 1M 1M 1M 1M 1A

6. (b) $(bx-1)^n$
$= (-1)^n + C_1^n (-1)^{n-1}(bx) + C_2^n (-1)^{n-2}(bx)^2 + \cdots + (bx)^n$
$= (-1)^n + (-1)^{n-1}bnx + (-1)^{n-2} \frac{b^2n(n-1)}{2}x^2 + \cdots + b^nx^n$
$\lambda_0 = \mu_0$
$(-1)^n = a^n$
$a = -1$
$\lambda_1 = 2\mu_1$
$(-1)^{n-1}bn = 2a^{n-1}n$
$b = 2$
$a^{n-2}n(n-1) = -20$
$(-1)^{n-2}n(n-1) = -20$
$n(n-1) = 20$ (since $n$ is an odd number)
$n^2 - n - 20 = 0$
$(n-5)(n+4) = 0$
$n = 5$ or $n = -4$ (rejected)
6. (a) Note that $x^2 + 2x + 5 \equiv (x+1)^2 + 2^2$.
Let $x+1 = 2 \tan \theta$.
So, we have $\frac{dx}{d\theta} = 2 \sec^2 \theta$.
$\int \frac{1}{x^2 + 2x + 5} dx$
$= \int \frac{1}{4 \tan^2 \theta + 4} (2 \sec^2 \theta) d\theta$
$= \int \frac{1}{2} d\theta$
$= \frac{1}{2} \theta + \text{constant}$
$= \frac{1}{2} \tan^{-1} \left( \frac{x+1}{2} \right) + \text{constant}$
(b) $y$
$= \int \frac{2x+1}{x^2 + 2x+5} dx$
$= \int \frac{2x+2}{x^2 + 2x+5} dx - \int \frac{1}{x^2 + 2x+5} dx$
$= \int \frac{1}{x^2 + 2x+5} d(x^2 + 2x+5) - \int \frac{1}{x^2 + 2x+5} dx$
$= \ln |x^2 + 2x+5| - \frac{1}{2} \tan^{-1} \left( \frac{x+1}{2} \right) + C$, where $C$ is a constant
When $x = -3$, $y = \ln 2$.
$\ln 2 = \ln |(-3)^2 + 2(-3) + 5| - \frac{1}{2} \tan^{-1} \left( \frac{(-3)+1}{2} \right) + C$
$\ln 2 = \ln 8 - (\frac{1}{2})(\frac{-\pi}{4}) + C$
$C = -2 \ln 2 - \frac{\pi}{8}$
The equation of $G$ is $y = \ln |x^2 + 2x+5| - \frac{1}{2} \tan^{-1} \left( \frac{x+1}{2} \right) - 2 \ln 2 - \frac{\pi}{8}$.
When $x = -1$, $y$
$= \ln |(-1)^2 + 2(-1)+5| - \frac{1}{2} \tan^{-1} \left( \frac{(-1)+1}{2} \right) - 2 \ln 2 - \frac{\pi}{8}$
$= \frac{-\pi}{8}$
Thus, $G$ passes through the point $\left(-1, \frac{-\pi}{8}\right)$.

## 第 7 題  <!-- 頁 [8]｜8/8（題目卷為準；MS 讀到 subtotals=無 cells=19） -->

Marks: 1M 1M 1M 1M 1M 1 1 1M 1M 1M 1M 1M 1M 1M 1M 1M 1A 1A 1A

7. (a) $\frac{\mathrm{d}y}{\mathrm{d}x} = \frac{1}{x+2}$
The equation of $L$ is $y = \frac{1}{h+2}(x-h) + \ln(h+2)$.
$= \int_{0}^{h}\left(\frac{1}{h+2}(x-h) + \ln(h+2) - \ln(x+2)\right)\mathrm{d}x$
$= \left[\frac{1}{h+2}\left(\frac{1}{2}x^2 - hx\right) + x\ln(h+2)\right]_{0}^{h} - \left[x\ln(x+2)\right]_{0}^{h} + \int_{0}^{h}\frac{x}{x+2}\mathrm{d}x$
$= \frac{1}{h+2}\left(\frac{1}{2}h^2 - h^2\right) + h\ln(h+2) - h\ln(h+2) + \int_{0}^{h}\left(1 - \frac{2}{x+2}\right)\mathrm{d}x$
$= \frac{-h^2}{2h+4} + \left[x-2\ln|x+2|\right]_{0}^{h}$
$= \frac{h^2+4h}{2h+4} - 2\ln(h+2) + 2\ln 2$
(b) $h = 3^{-t} = e^{-t\ln 3}$
$\frac{\mathrm{d}h}{\mathrm{d}t} = (-\ln 3)e^{-t\ln 3} = (-\ln 3)3^{-t}$
$\frac{\mathrm{d}A}{\mathrm{d}h}$
$= \frac{(2h+4)(2h+4) - (h^2+4h)(2)}{(2h+4)^2} - \frac{2}{h+2}$
$= \frac{h^2}{2(h+2)^2}$
$\frac{\mathrm{d}A}{\mathrm{d}t}$
$= \frac{\mathrm{d}A}{\mathrm{d}h}\frac{\mathrm{d}h}{\mathrm{d}t}$
$= \frac{(3^{-t})^2}{2(3^{-t}+2)^2}(-\ln 3)3^{-t}$
$= \frac{-\ln 3}{2(3^t)(1+2(3^t))^2}$
$\left.\frac{\mathrm{d}A}{\mathrm{d}t}\right|_{t=1}$
$= \frac{-\ln 3}{2(3^1)(1+2(3^1))^2}$
$= \frac{-\ln 3}{294}$
Thus, the rate of change of $A$ is $\frac{-\ln 3}{294}$ when $t=1$.

## 第 8 題  <!-- 頁 [9]｜7/7（題目卷為準；MS 讀到 subtotals=無 cells=8） -->

Marks: 1M 1M+1A 1M 1M 1M 1M 1A

8. (a) $\Delta = \begin{vmatrix} a & 2 & -1 \\ -1 & a & 2 \\ 2 & -1 & a \end{vmatrix} = a^3 + 6a + 7$
$\Delta_y = \begin{vmatrix} a & 4k & -1 \\ -1 & 4 & 2 \\ 2 & k^2 & a \end{vmatrix} = 4a^2 + 4ak - 2ak^2 + k^2 + 16k + 8$
Note that $\Delta \neq 0$.
$y = \frac{\Delta_y}{\Delta} = \frac{4a^2 + 4ak - 2ak^2 + k^2 + 16k + 8}{a^3 + 6a + 7}$
(b) As $(E)$ has infinitely many solutions, $\Delta = 0$
$a^3 + 6a + 7 = 0$
$(a+1)(a^2 - a+7) = 0$
$a = -1$
The augmented matrix of $(E)$ becomes
$\begin{pmatrix} -1 & 2 & -1 & 4k \\ -1 & -1 & 2 & 4 \\ 2 & -1 & -1 & k^2 \end{pmatrix} \sim \begin{pmatrix} -1 & 2 & -1 & 4k \\ 0 & -3 & 3 & 4-4k \\ 0 & 0 & 0 & k^2+4k+4 \end{pmatrix}$
$k^2 + 4k + 4 = 0$
$(k+2)^2 = 0$
$k = -2$
Hence, the augmented matrix of $(E)$ becomes
$\begin{pmatrix} -1 & 2 & -1 & -8 \\ 0 & -3 & 3 & 12 \\ 0 & 0 & 0 & 0 \end{pmatrix} \sim \begin{pmatrix} -1 & 2 & -1 & -8 \\ 0 & -1 & 1 & 4 \\ 0 & 0 & 0 & 0 \end{pmatrix}$
Thus, the solution set of $(E)$ is $\{(t, t-4, t): t \in \mathbf{R}\}$.

## 第 9 題  <!-- 頁 [10, 11]｜13/13（題目卷為準；MS 讀到 subtotals=[3] cells=7） -->

Marks: 1A 1M 1A 1M 1M+1A 1A

9. (a) The equation of the vertical asymptote is $x - 1 = 0$.
Note that $\frac{x^2 + 3x}{x - 1} = x + 4 + \frac{4}{x - 1}$.
Thus, the equation of the oblique asymptote is $y = x + 4$.
(b) $f'(x) = 1 - \frac{4}{(x - 1)^2}$
$f'(x) = 0$
$1 - \frac{4}{(x - 1)^2} = 0$
$x^2 - 2x - 3 = 0$
$x = -1$ or $x = 3$
$x$ | $(-\infty, -1)$ | $-1$ | $(-1, 1)$ | $(1, 3)$ | $3$ | $(3, \infty)$
$f'(x)$ | $+$ | $0$ | $-$ | $-$ | $0$ | $+$
Thus, the maximum point and minimum point of $H$ are $(-1, 1)$ and $(3, 9)$ respectively.
(c)
(d) $f(x) = 10$
$\frac{x^2 + 3x}{x - 1} = 10$
$x^2 - 7x + 10 = 0$
$x = 2$ or $x = 5$
The required volume
$= \pi \int_2^5 (f(x) - 10)^2 dx$
$= \pi \int_2^5 \left( x + 4 + \frac{4}{x - 1} - 10 \right)^2 dx$
$= \pi \int_2^5 \left( x - 6 + \frac{4}{x - 1} \right)^2 dx$
$= \pi \int_2^5 \left( (x - 6)^2 + \frac{8(x - 6)}{x - 1} + \frac{16}{(x - 1)^2} \right) dx$
$= \pi \int_2^5 \left( (x - 6)^2 + 8 - \frac{40}{x - 1} + \frac{16}{(x - 1)^2} \right) dx$
$= \pi \left[ \frac{(x - 6)^3}{3} + 8x - 40 \ln|x - 1| - \frac{16}{x - 1} \right]_2^5$
$= \pi (57 - 80 \ln 2)$

## 第 10 題  <!-- 頁 [12, 13, 14]｜12/12（題目卷為準；MS 讀到 subtotals=無 cells=13） -->

Marks: 1M 1 1M 1 1M 1A 1M 1M 1M 1A 1M 1M 1A

10. (a) $\int g(x)dx$
$= \frac{\sin 2x\cos^2 x}{2} - \int \frac{\sin 2x}{2}(2\cos x)(-\sin x)dx$
$= \frac{\sin 2x\cos^2 x}{2} + \frac{1}{2}\int \sin^2 2xdx$
$\frac{d}{dx}\left(\frac{\sin 2x\cos^2 x}{2}\right)$
$= \frac{1}{2}(\cos 2x)(2)(\cos^2 x) + \frac{1}{2}(\sin 2x)(2\cos x)(-\sin x)$
$= \cos^2 x\cos 2x - \frac{1}{2}\sin^2 2x$
$\therefore \cos^2 x\cos 2x = \frac{d}{dx}\left(\frac{\sin 2x\cos^2 x}{2}\right) + \frac{1}{2}\sin^2 2x$
$\int \cos^2 x\cos 2x dx = \int \left(\frac{d}{dx}\left(\frac{\sin 2x\cos^2 x}{2}\right) + \frac{1}{2}\sin^2 2x\right)dx$
$\int g(x)dx = \frac{\sin 2x\cos^2 x}{2} + \frac{1}{2}\int \sin^2 2xdx$
(b) $\int_0^{\pi}g(x)dx$
$= \left[\frac{\sin 2x\cos^2 x}{2}\right]_0^{\pi} + \frac{1}{2}\int_0^{\pi}\sin^2 2xdx$ (by (a))
$= \left[\frac{\sin 2x\cos^2 x}{2}\right]_0^{\pi} + \frac{1}{2}\int_0^{\pi}\frac{1-\cos 4x}{2}dx$
$= 0 + \frac{1}{4}\left[x - \frac{\sin 4x}{4}\right]_0^{\pi}$
$= \frac{\pi}{4}$
(c) Let $u = \pi - x$.
$$\int_{0}^{\pi} xg(x) \mathrm{d}x$$
$$= \int_{0}^{0} -(\pi - u)\cos^{2}(\pi - u)\cos 2(\pi - u) \mathrm{d}u$$
$$= \int_{0}^{\pi} (\pi - u)\cos^{2} u \cos 2u \mathrm{d}u$$
$$= \int_{0}^{\pi} (\pi - x)\cos^{2} x \cos 2x \mathrm{d}x$$
$$= \pi \int_{0}^{\pi} g(x) \mathrm{d}x - \int_{0}^{\pi} xg(x) \mathrm{d}x$$
$$\int_{0}^{\pi} xg(x) \mathrm{d}x$$
$$= \frac{\pi}{2} \int_{0}^{\pi} g(x) \mathrm{d}x$$
$$= \frac{\pi}{2} \left( \frac{\pi}{4} \right)$$
$$= \frac{\pi^{2}}{8}$$
(d) $(-x)g(-x)$ $= (-x)\cos^2(-x)\cos2(-x)$ $= -x\cos^2x\cos2x$ $= -xg(x)$ $\therefore xg(x)$ is an odd function. So, we have $\int_{-\pi}^{\pi} xg(x)dx = 0$.
Let $y = x - \pi$. $\int_{-\pi}^{2\pi} xg(x)dx$ $= \int_{0}^{\pi} (\pi + y)\cos^2(\pi + y)\cos2(\pi + y)dy$ $= \int_{0}^{\pi} (\pi + y)\cos^2y\cos2ydy$ $= \int_{0}^{\pi} (\pi + x)\cos^2x\cos2xdx$ $= \pi \int_{0}^{\pi} g(x)dx + \int_{0}^{\pi} xg(x)dx$ $= \pi \left( \frac{\pi}{4} \right) + \frac{\pi^2}{8}$ (by (b) and (c))
$= \frac{3\pi^2}{8}$
$\int_{-\pi}^{2\pi} xg(x)dx$ $= \int_{-\pi}^{\pi} xg(x)dx + \int_{-\pi}^{2\pi} xg(x)dx$ $= 0 + \frac{3\pi^2}{8}$ $= \frac{3\pi^2}{8}$

## 第 11 題  <!-- 頁 [15, 16, 17]｜13/13（題目卷為準；MS 讀到 subtotals=無 cells=15） -->

Marks: 1A 1M 1M 1 1M 1M 1 1 1M 1M 1A 1M 1M 1M 1A

11. (a) (i) $(I - A)(I + A + A^2 + \cdots + A^n)$ $= I + A + A^2 + \cdots + A^n - (A + A^2 + A^3 + \cdots + A^{n+1})$ $= I - A^{n+1}$
(ii) (1) $I - A$ $= \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} - \begin{pmatrix} \cos \theta & -\sin \theta \\ \sin \theta & \cos \theta \end{pmatrix}$ $= \begin{pmatrix} 1 - \cos \theta & \sin \theta \\ -\sin \theta & 1 - \cos \theta \end{pmatrix}$
$|I - A|$ $= (1 - \cos \theta)^2 + \sin^2 \theta$ $= 2(1 - \cos \theta)$
$(I - A)^{-1}$ $= \frac{1}{2(1 - \cos \theta)} \begin{pmatrix} 1 - \cos \theta & -\sin \theta \\ \sin \theta & 1 - \cos \theta \end{pmatrix}$
$= \frac{1}{2} \begin{pmatrix} 1 & \frac{- \sin \theta}{1 - \cos \theta} \\ \frac{\sin \theta}{1 - \cos \theta} & 1 \end{pmatrix}$
$= \frac{1}{2} \begin{pmatrix} 1 & \frac{- 2 \sin \frac{\theta}{2} \cos \frac{\theta}{2}}{2 \sin^2 \frac{\theta}{2}} \\ \frac{2 \sin \frac{\theta}{2} \cos \frac{\theta}{2}}{2 \sin^2 \frac{\theta}{2}} & 1 \end{pmatrix}$
$= \frac{1}{2 \sin \frac{\theta}{2}} \begin{pmatrix} \sin \frac{\theta}{2} & -\cos \frac{\theta}{2} \\ \cos \frac{\theta}{2} & \sin \frac{\theta}{2} \end{pmatrix}$
(2) $I + A + A^2 + \cdots + A^n = (I - A)^{-1}(I - A^{n+1})$
$= \frac{1}{2 \sin \frac{\theta}{2}} \begin{pmatrix} \sin \frac{\theta}{2} & -\cos \frac{\theta}{2} \\ \cos \frac{\theta}{2} & \sin \frac{\theta}{2} \end{pmatrix} \begin{pmatrix} 1 - \cos(n+1)\theta & \sin(n+1)\theta \\ -\sin(n+1)\theta & 1 - \cos(n+1)\theta \end{pmatrix}$
$= \frac{1}{2 \sin \frac{\theta}{2}} \begin{pmatrix} \sin \frac{\theta}{2} & -\cos \frac{\theta}{2} \\ \cos \frac{\theta}{2} & \sin \frac{\theta}{2} \end{pmatrix} \begin{pmatrix} 2 \sin \frac{(n+1)\theta}{2} \\ -\cos \frac{(n+1)\theta}{2} & \sin \frac{(n+1)\theta}{2} \end{pmatrix}$
$= \frac{\sin \frac{(n+1)\theta}{2}}{\sin \frac{\theta}{2}} \begin{pmatrix} \sin \frac{\theta}{2} \sin \frac{(n+1)\theta}{2} + \cos \frac{\theta}{2} \cos \frac{(n+1)\theta}{2} & \sin \frac{\theta}{2} \cos \frac{(n+1)\theta}{2} - \cos \frac{\theta}{2} \sin \frac{(n+1)\theta}{2} \\ \cos \frac{\theta}{2} \sin \frac{(n+1)\theta}{2} - \sin \frac{\theta}{2} \cos \frac{(n+1)\theta}{2} & \cos \frac{\theta}{2} \cos \frac{(n+1)\theta}{2} + \sin \frac{\theta}{2} \sin \frac{(n+1)\theta}{2} \end{pmatrix}$
$= \frac{\sin \frac{(n+1)\theta}{2}}{\sin \frac{\theta}{2}} \begin{pmatrix} \cos \frac{n\theta}{2} & -\sin \frac{n\theta}{2} \\ \sin \frac{n\theta}{2} & \cos \frac{n\theta}{2} \end{pmatrix}$
(b) (i) $I + A + A^2 + \cdots + A^n$
$= \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} + \begin{pmatrix} \cos \theta & -\sin \theta \\ \sin \theta & \cos \theta \end{pmatrix} + \begin{pmatrix} \cos \theta & -\sin \theta \\ \sin \theta & \cos \theta \end{pmatrix}^2 + \cdots$
$+ \begin{pmatrix} \cos \theta & -\sin \theta \\ \sin \theta & \cos \theta \end{pmatrix}^n$
$= \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} + \begin{pmatrix} \cos \theta & -\sin \theta \\ \sin \theta & \cos \theta \end{pmatrix} + \begin{pmatrix} \cos 2\theta & -\sin 2\theta \\ \sin 2\theta & \cos 2\theta \end{pmatrix} + \cdots$
$+ \begin{pmatrix} \cos n\theta & -\sin n\theta \\ \sin n\theta & \cos n\theta \end{pmatrix}$
$= \begin{pmatrix} 1 + \cos \theta + \cos 2\theta + \cdots + \cos n\theta & -\sin \theta - \sin 2\theta - \cdots - \sin n\theta \\ \sin \theta + \sin 2\theta + \cdots + \sin n\theta & 1 + \cos \theta + \cos 2\theta + \cdots + \cos n\theta \end{pmatrix}$
$\therefore 1 + \cos \theta + \cos 2\theta + \cdots + \cos n\theta = \frac{\sin \frac{(n+1)\theta}{2} \cos \frac{n\theta}{2}}{\sin \frac{\theta}{2}}$
Putting $\theta = \frac{5\pi}{18}$ and $n = 90$,
$\cos \frac{5\pi}{18} + \cos \frac{5\pi}{9} + \cos \frac{5\pi}{6} + \cdots + \cos 25\pi$
$= \frac{\sin \frac{445\pi}{36} \cos \frac{25\pi}{2}}{\sin \frac{5\pi}{36}} - 1$
$= -1$
$(ii) \quad \cos^2 \frac{\pi}{7} + \cos^2 \frac{2\pi}{7} + \cos^2 \frac{3\pi}{7} + \cdots + \cos^2 7\pi$
$= \frac{1}{2} \left( 1 + \cos \frac{2\pi}{7} \right) + \frac{1}{2} \left( 1 + \cos \frac{4\pi}{7} \right) + \frac{1}{2} \left( 1 + \cos \frac{6\pi}{7} \right) + \cdots$
$+ \frac{1}{2} \left( 1 + \cos 14\pi \right)$
$= \frac{1}{2} \left( 49 + \cos \frac{2\pi}{7} + \cos \frac{4\pi}{7} + \cos \frac{6\pi}{7} + \cdots + \cos 14\pi \right)$
$\cos \frac{2\pi}{7} + \cos \frac{4\pi}{7} + \cos \frac{6\pi}{7} + \cdots + \cos 14\pi$
$= \frac{\sin \frac{50\pi}{7} \cos 7\pi}{\sin \frac{\pi}{7}} - 1$ (putting $\theta = \frac{2\pi}{7}$ and $n = 49$ in (b)(i))
$= 0$
$\therefore \cos^2 \frac{\pi}{7} + \cos^2 \frac{2\pi}{7} + \cos^2 \frac{3\pi}{7} + \cdots + \cos^2 7\pi = \frac{49}{2}$

## 第 12 題  <!-- 頁 [18, 19, 20]｜12/12（題目卷為準；MS 讀到 subtotals=無 cells=12） -->

Marks: 1M 1 1M 1M 1 1M 1 1M 1A 1M 1M 1A

12. (a) (i) $\overrightarrow{OD}$ $= \frac{b}{b+c} \overrightarrow{OB} + \frac{c}{b+c} \overrightarrow{OC}$
$\overrightarrow{AD}$ $= \overrightarrow{OD} - \overrightarrow{OA}$
$= \frac{b}{b+c} \overrightarrow{OB} + \frac{c}{b+c} \overrightarrow{OC} - \overrightarrow{OA}$
$= -\overrightarrow{OA} + \frac{b}{b+c} \overrightarrow{OB} + \frac{c}{b+c} \overrightarrow{OC}$
(ii) $\overrightarrow{AJ}$ $= \overrightarrow{OJ} - \overrightarrow{OA}$
$= \frac{a}{a+b+c} \overrightarrow{OA} + \frac{b}{a+b+c} \overrightarrow{OB} + \frac{c}{a+b+c} \overrightarrow{OC} - \overrightarrow{OA}$
$= \frac{-(b+c)}{a+b+c} \overrightarrow{OA} + \frac{b}{a+b+c} \overrightarrow{OB} + \frac{c}{a+b+c} \overrightarrow{OC}$
$= \left( \frac{b+c}{a+b+c} \right)\left( -\overrightarrow{OA} + \frac{b}{b+c} \overrightarrow{OB} + \frac{c}{b+c} \overrightarrow{OC} \right)$
$= \frac{b+c}{a+b+c} \overrightarrow{AD}$
Since $0 $J$ lies on $AD$.
$\overrightarrow{OE}$ $= \frac{a}{a+c} \overrightarrow{OA} + \frac{c}{a+c} \overrightarrow{OC}$
$\overrightarrow{BE}$ $= \overrightarrow{OE} - \overrightarrow{OB}$
$= \frac{a}{a+c} \overrightarrow{OA} - \overrightarrow{OB} + \frac{c}{a+c} \overrightarrow{OC}$
$\overrightarrow{BJ}$ $= \overrightarrow{OJ} - \overrightarrow{OB}$
$= \frac{a}{a+b+c} \overrightarrow{OA} + \frac{b}{a+b+c} \overrightarrow{OB} + \frac{c}{a+b+c} \overrightarrow{OC} - \overrightarrow{OB}$
$= \frac{a}{a+b+c} \overrightarrow{OA} - \frac{a+c}{a+b+c} \overrightarrow{OB} + \frac{c}{a+b+c} \overrightarrow{OC}$
$= \left( \frac{a+c}{a+b+c} \right)\left( \frac{a}{a+c} \overrightarrow{OA} - \overrightarrow{OB} + \frac{c}{a+c} \overrightarrow{OC} \right)$
$= \frac{a+c}{a+b+c} \overrightarrow{BE}$
Since $0 Thus, $AD$ and $BE$ intersect at $J$.
(b) (i) Define BC = a, AC = b and AB = c.
a = |$\overrightarrow{OC} - \overrightarrow{OB}$|
= |(-3j+k) - (40i-3j+k)|
= |-40i|
= 40
b = |$\overrightarrow{OC} - \overrightarrow{OA}$|
= |(-3j+k) - (35i+9j+k)|
= |-35i-12j|
= 37
c = |$\overrightarrow{OB} - \overrightarrow{OA}$|
= |(40i-3j+k) - (35i+9j+k)|
= |5i-12j|
$\overrightarrow{OI}$
= 32i + $\frac{7}{3}$j + k
$(ii) \quad \overrightarrow{AI} = \overrightarrow{OI} - \overrightarrow{OA}$ $= \left( 32i + \frac{7}{3}j + k \right) - (35i + 9j + k)$ $= -3i - \frac{20}{3}j$
$\overrightarrow{AI} \times \overrightarrow{AB} = \left( -3i - \frac{20}{3}j \right) \times (5i - 12j)$
$= \begin{vmatrix} i & j & k \\ -3 & \frac{-20}{3} & 0 \\ 5 & -12 & 0 \end{vmatrix}$
$= \frac{208}{3}k$
The radius of the inscribed circle
$= AI \sin \angle BAI$
$= \frac{(AI)(AB) \sin \angle BAI}{AB}$
$= \frac{\left| \overrightarrow{AI} \times \overrightarrow{AB} \right|}{c}$
$= \frac{16}{3}$


**合計 100 / 100**
