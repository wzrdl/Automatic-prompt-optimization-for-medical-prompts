import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

# 创建自定义数据集
n_samples = 300
random_state = 42
X, y = make_blobs(n_samples=n_samples, random_state=random_state)

# 定义K均值聚类模型
n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)

# 对数据进行聚类
kmeans.fit(X)
y_kmeans = kmeans.predict(X)

# 可视化聚类结果
plt.figure(figsize=(8, 6))

# 绘制原始数据点
plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')

# 绘制聚类中心
centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.9)

plt.title('K-Means Clustering')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()
