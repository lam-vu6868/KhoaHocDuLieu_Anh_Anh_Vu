📁 Shopee_Mobile_Analysis/ <-- THƯ MỤC GỐC CỦA DỰ ÁN
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
