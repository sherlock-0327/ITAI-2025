import matplotlib.pyplot as plt

# N值与对应的运行时间（秒）
n_values = [4, 5, 6, 7, 8, 9, 10, 11, 12]
times = [0.00002910, 0.00008270, 0.00012300, 0.00063870, 0.00251910,
         0.00550090, 0.01816120, 0.06592700, 0.34700270]

# 创建图形
plt.figure(figsize=(10, 6))

# 绘制折线图
plt.plot(n_values, times, marker='o', linestyle='-', color='blue', label='time')

# 绘制柱状图（叠加在折线上）
plt.bar(n_values, times, width=0.4, alpha=0.3, color='skyblue', label='Distribution')

# 添加数据标签
for n, t in zip(n_values, times):
    plt.text(n, t, f'{t:.8f}s', ha='center', va='bottom', fontsize=9)

# 图表设置
plt.xlabel('N', fontsize=12)
plt.ylabel('time', fontsize=12)
plt.title('N=4-12', fontsize=14, fontweight='bold')
plt.xticks(n_values)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()

# 显示对数坐标轴（可选，用于观察指数增长趋势）
# plt.yscale('log')

# 保存图片并显示
plt.savefig('n_queen_time_trend.png', dpi=300)
plt.show()