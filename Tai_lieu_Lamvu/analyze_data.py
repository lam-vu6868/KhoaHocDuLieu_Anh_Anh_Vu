import pandas as pd

# Đọc file
file_path = r'd:\TLKhoaHocDiLieu\data.xlsx'
df = pd.read_excel(file_path)

print('='*80)
print('PHÂN TÍCH DATASET - KHÁCH HÀNG MUA ĐIỆN THOẠI SHOPEE')
print('='*80)
print(f'\nKÍCH THƯỚC DATASET:')
print(f'   • Số dòng: {df.shape[0]:,}')
print(f'   • Số cột: {df.shape[1]}')

print(f'\nCÁC CỘT:')
for i, col in enumerate(df.columns, 1):
    print(f'   {i}. {col}')

print(f'\nKIỂU DỮ LIỆU:')
print(df.dtypes)

print(f'\nDỮ LIỆU MẪU (10 DÒNG ĐẦU):')
print(df.head(10).to_string())

print(f'\n\nTHỐNG KÊ MÔ TẢ:')
print(df.describe().to_string())

print(f'\n\nDỮ LIỆU THIẾU (NULL):')
print(df.isnull().sum())
