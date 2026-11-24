# 2021 M2 Paper 1 — 評卷參考（分題）

> 分題依據：MS 題號行 + marks 對題目卷分數 [4, 5, 6, 6, 7, 7, 7, 8, 12, 13, 12, 13]｜合計 100

## 第 1 題  <!-- 頁 [3]｜4/4（MS 小計） -->

Marks: 1M 1M 1M 1M 1A

1. f'(x)
$$= \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$
$$= \lim_{h \to 0} \frac{\frac{1}{3(x+h)^2 + 4} - \frac{1}{3x^2 + 4}}{h}$$
$$= \lim_{h \to 0} \frac{(3x^2 + 4) - (3(x+h)^2 + 4)}{h(3(x+h)^2 + 4)(3x^2 + 4)}$$
$$= \lim_{h \to 0} \frac{-3h(2x+h)}{h(3(x+h)^2 + 4)(3x^2 + 4)}$$
$$= \lim_{h \to 0} \frac{-3(2x+h)}{(3(x+h)^2 + 4)(3x^2 + 4)}$$
$$= \frac{-6x}{(3x^2 + 4)^2}$$

## 第 2 題  <!-- 頁 [3]｜5/5（題目卷為準；MS 讀到 subtotals=無 cells=5） -->

Marks: 1 1M 1M 1M 1

2. Note that $\sum_{k=1}^{1} (3k^5 + k^3) = 4 = \frac{1^3(1+1)^3}{2}$.
Therefore, the statement is true for $n=1$.
Assume that $\sum_{k=1}^{m} (3k^5 + k^3) = \frac{m^3(m+1)^3}{2}$, where $m$ is a positive integer.
$$\sum_{k=1}^{m+1} (3k^5 + k^3)$$
$$= \sum_{k=1}^{m} (3k^5 + k^3) + 3(m+1)^5 + (m+1)^3$$
$$= \frac{m^3(m+1)^3}{2} + 3(m+1)^5 + (m+1)^3$$
$$= \frac{m^3(m+1)^3 + 6(m+1)^5 + 2(m+1)^3}{2}$$
$$= \frac{(m+1)^3(m^3 + 6(m+1)^2 + 2)}{2}$$
$$= \frac{(m+1)^3(m^3 + 6m^2 + 12m + 8)}{2}$$
$$= \frac{(m+1)^3(m+2)^3}{2}$$
So, the statement is true for $n=m+1$ if it is true for $n=m$.
By mathematical induction, the statement is true for all positive integers $n$.

## 第 3 題  <!-- 頁 [4]｜6/6（MS 小計） -->

Marks: 1M 1M 1A 1M 1M 1A

3. (a) $(1-4x)^n$
$= 1-n(4x) + \frac{n(n-1)}{2}(4x)^2 - \cdots + (-1)^n(4x)^n$
$\frac{n(n-1)}{2}(4^2) = 240$
$n^2 - n - 30 = 0$
$n = 6$ or $n = -5$ (rejected)
Thus, we have $n = 6$.
(b) $\left(1 + \frac{2}{x}\right)^5$
$= 1 + 5\left(\frac{2}{x}\right) + 10\left(\frac{2}{x}\right)^2 + 10\left(\frac{2}{x}\right)^3 + 5\left(\frac{2}{x}\right)^4 + \left(\frac{2}{x}\right)^5$
$= 1 + \frac{10}{x} + \frac{40}{x^2} + \frac{80}{x^3} + \frac{80}{x^4} + \frac{32}{x^5}$
$(1-4x)^6$
$= 1-6(4x) + 15(4x)^2 - 20(4x)^3 + 15(4x)^4 - 6(4x)^5 + (4x)^6$
$= 1-24x + 240x^2 - 1280x^3 + 3840x^4 - 6144x^5 + 4096x^6$
The coefficient of $x^4$
$= (1)(3840) + (10)(-6144) + (40)(4096)$
$= 106240$

## 第 4 題  <!-- 頁 [4]｜6/6（MS 小計） -->

Marks: 1M 1M 1 1M 1M 1A

4. (a) $\cos 2x + \cos 4x + \cos 6x$
$= 2\cos^2 x - 1 + \cos 4x + \cos 6x$
$= 2\cos^2 x - 1 + 2\cos 5x\cos x$
$= 2\cos x(\cos x + \cos 5x) - 1$
$= 2\cos x(2\cos 3x\cos 2x) - 1$
$= 4\cos x\cos 2x\cos 3x - 1$
(b) $\cos 4\theta + \cos 8\theta + \cos 12\theta = -1$
$4\cos 2\theta\cos 4\theta\cos 6\theta - 1 = -1$ (by putting $x = 2\theta$ in (a))
$\cos 2\theta\cos 4\theta\cos 6\theta = 0$
$\cos 2\theta = 0$, $\cos 4\theta = 0$ or $\cos 6\theta = 0$
$\theta = \frac{\pi}{12}$, $\theta = \frac{\pi}{8}$, $\theta = \frac{\pi}{4}$, $\theta = \frac{3\pi}{8}$ or $\theta = \frac{5\pi}{12}$

## 第 5 題  <!-- 頁 [5]｜7/7（題目卷為準；MS 讀到 subtotals=無 cells=4） -->

Marks: 1A 1M 1A 1M

5. (a) The equation of the vertical asymptote is $x-1=0$. Note that $r(x)=x+1-\frac{x-2}{(x-1)^2}$. Thus, the equation of the oblique asymptote is $y=x+1$.
1M
1A
(b) $\frac{d}{dx}r(x)$ = $\frac{d}{dx}\left(x+1-\frac{x-2}{(x-1)^2}\right)$ = $1-\frac{(x-1)^2-2(x-2)(x-1)}{(x-1)^4}$ = $1+\frac{x-3}{(x-1)^3}$
1M
1A
(c) Note that $\frac{d^2}{dx^2}r(x)=\frac{(x-1)^3-3(x-1)^2(x-3)}{(x-1)^6}=\frac{-2(x-4)}{(x-1)^4}$. So, we have $\frac{d^2}{dx^2}r(x)=0 \iff x=4$.
1M
1A
Therefore, there is only one point of inflexion of the graph of $y=r(x)$. Thus, the claim is agreed.

## 第 6 題  <!-- 頁 [6]｜7/7（MS 小計） -->

Marks: 1M 1M 1A 1M+1A 1M 1A

6. (a) $y = e^{2x-6}$
$\frac{dy}{dx} = 2e^{2x-6}$
$\frac{dy}{dx}|_{x=3} = 2e^{2(3)-6} = 2$
The equation of $L$ is
$y-1 = \frac{-1}{2}(x-3)$
$x+2y-5 = 0$
Putting $x = c$ and $y = 0$ in $x+2y-5 = 0$, we have $c+2(0)-5 = 0$.
Thus, we have $c = 5$.
(b) The required area
$= \int_{3}^{5} \left(e^{2x-6} - \left(\frac{-x}{2} + \frac{5}{2}\right)\right) dx$
$= \int_{3}^{5} \left(e^{2x-6} + \frac{x}{2} - \frac{5}{2}\right) dx$
$= \left[ \frac{e^{2x-6}}{2} + \frac{x^2}{4} - \frac{5x}{2} \right]_{3}^{5}$
$= \frac{e^4-3}{2}$

## 第 7 題  <!-- 頁 [6]｜7/7（題目卷為準；MS 讀到 subtotals=無 cells=7） -->

Marks: 1M 1M 1A 1M 1M 1M 1A

7. (a) $\int (\ln x)^2 dx$
$= x(\ln x)^2 - \int x\left(\frac{2\ln x}{x}\right) dx$
$= x(\ln x)^2 - 2\left(x\ln x - \int x\left(\frac{1}{x}\right) dx\right)$
$= x(\ln x)^2 - 2x\ln x + 2x + \text{constant}$
(b) The required volume
$= \int_{0}^{1} \pi \left(\sqrt{x} \ln(x^2+1)\right)^2 dx$
$= \pi \int_{0}^{1} x\left(\ln(x^2+1)\right)^2 dx$
$= \frac{\pi}{2} \int_{1}^{2} (\ln u)^2 du$
$= \frac{\pi}{2} \left[ u(\ln u)^2 - 2u\ln u + 2u \right]_{1}^{2}$
$= \pi \left((\ln 2)^2 - 2\ln 2 + 1\right)$

## 第 8 題  <!-- 頁 [7]｜8/8（題目卷為準；MS 讀到 subtotals=無 cells=7） -->

Marks: 1M 1M 1M 1M 1A 1A 1M

8. (a) Note that $$\begin{vmatrix} 1 & d-1 & d+3 \\ 2 & d+2 & -1 \\ 3 & d+4 & 5 \end{vmatrix}=5(d+2)+2(d+4)(d+3)+3(-1)(d-1)-3(d+2)(d+3)-10(d-1)-(-1)(d+4)=-d^{2}-8d+33$$
As $(E)$ has infinitely many solutions, we have $$\begin{vmatrix} 1 & d-1 & d+3 \\ 2 & d+2 & -1 \\ 3 & d+4 & 5 \end{vmatrix}=0.$$
So, we have $-d^{2}-8d+33=0$. Solving, we have $d=-11$ or $d=3$.
When $d=-11$, the augmented matrix of $(E)$ is $$\begin{pmatrix} 1 & -12 & -8 & 15 \\ 2 & -9 & -1 & -27 \\ 3 & -7 & 5 & 2 \end{pmatrix}\sim\begin{pmatrix} 1 & -12 & -8 & 15 \\ 0 & -15 & -15 & 57 \\ 0 & -29 & -29 & 43 \end{pmatrix}\sim\begin{pmatrix} 1 & -12 & -8 & 15 \\ 0 & -15 & -15 & 57 \\ 0 & 0 & 0 & 1 \end{pmatrix}$$
Since $(E)$ is consistent, we have $d\neq-11$.
Therefore, we have $d=3$.
Hence, the augmented matrix of $(E)$ is $$\begin{pmatrix} 1 & 2 & 6 & 1 \\ 2 & 5 & -1 & 1 \\ 3 & 7 & 5 & 2 \end{pmatrix}\sim\begin{pmatrix} 1 & 2 & 6 & 1 \\ 0 & -1 & 13 & 1 \\ 0 & -1 & 13 & 1 \end{pmatrix}\sim\begin{pmatrix} 1 & 2 & 6 & 1 \\ 0 & -1 & 13 & 1 \\ 0 & 0 & 0 & 0 \end{pmatrix}$$
Thus, the solution set of $(E)$ is $\{(3-32t, 13t-1, t): t\in\mathbb{R}\}$.
(b) Putting $x=3-32t$, $y=13t-1$ and $z=t$ in $xy+2xz=3$, we have $(3-32t)(13t-1)+2(3-32t)t=3$. Therefore, we have $-480t^{2}+77t-6=0$. Note that $77^{2}-4(-480)(-6)=-5591&lt;0$. So, $(E)$ does not have a real solution $(x,y,z)$ satisfying $xy+2xz=3$. Thus, the claim is not correct.

## 第 9 題  <!-- 頁 [8, 9]｜12/12（題目卷為準；MS 讀到 subtotals=無 cells=16） -->

Marks: 1A 1A 1M 1M 1M 1M 1M 1M 1M 1M 1M 1M 1M 1M 1M 1A

9. (a) (i) $\frac{d}{d\theta}\ln(\sec\theta + \tan\theta)$ $= \left( \frac{1}{\sec\theta + \tan\theta} \right)(\sec\theta\tan\theta + \sec^2\theta)$ $= \sec\theta$
(ii) By (a)(i), we have $\frac{d}{d\theta}\ln(\sec\theta + \tan\theta) = \sec\theta$. So, we have $\int\sec\theta d\theta = \ln(\sec\theta + \tan\theta) + \text{constant}$. $\int\sec^3\theta d\theta = \sec\theta\tan\theta - \int\tan^2\theta\sec\theta d\theta$ $\int\sec^3\theta d\theta = \sec\theta\tan\theta - \int(\sec^2\theta - 1)\sec\theta d\theta$ $2\int\sec^3\theta d\theta = \sec\theta\tan\theta + \int\sec\theta d\theta$ $\int\sec^3\theta d\theta = \frac{1}{2}(\sec\theta\tan\theta + \ln(\sec\theta + \tan\theta)) + \text{constant}$
(b) Note that $\int_{-a}^{a} g(x)h(x)dx = -\int_{a}^{-a} g(-x)h(-x)dx = \int_{-a}^{a} g(-x)h(x)dx$.
$\int_{-a}^{a} g(x)h(x)dx$ $= \frac{1}{2}\left(\int_{-a}^{a} g(x)h(x)dx + \int_{-a}^{a} g(x)h(x)dx\right)$ $= \frac{1}{2}\left(\int_{-a}^{a} g(x)h(x)dx + \int_{-a}^{a} g(-x)h(x)dx\right)$ $= \frac{1}{2}\int_{-a}^{a}(g(x) + g(-x))h(x)dx$ $= \frac{1}{2}\int_{-a}^{a}h(x)dx$ $= \frac{1}{2}\left(\int_{-a}^{0}h(x)dx + \int_{0}^{a}h(x)dx\right)$ $= \frac{1}{2}\left(-\int_{a}^{0}h(-y)dy + \int_{0}^{a}h(x)dx\right)$ (by letting $x = -y$) $= \frac{1}{2}\left(\int_{0}^{a}h(-x)dx + \int_{0}^{a}h(x)dx\right)$ $= \frac{1}{2}\left(\int_{0}^{a}h(x)dx + \int_{0}^{a}h(x)dx\right)$ $= \frac{1}{2}\left(2\int_{0}^{a}h(x)dx\right)$ $= \int_{0}^{a}h(x)dx$
$(c) \text{ Let } g(x) = \frac{3^x}{3^x + 3^{-x}} \text{ and } h(x) = \frac{x^2}{\sqrt{x^2 + 1}} \text{ for all } x \in \mathbf{R}.$
Note that $g(x) + g(-x) = \frac{3^x}{3^x + 3^{-x}} + \frac{3^{-x}}{3^{-x} + 3^{-(-x)}} = 1$ and $h(-x) = h(x).$
$\int_{-1}^{1} \frac{3^x x^2}{(3^x + 3^{-x})\sqrt{x^2 + 1}} \mathrm{d}x$
$= \int_{-1}^{1} g(x)h(x) \mathrm{d}x$
$= \int_{0}^{1} h(x) \mathrm{d}x$ (by putting $a = 1$ in (b))
$= \int_{0}^{1} \frac{x^2}{\sqrt{x^2 + 1}} \mathrm{d}x$
$= \int_{0}^{\frac{\pi}{4}} \frac{\tan^2 \theta \sec^2 \theta}{\sqrt{\tan^2 \theta + 1}} \mathrm{d}\theta$ (by letting $x = \tan \theta$)
$= \int_{0}^{\frac{\pi}{4}} \tan^2 \theta \sec \theta \mathrm{d}\theta$
$= \int_{0}^{\frac{\pi}{4}} (\sec^3 \theta - \sec \theta) \mathrm{d}\theta$
$= \int_{0}^{\frac{\pi}{4}} \sec^3 \theta \mathrm{d}\theta - \int_{0}^{\frac{\pi}{4}} \sec \theta \mathrm{d}\theta$
$= \left[ \frac{1}{2} (\sec \theta \tan \theta + \ln(\sec \theta + \tan \theta)) \right]_{0}^{\frac{\pi}{4}} - \left[ \ln(\sec \theta + \tan \theta) \right]_{0}^{\frac{\pi}{4}}$ (by (a)(ii))
$= \frac{1}{2} \left( \sqrt{2} - \ln(\sqrt{2} + 1) \right)$

## 第 10 題  <!-- 頁 [10]｜13/13（MS 小計之和） -->

Marks: 1M 1M 1A 1M 1M 1M 1A 1M 1M 1M 1M 1M 1M 1A

10. (a) $PQ = \sqrt{u^2 + 36} + \sqrt{(20 - u)^2 + 16}$ $\frac{dPQ}{du} = \frac{u}{\sqrt{u^2 + 36}} - \frac{20 - u}{\sqrt{(20 - u)^2 + 16}}$ $= \frac{u\sqrt{(20 - u)^2 + 16} - (20 - u)\sqrt{u^2 + 36}}{\sqrt{u^2 + 36}\sqrt{(20 - u)^2 + 16}}$ $= \frac{-20(u - 12)(u - 60)}{\sqrt{u^2 + 36}\sqrt{(20 - u)^2 + 16} \left( u\sqrt{(20 - u)^2 + 16} + (20 - u)\sqrt{u^2 + 36} \right)}$
For $\frac{dPQ}{du} = 0$, we have $u = 12$.
Thus, we have $a = 12$.
(b) (i) Let $A$ square units be the area of the rectangle $PQSR$. Then, we have $A = u\left(\sqrt{u^2 + 36} + \sqrt{(20 - u)^2 + 16}\right)$.
$\frac{dA}{du} = u\left(\frac{u}{\sqrt{u^2 + 36}} - \frac{20 - u}{\sqrt{(20 - u)^2 + 16}}\right) + \sqrt{u^2 + 36} + \sqrt{(20 - u)^2 + 16}$
Therefore, we have $\left.\frac{dA}{du}\right|_{u=12} = 10\sqrt{5} \neq 0$.
Hence, $A$ does not attain its minimum value when $u = 12$. Thus, the claim is disagreed.
(ii) Since $OP = \sqrt{u^2 + u^2 + 36}$, we have $OP = \sqrt{2u^2 + 36}$.
At time $t$ minutes, we have $\frac{dOP}{dt} = \frac{2u}{\sqrt{2u^2 + 36}}\left(\frac{du}{dt}\right)$.
As $28 = \frac{2(12)}{\sqrt{2(12^2) + 36}}\left(\frac{du}{dt}\right|_{u=12}\right)$, we have $\frac{du}{dt}|_{u=12} = 21$.
Let $w$ units be the perimeter of the rectangle $PQSR$. Then, we have $w = 2\left(u + \sqrt{u^2 + 36} + \sqrt{(20 - u)^2 + 16}\right)$.
Therefore, we have $\frac{dw}{dt} = 2\left(1 + \frac{u}{\sqrt{u^2 + 36}} - \frac{(20 - u)}{\sqrt{(20 - u)^2 + 16}}\right)\frac{du}{dt}$.
$\frac{dw}{dt}|_{u=12} = 2\left(1 + \frac{12}{\sqrt{180}} - \frac{8}{\sqrt{80}}\right)(21)$
= 42
Thus, the required rate of change is 42 units per minute.

## 第 11 題  <!-- 頁 [11, 12]｜12/12（題目卷為準；MS 讀到 subtotals=無 cells=36） -->

Marks: 1A 1M 1 1 1 1M 1M 1A 1A 1M 1M 1M 1M 1M 1M 1M 1M 1 1M 1M 1M 1A 1A 1A 1M 1M 1M 1M 1M 1M 1A 1M 1A 1A 1A 1A

11. (a) Note that $P^{-1} = \begin{pmatrix} \sin \theta & -\cos \theta \\ \cos \theta & \sin \theta \end{pmatrix}$.
$PAP^{-1} = \begin{pmatrix} \sin \theta & \cos \theta \\ -\cos \theta & \sin \theta \end{pmatrix} \begin{pmatrix} \alpha & \beta \\ \beta & -\alpha \end{pmatrix} \begin{pmatrix} \sin \theta & -\cos \theta \\ \cos \theta & \sin \theta \end{pmatrix}$
$= \begin{pmatrix} \alpha \sin \theta + \beta \cos \theta & \beta \sin \theta - \alpha \cos \theta \\ -\alpha \cos \theta + \beta \sin \theta & -\beta \cos \theta - \alpha \sin \theta \end{pmatrix} \begin{pmatrix} \sin \theta & -\cos \theta \\ \cos \theta & \sin \theta \end{pmatrix}$
$= \begin{pmatrix} \alpha \sin^2 \theta + 2\beta \sin \theta \cos \theta - \alpha \cos^2 \theta & -2\alpha \sin \theta \cos \theta - \beta \cos^2 \theta + \beta \sin^2 \theta \\ -2\alpha \sin \theta \cos \theta - \beta \cos^2 \theta + \beta \sin^2 \theta & -\alpha \sin^2 \theta - 2\beta \sin \theta \cos \theta + \alpha \cos^2 \theta \end{pmatrix}$
$= \begin{pmatrix} -\alpha \cos 2\theta + \beta \sin 2\theta & -\beta \cos 2\theta - \alpha \sin 2\theta \\ -\beta \cos 2\theta - \alpha \sin 2\theta & \alpha \cos 2\theta - \beta \sin 2\theta \end{pmatrix}$
(b) (i) By (a), we have $PBP^{-1} = \begin{pmatrix} -\cos 2\theta + \sqrt{3} \sin 2\theta & -\sqrt{3} \cos 2\theta - \sin 2\theta \\ -\sqrt{3} \cos 2\theta - \sin 2\theta & \cos 2\theta - \sqrt{3} \sin 2\theta \end{pmatrix}$.
For $PBP^{-1} = \begin{pmatrix} \lambda & 0 \\ 0 & \mu \end{pmatrix}$, we have $-\sqrt{3} \cos 2\theta - \sin 2\theta = 0$.
So, we have $\tan 2\theta = -\sqrt{3}$.
Since $\frac{\pi}{2} < \theta < \pi$, we have $\theta = \frac{5\pi}{6}$.
(ii) Since $\theta = \frac{5\pi}{6}$, we have $\lambda = -2$ and $\mu = 2$.
So, we have $PBP^{-1} = \begin{pmatrix} -2 & 0 \\ 0 & 2 \end{pmatrix}$.
Therefore, we have $B = P^{-1} \begin{pmatrix} -2 & 0 \\ 0 & 2 \end{pmatrix} P$.
$B^n = \begin{pmatrix} P^{-1} \begin{pmatrix} -2 & 0 \\ 0 & 2 \end{pmatrix} P \end{pmatrix}^n$
$= P^{-1} \begin{pmatrix} -2 & 0 \\ 0 & 2 \end{pmatrix}^n P$
$= P^{-1} \begin{pmatrix} (-2)^n & 0 \\ 0 & 2^n \end{pmatrix} P$
$= \begin{pmatrix} \frac{1}{2} & \frac{\sqrt{3}}{2} \\ \frac{-\sqrt{3}}{2} & \frac{1}{2} \end{pmatrix} \begin{pmatrix} (-2)^n & 0 \\ 0 & 2^n \end{pmatrix} \begin{pmatrix} \frac{1}{2} & \frac{-\sqrt{3}}{2} \\ \frac{\sqrt{3}}{2} & \frac{1}{2} \end{pmatrix}$
$= \frac{1}{4} \begin{pmatrix} (-1)^n 2^n & \sqrt{3} (2^n) \\ \sqrt{3} (-1)^{n+1} 2^n & 2^n \end{pmatrix} \begin{pmatrix} 1 & -\sqrt{3} \\ \sqrt{3} & 1 \end{pmatrix}$
$= 2^{n-2} \begin{pmatrix} (-1)^n + 3 & \sqrt{3} (-1)^{n+1} + \sqrt{3} \\ \sqrt{3} (-1)^{n+1} + \sqrt{3} & 3 (-1)^n + 1 \end{pmatrix}$
$$B^{555} = 2^{555-2} \begin{pmatrix} (-1)^{555} + 3 & \sqrt{3} (-1)^{556} + \sqrt{3} \\ \sqrt{3} (-1)^{556} + \sqrt{3} & 3 (-1)^{555} + 1 \end{pmatrix} \quad (\text{by (b)(ii)})$$
$$2^{553} \begin{pmatrix} 2 & 2\sqrt{3} \\ 2\sqrt{3} & -2 \end{pmatrix}$$
$$(B^{-1})^{555} = (B^{555})^{-1}$$
$$= \frac{1}{2^{553}} \begin{pmatrix} 2 & 2\sqrt{3} \\ 2\sqrt{3} & -2 \end{pmatrix}^{-1}$$
$$= \frac{1}{2^{553}} \begin{pmatrix} \frac{1}{8} & \frac{\sqrt{3}}{8} \\ \frac{\sqrt{3}}{8} & \frac{-1}{8} \end{pmatrix}$$
$$= \frac{1}{2^{556}} \begin{pmatrix} 1 & \sqrt{3} \\ \sqrt{3} & -1 \end{pmatrix}$$
$$B = \begin{pmatrix} 1 & \sqrt{3} \\ \sqrt{3} & -1 \end{pmatrix}$$
$$B^{2} = \begin{pmatrix} 1 & \sqrt{3} \\ \sqrt{3} & -1 \end{pmatrix} \begin{pmatrix} 1 & \sqrt{3} \\ \sqrt{3} & -1 \end{pmatrix} = 4 \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} = 2^{2} I$$
$$B^{4} = (B^{2})^{2} = (2^{2} I)^{2} = 2^{4} I$$
$$B^{6} = 2^{6} I$$
$$B^{554} = 2^{554} I$$
$$B^{-1} = \frac{1}{-4} \begin{pmatrix} -1 & -\sqrt{3} \\ -\sqrt{3} & 1 \end{pmatrix}$$
$$= \begin{pmatrix} \frac{1}{4} & \frac{\sqrt{3}}{4} \\ \frac{\sqrt{3}}{4} & \frac{-1}{4} \end{pmatrix}$$
$$(B^{-1})^{555} = (B^{555})^{-1}$$
$$= (B(B^{554}))^{-1}$$
$$= (2^{554} B)^{-1}$$
$$= \frac{1}{2^{554}} B^{-1}$$
$$= \frac{1}{2^{556}} \begin{pmatrix} 1 & \sqrt{3} \\ \sqrt{3} & -1 \end{pmatrix}$$

## 第 12 題  <!-- 頁 [13]｜13/13（題目卷為準；MS 讀到 subtotals=無 cells=5） -->

Marks: 1M 1M 1M 1M 1M

12. (a) (i) Note that $\overrightarrow{AB} = (12 - t)\mathbf{i} - (s + 14)\mathbf{j} - (2 + s)\mathbf{k}$. Since $\overrightarrow{AB}$ is parallel to $5\mathbf{i} - 4\mathbf{j} - 2\mathbf{k}$, we have $\frac{12 - t}{5} = \frac{-(s + 14)}{-4} = \frac{-(2 + s)}{-2}$. Solving, we have $s = 10$ and $t = -18$.
(ii) Note that $\overrightarrow{AB} \times \overrightarrow{AC} = \begin{vmatrix} i & j & k \\ 30 & -24 & -12 \\ 30 & -30 & 0 \end{vmatrix} = -360\mathbf{i} - 360\mathbf{j} - 180\mathbf{k}$. The area of $\Delta ABC$ is $\frac{1}{2}|\overrightarrow{AB} \times \overrightarrow{AC}| = \frac{1}{2}\sqrt{360^2 + 360^2 + 180^2} = 270$.
(iii) Note that $\overrightarrow{AD} = 36\mathbf{i} - 2\mathbf{j} + 4\mathbf{k}$. The required volume is $\frac{1}{6}|\overrightarrow{AB} \times \overrightarrow{AC}| \cdot \overrightarrow{AD}| = \frac{1}{6}|(-360\mathbf{i} - 360\mathbf{j} - 180\mathbf{k}) \cdot (36\mathbf{i} - 2\mathbf{j} + 4\mathbf{k})| = \frac{1}{6}|(-360)(36) + (-360)(-2) + (-180)(4)| = \frac{1}{6}|-12960| = 2160$.
(iv) Let $d$ be the shortest distance from $D$ to $\Pi$. $\frac{1}{3}(270)d = 2160$ $d = 24$. Thus, the shortest distance from $D$ to $\Pi$ is 24.
(b) Note that $\overrightarrow{AB} \times \overrightarrow{AC} = -360\mathbf{i} - 360\mathbf{j} - 180\mathbf{k}$ and $(\overrightarrow{AB} \times \overrightarrow{AC}) \cdot \overrightarrow{AD} < 0$. $\overrightarrow{DE} = \frac{24}{\sqrt{(-360)^2 + (-360)^2 + (-180)^2}}(-360\mathbf{i} - 360\mathbf{j} - 180\mathbf{k}) = -16\mathbf{i} - 16\mathbf{j} - 8\mathbf{k}$ Also note that $\overrightarrow{EA} = -20\mathbf{i} + 18\mathbf{j} + 4\mathbf{k}$ and $\overrightarrow{EB} = 10\mathbf{i} - 6\mathbf{j} - 8\mathbf{k}$. Let $M$ be the mid-point of $AB$. $\overrightarrow{EM} = \frac{1}{2}(\overrightarrow{EA} + \overrightarrow{EB}) = -5\mathbf{i} + 6\mathbf{j} - 2\mathbf{k}$ $\overrightarrow{EM} \cdot \overrightarrow{AB} = (-5)(30) + (6)(-24) + (-2)(-12) = -270 \neq 0$. So, $EM$ is not perpendicular to $AB$. Thus, $E$ is not the circumcentre of $\Delta ABC$.


**合計 100 / 100**
