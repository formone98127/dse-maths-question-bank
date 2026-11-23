# 2025 M2 Paper 1 — 評卷參考（分題）

> marks 來源：每頁右側 52% 裁條獨立 OCR（逐頁累加，對題目卷分數）｜題目卷合計 100 分

## 第 1 題  <!-- 頁 [3]｜marks 逐頁 OCR；OK -->

Marks: 1 1 1 1  <!-- 小計 4 -->
1. $(1+5x)^n$
$= C_0^n(5x)^0 + C_1^n(5x)^1 + C_2^n(5x)^2 + \cdots + C_n^n(5x)^n$
$= 1 + 5nx + \frac{25n(n-1)}{2}x^2 + \cdots + (5x)^n$
Marks(cell): 1M

Hence, we have
$5n + m = 27$
$\frac{25n(n-1)}{2} + (m)(5n) = 285$
Marks(cell): 1M

So, we have
$\frac{25n(n-1)}{2} + (27-5n)(5n) = 285$
$5n^2 - 49n + 114 = 0$
$(n-6)(5n-19) = 0$
$n = 6$ or $n = \frac{19}{5}$ (rejected)
Marks(cell): 1M

When $n = 6$
$5(6) + m = 27$
$m = -3$
Marks(cell): 1A

## 第 2 題  <!-- 頁 [4]｜marks 逐頁 OCR；OK -->

Marks: 1 1 1 1 1  <!-- 小計 5 -->
2. (a) $f\left(\frac{\pi}{4}+h\right)-f\left(\frac{\pi}{4}\right)$

$= \frac{2\left(\frac{\pi}{4}+h\right)}{\tan\left(\frac{\pi}{4}+h\right)}-\frac{2\left(\frac{\pi}{4}\right)}{\tan\left(\frac{\pi}{4}\right)}$
Marks(cell): 1M

$= \left(\frac{\pi}{2}+2h\right)\left(\frac{1-\tan \frac{\pi}{4}\tan h}{\tan \frac{\pi}{4}+\tan h}\right)-\frac{\pi}{2}$

$= \left(\frac{\pi}{2}+2h\right)\left(\frac{1-\tan h}{1+\tan h}\right)-\frac{\pi}{2}$

$= \frac{\frac{\pi}{2}+2h-\frac{\pi}{2}\tan h-2h\tan h-\frac{\pi}{2}-\frac{\pi}{2}\tan h}{1+\tan h}$
Marks(cell): 1

$= \frac{2h-2h\tan h-\pi\tan h}{1+\tan h}$

(b) $f^{\prime}\left(\frac{\pi}{4}\right)$
Marks(cell): 1M

$= \lim_{h\to0} \frac{f\left(\frac{\pi}{4}+h\right)-f\left(\frac{\pi}{4}\right)}{h}$

$= \lim_{h\to0} \frac{2h-2h\tan h-\pi\tan h}{h(1+\tan h)}$

$= \lim_{h\to0}\left(\frac{2-2\tan h}{1+\tan h}-\frac{\pi\tan h}{h(1+\tan h)}\right)$
Marks(cell): 1M

$= \lim_{h\to0}\left(\frac{2-2\tan h}{1+\tan h}-\left(\frac{\pi}{(1+\tan h)\cos h}\right)\left(\frac{\sin h}{h}\right)\right)$

$= \frac{2-0}{1+0}-\left(\frac{\pi}{(1+0)(1)}\right)(1)$
Marks(cell): 1A

$= 2-\pi$
Marks(cell): (5)

## 第 3 題  <!-- 頁 [5, 6]｜marks 逐頁 OCR；⚠ 累計 9 ≠ 題目卷 6 -->

Marks: 1 1 1 1 1 1 1 1 1  <!-- 小計 6 -->
3. (a) $\frac{d}{dx} \ln \left( \sqrt{x^4+9} - x^2 \right)$
Marks(cell): 1M

$= \left( \frac{1}{\sqrt{x^4+9} - x^2} \right) \left( \left( \frac{1}{2\sqrt{x^4+9}} \right) (4x^3) - 2x \right)$

$= \left( \frac{1}{\sqrt{x^4+9} - x^2} \right) \left( \frac{2x^3 - 2x\sqrt{x^4+9}}{\sqrt{x^4+9}} \right)$

$= \left( \frac{1}{\sqrt{x^4+9} - x^2} \right) \left( \frac{2x(x^2 - \sqrt{x^4+9})}{\sqrt{x^4+9}} \right)$

$= \frac{-2x}{\sqrt{x^4+9}}$

Thus, we have $k = -2$.
Marks(cell): 1A

(b) $y$
Marks(cell): 1M

$= \int \frac{4x^3 - x}{\sqrt{x^4+9}} dx$

$= \int \frac{4x^3}{\sqrt{x^4+9}} dx - \frac{1}{2} \int \frac{2x}{\sqrt{x^4+9}} dx$

$= \int \frac{1}{\sqrt{x^4+9}} d(x^4 + 9) - \frac{1}{2} \int \frac{2x}{\sqrt{x^4+9}} dx$
Marks(cell): 1M

$= 2\sqrt{x^4+9} + \frac{1}{2} \ln \left( \sqrt{x^4+9} - x^2 \right) + C$, where $C$ is a constant
Marks(cell): 1M

Let $y = f(x)$.

$f(-x)$

$= 2\sqrt{(-x)^4+9} + \frac{1}{2} \ln \left( \sqrt{(-x)^4+9} - (-x)^2 \right) + C$

$= 2\sqrt{x^4+9} + \frac{1}{2} \ln \left( \sqrt{x^4+9} - x^2 \right) + C$

$= f(x)$

So, $f(x)$ is an even function.
Marks(cell): 1M

Therefore, $f(-2) = f(2) = 5$.

Thus, $\Gamma$ passes through the point $(-2, 5)$.
Marks(cell): 1A

$$y = \int \frac{4x^3 - x}{\sqrt{x^4 + 9}} dx
= \int \frac{4x^3}{\sqrt{x^4 + 9}} dx - \frac{1}{2} \int \frac{2x}{\sqrt{x^4 + 9}} dx
= \int \frac{1}{\sqrt{x^4 + 9}} d(x^4 + 9) - \frac{1}{2} \int \frac{2x}{\sqrt{x^4 + 9}} dx
= 2\sqrt{x^4 + 9} + \frac{1}{2} \ln\left(\sqrt{x^4 + 9} - x^2\right) + C, \text{ where } C \text{ is a constant}$
Marks(cell): 1M

Since $\Gamma$ passes through the point (2, 5), we have
$$2\sqrt{2^4 + 9} + \frac{1}{2} \ln\left(\sqrt{2^4 + 9} - 2^2\right) + C = 5
C = -5$$
Marks(cell): 1M

So, the equation of $\Gamma$ is $y = 2\sqrt{x^4 + 9} + \frac{1}{2} \ln\left(\sqrt{x^4 + 9} - x^2\right) - 5$.

When $x = -2$,
$$y = 2\sqrt{(-2)^4 + 9} + \frac{1}{2} \ln\left(\sqrt{(-2)^4 + 9} - (-2)^2\right) - 5
= 5$$

Thus, $\Gamma$ passes through the point $(-2, 5)$.
Marks(cell): 1A

## 第 4 題  <!-- 頁 [7]｜marks 逐頁 OCR；OK -->

Marks: 1 1 1  <!-- 小計 3 -->
4. CD
= $\begin{pmatrix} k & 1 \\ -1 & 2 \end{pmatrix} \begin{pmatrix} 2 & k-3 \\ k+3 & -4 \end{pmatrix}$
Marks(cell): 1M

= $\begin{pmatrix} 3k+3 & k^2-3k-4 \\ 2k+4 & -k-5 \end{pmatrix}$

DC
= $\begin{pmatrix} 2 & k-3 \\ k+3 & -4 \end{pmatrix} \begin{pmatrix} k & 1 \\ -1 & 2 \end{pmatrix}$

For CD = DC,
Marks(cell): 1M

$\begin{cases} 3k+3 = k+3 \\ k^2-3k-4 = 2k-4 \\ 2k+4 = k^2+3k+4 \\ -k-5 = k-5 \end{cases}$

$\begin{cases} 2k = 0 \\ k^2-5k = 0 \\ k^2+k = 0 \\ 2k = 0 \end{cases}$

$\begin{cases} k = 0 \\ k(k-5) = 0 \\ k(k+1) = 0 \end{cases}$
Marks(cell): 1A

$\begin{cases} k = 0 \text{ or } k = 5 \\ k = 0 \text{ or } k = -1 \end{cases}$

Thus, k = 0.

## 第 5 題  <!-- 頁 [8]｜marks 逐頁 OCR；⚠ 累計 4 ≠ 題目卷 6 -->

Marks: 1 1 1 1  <!-- 小計 6 -->
5. (a) Note that $\sum_{k=1}^{1} (-1)^k k^2 (k^2 - 1) = (-1)^1 (1)^2 (1^2 - 1) = 0$ and $\frac{(-1)^1 (1 - 1) (1 + 1) (1 + 2)}{2} = 0$. Therefore, the statement is true for $n = 1$.
Marks(cell): 1

Assume that $\sum_{k=1}^{m} (-1)^k k^2 (k^2 - 1) = \frac{(-1)^m (m - 1) m (m + 1) (m + 2)}{2}$, where $m$ is a positive integer.
Marks(cell): 1M

$\sum_{k=1}^{m+1} (-1)^k k^2 (k^2 - 1)$
$= \sum_{k=1}^{m} (-1)^k k^2 (k^2 - 1) + (-1)^{m+1} (m + 1)^2 \left((m + 1)^2 - 1\right)$
$= \frac{(-1)^m (m - 1) m (m + 1) (m + 2)}{2} + (-1)^{m+1} m (m + 1)^2 (m + 2)$
Marks(cell): 1M

(by induction assumption)
$= \frac{(-1)^{m+1} m (m + 1) (m + 2) \left(-(m - 1) + 2 (m + 1)\right)}{2}$
$= \frac{(-1)^{m+1} m (m + 1) (m + 2) (m + 3)}{2}$
Marks(cell): 1

So, the statement is true for $n = m + 1$ if it is true for $n = m$. By mathematical induction, the statement is true for all positive integers $n$.
Marks(cell): 1

(b) $\sum_{k=10}^{60} (-1)^k k^2 (k^2 - 1)$
$= \sum_{k=10}^{60} (-1)^k k^2 (k^2 - 1) - \sum_{k=1}^{9} (-1)^k k^2 (k^2 - 1)$
$= \frac{(-1)^{60} (60 - 1) (60) (60 + 1) (60 + 2)}{2} - \frac{(-1)^{9} (9 - 1) (9) (9 + 1) (9 + 2)}{2}$
$= 6 698 100$
Marks(cell): 1M

## 第 6 題  <!-- 頁 [9]｜marks 逐頁 OCR；OK -->

Marks: 1 1 1 1 1  <!-- 小計 5 -->
6. (a) $\frac{\sec x + \tan x}{\csc x - \cot x} + \frac{\sec x - \tan x}{\csc x + \cot x}$

$= \frac{(\sec x + \tan x)(\csc x + \cot x) + (\sec x - \tan x)(\csc x - \cot x)}{\csc^2 x - \cot^2 x}$

$= \frac{(\sec x \csc x + \tan x \csc x + \sec x \cot x + 1) + (\sec x \csc x - \tan x \csc x - \sec x \cot x + 1)}{1}$

$= 2 \sec x \csc x + 2$
Marks(cell): 1M

Thus, $h = 2$ and $k = 2$.
Marks(cell): 1A

(b) $\frac{\sec x + \tan x}{\csc x - \cot x} + \frac{\sec x - \tan x}{\csc x + \cot x} + 6 = 0$
Marks(cell): 1M

$2 \sec x \csc x + 2 + 6 = 0$
Marks(cell): 1M

$\frac{2}{\sin x \cos x} + 8 = 0$
Marks(cell): 1M

$\frac{4}{\sin 2x} + 8 = 0$
Marks(cell): 1M

$\sin 2x = \frac{-1}{2}$

$2x = \frac{7\pi}{6}$

$x = \frac{7\pi}{12}$
Marks(cell): 1A

## 第 7 題  <!-- 頁 [10]｜marks 逐頁 OCR；OK -->

Marks: 1 1 1 1 1 1  <!-- 小計 6 -->
7. (a) (i) $A = \begin{pmatrix} 4 & 3 \\ 0 & 1 \end{pmatrix} - \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} = \begin{pmatrix} 3 & 3 \\ 0 & 0 \end{pmatrix}$

$A^2 = \begin{pmatrix} 3 & 3 \\ 0 & 0 \end{pmatrix} \begin{pmatrix} 3 & 3 \\ 0 & 0 \end{pmatrix} = \begin{pmatrix} 3^2 & 3^2 \\ 0 & 0 \end{pmatrix}$

$A^3 = A^2 A = \begin{pmatrix} 3^2 & 3^2 \\ 0 & 0 \end{pmatrix} \begin{pmatrix} 3 & 3 \\ 0 & 0 \end{pmatrix} = \begin{pmatrix} 3^3 & 3^3 \\ 0 & 0 \end{pmatrix}$
Marks(cell): 1A

(ii) $A^n = \begin{pmatrix} 3^n & 3^n \\ 0 & 0 \end{pmatrix}$
Marks(cell): 1A

(b) $B^n = (I + A)^n$

$= I + \sum_{k=1}^{n} C_k^n A^k$

$= \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} + \sum_{k=1}^{n} C_k^n \begin{pmatrix} 3^k & 3^k \\ 0 & 0 \end{pmatrix}$

$= \begin{pmatrix} 1 + \sum_{k=1}^{n} C_k^n 3^k & \sum_{k=1}^{n} C_k^n 3^k \\ 0 & 1 \end{pmatrix}$
Marks(cell): 1M

$= \begin{pmatrix} (1+3)^n & (1+3)^n -1 \\ 0 & 1 \end{pmatrix}$

$= \begin{pmatrix} 4^n & 4^n -1 \\ 0 & 1 \end{pmatrix}$
Marks(cell): 1A

(c) $A^m - B^m$

$= \begin{pmatrix} 3^m & 3^m \\ 0 & 0 \end{pmatrix} - \begin{pmatrix} 4^m & 4^m -1 \\ 0 & 1 \end{pmatrix}$

$= \begin{pmatrix} 3^m - 4^m & 3^m - 4^m +1 \\ 0 & -1 \end{pmatrix}$

$\det(A^m - B^m)$

$= 4^m - 3^m \neq 0$ for all positive integers $m$.

Thus, there does not exist a positive integer $m$ such that $A^m - B^m$ is singular.

## 第 8 題  <!-- 頁 [11]｜marks 逐頁 OCR；OK -->

Marks: 1 1 1 1 1 1 1  <!-- 小計 未讀到 -->
8. (a) Note that the coordinates of $P$ are $(0, 4)$.

$$A = \frac{(4 + h^2 + 4)h}{2} = \frac{1}{2}h^3 + 4h$$
Marks(cell): 1M

$$\frac{dA}{dh} = \frac{3}{2}h^2 + 4$$
Marks(cell): 1A

(b) $\frac{dh}{dt}$

$$= -2(-e^{-t})$$

$$= 2e^{-t}$$

$$\frac{dA}{dt}$

$$= \left(\frac{dA}{dh}\right)\left(\frac{dh}{dt}\right)$
Marks(cell): 1M

$$= \left(\frac{3}{2}(3 - 2e^{-t})^2 + 4\right)(2e^{-t})$$

$$= 35e^{-t} - 36e^{-2t} + 12e^{-3t}$$

$$\frac{d}{dt}\left(\frac{dA}{dt}\right)$

$$= -35e^{-t} + 72e^{-2t} - 36e^{-3t}$

$$= e^{-t}(-35 + 72e^{-t} - 36e^{-2t})$$

When $\frac{d}{dt}\left(\frac{dA}{dt}\right) = 0$, we have

$-35 + 72e^{-t} - 36e^{-2t} = 0$

$(6e^{-t} - 5)(6e^{-t} - 7) = 0$

$e^{-t} = \frac{5}{6}$ or $e^{-t} = \frac{7}{6}$

When $e^{-t} = \frac{7}{6}$, $t = -\ln \frac{7}{6} < 0$. (rejected)

When $e^{-t} = \frac{5}{6}$, $t = \ln \frac{6}{5}$.

$t$
Marks(cell): $\left(0, \ln \frac{6}{5}\right)$

$\frac{d}{dt}\left(\frac{dA}{dt}\right)$
Marks(cell): +

So, $\frac{dA}{dt}$ attains its maximum value when $t = \ln \frac{6}{5}$. Thus, the claim is agreed.

## 第 9 題  <!-- 頁 [12]｜marks 逐頁 OCR；⚠ 累計 7 ≠ 題目卷 8 -->

Marks: 1 1 1 1 1 1 1  <!-- 小計 8 -->
9. (a) Let $x = \tan \theta$.
So, we have $\frac{dx}{d\theta} = \sec^2 \theta$.
Marks(cell): 1M

$$\int \frac{1}{(1+x^2)^2} dx$$
$$= \int \left( \frac{1}{(1+\tan^2 \theta)^2} \right) \sec^2 \theta d\theta$$
$$= \int \left( \frac{1}{\sec^4 \theta} \right) \sec^2 \theta d\theta$$
$$= \int \cos^2 \theta d\theta$$
$$= \int \frac{1+\cos 2\theta}{2} d\theta$$
$$= \frac{1}{2} \theta + \frac{1}{4} \sin 2\theta + \text{constant}$$
$$= \frac{1}{2} \theta + \frac{1}{2} \sin \theta \cos \theta + \text{constant}$$
$$= \frac{1}{2} \theta + \frac{1}{2} \left( \frac{\tan \theta}{1+\tan^2 \theta} \right) + \text{constant}$$
$$= \frac{1}{2} \tan^{-1} x + \frac{x}{2(1+x^2)} + \text{constant}$$
Marks(cell): 1M

(b) The required volume
Marks(cell): 1M

$$= \pi \int_0^1 \frac{1}{(1+3x^2)^2} dx$$
$$= \frac{\pi}{\sqrt{3}} \int_0^{\sqrt{3}} \frac{1}{(1+y^2)^2} dy$$
(by letting $y = \sqrt{3}x$)
Marks(cell): 1M

$$= \frac{\pi}{\sqrt{3}} \left[ \frac{1}{2} \tan^{-1} y + \frac{y}{2(1+y^2)} \right]_0^{\sqrt{3}}$$
$$= \frac{\sqrt{3} \pi^2}{18} + \frac{\pi}{8}$$
Marks(cell): 1M

## 第 10 題  <!-- 頁 [13, 14]｜marks 逐頁 OCR；⚠ 累計 10 ≠ 題目卷 12 -->

Marks: 1 1 1 1 1 1 1 1 1 1  <!-- 小計 3 -->
10. (a) f(x)
$$= \frac{x^3+25x}{x^2+3}\\= x+\frac{22x}{x^2+3}$$
Marks(cell): 1M

Thus, the equation of the oblique asymptote of G is y=x.
Marks(cell): 1A

(b) f'(x)
$$= 1+\frac{(x^2+3)(22)-(22x)(2x)}{(x^2+3)^2}\\= 1+\frac{-22x^2+66}{(x^2+3)^2}\\= \frac{x^4-16x^2+75}{(x^2+3)^2}\\= \frac{(x^2-8)^2+11}{(x^2+3)^2}\\>&gt; 0$$
Marks(cell): 1M

Thus, the claim is agreed.
Marks(cell): 1A

(c) f(-x) = \frac{(-x)^3+25(-x)}{(-x)^2+3} = \frac{-x^3-25x}{x^2+3} = -f(x)
Marks(cell): 1

So, f(x) is an odd function

Thus, G has rotational symmetry about the origin.

(d) $f''(x)$
Marks(cell): 1M

$= \frac{(x^2+3)^2(4x^3-32x)-(x^4-16x^2+75)(2)(x^2+3)(2x)}{(x^2+3)^4}$

$= \frac{4x((x^2+3)(x^2-8)-(x^4-16x^2+75))}{(x^2+3)^3}$

$= \frac{4x(11x^2-99)}{(x^2+3)^3}$

$= \frac{44x(x-3)(x+3)}{(x^2+3)^3}$

When $f''(x)=0$, we have $x=-3, 0$ or $3$.
Marks(cell): 1M

$$\begin{array}{c|cccccc} x & (-\infty,-3) & -3 & (-3,0) & 0 & (0,3) & 3 & (3,\infty) \\ f''(x) & - & 0 & + & 0 & - & 0 & + \\ \end{array}$$
Marks(cell): 1M

Thus, the points of inflexion of $G$ are $\left(-3, \frac{-17}{2}\right), (0, 0)$ and $\left(3, \frac{17}{2}\right)$.
Marks(cell): 1A

(e) The required area
Marks(cell): 1M

$= 2\left(\int_0^3 f(x) \, dx - \left(\frac{1}{2}\right)(3)\left(\frac{17}{2}\right)\right)$

$= 2\left(\int_0^3 \left(x + \frac{22x}{x^2+3}\right) \, dx - \frac{51}{4}\right)$

$= 2\left(\int_0^3 x \, dx + 44 \int_0^3 \frac{x}{x^2+3} \, dx - \frac{51}{2}\right)$

$= 2\left[\frac{x^2}{2}\right]_0^3 + 44 \int_0^3 \frac{x}{x^2+3} \, dx - \frac{51}{2}$

$= 44 \int_0^3 \frac{x}{x^2+3} \, dx - \frac{33}{2}$

$= 22 \int_3^{12} \frac{1}{y} \, dy - \frac{33}{2}$
Marks(cell): 1M

$= 44 \ln 2 - \frac{33}{2}$
Marks(cell): 1A

## 第 11 題  <!-- 頁 [15, 16]｜marks 逐頁 OCR；OK -->

Marks: 1 1 1 1 1 1 1 1 1 1 1 1 1  <!-- 小計 4 -->
11. (a) $\int_{0}^{\pi} e^{-x} \sin 2mx \, dx$

$= -\left[ e^{-x} \sin 2mx \right]_{0}^{\pi} + 2m \int_{0}^{\pi} e^{-x} \cos 2mx \, dx$
Marks(cell): 1M

$= 2m \int_{0}^{\pi} e^{-x} \cos 2mx \, dx$

$= -\left[ 2me^{-x} \cos 2mx \right]_{0}^{\pi} - 4m^{2} \int_{0}^{\pi} e^{-x} \sin 2mx \, dx$
Marks(cell): 1M

$= -2me^{-\pi} + 2m - 4m^{2} \int_{0}^{\pi} e^{-x} \sin 2mx \, dx$

$(1 + 4m^{2}) \int_{0}^{\pi} e^{-x} \sin 2mx \, dx = 2m - 2me^{-\pi}$

$\int_{0}^{\pi} e^{-x} \sin 2mx \, dx = \frac{2m}{1 + 4m^{2}} (1 - e^{-\pi})$
Marks(cell): 1A

12. (b) (i) $\int_{0}^{\pi} e^{-x} \sin 5x \cos 3x \, dx$

$= \frac{1}{2} \int_{0}^{\pi} e^{-x} (\sin 8x + \sin 2x) \, dx$
Marks(cell): 1M

$= \frac{1}{2} \left( \frac{2(4)}{1 + 4(4^{2})} (1 - e^{-\pi}) + \frac{2(1)}{1 + 4(1^{2})} (1 - e^{-\pi}) \right)$
Marks(cell): 1M

$= \frac{17}{65} (1 - e^{-\pi})$
Marks(cell): 1A

13. (ii) $\int_{0}^{2\pi} e^{-x} \sin 5x \cos 3x \, dx$

$= \int_{0}^{\pi} e^{-x} \sin 5x \cos 3x \, dx + \int_{0}^{\pi} e^{-x} \sin 5x \cos 3x \, dx$
Marks(cell): 1M

$= \frac{17}{65} (1 - e^{-\pi}) + \int_{0}^{\pi} e^{-x} \sin 5x \cos 3x \, dx$

$= \frac{17}{65} (1 - e^{-\pi}) + \int_{0}^{\pi} e^{-u - \pi} \sin(5u + 5\pi) \cos(3u + 3\pi) \, du$

$= \frac{17}{65} (1 - e^{-\pi}) + e^{-\pi} \int_{0}^{\pi} e^{-u} \sin 5u \cos 3u \, du$

$= \frac{17}{65} (1 - e^{-\pi}) + e^{-\pi} \left( \frac{17}{65} (1 - e^{-\pi}) \right)$

$= \frac{17}{65} (1 - e^{-2\pi})$
Marks(cell): 1M

(c) Let $\ln x = \frac{\pi}{2} - u$.
Marks(cell): 1M

$$\int_{e}^{\frac{\pi}{2}} \cos(\ln x^5) \sin(\ln x^3) \, dx$$

$= \int_{e}^{\frac{\pi}{2}} \cos(5 \ln x) \sin(3 \ln x) \, dx$
Marks(cell): 1M

$= -\int_{2\pi}^{0} e^{\frac{\pi}{2}-u} \cos\left(\frac{5\pi}{2}-5u\right) \sin\left(\frac{3\pi}{2}-3u\right) \, du$
Marks(cell): 1M

$= -e^{\frac{\pi}{2}} \int_{0}^{2\pi} e^{-u} \sin 5u \cos 3u \, du$

$= -\left(e^{\frac{\pi}{2}}\right)\left(\frac{17}{65}\left(1-e^{-2\pi}\right)\right)$

$= \frac{17}{65}\left(e^{\frac{-3\pi}{2}}-e^{\frac{\pi}{2}}\right)$
Marks(cell): 1A

## 第 12 題  <!-- 頁 [17, 18]｜marks 逐頁 OCR；OK -->

Marks: 1 1 1 1 1 1 1 1 1 1 1 1  <!-- 小計 7 -->
12. (a) (i) Note that
$$\begin{vmatrix} 1 & -(a+1) & 2 \\ 2 & a & 7 \\ 4 & a+6 & 3a+14 \end{vmatrix} = (1)(a)(3a+14) - (a+1)(7)(4) + (2)(2)(a+6) - (2)(a)(4) + (a+1)(2)(3a+14) - (1)(7)(a+6) = 9a^2 + 9a - 18 = 9(a+2)(a-1)$$
Marks(cell): 1M

If $(E)$ has a unique solution, then
$$\begin{vmatrix} 1 & -(a+1) & 2 \\ 2 & a & 7 \\ 4 & a+6 & 3a+14 \end{vmatrix} \neq 0.$$
Marks(cell): 1M

So, we have $9(a+2)(a-1) \neq 0$.
Solving, we have $a \neq -2$ and $a \neq 1$.
Thus, we have $a < -2$, $-2 < a < 1$ or $a > 1$.
Marks(cell): 1A

(ii) $y$
$$= \frac{1}{9(a+2)(a-1)} \sim \frac{-3b+12}{9(a+2)(a-1)} \sim \frac{-b+4}{3(a+2)(a-1)}$$
Marks(cell): 1M

(b) (i) We have $a = 1$.
The augmented matrix of $(E)$ is
$$\begin{pmatrix} 1 & -2 & 2 & 1 \\ 2 & 1 & 7 & 2 \\ 4 & 7 & 17 & b \end{pmatrix} \sim \begin{pmatrix} 1 & -2 & 2 & 1 \\ 0 & 5 & 3 & 0 \\ 0 & 15 & 9 & b-4 \end{pmatrix} \sim \begin{pmatrix} 1 & -2 & 2 & 1 \\ 0 & 5 & 3 & 0 \\ 0 & 0 & 0 & b-4 \end{pmatrix}$$
Marks(cell): 1M

Therefore, we have $b = 4$.
Hence, the augmented matrix of $(E)$ is
$$\begin{pmatrix} 1 & -2 & 2 & 1 \\ 0 & 5 & 3 & 0 \\ 0 & 0 & 0 & 0 \end{pmatrix}$$
Marks(cell): 1A

Thus, the solution set of $(E)$ is $\{(16t+1, 3t, -5t) : t \in \mathbb{R}\}$.

(b) (ii) Putting $x = 16t + 1$, $y = 3t$ and $z = -5t$, we have

$k(16t + 1) + (3t) + 4k(-5t)^2 > 0$
Marks(cell): 1M

$100kt^2 + (16k + 3)t + k > 0$

$100kt^2 + (16k + 3)t + k > 0$ for all $t$, we have

$100k > 0$ and $(16k + 3)^2 - 4(100k)(k) < 0$
Marks(cell): 1M + 1M

$k > 0$ and $(16k + 3)^2 - (20k)^2 < 0$

$k > 0$ and $(16k + 3 + 20k)(16k + 3 - 20k) < 0$

$k > 0$ and $(12k + 1)(4k - 3) > 0$

$k > 0$ and $\left(k < \frac{-1}{12} \text{ or } k > \frac{3}{4}\right)$
Marks(cell): 1A

$k > \frac{3}{4}$
Marks(cell): ---------(7)

## 第 13 題  <!-- 頁 [19, 20]｜marks 逐頁 OCR；OK -->

Marks: 1 1 1 1 1 1 1 1 1 1 1 1 1  <!-- 小計 3 -->
13. (a) $\overrightarrow{AB} = (-2i + 5j + 2k) - (i - 2j + 3k)$
$= -3i + 7j - k$
Marks(cell): 1M

$\overrightarrow{AC} = (2i - k) - (i - 2j + 3k)$
$= i + 2j - 4k$

$\overrightarrow{AB} \times \overrightarrow{AC}$
Marks(cell): 1M

$= \begin{vmatrix} i & j & k \\ -3 & 7 & -1 \\ 1 & 2 & -4 \end{vmatrix}$
Marks(cell): 1A

$= -26i - 13j - 13k$
Marks(cell): (3)

13. (b) $\overrightarrow{AD} = (-2i - 6j + 2k) - (i - 2j + 3k) = -3i - 4j - k$

$\overrightarrow{ED} = \frac{\overrightarrow{AD} \cdot (\overrightarrow{AB} \times \overrightarrow{AC})}{(\overrightarrow{AB} \times \overrightarrow{AC}) \cdot (\overrightarrow{AB} \times \overrightarrow{AC})} (\overrightarrow{AB} \times \overrightarrow{AC})$
Marks(cell): 1M

$= \frac{(-3i - 4j - k) \cdot (-26i - 13j - 13k)}{(-26i - 13j - 13k) \cdot (-26i - 13j - 13k)} (-26i - 13j - 13k)$
Marks(cell): 1A

$= \frac{-11}{3}i - \frac{11}{6}j - \frac{11}{6}k$
Marks(cell): 1A

$\overrightarrow{EA} = \overrightarrow{ED} - \overrightarrow{AD}$
Marks(cell): 1M

$= \left( \frac{-11}{3}i - \frac{11}{6}j - \frac{11}{6}k \right) - (-3i - 4j - k)$
Marks(cell): 1A

$= \frac{-2}{3}i + \frac{13}{6}j - \frac{5}{6}k$
Marks(cell): (4)

(c) $\overrightarrow{AF} = \frac{1}{1+t}(t\overrightarrow{AB} + \overrightarrow{AC})$
$= \frac{1}{1+t}\left(t(-3\mathbf{i} + 7\mathbf{j} - \mathbf{k}) + (\mathbf{i} + 2\mathbf{j} - 4\mathbf{k})\right)$
$= \frac{1}{1+t}\left((-3t+1)\mathbf{i} + (7t+2)\mathbf{j} + (-t-4)\mathbf{k}\right)$
Marks(cell): 1M

Since $EA // AF$, we have $\frac{\frac{-3t+1}{1+t}}{\frac{-2}{3}} = \frac{\frac{7t+2}{1+t}}{\frac{13}{6}} = \frac{\frac{-t-4}{1+t}}{\frac{-5}{6}}$.
Marks(cell): 1M

Thus, we have $t = \frac{21}{11}$.
Marks(cell): 1A

(d) Area of $\Delta ABF$
$= \left(\frac{1}{2}\sqrt{26^2 + 13^2 + 13^2}\right)\left(\frac{1}{1 + \frac{21}{11}}\right)$
$= \frac{143\sqrt{6}}{64}$
Marks(cell): 1M

Volume of pyramid $ABDF$
$= \frac{1}{3}\left(\frac{143\sqrt{6}}{64}\right)\sqrt{\left(\frac{-11}{3}\right)^2 + \left(\frac{-11}{6}\right)^2 + \left(\frac{-11}{6}\right)^2}$
$= \frac{1573}{192}$
Marks(cell): 1M


**合計 98 / 100**
