import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# 数据
labels = ['Prophase', 'Metaphase', 'Anaphase', 'Telophase', 'Interphase']
sizes = [1.85, 0.37, 0.37, 2.95, 94.46]
colors = ['#55a84f', '#a05195', '#de8452', "#52eefd", '#2c5973']

fig, ax = plt.subplots(figsize=(12, 8))
plt.subplots_adjust(left=0.1, right=0.7)  # 右侧空间放图例

# 绘制环形图
wedges, _ = ax.pie(
    sizes,
    wedgeprops=dict(width=0.45, edgecolor='w', linewidth=2),
    startangle=140,
    colors=colors
)

# 分开左右两侧的标签列表
right_y_positions = []
left_y_positions = []

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    x, y = np.cos(np.deg2rad(ang)), np.sin(np.deg2rad(ang))
    
    # 初始标签位置
    tx = 1.3 * np.sign(x)
    ty = 1.3 * y

    # 调整位置避免重叠
    y_list = right_y_positions if x > 0 else left_y_positions
    if y_list:
        for prev_y in y_list:
            if abs(ty - prev_y) < 0.2:
                ty = prev_y + (0.2 if ty > prev_y else -0.2)
    y_list.append(ty)

    # 绘制箭头标注
    ax.annotate(
        f"{labels[i]}\n{sizes[i]}%",
        xy=(0.85*x, 0.85*y),
        xytext=(tx*1.2, ty),
        ha="left" if x > 0 else "right",
        va='center',
        fontsize=10,
        color='#2c3e50',
        arrowprops=dict(
            arrowstyle="-",
            color=colors[i],
            connectionstyle="angle3,angleA=0,angleB=90",
            lw=1.5
        )
    )

# 优化图例
legend_elements = [Patch(facecolor=colors[i], edgecolor='w', label=f"{labels[i]} ({sizes[i]}%)") 
                   for i in range(len(labels))]
ax.legend(
    handles=legend_elements,
    title="Mitotic Phases",
    loc='center left',
    bbox_to_anchor=(1, 0.5),
    frameon=False,
    fontsize=11,
    title_fontsize=12,
    handlelength=1.5,
    handleheight=1.5,
    labelspacing=1.0
)

ax.set_title("Mitotic Phase Distribution (Optimized)", fontsize=16, fontweight='bold', pad=25)
ax.set_aspect('equal')

plt.show()