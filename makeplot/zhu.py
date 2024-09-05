import seaborn as sns
import matplotlib.pyplot as plt

# 示例数据
provinces = ['Physician\'s exam','Nursing exams','Pharmacist exam','Medical Technology Exam','Professional knowledge exams','Medical Exam']
num = [122876,15279,30074,25774, 60631,14725]
color_series = ["#8ECFC9","#FFBE7A","#FA7F6F","#82B0D2","#BEB8DC","#E7DAD2"]

# 使用Seaborn绘制柱状图，并指定配色方案
ax=sns.barplot(x=provinces, y=num, palette=color_series)
# 在柱状图顶部显示数字标签
for p in ax.patches:
    ax.annotate(format(p.get_height(), '.1f'), 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha = 'center', va = 'center', 
                xytext = (0, 10), 
                textcoords = 'offset points')

# 添加标题和标签
plt.title('Bar Plot Example')
plt.xlabel('X-axis Label')
plt.ylabel('Y-axis Label')

# 显示图形
plt.show()
