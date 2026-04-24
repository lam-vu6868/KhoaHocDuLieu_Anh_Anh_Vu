"""""
BƯỚC 0: CHUẨN BỊ DỮ LIỆU
Làm sạch 3 sheet, xử lý NULL, tạo features, ghép thành 1 dataset hoàn chỉnh
Output: data_cleaned.csv (3,060 × 24 cols, 0 NULLs)
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ========== LOAD 3 SHEET TỪ DATA.XLSX ==========
print("=" * 60)
print("BƯỚC 0: CHUẨN BỊ DỮ LIỆU")
print("=" * 60)

try:
    df_id = pd.read_excel('data.xlsx', sheet_name='ID')
    df_data = pd.read_excel('data.xlsx', sheet_name='DATA')
    df_rating = pd.read_excel('data.xlsx', sheet_name='RATING')
    print("✅ Load 3 sheet thành công")
    print(f"   ID: {df_id.shape} | DATA: {df_data.shape} | RATING: {df_rating.shape}")
except Exception as e:
    print(f"❌ Lỗi load file: {e}")
    exit()

# ========== XỬ LÝ NULL - SHEET DATA ==========
print("\n--- Xử lý NULL - Sheet DATA ---")

# Vấn đề 1: brand NULL
null_brand = df_data['brand'].isna().sum()
print(f"1. brand NULL: {null_brand} ({null_brand/len(df_data)*100:.1f}%)")
df_data['brand'] = df_data['brand'].fillna('Unknown')
print(f"   ✅ Xử lý: Gán 'Unknown'")

# Vấn đề 2: original_price = 0
null_orig_price = (df_data['original_price'] == 0).sum()
print(f"\n2. original_price = 0: {null_orig_price} ({null_orig_price/len(df_data)*100:.1f}%)")
df_data.loc[df_data['original_price'] == 0, 'original_price'] = \
    df_data.loc[df_data['original_price'] == 0, 'discount_price']
print(f"   ✅ Xử lý: Gán = discount_price")

# Vấn đề 3: discount NULL
null_discount = df_data['discount'].isna().sum()
print(f"\n3. discount NULL: {null_discount} ({null_discount/len(df_data)*100:.1f}%)")
df_data['discount'] = df_data['discount'].fillna('0%')

# Extract %
def extract_discount_pct(s):
    if isinstance(s, str) and '%' in s:
        try:
            return int(s.replace('%', ''))
        except:
            return 0
    return 0

df_data['discount_pct'] = df_data['discount'].apply(extract_discount_pct)

# Tính lại nếu discount_pct = 0
calculated = ((df_data['original_price'] - df_data['discount_price']) / 
              (df_data['original_price'] + 1) * 100).astype(int)
df_data.loc[df_data['discount_pct'] == 0, 'discount_pct'] = calculated[df_data['discount_pct'] == 0]

print(f"   ✅ Xử lý: Tính lại từ công thức")

# ========== XỬ LÝ NULL - SHEET RATING ==========
print("\n--- Xử lý NULL - Sheet RATING ---")

null_user = df_rating['user_name'].isna().sum()
print(f"1. user_name NULL: {null_user} ({null_user/len(df_rating)*100:.1f}%)")
df_rating['user_name'] = df_rating['user_name'].fillna('Anonymous')
print(f"   ✅ Xử lý: Gán 'Anonymous'")

null_comment = df_rating['comment'].isna().sum()
print(f"2. comment NULL: {null_comment} ({null_comment/len(df_rating)*100:.1f}%)")
df_rating['comment'] = df_rating['comment'].fillna('')
print(f"   ✅ Xử lý: Gán ''")

# ========== AGGREGATE RATING ==========
print("\n--- Aggregate Sheet RATING ---")

df_rating['has_comment'] = (df_rating['comment'] != '').astype(int)

rating_agg = df_rating.groupby('item_id').agg({
    'rating_star': ['mean', 'std', 'count'],
    'has_comment': 'mean'
}).reset_index()

rating_agg.columns = ['item_id', 'avg_rating_from_comments', 
                      'std_rating_from_comments', 'count_comments', 'comment_ratio']
rating_agg['comment_ratio'] = rating_agg['comment_ratio'] * 100

print(f"✅ Aggregate: {len(df_rating):,} ratings → {len(rating_agg):,} products")
print(f"   Trung bình comment/product: {rating_agg['count_comments'].mean():.1f}")

# ========== MERGE 3 SHEET ==========
print("\n--- Merge 3 Sheet ---")

# Merge ID + DATA
df_merged = pd.merge(df_id, df_data, on=['item_id', 'shop_id'], how='inner')
print(f"1. ID + DATA: {df_merged.shape} rows × cols")

# Merge + RATING
df_final = pd.merge(df_merged, rating_agg, on='item_id', how='left')
print(f"2. + RATING: {df_final.shape} rows × cols")

# Fill NaN (sản phẩm không có comment)
df_final['avg_rating_from_comments'] = df_final['avg_rating_from_comments'].fillna(df_final['rating_star'])
df_final['std_rating_from_comments'] = df_final['std_rating_from_comments'].fillna(0)
df_final['count_comments'] = df_final['count_comments'].fillna(0).astype(int)
df_final['comment_ratio'] = df_final['comment_ratio'].fillna(0)

print(f"3. Fill NaN: {df_final.isna().sum().sum()} NULLs remaining")

# ========== TẠO FEATURES BỔ SUNG ==========
print("\n--- Tạo Features bổ sung ---")

# 1. Price ratio
df_final['price_ratio'] = df_final['discount_price'] / (df_final['original_price'] + 1)
print(f"1. price_ratio (discount intensity) ✅")

# 2. Revenue proxy
df_final['revenue_proxy'] = df_final['sold_quantity'] * df_final['discount_price']
print(f"2. revenue_proxy (estimated revenue) ✅")

# 3. Popularity score
liked_norm = (df_final['liked_count'] - df_final['liked_count'].min()) / \
             (df_final['liked_count'].max() - df_final['liked_count'].min() + 1)
rating_norm = (df_final['number_of_ratings'] - df_final['number_of_ratings'].min()) / \
              (df_final['number_of_ratings'].max() - df_final['number_of_ratings'].min() + 1)
df_final['popularity_score'] = (liked_norm + rating_norm) / 2
print(f"3. popularity_score (normalized) ✅")

# 4. Brand category
top_brands = df_final['brand'].value_counts().head(5).index.tolist()
df_final['brand_category'] = df_final['brand'].apply(lambda x: x if x in top_brands else 'Others')
print(f"4. brand_category (Top 5 + Others) ✅")

# ========== EXPORT & KIỂM TRA ==========
print("\n--- Export & Kiểm tra ---")

df_final.to_csv('processed_data/data_cleaned.csv', index=False, encoding='utf-8')
print(f"✅ Export: processed_data/data_cleaned.csv")
print(f"   Shape: {df_final.shape[0]:,} rows × {df_final.shape[1]} cols")
print(f"   NULLs: {df_final.isna().sum().sum()}")

# Thông tin chi tiết
info_text = f"""=== THÔNG TIN DỮ LIỆU SAU XỬ LÝ ===
Số dòng: {df_final.shape[0]:,}
Số cột: {df_final.shape[1]}

DANH SÁCH CỘT:
{', '.join(df_final.columns.tolist())}

LOẠI DỮ LIỆU:
{df_final.dtypes.to_string()}

THỐNG KÊ MÔ TẢ:
{df_final.describe().to_string()}

TỔNG NULL:
{df_final.isna().sum().to_string()}
"""

with open('processed_data/data_eda_info.txt', 'w', encoding='utf-8') as f:
    f.write(info_text)

print(f"✅ Export: processed_data/data_eda_info.txt")

print("\n" + "=" * 60)
print("✅ BƯỚC 0 HOÀN THÀNH!")
print("=" * 60)
print("\n📊 Dataset sạch: data_cleaned.csv (3,060 × 24 cols)")
print("💾 Tiếp theo: Chạy 1_eda_analysis.py")

