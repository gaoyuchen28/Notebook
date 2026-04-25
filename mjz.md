1 \\ 
\vdots & \vdots & \vdots & \ddots & \vdots & \vdots \\ 
0 & 1-n & 1 & \dots & 1 & 1 
\end{vmatrix}$$

---

### 第三步：按第 $1$ 列展开（降阶）

现在第 $1$ 列只有一个 $1$，其余全是 $0$。我们按第 $1$ 列展开，行列式就降到了 $n-1$ 阶，记这个新的行列式为 $\Delta$：
$$D_n = \frac{n(n+1)}{2} \times \Delta$$

其中，留下的余子式 $\Delta$ 是：
$$\Delta = \begin{vmatrix} 
1 & 1 & \dots & 1 & 1-n \\ 
1 & 1 & \dots & 1-n & 1 \\ 
\vdots & \vdots & \ddots & \vdots & \vdots \\ 
1-n & 1 & \dots & 1 & 1 
\end{vmatrix}$$

---

### 第四步：计算降阶后的行列式 $\Delta$

仔细观察 $\Delta$，它的每一行有 $(n-2)$ 个 $1$ 和 $1$ 个 $1-n$。所以每一行元素之和是：$1 \times (n-2) + (1-n) = -1$。

**操作 1：** 将 $\Delta$ 的第 $1, 2, \dots, n-2$ 列全部加到最后一列。
此时，最后一列的所有元素都变成了 $-1$。我们将 $-1$ 提取出来：
$$\Delta = (-1) \times \begin{vmatrix} 
1 & 1 & \dots & 1 & 1 \\ 
1 & 1 & \dots & 1-n & 1 \\ 
\vdots & \vdots & \ddots & \vdots & \vdots \\ 
1-n & 1 & \dots & 1 & 1 
\end{vmatrix}$$

**操作 2：** 用第 $2, 3, \dots, n-1$ 行，分别**减去**第 $1$ 行。
*   除了含有 $1-n$ 的那个位置变成了 $(1-n) - 1 = -n$ 之外，其余位置 $(1-1)$ 全部变成了 $0$！
由于原本的 $1-n$ 是沿着副对角线排列的，减法过后，矩阵化简成了一个**极其干净的副对角线矩阵**：
$$\Delta = (-1) \times \begin{vmatrix} 
1 & 1 & \dots & 1 & 1 \\ 
0 & 0 & \dots & -n & 0 \\ 
\vdots & \vdots & \ddots & \vdots & \vdots \\ 
-n & 0 & \dots & 0 & 0 
\end{vmatrix}$$

**操作 3：** 展开求解。
将这个副对角线矩阵展开，经过严谨的符号推导（奇偶排列计算），这个 $\Delta$ 的最终值为：
$$\Delta = (-1)^{\frac{n(n-1)}{2}} \times n^{n-2}$$

*(注：在我上一条回复末尾的总结中