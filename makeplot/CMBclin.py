import pandas as pd

# 读取CSV文件
df = pd.read_csv('D:LLMdata/test_acc/elseF1.csv')

# 计算每一列的平均值
averages = df.mean()

# 打印每一列的平均值
print("Averages of each column:")
print(averages)