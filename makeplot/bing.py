import seaborn as sns
import matplotlib.pyplot as plt

# 设置全局字体大小
plt.rcParams['font.size'] = 11  # 设置全局字体大小为14

# 示例数据：各类别的数量
x_out = ['Completion of training','Licensed physician assistant','Practitioner','Intermediate title','Senior title']
y_out = [14201,15006,25231,55729, 12709]
color_series_out = ["#8ECFC9","#FFBE7A","#FA7F6F","#82B0D2","#BEB8DC"]




x_in = ['Physician\'s exam','Nursing exams','Pharmacist exam','Medical Technology Exam','Professional knowledge exams','Medical Exam']
y_in = [122876,15279,30074,25774, 60631,14725]
color_series_in = ["#8ECFC9","#FFBE7A","#FA7F6F","#82B0D2","#BEB8DC","#E7DAD2"]


# 绘制饼图
plt.subplot(121)
#plt.figure(figsize=(6, 6))
plt.pie(y_out, labels=x_out, colors=color_series_out, autopct='%1.1f%%', startangle=90)


plt.subplot(122)
#plt.figure(figsize=(6, 6))
plt.pie(y_in, labels=x_in, colors=color_series_in, autopct='%1.1f%%', startangle=90)

# 添加标题
#plt.title('Distribution of Categories')

# 显示饼图
plt.axis('equal')  # 保证饼图是圆形
#plt.tight_layout()
plt.show()
