# 📋 HƯỚNG DẪN LÀM SẠCH DỮ LIỆU (Với Ghi Chú Tiếng Việt)

## 1. TỔNG QUAN 3 SHEET

### Sheet "ID" (3,060 rows × 4 cột)

| Cột               | Ghi Chú Tiếng Việt                   | Ví Dụ                       |
| ----------------- | ------------------------------------ | --------------------------- |
| **item_id**       | Mã sản phẩm - dùng để ghép các sheet | 12345                       |
| **shop_id**       | Mã cửa hàng trên Shopee              | 67890                       |
| **shop_location** | Tỉnh/Thành phố nơi cửa hàng bán      | "TP. Hồ Chí Minh", "Hà Nội" |
| **name**          | Tên sản phẩm/Model điện thoại        | "iPhone 15", "Galaxy S24"   |

**⚠️ Vấn Đề NULL:** Ít gặp (dữ liệu ID thường đầy đủ)

---

### Sheet "DATA" (3,060 rows × 12 cột)

| Cột                   | Ghi Chú Tiếng Việt        | Ví Dụ              | Vấn Đề      |
| --------------------- | ------------------------- | ------------------ | ----------- |
| **item_id**           | Mã sản phẩm (ghép với ID) | 12345              | -           |
| **shop_id**           | Mã cửa hàng               | 67890              | -           |
| **brand**             | Hãng sản xuất             | "Apple", "Samsung" | 🔴 28% NULL |
| **sold_quantity**     | Số lượng bán ra           | 500                | -           |
| **stock**             | Tồn kho hiện tại          | 100                | -           |
| **original_price**    | Giá gốc (trước giảm)      | 30M VNĐ            | 🔴 57% = 0  |
| **discount_price**    | Giá bán hiện tại          | 25M VNĐ            | -           |
| **discount**          | Phần trăm giảm            | "16%", "20%"       | 🔴 57% NULL |
| **liked_count**       | Số lượt "thích"           | 1000               | -           |
| **rating_star**       | Điểm đánh giá TB          | 4.8                | -           |
| **number_of_ratings** | Số lượt đánh giá          | 500                | -           |

---

### Sheet "RATING" (61,472 rows × 6 cột)

| Cột             | Ghi Chú Tiếng Việt      | Ví Dụ          | Vấn Đề        |
| --------------- | ----------------------- | -------------- | ------------- |
| **item_id**     | Mã sản phẩm (ghép DATA) | 12345          | -             |
| **order_id**    | Mã đơn hàng             | "111222333"    | -             |
| **user_name**   | Tên khách hàng          | "Nguyễn Văn A" | 🔴 2.9% NULL  |
| **comment**     | Bình luận/Phản hồi      | "Sản phẩm tốt" | 🔴 25.7% NULL |
| **rating_star** | Điểm đánh giá           | 5, 4, 3        | -             |

---

## 2. BƯỚC 0.5: KHÁM PHÁ DỮ LIỆU LẦN 1 (Vì Sao Cần?)

### 📌 Tại Sao PHẢI Khám Phá TRƯỚC Khi Làm Sạch?

| Lý Do                   | Chi Tiết                                                  | Hậu Quả Nếu Bỏ Qua                  |
| ----------------------- | --------------------------------------------------------- | ----------------------------------- |
| **Phát hiện vấn đề**    | Biết chính xác lỗi ở đâu (NULL, lỗi type, outliers)       | Làm sạch không đúng, mất dữ liệu    |
| **Hiểu cấu trúc**       | Shape (3,060×12), kiểu dữ liệu, mối quan hệ               | Merge sai → phùng hoặc mất sản phẩm |
| **Quyết định xử lý**    | NULL 28% → nên điền hay xóa? → Quyết định dựa dữ liệu     | Xóa hết → mất 856 sản phẩm vô tình  |
| **Tránh mất thông tin** | Biết giá trị "0" có ý nghĩa hay là lỗi (original_price=0) | Xử lý sai, thông tin sai lệch       |
| **Lập chiến lược**      | Biết đặc tính trước → có thể lên kế hoạch tối ưu          | Làm vội → kết quả tệ                |

### 🔍 Các Câu Hỏi Khám Phá:

```python
# 1️⃣ Cấu trúc chung:
df_id.shape          # → (3060, 4)
df_id.dtypes         # → item_id: int, shop_location: str, ...
df_id.info()         # → Tổng hợp trên

# 2️⃣ NULL phân bố:
df_data['brand'].isna().sum()           # → 856 NULL (28%)
df_data['original_price'].isna().sum()  # → Bao nhiêu NULL?

# 3️⃣ Giá trị lạ:
df_data['original_price'].describe()    # → min, max, mean
(df_data['original_price'] == 0).sum()  # → 1,742 giá trị = 0

# 4️⃣ Mối quan hệ:
df_rating['item_id'].nunique()          # → Bao nhiêu sản phẩm có rating?
df_rating['item_id'].value_counts()     # → 1 sản phẩm có mấy rating?

# 5️⃣ Tiến độ khám phá:
df_id.set_index('item_id').index.isin(df_data['item_id']).sum()
→ Kiểm tra: Tất cả item_id ở DATA có ở ID không?
```

### 📊 Kết Quả Khám Phá Expected:

| Khám Phá                  | Kết Quả Expected                           | Hành Động Tiếp            |
| ------------------------- | ------------------------------------------ | ------------------------- |
| **NULL brand**            | ~856 NULL (28%)                            | Điền "Unknown"            |
| **original_price = 0**    | ~1,742 giá trị = 0                         | Gán = discount_price      |
| **discount NULL**         | ~1,742 NULL                                | Tính lại công thức        |
| **1 sản phẩm = ? rating** | Trung bình 20 rating/sản phẩm              | Aggregate trước khi merge |
| **item_id trùng**         | ID có 3,060 unique; RATING có 3,060 unique | Merge 1:1 an toàn ✅      |

---

## 3. CHI TIẾT XỬ LÝ CÁC VẤN ĐỀ NULL

### 🔴 Vấn Đề 1: `brand` NULL (~28%)

```
📌 LÝ DO: Sản phẩm không có thông tin hãng sản xuất
📌 XỬ LÝ: Gán "Unknown" (Không xác định)
📌 LÝ DO CHỌN: Giữ dòng dữ liệu, không mất thông tin sản phẩm
📌 CODE: df_data['brand'] = df_data['brand'].fillna('Unknown')
📌 KẾT QUẢ: 3,060 sản phẩm, 0 NULL ✅
```

### 🔴 Vấn Đề 2: `original_price` = 0 (~57%)

```
📌 LÝ DO: Dữ liệu lỗi hoặc sản phẩm không giảm giá
📌 VÍ DỤ: discount_price = 100,000 nhưng original_price = 0 → Vô lý
📌 XỬ LÝ: Gán original_price = discount_price
📌 LÝ DO: Coi sản phẩm không giảm (giá gốc = giá bán hiện tại)
📌 CODE:
   df_data.loc[df_data['original_price'] == 0, 'original_price'] = \
       df_data.loc[df_data['original_price'] == 0, 'discount_price']
```

### 🔴 Vấn Đề 3: `discount` NULL (~57%)

```
📌 LÝ DO: Vì original_price = 0, không tính được % giảm
📌 XỬ LÝ:
   - Gán mặc định "0%"
   - Tính lại từ công thức toán
📌 CODE:
   df_data['discount'] = df_data['discount'].fillna('0%')
   discount_pct = ((original - discount) / original * 100)
```

### 🔴 Vấn Đề 4: Sheet RATING - `user_name` NULL (~2.9%)

```
📌 LÝ DO: Khách hàng vô danh
📌 XỬ LÝ: Gán "Anonymous"
📌 CODE: df_rating['user_name'] = df_rating['user_name'].fillna('Anonymous')
```

### 🔴 Vấn Đề 5: Sheet RATING - `comment` NULL (~25.7%)

```
📌 LÝ DO: Khách đánh giá nhưng không viết bình luận
📌 XỬ LÝ: Giữ nguyên (gán "") - rating_star vẫn có
📌 CODE: df_rating['comment'] = df_rating['comment'].fillna('')
```

---

## 3. CHIẾN LƯỢC GỘP 3 SHEET (QUAN TRỌNG)

### ❌ SAI: Gộp trực tiếp → PHÙNG DỮ LIỆU

```
ID: 3,060 rows
DATA: 3,060 rows (1:1 với ID)
RATING: 61,472 rows (1 sản phẩm = nhiều bình luận)

Nếu merge: 3,060 × 61,472 = 187 TRIỆU rows ☠️ PHÙNG!
Lý do: 1 sản phẩm có 20 bình luận → lặp 20 lần
```

### ✅ ĐÚNG: Aggregate RATING trước

```
BƯỚC 1: Tóm tắt 61,472 bình luận → 3,060 summary
  item_id=1 → [5,4,5,5,...] (20 bình luận)
  Thành: item_id=1 → avg_rating=4.75, count=20, std=0.43

BƯỚC 2: Merge tuần tự
  Step 1: ID + DATA (1:1) → 3,060 rows
  Step 2: (ID+DATA) + RATING_agg (1:1) → 3,060 rows ✅

CODE:
  rating_agg = df_rating.groupby('item_id').agg({
      'rating_star': ['mean', 'std', 'count']
  }).reset_index()

  df_merged = pd.merge(df_id, df_data, on=['item_id', 'shop_id'])
  df_final = pd.merge(df_merged, rating_agg, on='item_id')
```

---

## 4. FEATURES MỚI TẠO THÊM

| Feature              | Công Thức                       | Ý Nghĩa                |
| -------------------- | ------------------------------- | ---------------------- |
| **price_ratio**      | discount_price / original_price | Bao nhiêu % giá so gốc |
| **revenue_proxy**    | sold_qty × discount_price       | Ước tính doanh thu     |
| **popularity_score** | (likes_norm + ratings_norm) / 2 | Độ phổ biến 0-1        |
| **brand_category**   | Top 5 brand + "Others"          | Gộp brand nhỏ          |

---

## 5. KIỂM TRA CUỐI CÙNG

| Check       | Kỳ Vọng | Tại Sao                     |
| ----------- | ------- | --------------------------- |
| Số rows     | 3,060   | Không mất sản phẩm nào      |
| Số cột      | ~24     | Có đủ features để phân tích |
| NULL values | 0       | Dữ liệu sạch 100%           |
| Duplicates  | 0       | Không item_id trùng         |

---

**📌 TÓM TẮT:**

1. ✅ Xử lý NULL từng sheet (brand, original_price, discount, user_name, comment)
2. ✅ Aggregate RATING TRƯỚC khi merge (tránh phùng)
3. ✅ Merge tuần tự: ID+DATA → +RATING_agg
4. ✅ Output: data_cleaned.csv (3,060 × 24 cols, 0 NULL)
