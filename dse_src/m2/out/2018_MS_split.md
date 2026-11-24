# 2018 M2 Paper 1 — 評卷參考（分題）

> 分題依據：MS 題號行 + marks 對題目卷分數 [4, 5, 5, 6, 7, 7, 8, 8, 12, 13, 12, 13]｜合計 100

## 第 1 題  <!-- 頁 [2]｜4/4（MS 小計） -->

Marks: 1A 1M 1M 1A

1. f(1+h) = ((1+h)²-1)e¹+h = (2h+h²)e¹+h
f'(1) = lim h→0 f(1+h)-f(1) = lim h→0 (2h+h²)e¹+h-0 = lim h→0 (2+h)e¹+h = 2e

## 第 2 題  <!-- 頁 [2]｜5/5（MS 小計） -->

Marks: 1M 1A 1M 1A

2. (x+3)⁵ = x⁵+5(3)x⁴+10(3²)x³+10(3³)x²+5(3⁴)x+3⁵ = x⁵+15x⁴+90x³+270x²+405x+243
$\left(x-\frac{4}{x}\right)²$ = x²-2x\left(\frac{4}{x}\right)+\left(\frac{4}{x}\right)²$ = x²-8+\frac{16}{x²}$
The coefficient of x³ = (1)(16)+(90)(-8)+(405)(1) = -299

## 第 3 題  <!-- 頁 [3]｜5/5（MS 小計） -->

Marks: 1M 1 1 1M 1M 1M 1A 1A

3. (a) $\cot A = 3\cot B$ $\frac{\cos A}{\sin A} = \frac{3\cos B}{\sin B}$ $3\sin A\cos B = \cos A\sin B$
$\sin(A+B) - 2\sin(B-A)$ $= (\sin A\cos B + \cos A\sin B) - 2(\sin B\cos A - \cos B\sin A)$ $= 3\sin A\cos B - \cos A\sin B$ $= 0$
Thus, we have $\sin(A+B) = 2\sin(B-A)$.
(b) $\cot\left(x + \frac{4\pi}{9}\right) = 3\cot\left(x + \frac{5\pi}{18}\right)$
By letting $A = x + \frac{4\pi}{9}$ and $B = x + \frac{5\pi}{18}$, we have $\cot A = 3\cot B$.
By (a), we have $\sin(A+B) = 2\sin(B-A)$.
With the help of $\sin\left(\frac{-\pi}{6}\right) = \frac{-1}{2}$, we have $\sin\left(2x + \frac{13\pi}{18}\right) = -1$.
Noting that $0 \leq x \leq \frac{\pi}{2}$, we have $x = \frac{7\pi}{18}$.
Since $\cot\left(\frac{7\pi}{18} + \frac{4\pi}{9}\right) = -\sqrt{3} = 3\cot\left(\frac{7\pi}{18} + \frac{5\pi}{18}\right)$, the required solution of the equation $\cot\left(x + \frac{4\pi}{9}\right) = 3\cot\left(x + \frac{5\pi}{18}\right)$ is $x = \frac{7\pi}{18}$.

## 第 4 題  <!-- 頁 [3]｜6/6（題目卷為準；MS 讀到 subtotals=無 cells=10） -->

Marks: 1M 1A 1A 1A 1M 1M 1M 1M 1A 1A

4. (a) $\int u(5^u) \, du$
$= \frac{1}{\ln 5}\left(u(5^u) - \int 5^u \, du\right)$
$= \frac{1}{\ln 5}\left(u(5^u) - \frac{5^u}{\ln 5}\right) + \text{constant}$
$= \frac{5^u\left(u\ln 5 - 1\right)}{(\ln 5)^2} + \text{constant}$
(b) The required area
$= \int_0^1 x(5^{2x}) \, dx$
$= \frac{1}{4}\int_0^2 u(5^u) \, du$
$= \frac{1}{4(\ln 5)^2}\left[5^u\left(u\ln 5 - 1\right)\right]_0^2$
$= \frac{50\ln 5 - 24}{4(\ln 5)^2}$
$= \frac{25\ln 5 - 12}{2(\ln 5)^2}$

## 第 5 題  <!-- 頁 [4]｜7/7（題目卷為準；MS 讀到 subtotals=無 cells=3） -->

Marks: 1M 1M 1M

5. (a) Let $u = 1 + x^2$. Then, we have $\frac{du}{dx} = 2x$. $\int x^3\sqrt{1+x^2} \, dx$ $= \int \frac{1}{2}(u-1)u^{\frac{1}{2}} \, du$ $= \frac{1}{2}\left(\int u^{\frac{3}{2}} \, du - \int u^{\frac{1}{2}} \, du\right)$ $= \frac{1}{5}\left(\sqrt{1+x^2}\right)^5 - \frac{1}{3}\left(\sqrt{1+x^2}\right)^3 + \text{constant}$
Let $x = \tan \theta$. Then, we have $\frac{dx}{d\theta} = \sec^2 \theta$. $\int x^3\sqrt{1+x^2} \, dx$ $= \int \tan^3 \theta \sec \theta(\sec^2 \theta) \, d\theta$ $= \int \tan^3 \theta \sec^3 \theta \, d\theta$ $= \int(\sec^2 \theta - 1)\sec^2 \theta \, d\sec \theta$ $= \int \sec^4 \theta \, d\sec \theta - \int \sec^2 \theta \, d\sec \theta$ $= \frac{\sec^5 \theta}{5} - \frac{\sec^3 \theta}{3} + \text{constant}$ $= \frac{1}{5}\left(\sqrt{1+x^2}\right)^5 - \frac{1}{3}\left(\sqrt{1+x^2}\right)^3 + \text{constant}$
(b) $y = \int 15x^3\sqrt{1+x^2} \, dx$ $= 15\int x^3\sqrt{1+x^2} \, dx$ $= 15\left(\frac{1}{5}\left(\sqrt{1+x^2}\right)^5 - \frac{1}{3}\left(\sqrt{1+x^2}\right)^3\right) + C$ (by (a)) $= 3\left(\sqrt{1+x^2}\right)^5 - 5\left(\sqrt{1+x^2}\right)^3 + C$, where $C$ is a constant Since the $y$-intercept of $\Gamma$ is 2, we have $3 - 5 + C = 2$. Solving, we have $C = 4$. Thus, the equation of $\Gamma$ is $y = 3\left(\sqrt{1+x^2}\right)^5 - 5\left(\sqrt{1+x^2}\right)^3 + 4$.

## 第 6 題  <!-- 頁 [5]｜7/7（題目卷為準；MS 讀到 subtotals=無 cells=2） -->

Marks: 1 1M

6. (a) Note that $(1)(1+4) = 5 = \frac{(1)(2)(15)}{6}$. So, the statement is true for $n = 1$. Assume that $\sum_{k=1}^{m} k(k+4) = \frac{m(m+1)(2m+13)}{6}$ for some positive integer $m$. $$\sum_{k=1}^{m+1} k(k+4) = \sum_{k=1}^{m} k(k+4) + (m+1)(m+5) = \frac{m(m+1)(2m+13)}{6} + (m+1)(m+5) \quad (\text{by induction assumption})$$ $$= \frac{(m+1)(2m^2+13m+6m+30)}{6}$$ $$= \frac{(m+1)(2m^2+19m+30)}{6}$$ $$= \frac{(m+1)(m+2)(2m+15)}{6}$$ So, the statement is true for $n = m+1$ if it is true for $n = m$. By mathematical induction, the statement is true for all positive integers $n$.
(b) Putting $n = 555$ in (a), we have $$\sum_{k=1}^{555} k(k+4) = \frac{(555)(556)(1123)}{6} = 57755890.$ Putting $n = 332$ in (a), we have $$\sum_{k=1}^{332} k(k+4) = \frac{(332)(333)(677)}{6} = 12474402.$ $$\sum_{k=333}^{555} \left( \frac{k}{112} \right) \left( \frac{k+4}{223} \right) = \left( \frac{1}{112} \right) \left( \frac{1}{223} \right) \sum_{k=333}^{555} k(k+4) = \frac{1}{(112)(223)} \left( \sum_{k=1}^{555} k(k+4) - \sum_{k=1}^{332} k(k+4) \right) = \frac{1}{24976} (57755890 - 12474402) = 1813$$

## 第 7 題  <!-- 頁 [6]｜8/8（題目卷為準；MS 讀到 subtotals=無 cells=5） -->

Marks: 1M 1M 1A 1M 1M

7. (a) MX = XM
$$\begin{pmatrix} 7 & 3 \\ -1 & 5 \end{pmatrix} \begin{pmatrix} a & 6a \\ b & c \end{pmatrix} = \begin{pmatrix} a & 6a \\ b & c \end{pmatrix} \begin{pmatrix} 7 & 3 \\ -1 & 5 \end{pmatrix}$$
$$\begin{pmatrix} 7a + 3b & 42a + 3c \\ -a + 5b & -6a + 5c \end{pmatrix} = \begin{pmatrix} a & 33a \\ 7b - c & 3b + 5c \end{pmatrix}$$
$$\begin{cases} 7a + 3b = a \\ -a + 5b = 7b - c \\ 42a + 3c = 33a \\ -6a + 5c = 3b + 5c \end{cases}$$
(b) |X|
= |a & 6a| / |-2a & -3a| = (a)(-3a) - (6a)(-2a) = 9a²
Note that X is a non-zero real matrix. By (a), a is a non-zero real number. So, we have |X| &gt; 0.
Therefore, we have |X| &ne; 0.
Thus, X is a non-singular matrix.
(c) $(X^T)^-1$
= $(X^{-1})^T = \left( \frac{1}{|X|} \begin{pmatrix} -3a & -6a \\ 2a & a \end{pmatrix} \right)^T = \left( \frac{1}{9a} \begin{pmatrix} -3 & -6 \\ 2 & 1 \end{pmatrix} \right)^T = \frac{1}{9a} \begin{pmatrix} -3 & 2 \\ -6 & 1 \end{pmatrix}$
$(X^T)^-1$
= $\begin{pmatrix} a & -2a \\ 6a & -3a \end{pmatrix}^{-1}$
= $\frac{1}{|X^T|} \begin{pmatrix} -3a & 2a \\ -6a & a \end{pmatrix}$
= $\frac{1}{|X|} \begin{pmatrix} -3a & 2a \\ -6a & a \end{pmatrix}$
= $\frac{1}{9a} \begin{pmatrix} -3 & 2 \\ -6 & 1 \end{pmatrix}$

## 第 8 題  <!-- 頁 [7]｜8/8（題目卷為準；MS 讀到 subtotals=無 cells=3） -->

Marks: 1M 1M 1M

8. (a) Note that $A \neq 0$. $f'(x)$ $$= \frac{-A(2x-4)}{(x^2-4x+7)^2}$$ So, we have $f'(x) = 0 \iff x = 2$. Since the equation $f'(x) = 0$ has only one solution $x = 2$ and the extreme value of $f(x)$ is 4, we have $f(2) = 4$. Hence, we have $\frac{A}{2^2-4(2)+7} = 4$. Therefore, we have $A = 12$. Thus, we have $f'(x) = \frac{24(2-x)}{(x^2-4x+7)^2}$.
(b) Note that $x^2-4x+7 = (x-2)^2+3 > 0$ for all real values of $x$. So, there are no vertical asymptotes of the graph of $y = f(x)$. Also note that $f(x) = \frac{12}{x^2-4x+7}$. Therefore, $y = 0$ is the only asymptote of the graph of $y = f(x)$. Hence, there is only one asymptote of the graph of $y = f(x)$. Thus, the claim is disagreed.
(c) $f''(x)$ $$= \frac{(x^2-4x+7)^2(-24) - (-24x+48)(2)(x^2-4x+7)(2x-4)}{(x^2-4x+7)^4}$ $$= \frac{72(x-3)(x-1)}{(x^2-4x+7)^3}$ So, we have $f''(x) = 0 \iff x = 1$ or $x = 3$.
Thus, the points of inflexion are $(1,3)$ and $(3,3)$.

## 第 9 題  <!-- 頁 [8, 9]｜12/12（題目卷為準；MS 讀到 subtotals=無 cells=9） -->

Marks: 1M 1M 1 1M 1A 1M 0 1M 1M 1M

9. (a) $y = \frac{\ln x}{2}$
$\frac{dy}{dx} = \frac{1}{2x}$
The slope of the tangent at $P$ is $\frac{1}{2r}$.
The slope of the normal at $P$ is $-2r$.
Let $a$ be the $x$-coordinate of $Q$.
$\frac{0 - \ln \sqrt{r}}{a - r} = -2r$
$\frac{-1}{2} \ln r = 2r^2 - 2ar$
$2ar = 2r^2 + \frac{1}{2} \ln r$
$a = \frac{4r^2 + \ln r}{4r}$
Thus, the $x$-coordinate of $Q$ is $\frac{4r^2 + \ln r}{4r}$.
(b) Let $A$ square units be the area of $\Delta PQR$.
$A = \frac{1}{2} \left( \frac{4r^2 + \ln r}{4r} - r \right) \ln \sqrt{r}$
$= \frac{(\ln r)^2}{16r}$
$\frac{dA}{dr}$
$= \frac{r(2 \ln r) \frac{1}{r} - (\ln r)^2}{16r^2}$
$= \frac{2 \ln r - (\ln r)^2}{16r^2}$
$= \frac{(2 - \ln r) \ln r}{16r^2}$
So, we have $\frac{dA}{dr} = 0 \iff \ln r = 2$ or $\ln r = 0$ (rejected).
Hence, we have $\frac{dA}{dr} = 0 \iff r = e^2$.
$r$
$\frac{dA}{dr}$
$A$
Therefore, $A$ attains its greatest value when $r = e^2$.
Thus, the greatest area of $\Delta PQR$ is $\frac{1}{4e^2}$ square units.
(c) $OP = \sqrt{r^2 + (\ln \sqrt{r})^2} = \frac{1}{2} \sqrt{4r^2 + (\ln r)^2}$
$\frac{dOP}{dt} = \left( \frac{4r^2 + \ln r}{2r \sqrt{4r^2 + (\ln r)^2}} \right) \left( \frac{dr}{dt} \right)$
$\frac{dA}{dt} = \left( \frac{dA}{dr} \right) \left( \frac{dr}{dt} \right)$
$= \left( \frac{(2 - \ln r) \ln r}{16r^2} \right) \left( \frac{dr}{dt} \right)$ (by (b))
$= \left( \frac{(2 - \ln r) \ln r}{16r^2} \right) \left( \frac{2r \sqrt{4r^2 + (\ln r)^2}}{4r^2 + \ln r} \right) \left( \frac{dOP}{dt} \right)$
$= \frac{(2 - \ln r)(\ln r) \sqrt{4r^2 + (\ln r)^2}}{8r(4r^2 + \ln r)} \left( \frac{dOP}{dt} \right)$
$\left. \frac{dA}{dt} \right|_{r=e}$
$= \frac{(2 - \ln e)(\ln e) \sqrt{4e^2 + (\ln e)^2}}{8e(4e^2 + \ln e)} \left( \frac{dOP}{dt} \right|_{r=e}$
$= \frac{\sqrt{4e^2 + 1}}{8e(4e^2 + 1)} \left( \frac{dOP}{dt} \right|_{r=e}$
Since $0 \leq \frac{dOP}{dt} \bigg|_{r=e} \leq 32e^2$, we have $0 \leq \frac{dA}{dt} \bigg|_{r=e} \leq \frac{32e^2 \sqrt{4e^2 + 1}}{8e(4e^2 + 1)}$.
So, we have $0 \leq \frac{dA}{dt} \bigg|_{r=e} \leq \frac{4e}{\sqrt{4e^2 + 1}}$.
Therefore, we have $0 \leq \frac{dA}{dt} \bigg|_{r=e} < \frac{4e}{\sqrt{4e^2}}$.
Hence, we have $0 \leq \frac{dA}{dt} \bigg|_{r=e} < 2$.
Thus, the claim is correct.

## 第 10 題  <!-- 頁 [10, 11]｜13/13（題目卷為準；MS 讀到 subtotals=[5, 3] cells=16） -->

Marks: 1M 1 1M 1M 1A 1M 1M 1A 1M 1 1M 1M 1M 1M 1M 1A

10. (a) (i) $\int \sin^4 x \, dx$ $= -\cos x \sin^3 x + \int \cos x (3 \sin^2 x \cos x) \, dx$ $= -\cos x \sin^3 x + 3 \int (1 - \sin^2 x) (\sin^2 x) \, dx$
So, we have $\int \sin^4 x \, dx = -\cos x \sin^3 x + 3 \int \sin^2 x \, dx - 3 \int \sin^4 x \, dx$. Hence, we have $4 \int \sin^4 x \, dx = -\cos x \sin^3 x + 3 \int \sin^2 x \, dx$.
Thus, we have $\int \sin^4 x \, dx = \frac{-\cos x \sin^3 x}{4} + \frac{3}{4} \int \sin^2 x \, dx$.
(ii) $\int \sin^4 x \, dx$ $= \frac{-\cos x \sin^3 x}{4} + \frac{3}{4} \int \sin^2 x \, dx$ (by (a)(i))
$= \frac{-\cos x \sin^3 x}{4} + \frac{3}{4} \int \frac{1 - \cos 2x}{2} \, dx$
$= \frac{-\cos x \sin^3 x}{4} + \frac{3}{4} \left( \frac{x}{2} - \frac{\sin 2x}{4} \right) + \text{constant}$
$= \frac{3x}{8} - \frac{\cos x \sin^3 x}{4} - \frac{3 \sin 2x}{16} + \text{constant}$
$\int_0^{\pi} \sin^4 x \, dx$
$= \left[ \frac{3x}{8} - \frac{\cos x \sin^3 x}{4} - \frac{3 \sin 2x}{16} \right]_0^{\pi}$
$= \frac{3\pi}{8}$
$\int_0^{\pi} \sin^4 x \, dx$
$= \int_0^{\pi} \left( \frac{1 - \cos 2x}{2} \right)^2 \, dx$
$= \frac{1}{4} \int_0^{\pi} (1 - 2 \cos 2x + \cos^2 2x) \, dx$
$= \frac{1}{4} \int_0^{\pi} \left( 1 - 2 \cos 2x + \frac{1 + \cos 4x}{2} \right) \, dx$
$= \frac{1}{8} \int_0^{\pi} (3 - 4 \cos 2x + \cos 4x) \, dx$
$= \frac{1}{8} \left[ 3x - 2 \sin 2x + \frac{\sin 4x}{4} \right]_0^{\pi}$
$= \frac{3\pi}{8}$
(b) (i) Let $x = \beta - u$. Then, we have $\frac{dx}{du} = -1$.
$$\int_{0}^{\beta} x f(x) dx$$
$$= \int_{0}^{0} -(\beta - u) f(\beta - u) du$$
$$= \int_{0}^{\beta} (\beta f(\beta - u) - u f(\beta - u)) du$$
$$= \int_{0}^{\beta} \beta f(x) dx - \int_{0}^{\beta} x f(x) dx$$
So, we have $2 \int_{0}^{\beta} x f(x) dx = \beta \int_{0}^{\beta} f(x) dx$.
Thus, we have $\int_{0}^{\beta} x f(x) dx = \frac{\beta}{2} \int_{0}^{\beta} f(x) dx$.
(ii) Note that $\sin^{4}(\pi - x) = \sin^{4}x$ for all real numbers $x$.
$$\int_{0}^{\pi} x \sin^{4}x dx$$
$$= \frac{\pi}{2} \int_{0}^{\pi} \sin^{4}x dx$$
$$= \frac{\pi}{2} \left( \frac{3\pi}{8} \right)$$
$$= \frac{3\pi^{2}}{16}$$
(c) The required volume
$$= \int_{0}^{2\pi} \pi (\sqrt{x} \sin^{2}x)^{2} dx$$
$$= \pi \int_{0}^{2\pi} x \sin^{4}x dx$$
$$= \pi \int_{0}^{\pi} (\pi + y) \sin^{4}(\pi + y) dy$$
$$= \pi \int_{0}^{\pi} (\pi \sin^{4}y + y \sin^{4}y) dy$$
$$= \pi \int_{0}^{\pi} (\pi \sin^{4}x + x \sin^{4}x) dx$$
$$= \pi \left( \pi \int_{0}^{\pi} \sin^{4}x dx + \int_{0}^{\pi} x \sin^{4}x dx \right)$
$$= \pi \left( \pi \left( \frac{3\pi}{8} \right) + \frac{3\pi^{2}}{16} \right)$
$$= \frac{9\pi^{3}}{16}$$

## 第 11 題  <!-- 頁 [12]｜12/12（題目卷為準；MS 讀到 subtotals=無 cells=8） -->

Marks: 1A 1M 1A 1M 1A 1M 1A+1A

11. (a) (i) (1) Note that $$\begin{vmatrix} 1 & a & 4(a+1) \\ 2 & a-1 & 2(a-1) \\ 1 & -1 & -12 \end{vmatrix} = (a-1)(-12) + a(2)(a-1) + 4(a+1)(2)(-1) - 4(a-1)(a+1) + 2(a-1) - 2a(-12) = -2(a-3)(a+1)$$
Since $(E)$ has a unique solution, we have $\begin{vmatrix} 1 & a & 4(a+1) \\ 2 & a-1 & 2(a-1) \\ 1 & -1 & -12 \end{vmatrix} \neq 0$.
So, we have $-2(a-3)(a+1) \neq 0$. Therefore, we have $a \neq 3$ and $a \neq -1$. Thus, we have $a 3$.
The augmented matrix of $(E)$ is $$\begin{pmatrix} 1 & a & 4(a+1) \\ 2 & a-1 & 2(a-1) \\ 1 & -1 & -12 \end{pmatrix} \sim \begin{pmatrix} 1 & a & 4(a+1) \\ 0 & -a-1 & -6a-10 \\ 0 & -a-1 & -4a-16 \end{pmatrix} \sim \begin{pmatrix} 1 & a & 4(a+1) \\ 0 & -a-1 & -6a-10 \\ 0 & 0 & 2a-6 \end{pmatrix}$$
Since $(E)$ has a unique solution, we have $2a-6 \neq 0$ and $-a-1 \neq 0$. Therefore, we have $a \neq 3$ and $a \neq -1$. Thus, we have $a 3$.
(2) Since $(E)$ has a unique solution, we have $$x = \frac{18a + 4(a+1)}{-2(a-3)(a+1)} = \frac{a^2b + ab + 10a - 2b - 50}{(a-3)(a+1)}$$
y = \frac{18a + 4(a+1)}{-2(a-3)(a+1)} = \frac{-3ab + 22a - 5b - 38}{(a-3)(a+1)}$
z = \frac{18a + 4(a+1)}{-2(a-3)(a+1)} = \frac{b-2}{2(a-3)}$

## 第 12 題  <!-- 頁 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]｜13/13（題目卷為準；MS 讀到 subtotals=無 cells=8） -->

Marks: 1A 1M 1A 1M 1A 1M 1A+1A

11. (a) (i) (1) Note that $$\begin{vmatrix} 1 & a & 4(a+1) \\ 2 & a-1 & 2(a-1) \\ 1 & -1 & -12 \end{vmatrix} = (a-1)(-12) + a(2)(a-1) + 4(a+1)(2)(-1) - 4(a-1)(a+1) + 2(a-1) - 2a(-12) = -2(a-3)(a+1)$$
Since $(E)$ has a unique solution, we have $\begin{vmatrix} 1 & a & 4(a+1) \\ 2 & a-1 & 2(a-1) \\ 1 & -1 & -12 \end{vmatrix} \neq 0$.
So, we have $-2(a-3)(a+1) \neq 0$. Therefore, we have $a \neq 3$ and $a \neq -1$. Thus, we have $a 3$.
The augmented matrix of $(E)$ is $$\begin{pmatrix} 1 & a & 4(a+1) \\ 2 & a-1 & 2(a-1) \\ 1 & -1 & -12 \end{pmatrix} \sim \begin{pmatrix} 1 & a & 4(a+1) \\ 0 & -a-1 & -6a-10 \\ 0 & -a-1 & -4a-16 \end{pmatrix} \sim \begin{pmatrix} 1 & a & 4(a+1) \\ 0 & -a-1 & -6a-10 \\ 0 & 0 & 2a-6 \end{pmatrix}$$
Since $(E)$ has a unique solution, we have $2a-6 \neq 0$ and $-a-1 \neq 0$. Therefore, we have $a \neq 3$ and $a \neq -1$. Thus, we have $a 3$.
(2) Since $(E)$ has a unique solution, we have $$x = \frac{18a + 4(a+1)}{-2(a-3)(a+1)} = \frac{a^2b + ab + 10a - 2b - 50}{(a-3)(a+1)}$$
y = \frac{18a + 4(a+1)}{-2(a-3)(a+1)} = \frac{-3ab + 22a - 5b - 38}{(a-3)(a+1)}$
z = \frac{18a + 4(a+1)}{-2(a-3)(a+1)} = \frac{b-2}{2(a-3)}$


**合計 100 / 100**
