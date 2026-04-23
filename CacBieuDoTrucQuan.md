# 📊 HƯỚNG DẪN CHỌN 9 BIỂU ĐỒ TRỰC QUAN (Với Ghi Chú Tiếng Việt)

## 1. TẠI SAO CẦN 9 BIỂU ĐỒ?

### 🔄 Quy Trình Phân Tích Dữ Liệu:

```
BƯỚC 0: Khám phá dữ liệu (file: 01_DATA_CLEANING_GUIDE.md)
   ↓
BƯỚC 1: LÀM SẠCH (Xử lý NULL, outliers, type)
   ↓
BƯỚC 2: KHÁM PHÁ LẦN 2 - EDA + Trực Quan (9 BIỂU ĐỒ NÀY)
   ├─ 3 biểu đồ EDA (phân bố, top brands, rating)
   ├─ 3 biểu đồ tương quan (tìm yếu tố ảnh hưởng)
   ├─ 2 biểu đồ clustering (phân nhóm khách)
   └─ 1 biểu đồ feature importance (ưu tiên cải thiện)
   ↓
BƯỚC 3: Phân tích thống kê (hypothesis testing)
   ↓
BƯỚC 4: PCA + Clustering
   ↓
BƯỚC 5: Regression + Dự báo
   ↓
BƯỚC 6: Báo cáo & Marketing strategy
```

### 📌 9 Biểu Đồ Trả Lời CÁC CÂU HỎI CHỦ YẾU:

| Giai Đoạn      | Câu Hỏi Chủ Yếu                              | Biểu Đồ Trả Lời |
| -------------- | -------------------------------------------- | --------------- |
| **EDA**        | Thị trường điện thoại Shopee như thế nào?    | 1, 2, 3         |
| **Tương Quan** | Yếu tố nào ảnh hưởng tới bán hàng?           | 4, 5, 6         |
| **Phân Nhóm**  | Có mấy loại khách? Phân khúc nào?            | 7, 8            |
| **Ưu Tiên**    | Marketing strategy nên tập trung vào cái gì? | 9               |

---

## 2. LỰA CHỌN BIỂU ĐỒ

```
❌ KHÔNG: Lấy hết 20+ biểu đồ (quá nhiều, khó trình bày)
✅ ĐÚNG: Lấy 9 biểu đồ trả lời các câu hỏi kinh doanh quan trọng
```

---

## 2. 9 BIỂU ĐỒ CHÍNH

### 📈 PHẦN 1: KHÁM PHÁ DỮ LIỆU (3 biểu đồ)

#### **Biểu Đồ 1: Phân Bố Doanh Số (Sold Quantity)**

| Thông Tin   | Chi Tiết                                                          |
| ----------- | ----------------------------------------------------------------- |
| **Tên**     | Histogram - Phân bố số lượng sản phẩm bán ra                      |
| **Kiểu**    | 2 Histogram cạnh nhau                                             |
| **Trái**    | Dữ liệu gốc (thường lệch phải)                                    |
| **Phải**    | Log scale (để so sánh)                                            |
| **Trục X**  | sold_quantity (bao nhiêu sản phẩm bán)                            |
| **Trục Y**  | Tần suất (bao nhiêu sản phẩm cùng mức bán)                        |
| **Câu Hỏi** | Doanh số phân bố như thế nào? Lệch phải? Chuẩn hóa?               |
| **Lý Do**   | sold_qty là Y (mục tiêu) - cần hiểu để chọn model                 |
| **Insight** | Nếu lệch phải → dùng log transform; Nếu chuẩn → linear regression |

---

#### **Biểu Đồ 2: Top 10 Địa Điểm & Hãng**

| Thông Tin   | Chi Tiết                                                 |
| ----------- | -------------------------------------------------------- |
| **Tên**     | Bar Chart Ngang - Top 10 Địa Điểm & Hãng                 |
| **Kiểu**    | 2 Horizontal Bar Chart                                   |
| **Bar 1**   | Top 10 shop_location (TP. HCM, Hà Nội, ...)              |
| **Bar 2**   | Top 10 brand_category (Apple, Samsung, ...)              |
| **Trục X**  | Số lượng sản phẩm                                        |
| **Trục Y**  | Tên địa điểm / Tên hãng                                  |
| **Câu Hỏi** | Thị trường (tỉnh/hãng) nào bán chạy nhất?                |
| **Lý Do**   | Input cho chiến lược marketing - tập trung ở đâu         |
| **Insight** | "TP. HCM bán chạy 1,200 sản phẩm", "Apple phổ biến nhất" |

---

#### **Biểu Đồ 3: Phân Bố Rating Sao**

| Thông Tin   | Chi Tiết                                                      |
| ----------- | ------------------------------------------------------------- |
| **Tên**     | Histogram - Phân bố điểm đánh giá                             |
| **Kiểu**    | Histogram                                                     |
| **Trục X**  | rating_star (0 → 5 sao)                                       |
| **Trục Y**  | Tần suất (bao nhiêu sản phẩm)                                 |
| **Câu Hỏi** | Khách Shopee cho mấy sao? Phần lớn 5 sao?                     |
| **Lý Do**   | Rating là feature quan trọng, ảnh hưởng bán hàng              |
| **Pattern** | Thường lệch trái (phần lớn 5 sao)                             |
| **Insight** | Khách Shopee dễ dãi (hay đánh giá cao) → rating không tin cậy |

---

### 🔍 PHẦN 2: TƯƠNG QUAN (3 biểu đồ)

#### **Biểu Đồ 4: Heatmap Tương Quan**

| Thông Tin      | Chi Tiết                                                 |
| -------------- | -------------------------------------------------------- |
| **Tên**        | Correlation Heatmap - Tương quan giữa features           |
| **Kiểu**       | Heatmap (ma trận màu)                                    |
| **Màu**        | Xanh (tương quan dương) → Đỏ (âm) → Trắng (0)            |
| **Trục X & Y** | Tên các biến (discount_price, rating, liked_count, v.v.) |
| **Giá Trị**    | -1 (âm hoàn toàn) → 0 (không) → +1 (dương hoàn toàn)     |
| **Câu Hỏi**    | Feature nào có tương quan MẠNH với sold_qty?             |
| **Lý Do**      | Tìm yếu tố nào ảnh hưởng nhất; Tìm đa cộng tuyến         |
| **Insight**    | Nếu number_of_ratings = 0.7 → rất ảnh hưởng              |

---

#### **Biểu Đồ 5: Rating vs Doanh Số (Scatter)**

| Thông Tin   | Chi Tiết                                  |
| ----------- | ----------------------------------------- |
| **Tên**     | Scatter Plot - Rating và Doanh Số         |
| **Kiểu**    | Scatter + tô màu theo liked_count         |
| **Trục X**  | rating_star (0-5)                         |
| **Trục Y**  | Log(sold_quantity)                        |
| **Màu**     | liked_count (càng đỏ = càng nhiều like)   |
| **Câu Hỏi** | Rating cao → bán nhiều? Quan hệ thế nào?  |
| **Lý Do**   | Thấy mối quan hệ 2 biến; Có outliers?     |
| **Pattern** | Thường KHÔNG rõ (5 sao ≠ bán nhiều)       |
| **Insight** | Khách 5 sao ít mua; 3-4 sao mua nhiều hơn |

---

#### **Biểu Đồ 6: Giá vs Doanh Số (Scatter)**

| Thông Tin   | Chi Tiết                                                 |
| ----------- | -------------------------------------------------------- |
| **Tên**     | Scatter Plot - Giá và Doanh Số                           |
| **Kiểu**    | Scatter                                                  |
| **Trục X**  | Log(discount_price) - dùng log vì phân bố rộng           |
| **Trục Y**  | Log(sold_quantity)                                       |
| **Câu Hỏi** | Giá rẻ → bán nhiều? Giá đắt → bán ít? (Price elasticity) |
| **Lý Do**   | Tìm quan hệ giá-doanh; Tối ưu giá bán                    |
| **Pattern** | Thường âm (giá cao ↔ bán ít)                             |
| **Insight** | Có thể điều chỉnh giá để tối ưu doanh số                 |

---

### 🎯 PHẦN 3: PHÂN NHÓM (2 biểu đồ)

#### **Biểu Đồ 7: Elbow & Silhouette**

| Thông Tin   | Chi Tiết                                             |
| ----------- | ---------------------------------------------------- |
| **Tên**     | Elbow Method + Silhouette Score                      |
| **Kiểu**    | 2 Line Plot cạnh nhau                                |
| **Plot 1**  | X: K (1-10), Y: Inertia (tổng khoảng cách)           |
| **Plot 2**  | X: K (1-10), Y: Silhouette (chất lượng 0-1)          |
| **Elbow**   | Nơi inertia "gập" (K tối ưu)                         |
| **Câu Hỏi** | Nên chia bao nhiêu nhóm? K=3? K=4?                   |
| **Lý Do**   | Phân khúc khách = tìm K tối ưu                       |
| **Insight** | K=3 hoặc K=4 thường tốt nhất; Silhouette > 0.5 = tốt |

---

#### **Biểu Đồ 8: 2D Clusters Visualization**

| Thông Tin   | Chi Tiết                                |
| ----------- | --------------------------------------- |
| **Tên**     | Scatter 2D - Các Cluster                |
| **Kiểu**    | Scatter (PC1 vs PC2)                    |
| **Trục X**  | PC1 (nhân tố chính 1)                   |
| **Trục Y**  | PC2 (nhân tố chính 2)                   |
| **Màu**     | Cluster (mỗi cluster = 1 màu)           |
| **Marker**  | Centroids = "X" đỏ lớn                  |
| **Câu Hỏi** | Cluster tách riêng không? Bị lẫn không? |
| **Lý Do**   | Xem trực quan kết quả phân nhóm         |
| **Tín Cậy** | Tách rõ ✅ → tốt; Lẫn lộn ❌ → kém      |

---

### 📉 PHẦN 4: YẾU TỐ QUAN TRỌNG (1 biểu đồ)

#### **Biểu Đồ 9: Feature Importance**

| Thông Tin    | Chi Tiết                                                                   |
| ------------ | -------------------------------------------------------------------------- |
| **Tên**      | Bar Chart - Feature Importance                                             |
| **Kiểu**     | Horizontal Bar Chart (xếp ngang)                                           |
| **Trục X**   | Importance Score (0-1)                                                     |
| **Trục Y**   | Tên features                                                               |
| **Model**    | Random Forest (tree-based, không bị scale ảnh hưởng)                       |
| **Hiển Thị** | Top 10 features (còn lại quá thấp)                                         |
| **Câu Hỏi**  | Feature nào ảnh hưởng nhất tới doanh số?                                   |
| **Lý Do**    | Biết nên ưu tiên cải thiện cái gì                                          |
| **Insight**  | "number_of_ratings" (0.6) → tăng review; "brand" (0.02) → không quan trọng |

---

## 3. TÓMI TẮT BẢNG 9 BIỂU ĐỒ

| #   | Tên                | Kiểu        | Trả Lời Câu Hỏi                 |
| --- | ------------------ | ----------- | ------------------------------- |
| 1   | Phân bố doanh số   | Histogram 2 | Doanh số lệch phải? Chuẩn?      |
| 2   | Top địa điểm/hãng  | 2 Bar chart | Thị trường mạnh? Hãng bán chạy? |
| 3   | Phân bố rating     | Histogram   | Khách cho mấy sao? Lệch trái?   |
| 4   | Heatmap tương quan | Heatmap     | Feature nào tương quan mạnh?    |
| 5   | Rating vs Doanh số | Scatter     | Rating cao → bán nhiều?         |
| 6   | Giá vs Doanh số    | Scatter     | Giá rẻ → bán nhiều?             |
| 7   | Elbow + Silhouette | 2 Line plot | Chia bao nhiêu nhóm?            |
| 8   | 2D Clusters        | Scatter 2D  | Cluster tách riêng?             |
| 9   | Feature Importance | Bar chart   | Yếu tố gì quan trọng nhất?      |

---

## 4. LÝ DO LOẠI BỎ CÁC BIỂU ĐỒ KHÁC

| Biểu Đồ Bị Loại          | Lý Do                                                 |
| ------------------------ | ----------------------------------------------------- |
| Boxplot by brand         | Dư thừa với Bar chart + Scatter; Khó giải thích       |
| Biplot PCA               | Kỹ thuật cao, khó hiểu; Không phải câu hỏi kinh doanh |
| Silhouette plot chi tiết | Chỉ cần silhouette score trên Elbow chart             |
| Predicted vs Actual      | Kỹ thuật (model performance), không phải insight      |
| Correlation bar chart    | Heatmap rõ hơn, nhìn dễ hơn                           |

---

## 5. LIÊN HỆ BIỂU ĐỒ → CÂU HỎI KINH DOANH

```
📊 Biểu đồ 1-3 (EDA):
   "Thị trường điện thoại Shopee Việt Nam như thế nào?"
   → Doanh số, thị trường, rating

📊 Biểu đồ 4-6 (Tương quan):
   "Các yếu tố nào ảnh hưởng tới doanh số?"
   → Rating, Giá, Likes, v.v.

📊 Biểu đồ 7-8 (Clustering):
   "Có bao nhiêu phân khúc khách hàng?"
   → Phân nhóm sản phẩm

📊 Biểu đồ 9 (Feature Importance):
   "Nên tập trung marketing vào cái gì?"
   → Ưu tiên top 3 factors
```

---

**✅ BƯỚC TIẾP THEO:** Khi bạn đồng ý → Tôi sẽ viết code cho Bước 0 (làm sạch dữ liệu)
