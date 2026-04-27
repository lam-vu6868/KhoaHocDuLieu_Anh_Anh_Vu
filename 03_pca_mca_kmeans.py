import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import prince  # Thư viện chuyên cho MCA
import os

# --- CẤU HÌNH HỆ THỐNG ---
os.makedirs('outputs/figures', exist_ok=True)
plt.style.use('seaborn-v0_8-whitegrid')

# 1. ĐỌC DỮ LIỆU SẠCH
print("🚀 Đang tải dữ liệu sạch...")
df = pd.read_csv('data/processed/data_cleaned.csv')

# =====================================================================
# PHẦN 1: PCA (GIẢM CHIỀU DỮ LIỆU SỐ)
# =====================================================================
print("\n--- [PHẦN 1: PCA - PHÂN TÍCH THÀNH PHẦN CHÍNH] ---")
cols_so = ['sold_quantity', 'discount_price', 'original_price', 'discount', 'liked_count', 'rating_star', 'number_of_ratings']
X_numeric = df[cols_so]

# Standard Scaler (Đưa về cùng đơn vị để PCA không bị lệch)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_numeric)

# Chạy PCA nén về 2 chiều
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# PRINT: Giải thích tỷ lệ giữ lại thông tin
var_ratio = pca.explained_variance_ratio_
print(f"✅ PC1 giữ {var_ratio[0]*100:.1f}% thông tin.")
print(f"✅ PC2 giữ {var_ratio[1]*100:.1f}% thông tin.")
print(f"💡 Tổng 2 trục giữ được {sum(var_ratio)*100:.1f}% thông tin gốc.")

# PRINT: Xem Loadings để biết trục đại diện cho cái gì
loadings = pd.DataFrame(pca.components_.T, columns=['PC1', 'PC2'], index=cols_so)
print("\n📊 BẢNG TRỌNG SỐ (LOADINGS):")
print(loadings)

# VẼ BIỂU ĐỒ PCA (SCATTER)
plt.figure(figsize=(10, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.5, c='teal')
plt.title('Biểu đồ Phân tán dữ liệu trong không gian PCA', fontsize=14)
plt.xlabel('PC1 (Thường là Phân khúc Giá)')
plt.ylabel('PC2 (Thường là Sức hút/Rating)')
plt.tight_layout()
# plt.show() 
plt.savefig('outputs/figures/5_pca_scatter.png', dpi=300)
plt.close()

# =====================================================================
# PHẦN 2: MCA (PHÂN TÍCH ĐA TƯƠNG ỨNG)
# =====================================================================
# Do thư viện prince mới đã bỏ một số thuộc tính cũ nên code sẽ phức tạp hơn
print("\n--- [PHẦN 2: CA - PHÂN TÍCH TƯƠNG ỨNG ĐƠN (2 BIẾN)] ---")
# Tạo bảng chéo (Contingency Table) giữa Brand và Location
crosstab = pd.crosstab(df['brand'], df['shop_location'])
# Sử dụng CA thay vì MCA
ca = prince.CA(n_components=2, n_iter=3, random_state=42)
ca = ca.fit(crosstab)
# Trích xuất tọa độ của Hãng (Row) và Địa điểm (Column)
row_coords = ca.row_coordinates(crosstab)
col_coords = ca.column_coordinates(crosstab)
plt.figure(figsize=(12, 8))
# Vẽ Brand (Điểm đỏ)
sns.scatterplot(x=row_coords.iloc[:, 0], y=row_coords.iloc[:, 1], s=150, color='crimson', label='Thương hiệu', marker='o')
for i, label in enumerate(row_coords.index):
    plt.annotate(label, (row_coords.iloc[i, 0], row_coords.iloc[i, 1]), xytext=(5, 5), textcoords='offset points', color='darkred', fontweight='bold')
# Vẽ Location (Điểm xanh)
sns.scatterplot(x=col_coords.iloc[:, 0], y=col_coords.iloc[:, 1], s=150, color='royalblue', label='Địa điểm', marker='s')
for i, label in enumerate(col_coords.index):
    plt.annotate(label, (col_coords.iloc[i, 0], col_coords.iloc[i, 1]), xytext=(5, 5), textcoords='offset points', color='darkblue')
plt.axhline(0, color='gray', linestyle='--', linewidth=1)
plt.axvline(0, color='gray', linestyle='--', linewidth=1)
plt.title('Bản đồ CA tương quan giữa Thương hiệu và Địa điểm', fontsize=16, fontweight='bold')
plt.xlabel('Dimension 1', fontsize=12)
plt.ylabel('Dimension 2', fontsize=12)
plt.legend()
plt.tight_layout()
plt.savefig('outputs/figures/6_ca_map.png', dpi=300)
plt.close()
# Lưu tọa độ
row_coords.to_csv('data/processed/ca_coords_brands.csv')
col_coords.to_csv('data/processed/ca_coords_locations.csv')
print("✅ Đã chạy thuật toán CA và lưu tọa độ thành công.")

# =====================================================================
# PHẦN 3: K-MEANS (GOM CỤM DỰA TRÊN PCA)
# =====================================================================
print("\n--- [PHẦN 3: K-MEANS - PHÂN CỤM CHIẾN LƯỢC] ---")

# Tìm số cụm tối ưu (Elbow Method)
inertias = []
K_range = range(1, 10)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_pca)
    inertias.append(km.inertia_)

plt.figure(figsize=(8, 4))
plt.plot(K_range, inertias, 'go--')
plt.title('Phương pháp Elbow để chọn số cụm K')
plt.xlabel('Số cụm K')
plt.ylabel('Inertia (Độ biến thiên)')
# plt.show()
plt.savefig('outputs/figures/7_elbow_method.png')
plt.close()

# Tính Silhouette Score cho các K từ 2 đến 8 (Silhouette không tính được cho K=1)
sil_scores = []
K_range_sil = range(2, 9)

for k in K_range_sil:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_pca)
    score = silhouette_score(X_pca, labels)
    sil_scores.append(score)

# Vẽ biểu đồ Silhouette
plt.figure(figsize=(8, 4))
plt.plot(K_range_sil, sil_scores, 'ro-', color='darkorange')
plt.title('Hệ số Silhouette để tìm K tối ưu (Càng cao càng tốt)')
plt.xlabel('Số lượng cụm K')
plt.ylabel('Silhouette Score')
# plt.show()
plt.savefig('outputs/figures/7b_silhouette_score.png')
plt.close()

# Chốt K=3 và Phân cụm
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(X_pca)


# PRINT: Đặc trưng cụm (Dữ liệu quan trọng nhất để báo cáo)
print("\n🏆 KẾT QUẢ PHÂN CỤM (GIÁ TRỊ TRUNG BÌNH MỖI CỤM):")
profile = df.groupby('cluster')[cols_so].mean()
print(profile)

# VẼ BIỂU ĐỒ K-MEANS
plt.figure(figsize=(10, 7))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=df['cluster'], palette='bright', s=80, alpha=0.8)
plt.title('Phân cụm Sản phẩm Shopee dựa trên K-Means', fontsize=15)
plt.xlabel('PC1 (Chỉ số Phân khúc Giá)')
plt.ylabel('PC2 (Chỉ số Sức hút)')
plt.legend(title='Nhóm cụm')
# plt.show()
plt.savefig('outputs/figures/8_kmeans_final.png', dpi=300)
plt.close()

# XUẤT DỮ LIỆU ĐÃ CÓ NHÃN CỤM 
df.to_csv('data/processed/data_with_clusters.csv', index=False)
print("\n✅ HOÀN TẤT! Đã lưu dữ liệu có nhãn cụm vào 'data_with_clusters.csv'.")