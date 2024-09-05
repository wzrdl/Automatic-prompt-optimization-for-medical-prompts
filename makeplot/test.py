import matplotlib.pyplot as plt
import seaborn as sns

# 数据
labels_outer = ['A', 'B', 'C']
sizes_outer = [30, 40, 30]

labels_inner = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
sizes_inner = [10, 20, 15, 25, 20, 10]

# 绘制外层饼图
plt.subplot(121)
plt.pie(sizes_outer, labels=labels_outer, autopct='%1.1f%%', startangle=90)

# 绘制内层饼图
plt.subplot(122)
plt.pie(sizes_inner, labels=labels_inner, autopct='%1.1f%%', startangle=90)

plt.show()
