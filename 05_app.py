import streamlit as st
import joblib
import pandas as pd
import numpy as np

# ==========================================
# CẤU HÌNH TRANG UI
# ==========================================
st.set_page_config(page_title="AI Dự Báo Phân Khúc Shopee", page_icon="🤖", layout="wide")

# ==========================================
# LOAD MÔ HÌNH 
# ==========================================
@st.cache_resource
def load_models():
    model = joblib.load('models/rf_model.pkl')
    le_brand = joblib.load('models/le_brand.pkl')
    le_loc = joblib.load('models/le_loc.pkl')
    return model, le_brand, le_loc

model, le_brand, le_loc = load_models()

# Tạo danh sách có thêm tùy chọn nhập tay
brand_list = ["--- NHẬP HÃNG KHÁC ---"] + list(le_brand.classes_)
loc_list = ["--- NHẬP TỈNH/THÀNH KHÁC ---"] + list(le_loc.classes_)

# ==========================================
# GIAO DIỆN CHÍNH
# ==========================================
st.title("🤖 Hệ thống AI Dự báo Phân khúc & Cảnh báo Tồn kho")
st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("📋 Nhập thông số sản phẩm")
    
    # 1. NHẬP THƯƠNG HIỆU
    selected_brand = st.selectbox("Thương hiệu", brand_list, index=1)
    if selected_brand == "--- NHẬP HÃNG KHÁC ---":
        brand_input = st.text_input("✍️ Vui lòng nhập tên hãng mới (Ví dụ: LEICA, SONY...)").upper().strip()
    else:
        brand_input = selected_brand

    # 2. NHẬP VỊ TRÍ SHOP
    selected_loc = st.selectbox("Vị trí Shop", loc_list, index=1)
    if selected_loc == "--- NHẬP TỈNH/THÀNH KHÁC ---":
        loc_input = st.text_input("✍️ Vui lòng nhập Tỉnh/Thành phố (Ví dụ: LAI CHAU, KON TUM...)").upper().strip()
    else:
        loc_input = selected_loc

    # 3. NHẬP GIÁ & GIẢM GIÁ
    price = st.number_input("Giá bán thực tế (Triệu VNĐ)", min_value=0.1, value=5.0, step=0.5)
    discount_pct = st.slider("Tỉ lệ giảm giá (%)", min_value=0, max_value=99, value=10, step=1)
    
    # 4. CÁC THÔNG SỐ TƯƠNG TÁC
    ratings = st.number_input("Số lượng đánh giá (Kỳ vọng)", min_value=0, max_value=100000, value=100, step=50)
    rating_star = st.slider("Điểm đánh giá (Sao)", min_value=1.0, max_value=5.0, value=4.5, step=0.1)
    
    btn = st.button("🚀 PHÂN TÍCH BẰNG AI", use_container_width=True)

with col2:
    st.header("📊 Kết quả dự báo của AI")
    if btn:
        if not brand_input or not loc_input:
            st.error("⚠️ Vui lòng nhập đầy đủ tên Hãng và Vị trí Shop!")
        else:
            # ==========================================
            # BƯỚC 1: XỬ LÝ NHÃN (LABEL ENCODING) & BẮT LỖI
            # ==========================================
            try:
                b_val = le_brand.transform([brand_input])[0]
            except ValueError:
                st.toast(f"Hãng '{brand_input}' là dữ liệu mới. AI sẽ nội suy tự động!", icon="⚠️")
                b_val = le_brand.transform(['UNKNOWN'])[0] if 'UNKNOWN' in le_brand.classes_ else 0
                
            try:
                l_val = le_loc.transform([loc_input])[0]
            except ValueError:
                st.toast(f"Tỉnh '{loc_input}' là dữ liệu mới. AI sẽ dùng trọng số chung.", icon="⚠️")
                l_val = 0
            
            # ==========================================
            # BƯỚC 2: QUY ĐỔI ĐƠN VỊ & TÍNH TOÁN LOGIC
            # ==========================================
            # Nhân 1.000.000 để đưa về đúng đơn vị Đồng như AI đã học
            actual_price = price * 1000000 
            
            # Tính phần trăm giảm giá và nội suy giá gốc
            discount_rate = discount_pct / 100.0
            original_price = actual_price / (1 - discount_rate)
            
            # Tính lượt thích tương đối
            liked_count = ratings * 5 
            
            # Đưa vào mảng Input theo đúng thứ tự Feature lúc Train
            input_data = [[b_val, l_val, actual_price, original_price, discount_rate, liked_count, rating_star, ratings]]
            
            # ==========================================
            # BƯỚC 3: DỰ ĐOÁN VÀ XUẤT KẾT QUẢ
            # ==========================================
            cluster = model.predict(input_data)[0]
            
            if cluster == 0:
                st.success("🎯 Phân khúc: CỤM 0 - NGÔI SAO DOANH SỐ (SẢN PHẨM MŨI NHỌN)")
                st.info("💡 **Hành vi thị trường:** Khách hàng cân nhắc kỹ, thích sản phẩm này vì uy tín và cấu hình ngon trong tầm giá.\n\n"
                        "🚀 **Khuyến nghị Marketing:**\n"
                        "- Tối ưu hóa chăm sóc khách hàng. Vì họ (like) nhiều, hãy dùng tính năng <Gửi tin nhắn cho người thích sản phẩm> để tung mã giảm giá độc quyền, chốt đơn ngay.")
            
            elif cluster == 2:
                st.warning("💎 Phân khúc: CỤM 2 - [HÀNG phân khúc Máy cỏ/Máy phụ] ")
                st.info("💡 **Hành vi thị trường:** Giá rẻ nhất, sold_quantity cao đột biến. Người ta mua không cần suy nghĩ nhiều vì quá rẻ.\n\n"
                        "🚀 **Khuyến nghị Marketing:**\n"
                        "- [Lấy số lượng đè chất lượng]. Đừng tốn tiền chạy Ads thương hiệu, hãy tập trung vào SEO từ khóa [điện thoại giá rẻ] và tham gia mọi chương trình Flash Sale của Shopee.")
            
            else:
                st.error("📦 Phân khúc: CỤM 1 - HÀNG LỠ CỠ / NGUY CƠ TỒN KHO")
                st.info("💡 **Hành vi thị trường:** Sản phẩm kém sức hút do giá lấp lửng, hoặc chất lượng không tương xứng. Nó không đủ rẻ để người ta mua đại, cũng không đủ xịn để người ta thích (như cụm 0).\n\n"
                        "🚀 **Khuyến nghị Marketing:**\n"
                        "- Tối ưu hóa lại tiêu đề và hình ảnh. Hoặc là giảm giá hẳn xuống để cạnh tranh với cụm 2, hoặc là tặng kèm phụ kiện (tai nghe, ốp lưng) để thúc đẩy doanh thu.\n")
