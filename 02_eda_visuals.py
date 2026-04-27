import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =====================================================================
# THIẾT LẬP MÔI TRƯỜNG VÀ ĐƯỜNG DẪN
# =====================================================================
os.makedirs('outputs/figures', exist_ok=True)

print("Đang đọc dữ liệu sạch...")
df = pd.read_csv('data/processed/data_cleaned.csv')

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'

print("Đang vẽ biểu đồ...")

# 1. BIỂU ĐỒ BAR CHART: TOP 10 HÃNG BÁN CHẠY NHẤT
plt.figure(figsize=(10, 6))
top_brands = df.groupby('brand')['sold_quantity'].sum().sort_values(ascending=False).head(10)
sns.barplot(x=top_brands.values, y=top_brands.index, hue=top_brands.index, palette='viridis', legend=False)
plt.title('Top 10 Thương hiệu có Doanh số cao nhất trên Shopee', fontsize=14, fontweight='bold')
plt.xlabel('Tổng số lượng máy đã bán', fontsize=12)
plt.ylabel('Thương hiệu', fontsize=12)
plt.tight_layout()
plt.savefig('outputs/figures/1_top_brands.png', dpi=300)
plt.close()

# 2. BIỂU ĐỒ HISTOGRAM: PHÂN BỐ DOANH SỐ
plt.figure(figsize=(10, 6))
sns.histplot(df['sold_quantity'], bins=50, kde=True, log_scale=True, color='coral')
plt.title('Phân bố Số lượng bán ra (Log Scale)', fontsize=14, fontweight='bold')
plt.xlabel('Số lượng đã bán (Log)', fontsize=12)
plt.ylabel('Số lượng mã sản phẩm', fontsize=12)
plt.tight_layout()
plt.savefig('outputs/figures/2_sales_distribution.png', dpi=300)
plt.close()

# 3. BIỂU ĐỒ SCATTER: QUAN HỆ GIỮA GIÁ BÁN VÀ DOANH SỐ
plt.figure(figsize=(10, 6))
gia_trieu_vnd = df['discount_price'] / 1000000 
sns.scatterplot(x=gia_trieu_vnd, y=df['sold_quantity'], alpha=0.5, color='teal')
plt.title('Mối quan hệ giữa Giá thực tế và Sức mua', fontsize=14, fontweight='bold')
plt.xlabel('Giá bán thực tế (Triệu VNĐ)', fontsize=12)
plt.ylabel('Số lượng đã bán', fontsize=12)
plt.tight_layout()
plt.savefig('outputs/figures/3_price_vs_sales.png', dpi=300)
plt.close()

# 4. MA TRẬN TƯƠNG QUAN (HEATMAP)
plt.figure(figsize=(10, 8))
cols_so = ['original_price', 'discount_price', 'discount', 'sold_quantity', 'liked_count', 'rating_star', 'number_of_ratings']
corr_matrix = df[cols_so].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Ma trận Tương quan (Heatmap) giữa các biến số', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('outputs/figures/4_correlation_heatmap.png', dpi=300)
plt.close()

print("✅ Đã vẽ xong các sơ đồ! Các ảnh được lưu trong thư muc output/figures/ !")