import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# 1. ĐỌC DỮ LIỆU ĐÃ CÓ NHÃN CỤM TỪ K-MEANS
print("🚀 Đang tải dữ liệu huấn luyện...")
df = pd.read_csv('data/processed/data_with_clusters.csv')

# 2. TIỀN XỬ LÝ: CHUYỂN CHỮ THÀNH SỐ ĐỂ AI HIỂU ĐƯỢC
# Dùng LabelEncoder để mã hóa Brand và Location
le_brand = LabelEncoder()
df['brand_encoded'] = le_brand.fit_transform(df['brand'].astype(str))

le_loc = LabelEncoder()
df['loc_encoded'] = le_loc.fit_transform(df['shop_location'].astype(str))

# Chọn các cột làm Input (X) và Output/Target (y)
# Bỏ qua item_id và shop_id vì nó không có ý nghĩa dự đoán
features = ['brand_encoded', 'loc_encoded', 'discount_price', 'original_price', 'discount', 'liked_count', 'rating_star', 'number_of_ratings']
X = df[features]
y = df['cluster'] # Cột cụm mà K-means đã tạo

# 3. CHIA TẬP HUẤN LUYỆN VÀ TẬP KIỂM TRA (80% Học - 20% Thi)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. HUẤN LUYỆN MÔ HÌNH RANDOM FOREST
print("🧠 AI đang học các đặc tính của từng phân khúc...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Đánh giá độ chính xác
accuracy = rf_model.score(X_test, y_test)
print(f"✅ Độ chính xác (Accuracy) của hệ thống: {accuracy * 100:.2f}%")

# Ma trận rối loạn - CONFUSION MATRIX 
y_pred = rf_model.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=rf_model.classes_)

plt.figure(figsize=(8, 6))
disp.plot(cmap='Blues')
plt.title('Ma trận rối loạn (Confusion Matrix)')
plt.savefig('outputs/figures/9_Confusion_Matrix.png', dpi=300)
plt.close()

# 5. VŨ KHÍ BÁO CÁO: TÌM YẾU TỐ QUAN TRỌNG NHẤT (FEATURE IMPORTANCE)
importances = rf_model.feature_importances_
feat_imp = pd.DataFrame({'Biến số': features, 'Mức độ đóng góp': importances})
feat_imp = feat_imp.sort_values(by='Mức độ đóng góp', ascending=False)

print("\n🏆 BẢNG MỨC ĐỘ QUAN TRỌNG CỦA CÁC YẾU TỐ QUYẾT ĐỊNH:")
print(feat_imp.to_string(index=False))

# Vẽ biểu đồ mức độ quan trọng để mai chép vào Slide
plt.figure(figsize=(10, 6))
sns.barplot(x='Mức độ đóng góp', y='Biến số', data=feat_imp, palette='viridis')
plt.title('Yếu tố nào quyết định điện thoại thuộc phân khúc nào?', fontsize=14, fontweight='bold')
plt.xlabel('Mức độ đóng góp (Feature Importance)')
plt.ylabel('Các chỉ số')
plt.tight_layout()
# plt.show()
plt.savefig('outputs/figures/10_feature_importance.png', dpi=300)
plt.close()

# 6. LƯU MÔ HÌNH VÀ ENCODERS
joblib.dump(rf_model, 'models/rf_model.pkl')
joblib.dump(le_brand, 'models/le_brand.pkl')
joblib.dump(le_loc, 'models/le_loc.pkl')
print("💾 Đã lưu mô hình thành công vào thư mục 'models/'!")
