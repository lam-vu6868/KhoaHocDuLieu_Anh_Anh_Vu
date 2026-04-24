# =====================================================================
# PHẦN 6: GIAO DIỆN NHẬP LIỆU TERMINAL DÀNH CHO SẾP DEMO
# =====================================================================
import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Cấu hình trang
st.set_page_config(page_title="AI Dự Báo Phân Khúc Shopee", layout="wide")

# Load mô hình (Dùng cache để web chạy nhanh hơn)
@st.cache_resource
def load_models():
    model = joblib.load('models/rf_model.pkl')
    le_brand = joblib.load('models/le_brand.pkl')
    le_loc = joblib.load('models/le_loc.pkl')
    return model, le_brand, le_loc

model, le_brand, le_loc = load_models()

# Giao diện chính
st.title("🤖 Hệ thống AI Dự báo Phân khúc & Chiến lược Marketing")
st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("📋 Nhập thông tin máy")
    brand = st.selectbox("Thương hiệu", le_brand.classes_)
    location = st.selectbox("Vị trí Shop", le_loc.classes_)
    price = st.slider("Giá bán dự kiến (Triệu VNĐ)", 1.0, 24.0, 0.5)
    ratings = st.number_input("Số lượng đánh giá kỳ vọng", 0, 10000, 100)
    
    btn = st.button("🚀 CHẠY AI DỰ ĐOÁN", use_container_width=True)

with col2:
    st.header("📊 Kết quả phân tích")
    if btn:
        # Tiền xử lý input
        b_val = le_brand.transform([brand])[0]
        l_val = le_loc.transform([location])[0]
        
        # Slider là 1.0 (triệu), tập train 1 triệu là 100 (do chia 10.000 ở file 01)
        # Vậy ta phải nhân với 100 để đồng nhất đơn vị
        actual_price_for_ai = price * 100 
        
        # Tạo vector input với giá đã được nhân 100
        input_data = [[b_val, l_val, actual_price_for_ai, actual_price_for_ai*1.1, 0.1, 500, 4.5, ratings]]
        
        # Dự đoán
        cluster = model.predict(input_data)[0]
        
        # Hiển thị kết quả
        if cluster == 0:
            st.success("🎯 Phân khúc: CỤM 0 - NGÔI SAO DOANH SỐ")
            st.info("💡 **Chiến lược:** Sản phẩm có tiềm năng Viral cực cao. Hãy tập trung ngân sách cho Flash Sale và nhập hàng số lượng lớn.")
        elif cluster == 2:
            st.warning("💎 Phân khúc: CỤM 2 - HÀNG CAO CẤP (FLAGSHIP)")
            st.info("💡 **Chiến lược:** Khách hàng quan tâm đến dịch vụ hơn giá. Tặng thêm gói bảo hiểm màn hình và cam kết bảo hành 1 đổi 1.")
        else:
            st.error("📦 Phân khúc: CỤM 1 - HÀNG LỠ CỠ / TỒN KHO")
            st.info("💡 **Chiến lược:** Nguy cơ khó đẩy hàng. Nên dùng làm quà tặng kèm khi mua máy ở Cụm 0 để giải phóng kho.")
    else:
        st.write("Vui lòng nhập thông số bên trái và nhấn nút để xem kết quả.")

st.sidebar.markdown("### 🛠️ Thông số kỹ thuật")
st.sidebar.write("Mô hình: Random Forest Classifier")
st.sidebar.write("Độ chính xác: ~95%") # Sếp lấy số từ file training bỏ vào đây