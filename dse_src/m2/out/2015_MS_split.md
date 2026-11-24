# 2015 M2 Paper 1 — 評卷參考（分題）

> 分題依據：MS 題號行 + marks 對題目卷分數 [4, 5, 7, 7, 6, 6, 7, 8, 13, 12, 12, 13]｜合計 100

## 第 1 題  <!-- 頁 [2]｜4/4（MS 小計） -->

Marks: 1M 1M 1M 1A

1. $\frac{d}{dx}(x^5 + 4)$
$= \lim_{h \to 0} \frac{((x+h)^5 + 4) - (x^5 + 4)}{h}$
$= \lim_{h \to 0} \frac{x^5 + 5hx^4 + 10h^2x^3 + 10h^3x^2 + 5h^4x + h^5 + 4 - x^5 - 4}{h}$
$= \lim_{h \to 0} (5x^4 + 10hx^3 + 10h^2x^2 + 5h^3x + h^4)$
$= 5x^4$

## 第 2 題  <!-- 頁 [2]｜5/5（題目卷為準；MS 讀到 subtotals=無 cells=6） -->

Marks: 1M 1A 1A 1M 1A 1A

2. (a) $\frac{dy}{dx}$
$= x \cos x + \sin x - \sin x$
$= x \cos x$
$\frac{d^2y}{dx^2}$
$= -x \sin x + \cos x$
(b) $x \frac{d^2y}{dx^2} + k \frac{dy}{dx} + xy$
$= x(-x \sin x + \cos x) + kx \cos x + x(x \sin x + \cos x)$ (by (a))
$= (2+k)x \cos x$
Since $x \frac{d^2y}{dx^2} + k \frac{dy}{dx} + xy = 0$ for all real values of $x$, we have $k = -2$

## 第 3 題  <!-- 頁 [3]｜7/7（MS 小計） -->

Marks: 1M 1A 1M 1M+1A 1M 1A

3. (a) $\int \frac{1}{e^{2u}} du$
$= \int e^{-2u} du$
$= \frac{-1}{2} e^{-2u} + \text{constant}$
(b) Let $u = \sqrt{x}$. Then, we have $\frac{du}{dx} = \frac{1}{2\sqrt{x}}$.
$\int_{1}^{9} \frac{1}{\sqrt{x} e^{2\sqrt{x}}} dx$
$= \int_{1}^{3} \frac{2}{e^{2u}} du$
$= 2 \int_{1}^{3} \frac{1}{e^{2u}} du$
$= 2 \left[ \frac{-1}{2} e^{-2u} \right]_{1}^{3}$ (by (a))
$= \frac{1}{e^{2}} - \frac{1}{e^{6}}$

## 第 4 題  <!-- 頁 [3]｜7/7（題目卷為準；MS 讀到 subtotals=無 cells=8） -->

Marks: 1M 1A 1A 1M 1M 1M 1M 1A

4. (a) $\int x^{2} \ln x dx$
$= \frac{1}{3} \int \ln x dx^{3}$
$= \frac{1}{3} \left( x^{3} \ln x - \int x^{3} d \ln x \right)$
$= \frac{1}{3} \left( x^{3} \ln x - \int x^{2} dx \right)$
$= \frac{1}{3} x^{3} \ln x - \frac{1}{9} x^{3} + \text{constant}$
(b) $y$
$= \int 9x^{2} \ln x dx$
$= 9 \left( \frac{1}{3} x^{3} \ln x - \frac{1}{9} x^{3} \right) + C$ (by (a))
$= 3x^{3} \ln x - x^{3} + C$, where $C$ is a constant
Since $\Gamma$ passes through the point $(1, 4)$, we have $4 = 3 \ln 1 - 1 + C$.
Solving, we have $C = 5$.
Thus, the equation of $\Gamma$ is $y = 3x^{3} \ln x - x^{3} + 5$.

## 第 5 題  <!-- 頁 [4]｜6/6（題目卷為準；MS 讀到 subtotals=無 cells=9） -->

Marks: 1M 1A 1M 1M 1M 1A 1M 1M 1M

5. (a) The augmented matrix is $\begin{pmatrix} 1 & 1 & 1 & 2 \\ 2 & 3 & -3 & 4 \end{pmatrix} \sim \begin{pmatrix} 1 & 1 & 1 & 2 \\ 0 & 1 & -5 & 0 \end{pmatrix}$.
Thus, the solution set is $\{(2-6t, 5t, t) : t \in \mathbf{R}\}$.
(b) Putting $(x, y, z) = (2-6t, 5t, t)$ in the last equation, we have $3(2-6t) + 2(5t) + kt = 6$.
So, we have $(k-8)t = 0$.
We now consider the cases $k=8$ and $k \neq 8$.
Case 1: $k=8$
The system of linear equations in (b) is equivalent to the system of linear equations in (a).
Thus, the solution set is $\{(2-6t, 5t, t) : t \in \mathbf{R}\}$.
Case 2: $k \neq 8$
So, we have $t=0$.
Thus, the solution is $(2, 0, 0)$.
The augmented matrix is $\begin{pmatrix} 1 & 1 & 1 & 2 \\ 2 & 3 & -3 & 4 \\ 3 & 2 & k & 6 \end{pmatrix} \sim \begin{pmatrix} 1 & 1 & 1 & 2 \\ 0 & 1 & -5 & 0 \\ 0 & 0 & k-8 & 0 \end{pmatrix}$.
We now consider the cases $k=8$ and $k \neq 8$.
Case 1: $k=8$
In this case, the augmented matrix becomes $\begin{pmatrix} 1 & 1 & 1 & 2 \\ 0 & 1 & -5 & 0 \\ 0 & 0 & 0 & 0 \end{pmatrix}$.
Thus, the solution set is $\{(2-6t, 5t, t) : t \in \mathbf{R}\}$.
Case 2: $k \neq 8$
The solution is $(2, 0, 0)$.

## 第 6 題  <!-- 頁 [5]｜6/6（題目卷為準；MS 讀到 subtotals=無 cells=4） -->

Marks: 1M 1 1M 1M

6. (a) Note that $|M^T| = |M|$ and $|-M| = -|M|$. Since $|M^T| = |-M|$, we have $|M| = -|M|$. So, we have $2|M| = 0$. Thus, we have $|M| = 0$.
(b) (i) $A + I = \begin{pmatrix} 0 & a & b \\ -a & 0 & -8 \\ -b & 8 & 0 \end{pmatrix}$
So, we have $(A + I)^T = \begin{pmatrix} 0 & -a & -b \\ a & 0 & 8 \\ b & -8 & 0 \end{pmatrix} = -(A + I)$. By (a), we have $|A + I| = 0$.
(ii) Note that $A^3 + I = (A + I)(A^2 - A + I)$. $|A^3 + I| = |A + I||A^2 - A + I| = (0)|A^2 - A + I|$ (by (b)(i)) $= 0$. Therefore, $A^3 + I$ is a singular matrix. Thus, the claim is agreed.

## 第 7 題  <!-- 頁 [6]｜7/7（題目卷為準；MS 讀到 subtotals=無 cells=7） -->

Marks: 1M 1 1M 1M 1A 1M 1A

7. (a) $\sin^2 x \cos^2 x$
$= \frac{(2 \sin x \cos x)^2}{4}$
$= \frac{\sin^2 2x}{4}$
$= \frac{1}{4} \left( \frac{1-\cos 4x}{2} \right)$
$= \frac{1-\cos 4x}{8}$
(b) (i) $f(x)$
$= \sin^4 x + \cos^4 x$
$= (\sin^2 x + \cos^2 x)^2 - 2 \sin^2 x \cos^2 x$
$= 1^2 - 2 \left( \frac{1-\cos 4x}{8} \right)$ (by (a))
$= \frac{1}{4} \cos 4x + \frac{3}{4}$
(ii) $8 f(x) = 7$
$8 \left( \frac{1}{4} \cos 4x + \frac{3}{4} \right) = 7$ (by (b)(i))
$2 \cos 4x + 6 = 7$
$\cos 4x = \frac{1}{2}$
$4x = \frac{\pi}{3}$ or $4x = \frac{5\pi}{3}$
$x = \frac{\pi}{12}$ or $x = \frac{5\pi}{12}$

## 第 8 題  <!-- 頁 [7]｜8/8（題目卷為準；MS 讀到 subtotals=無 cells=2） -->

Marks: 1 1M

8. (a) Note that $\sin \frac{x}{2} \cos \frac{(1+1)x}{2} = \sin \frac{x}{2} \cos x$. So, the statement is true for $n=1$. Assume that $\sin \frac{x}{2} \sum_{k=1}^{m} \cos kx = \sin \frac{mx}{2} \cos \frac{(m+1)x}{2}$ for some positive integer $m$. $\sin \frac{x}{2} \sum_{k=1}^{m+1} \cos kx$ $= \sin \frac{x}{2} \sum_{k=1}^{m} \cos kx + \sin \frac{x}{2} \cos(m+1)x$ $= \sin \frac{mx}{2} \cos \frac{(m+1)x}{2} + \sin \frac{x}{2} \cos(m+1)x$ (by induction assumption) $= \frac{1}{2} \left( \sin \frac{(2m+1)x}{2} - \sin \frac{x}{2} \right) + \frac{1}{2} \left( \sin \frac{(2m+3)x}{2} - \sin \frac{(2m+1)x}{2} \right)$ $= \frac{1}{2} \left( \sin \frac{(2m+3)x}{2} - \sin \frac{x}{2} \right)$ $= \cos \frac{(2m+4)x}{4} \sin \frac{(2m+2)x}{4}$ $= \sin \frac{(m+1)x}{2} \cos \frac{(m+2)x}{2}$ So, the statement is true for $n=m+1$ if it is true for $n=m$. By mathematical induction, we have $\sin \frac{x}{2} \sum_{k=1}^{n} \cos kx = \sin \frac{nx}{2} \cos \frac{(n+1)x}{2}$ for all positive integers $n$.
(b) Putting $x = \frac{\pi}{7}$ and $n=567$ in (a), we have $\sum_{k=1}^{567} \cos \frac{k\pi}{7}$ $= \frac{\sin \frac{(567)(\pi)}{(2)(7)}}{\sin \frac{\pi}{(2)(7)}}$ $= \frac{\sin \frac{\pi}{2}}{\cos \left( \frac{\pi}{2} + \frac{\pi}{14} \right)}$ $= \frac{-\sin \frac{\pi}{14}}{\sin \frac{\pi}{14}}$ $= -1$

## 第 9 題  <!-- 頁 [8]｜13/13（題目卷為準；MS 讀到 subtotals=[2] cells=2） -->

Marks: 1M 1A

9. (a) $f'(x)$
$$= \frac{(x-2)(2x)-(x^2+12)}{(x-2)^2}$$
$$= \frac{x^2-4x-12}{(x-2)^2}$$
(b) Note that $f'(x) = \frac{(x+2)(x-6)}{(x-2)^2}$.
So, we have $f'(x) = 0 \iff x = -2$ or $x = 6$.

## 第 10 題  <!-- 頁 [9, 10]｜12/12（題目卷為準；MS 讀到 subtotals=無 cells=15） -->

Marks: 1M 1A 1M 1M 1M 1A 1M 1A 1M 1M 1A 1M 1M 1A 1A

10. (a) (i) $\overrightarrow{OQ} = \frac{2}{3}\overrightarrow{OA} + \frac{1}{3}\overrightarrow{OB}$ $\overrightarrow{OC} = (1-t)\overrightarrow{OP} + t\overrightarrow{OR}$ $= (1-t)\left(\frac{1}{2}\overrightarrow{OA}\right) + t\left(\frac{3}{4}\overrightarrow{OB}\right)$ $= \frac{1-t}{2}\overrightarrow{OA} + \frac{3t}{4}\overrightarrow{OB}$
Note that $C$ lies on $OQ$. So, we have $\frac{1-t}{2} : \frac{2}{3} = \frac{3t}{4} : \frac{1}{3}$.
Thus, we have $t = \frac{1}{4}$.
(ii) By (a)(i), we have $\overrightarrow{OC} = \frac{3}{8}\overrightarrow{OA} + \frac{3}{16}\overrightarrow{OB}$.
Therefore, we have $\overrightarrow{OC} = \frac{9}{16}\overrightarrow{OQ}$.
Hence, we have $\left| \overrightarrow{OC} \right| = \frac{9}{16}\left| \overrightarrow{OQ} \right|$.
So, we have $OC:OQ = 9:16$.
Thus, we have $CQ:OQ = 7:16$.
(b) (i) The area of $\Delta OAB = \frac{1}{2}\left| \overrightarrow{OA} \times \overrightarrow{OB} \right|$
$= \frac{1}{2}\left\| \begin{array}{ccc} \mathbf{i} & \mathbf{j} & \mathbf{k} \\ 20 & -6 & -12 \\ 16 & -16 & 0 \end{array} \right\|$
$= \frac{1}{2}\left| -192\mathbf{i} - 192\mathbf{j} - 224\mathbf{k} \right|$
$= 176$
(ii) The volume of the tetrahedron $ABCD = \frac{1}{6}\left| \overrightarrow{CD} \cdot (\overrightarrow{CA} \times \overrightarrow{CB}) \right|$
$= \left(\frac{1}{6}\right)\left(\frac{7}{16}\right)\left| \overrightarrow{OD} \cdot (\overrightarrow{OA} \times \overrightarrow{OB}) \right|$ (by (a)(ii))
$= \frac{7}{96}\left| (\mathbf{i} + 3\mathbf{j} - 6\mathbf{k}) \cdot (-192\mathbf{i} - 192\mathbf{j} - 224\mathbf{k}) \right|$ (by (b)(i))
$= \left(\frac{7}{96}\right)(576)$
$= 42$
Since $\overrightarrow{OC} = \frac{3}{8}\overrightarrow{OA} + \frac{3}{16}\overrightarrow{OB}$, we have $\overrightarrow{OC} = \frac{21}{2}\mathbf{i} - \frac{21}{4}\mathbf{j} - \frac{9}{2}\mathbf{k}$. $\overrightarrow{CA} = \frac{19}{2}\mathbf{i} - \frac{3}{4}\mathbf{j} - \frac{15}{2}\mathbf{k}$ $\overrightarrow{CB} = \frac{11}{2}\mathbf{i} - \frac{43}{4}\mathbf{j} + \frac{9}{2}\mathbf{k}$ $\overrightarrow{CD} = \frac{-19}{2}\mathbf{i} + \frac{33}{4}\mathbf{j} - \frac{3}{2}\mathbf{k}$
The volume of the tetrahedron $ABCD$ $= \frac{1}{6} \left| \overrightarrow{CD} \cdot (\overrightarrow{CA} \times \overrightarrow{CB}) \right|$
$= \frac{1}{6} \left\| \begin{array}{cccc} \frac{-19}{2} & \frac{33}{4} & \frac{-3}{2} \\ \frac{19}{2} & \frac{-3}{4} & \frac{-15}{2} \\ \frac{11}{2} & \frac{-43}{4} & \frac{9}{2} \end{array} \right\|$
$= \frac{252}{6}$
$= 42$

## 第 11 題  <!-- 頁 [11, 12]｜12/12（題目卷為準；MS 讀到 subtotals=無 cells=9） -->

Marks: 1M 1A 1A 1M 1 1M 1 1M 1

11. (a) (i) AB = $\frac{1}{(\lambda - \mu + 2)^2} \begin{pmatrix} \lambda - \mu + 1 & 1 \\ \lambda - \mu + 1 & 1 \end{pmatrix} \begin{pmatrix} 1 & -1 \\ -\lambda + \mu - 1 & \lambda - \mu + 1 \end{pmatrix}$ = $\begin{pmatrix} 0 & 0 \\ 0 & 0 \end{pmatrix}$
BA = $\frac{1}{(\lambda - \mu + 2)^2} \begin{pmatrix} 1 & -1 \\ -\lambda + \mu - 1 & \lambda - \mu + 1 \end{pmatrix} \begin{pmatrix} \lambda - \mu + 1 & 1 \\ \lambda - \mu + 1 & 1 \end{pmatrix}$ = $\begin{pmatrix} 0 & 0 \\ 0 & 0 \end{pmatrix}$
A+B = $\frac{1}{(\lambda - \mu + 2)} \left[ \begin{pmatrix} \lambda - \mu + 1 & 1 \\ \lambda - \mu + 1 & 1 \end{pmatrix} + \begin{pmatrix} 1 & -1 \\ -\lambda + \mu - 1 & \lambda - \mu + 1 \end{pmatrix} \right]$ = $\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}$
(ii) $A^2$ = $A(I - B)$ (by (a)(i)) = $A - AB$ = $A - 0$ (by (a)(i)) = $A$
$B^2$ = $B(I - A)$ (by (a)(i)) = $B - BA$ = $B - 0$ (by (a)(i)) = $B$
(iii) $(\lambda + 1)A + (\mu - 1)B$ = $\frac{\lambda + 1}{\lambda - \mu + 2}(I - \mu I + M) + \frac{\mu - 1}{\lambda - \mu + 2}(I + \lambda I - M)$ = $\frac{-\mu \lambda + \lambda - \mu + 1}{\lambda - \mu + 2}I + \frac{\lambda + 1}{\lambda - \mu + 2}M + \frac{\mu \lambda - \lambda + \mu - 1}{\lambda - \mu + 2}I - \frac{\mu - 1}{\lambda - \mu + 2}M$ = $M$ So, we have $M = (\lambda + 1)A + (\mu - 1)B$. $M^2$ = $((\lambda + 1)A + (\mu - 1)B)((\lambda + 1)A + (\mu - 1)B)$ $= (\lambda + 1)^2A^2 + (\lambda + 1)(\mu - 1)AB + (\lambda + 1)(\mu - 1)BA + (\mu - 1)^2B^2$ $= (\lambda + 1)^2A + (\mu - 1)^2B$ (by (a)(i) and (a)(ii)) $M^3$ $= M^2M$ $= ((\lambda + 1)^2A + (\mu - 1)^2B)((\lambda + 1)A + (\mu - 1)B)$ $= (\lambda + 1)^3A^2 + (\lambda + 1)^2(\mu - 1)AB + (\lambda + 1)(\mu - 1)BA + (\mu - 1)^3B^2$ $= (\lambda + 1)^3A + (\mu - 1)^3B$ (by (a)(i) and (a)(ii)) Thus, we have $M^n = (\lambda + 1)^nA + (\mu - 1)^nB$.
$(\lambda+1)A + (\mu-1)B = \frac{\lambda+1}{\lambda-\mu+2} \begin{pmatrix} \lambda-\mu+1 & 1 \\ \lambda-\mu+1 & 1 \end{pmatrix} + \frac{\mu-1}{\lambda-\mu+2} \begin{pmatrix} 1 & -1 \\ -\lambda+\mu-1 & \lambda-\mu+1 \end{pmatrix} = \frac{1}{\lambda-\mu+2} \begin{pmatrix} \lambda^2 - \lambda\mu + 2\lambda & \lambda - \mu + 2 \\ (\lambda-\mu+1)(\lambda-\mu+2) & \lambda\mu - \mu^2 + 2\mu \end{pmatrix} = M$
So, the statement is true for $n=1$.
Assume that $M^k = (\lambda+1)^k A + (\mu-1)^k B$, where $k$ is a positive integer.
$M^{k+1} = MM^k$
$= ((\lambda+1)A + (\mu-1)B)((\lambda+1)^k A + (\mu-1)^k B)$
$= (\lambda+1)^{k+1} A^2 + (\lambda+1)(\mu-1)^k AB + (\lambda+1)^k (\mu-1)BA + (\mu-1)^{k+1} B^2$
$= (\lambda+1)^{k+1} A + (\mu-1)^{k+1} B$ (by (a)(i) and (a)(ii))
So, the statement is true for $n=k+1$ if it is true for $n=k$.
By mathematical induction, we have $M^n = (\lambda+1)^n A + (\mu-1)^n B$.

## 第 12 題  <!-- 頁 [13]｜13/13（題目卷為準；MS 讀到 subtotals=無 cells=4） -->

Marks: 1M 1M 1M 1M

12. (a) (i) Solving $\begin{cases} 3x+y-9=0 \\ x^2-4y+8=0 \end{cases}$, we have $x^2+12x-28=0$. So, we have $x=2$ or $x=-14$ (rejected). Thus, the coordinates of $B$ are $(2, 3)$.
1A
1M+1M+1A
1M
(ii) The required capacity = $\int_0^3 \pi \left(\frac{9-y}{3}\right)^2 \mathrm{d}y + \int_3^h \pi (4y-8) \mathrm{d}y$ = $\pi \int_0^3 \left(9-2y+\frac{y^2}{9}\right) \mathrm{d}y + \pi \int_3^h (4y-8) \mathrm{d}y$ = $\pi \left[9y-y^2+\frac{y^3}{27}\right]_0^3 + \pi \left[2y^2-8y\right]_3^h$ = $\pi(2h^2-8h+25)$
1
(7)
(b) (i) Putting $x=6$ in $x^2-4y+8=0$, we have $y=11$. The required capacity = $\pi(2(11)^2-8(11)+25)$ (by (a)(ii)) = $179\pi \mathrm{cm}^3$
1A
(ii) Let $h$ cm be the depth of water in the cup at time $t$ s. Also let $p$ cm be the depth of water when the volume of water in the cup is $35\pi \mathrm{cm}^3$. Note that the volume of the frustum is $19\pi \mathrm{cm}^3$. Since $35\pi > 19\pi$, we have $p>3$. By (a)(ii), we have $\pi(2p^2-8p+25)=35\pi$. Simplifying, we have $p^2-4p-5=0$. Solving, we have $p=5$ or $p=-1$ (rejected as $3<p\leq 11$). Hence, we have $p=5$. Let $V \mathrm{cm}^3$ be the volume of water in the cup at time $t$ s. For $3<h\leq 11$, we have $V=\pi(2h^2-8h+25)$ (by (a)(ii)). So, we have $\frac{\mathrm{d}V}{\mathrm{d}t}=\pi(4h-8)\frac{\mathrm{d}h}{\mathrm{d}t}$ for $3<h\leq 11$. Since $\frac{\mathrm{d}V}{\mathrm{d}t}|_{h=5}=24\pi$, we have $24\pi=\pi(4(5)-8)\frac{\mathrm{d}h}{\mathrm{d}t}|_{h=5}$. Therefore, we have $\frac{\mathrm{d}h}{\mathrm{d}t}|_{h=5}=2$. Thus, the required rate of change is $2 \mathrm{~cm/s}$.
1M
1A
(6)


**合計 100 / 100**
