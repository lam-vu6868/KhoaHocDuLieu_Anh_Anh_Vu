import pandas as pd
import numpy as np
import os
import unicodedata

# --- Hàm chuẩn hóa Tiếng Việt (Giữ nguyên) ---
def chuan_hoa_tieng_viet(text):
    if pd.isna(text): return text
    text = str(text).replace('Đ', 'D').replace('đ', 'd')
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
    return text.upper().strip()

# =====================================================================
# BƯỚC 0: THIẾT LẬP & KHÁM PHÁ CHI TIẾT
# =====================================================================
RAW_PATH = 'data/raw/data.xlsx'
df_id = pd.read_excel(RAW_PATH, sheet_name='ID')
df_data = pd.read_excel(RAW_PATH, sheet_name='DATA')

print("📊 [KHÁM PHÁ BAN ĐẦU] BÁO CÁO TÌNH TRẠNG DỮ LIỆU THÔ:")
print(f"- Tổng sản phẩm ban đầu: {len(df_id)} dòng")
print(f"- Số cột bảng DATA: {len(df_data.columns)}")
print(f"- Tỷ lệ thiếu Brand: {(df_data['brand'].isna().sum()/len(df_data)*100):.2f}%")
print(f"- Số máy có giá gốc bị bằng 0: {(df_data['original_price'] == 0).sum()} dòng")
print(f"- Khoảng giá bán: {df_data['original_price'].min():,}đ đến {df_data['original_price'].max():,}đ")
print("-" * 60)

# =====================================================================
# BƯỚC 1: LỌC SẢN PHẨM & CHUẨN HÓA ĐỊA DANH
# =====================================================================
print("🧹 Đang lọc sản phẩm không phải điện thoại & chuẩn hóa địa danh...")
keywords = 'điện thoại|smartphone|iphone|samsung|xiaomi|oppo|vivo|realme|nokia|tecno'
df_id_clean = df_id[df_id['name'].str.contains(keywords, case=False, na=False)].copy()
df_id_clean['shop_location'] = df_id_clean['shop_location'].apply(chuan_hoa_tieng_viet)

# =====================================================================
# BƯỚC 2: XỬ LÝ BRAND & GIÁ TIỀN 
# =====================================================================
print("🧹 Đang cứu vãn Brand, gán UNKNOWN và xử lý giá tiền...")
df_data_clean = df_data.copy()

# 2.1 Cứu Brand từ tên SP
brands_list = 'samsung|nokia|xiaomi|oppo|vivo|realme|apple|iphone|tecno|infinix|asus'
hang_tim_thay = df_id_clean['name'].str.extract(f'(?i)({brands_list})', expand=False)

# Đắp hãng tìm được vào chỗ trống
df_data_clean['brand'] = df_data_clean['brand'].fillna(hang_tim_thay)

# 🚨 BỔ SUNG: Gán 'UNKNOWN' cho các dòng vẫn trống
df_data_clean['brand'] = df_data_clean['brand'].fillna('UNKNOWN')

# Đồng nhất tên gọi và Viết hoa toàn bộ
df_data_clean['brand'] = df_data_clean['brand'].str.upper()
df_data_clean['brand'] = df_data_clean['brand'].replace('IPHONE', 'APPLE')

# 2.2 Xử lý giá & Lọc máy
df_data_clean.loc[df_data_clean['original_price'] == 0, 'original_price'] = df_data_clean['discount_price']

# Đưa về đơn vị Triệu VNĐ trước cho dễ tính toán IQR
df_data_clean['original_price'] /= 100000
df_data_clean['discount_price'] /= 100000

# Lọc phần đáy: Bỏ hẳn máy < 1 triệu (Loại bỏ phụ kiện/ốp lưng)
df_data_clean = df_data_clean[df_data_clean['original_price'] >= 1000000]

# --- HÀM XỬ LÝ NGOẠI LAI BẰNG IQR ---
print("🧹 Đang quét và loại bỏ giá ảo (Ngoại lai) bằng thuật toán IQR...")

# Tính Q1 (25%) và Q3 (75%)
Q1 = df_data_clean['original_price'].quantile(0.25)
Q3 = df_data_clean['original_price'].quantile(0.75)
IQR = Q3 - Q1

# Tính mức trần (Upper Bound)
# Thường công thức là Q3 + 1.5*IQR. 
# Nhưng với đồ công nghệ, giá phân tán rộng nên dùng hệ số 3.0 (Extreme Outliers) cho an toàn, tránh xóa nhầm máy Flagship.
upper_bound = Q3 + 3.0 * IQR 

# Lọc bỏ các dòng có giá vượt quá mức trần (Xóa bỏ ngoại lai)
so_luong_truoc = len(df_data_clean)
df_data_clean = df_data_clean[df_data_clean['original_price'] <= upper_bound]
so_luong_xoa = so_luong_truoc - len(df_data_clean)

print(f"✅ Đã xóa {so_luong_xoa} sản phẩm có giá ảo (lớn hơn {upper_bound:.1f}  VNĐ).")

# Xử lý discount
df_data_clean['discount'] = pd.to_numeric(df_data_clean['discount'].astype(str).str.replace('%',''), errors='coerce').fillna(0) / 100

# =====================================================================
# BƯỚC 3: GỘP BẢNG (1-1) & XUẤT FILE
# =====================================================================
print("🔗 Đang gộp bảng và kiểm tra lần cuối...")
df_final = pd.merge(df_id_clean[['item_id', 'shop_id', 'shop_location']], 
                     df_data_clean[['item_id', 'shop_id', 'brand', 'sold_quantity', 'discount_price', 
                                   'original_price', 'discount', 'liked_count', 'rating_star', 'number_of_ratings']], 
                     on=['item_id', 'shop_id'], how='inner')


print(f"✅ HOÀN TẤT! Data sạch còn lại: {len(df_final)} dòng.")
print(f"- Khoảng giá gốc: {df_final['original_price'].min():,}đ đến {df_final['original_price'].max():,}đ")
print(f"- Khoảng giá thực tế: {df_final['discount_price'].min():,}đ đến {df_final['discount_price'].max():,}đ")
print(f"Báo cáo cột:\n{df_final.dtypes}")
df_final.to_csv('data/processed/data_cleaned.csv', index=False)