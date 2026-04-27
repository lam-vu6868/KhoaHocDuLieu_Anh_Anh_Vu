### Cấu trúc thư mục dự án:

```bash
📁 KhoaHocDuLieu_Anh_Anh_Vu/ <-- THƯ MỤC GỐC CỦA DỰ ÁN
│
├── 📁 venv/ <-- 🔴 ĐẶT VENV Ở ĐÂY (Môi trường ảo)
│
├── 📁 data/ <-- NƠI CHỨA DỮ LIỆU
│ ├── 📁 raw/ <-- Bỏ 3 file gốc vào đây (ID, DATA, RATING)
│ └── 📁 processed/ <-- Để trống. Lát code chạy xong sẽ lưu data sạch vào đây.
│
├── 📁 outputs/ <-- NƠI CHỨA KẾT QUẢ XUẤT RA
│ └── 📁 figures/ <-- File code vẽ biểu đồ xong sẽ tự lưu ảnh (.png) vào đây.
│
├── 📜 01_data_cleaning.py <-- File code 1: Làm sạch & Gộp bảng
├── 📜 02_eda_visuals.py <-- File code 2: Vẽ biểu đồ tổng quan
├── 📜 03_pca_mca_kmeans.py <-- File code 3: Giảm chiều & Phân cụm
├── 📜 04_random_forest.py <-- File code 4: Tìm yếu tố quan trọng (Feature Importance)
│
└── 📜 requirements.txt <-- Danh sách thư viện (pandas, scikit-learn, matplotlib...)
```

### Tinh chỉ file requirements.txt - quản lý các thư viện - rất quan trọng

pip freeze > requirements.txt

### Hướng dẫn setup dự án

- Yêu cầu: Có Python version 3.12.0 hoặc cao hơn

```bash
# Kiểm tra verion pythom
python --version
# Nếu như đã tải nhưng lỗi có thể kill terminal hoặc đóng VS code sau đó chạy lại


# Tạo môt trường ảo quản lý các thư viện
python -m venv venv


# Tải các thư viện cho dự án
pip install -r requirements.txt


# Chạy file models AI (cd ở thư mục gốc)
cd KhoaHoc........
# chạy file mô hình
streamlit run 05_app.py
```

- Mọi thắc mắc vui lòng liên hệ qua email: 23050118@student.bdu.edu.vn hoặc sdt: 0328884320
