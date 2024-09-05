import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 生成一些示例数据
np.random.seed(10)
data = np.random.normal(loc=0, scale=1, size=(100, 4))  # 生成 100 行 4 列的正态分布数据

# 绘制玉玦图
sns.violinplot(data=data)

plt.title('Violin Plot with Custom Data')
plt.show()
