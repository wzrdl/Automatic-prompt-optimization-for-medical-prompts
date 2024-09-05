# 引入库
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# 数据准备
data=pd.DataFrame({'theme':['Physician\'s exam','Nursing exams','Pharmacist exam','Medical Technology Exam','Professional knowledge exams','Medical Exam'],'data':[122876,15279,30074,25774, 60631,14725]})
data

# 准备好角度
angles=np.arange(0,2*np.pi,2*np.pi/data.shape[0])
# 准备好半径

size_n=6
radius=np.array(data['data'])
fig=plt.figure(figsize=(size_n,size_n))
fig=fig.gca(polar=True)
fig.set_theta_offset(np.pi/2)
fig.set_theta_direction(-1)
fig.set_rlabel_position(0)

fig=plt.figure(figsize=(size_n,size_n))
fig=fig.gca(polar=True)
fig.set_theta_offset(np.pi/2)
fig.set_theta_direction(-1)
fig.set_rlabel_position(0)
# 绘制南丁格尔玫瑰图
plt.bar(angles,radius)

plt.show()