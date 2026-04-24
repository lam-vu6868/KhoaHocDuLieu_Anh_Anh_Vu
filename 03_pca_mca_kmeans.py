import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import prince
import os

os.makedirs('outputs/figures', exist_ok=True)

# 1. ĐỌC VÀ LÀM SẠCH NHẸ
print("1. Đang nạp dữ liệu...")
df = pd.read_csv('data/processed/data_cleaned.csv')
cols_so = ['original_price', 'discount_price', 'discount', 'sold_quantity', 'liked_count', 'rating_star', 'number_of_ratings']
cols_chu = ['brand', 'shop_location']

df[cols_so] = df[cols_so].fillna(df[cols_so].median)
df[cols_chu] = df[cols_chu].fillna('UNKNOWN')

# 2. XỬ LÝ CỘT SỐ (SCALER + PCA)
print("2. Đang chạy PCA cho cột Số...")
scaler = StandardScaler()
X_so_scaled = scaler.fit_transform(df[cols_so])

pca = PCA(n_components=2, random_state=42)
pca_result = pca.fit_transform(X_so_scaled)
df_pca = pd.DataFrame(pca_result, columns=['PC1', 'PC2'])

# 🔥 BẰNG CHỨNG 1: IN TRỌNG SỐ PCA (Để chém gió PC1, PC2 là gì)
pca_loadings = pd.DataFrame(pca.components_.T, columns=['PC1_Weight', 'PC2_Weight'], index=cols_so)
print("\n=== TRỌNG SỐ PCA (TẠI SAO CÓ PC1, PC2) ===")
print(pca_loadings.round(2))
print("-> Nhìn số nào lớn nhất để đoán ý nghĩa của PC1 và PC2 nhé sếp!\n")

# 3. XỬ LÝ CỘT CHỮ (MCA)
print("3. Đang chạy MCA cho cột Chữ...")
mca = prince.MCA(n_components=2, random_state=42)
mca_result = mca.fit_transform(df[cols_chu])
df_mca = pd.DataFrame(np.array(mca_result), columns=['MC1', 'MC2'])

# 4. HỘI QUÂN
X_combined = pd.concat([df_pca, df_mca], axis=1)

# 5. CHẠY ELBOW TÌM K TỐI ƯU
print("4. Đang vẽ biểu đồ Elbow...")
inertia = []
K_range = range(1, 8)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_combined)
    inertia.append(km.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(K_range, inertia, marker='o', color='purple')
plt.title('Phương pháp Khuỷu tay (Elbow) tìm K tối ưu', fontsize=14)
plt.xlabel('Số lượng cụm (K)')
plt.ylabel('Độ nhão (Inertia)')
plt.axvline(x=3, color='red', linestyle='--', label='K=3 (Khuỷu tay)')
plt.legend()
plt.tight_layout()
plt.savefig('outputs/figures/5_elbow.png', dpi=300)
plt.close()

# 6. PHÂN CỤM K-MEANS CHÍNH THỨC VỚI K=3
print("5. Đang gom cụm K-Means (K=3)...")
K_OPT = 3
kmeans = KMeans(n_clusters=K_OPT, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X_combined)

# 7. VẼ BẢN ĐỒ VÀ MỔ XẺ
plt.figure(figsize=(10, 7))
sns.scatterplot(data=df, x=df_pca['PC1'], y=df_pca['PC2'], hue='Cluster', palette='Set1', alpha=0.6)
plt.title('Bản đồ Thị trường 2D (Trục X: Định vị giá, Trục Y: Sức mua)')
plt.savefig('outputs/figures/6_clusters.png', dpi=300)
plt.close()

print("\n=== MỔ XẺ CÁC CỤM ĐỂ ĐẶT TÊN ===")
for i in range(K_OPT):
    print(f"\n🚀 CỤM SỐ {i}:")
    cum = df[df['Cluster'] == i]
    print(f"  - Giá bán TB : {cum['discount_price'].mean():.1f} triệu")
    print(f"  - Lượt bán TB: {cum['sold_quantity'].mean():.0f} chiếc")
    top_hang = cum['brand'].value_counts().head(2)
    print(f"  - Hãng trùm  : {', '.join(top_hang.index.tolist())}")

print("\n✅ Xong toàn bộ! Ảnh đã lưu trong thư mục outputs/figures.")