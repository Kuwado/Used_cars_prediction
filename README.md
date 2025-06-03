# Ứng Dụng Dự Đoán Giá Xe Ô Tô

Một ứng dụng web toàn diện để dự đoán giá xe ô tô cũ tại Việt Nam sử dụng các mô hình machine learning. Hệ thống bao gồm thu thập dữ liệu tự động từ Chợ Tốt (chotot.com), xử lý dữ liệu, huấn luyện mô hình và giao diện web thân thiện để dự đoán giá xe.

## 🚗 Tính Năng Chính

- **Thu Thập Dữ Liệu Tự Động**: Web crawler để lấy dữ liệu xe từ Chợ Tốt
- **Quản Lý Dữ Liệu**: Pipeline xử lý dữ liệu hoàn chỉnh từ thô đến sạch
- **Mô Hình Machine Learning**: Nhiều mô hình dự đoán (Linear Regression, Random Forest, XGBoost)
- **Giao Diện Web**: Interface dễ sử dụng để dự đoán giá xe
- **Theo Dõi Thời Gian Thực**: Giám sát trực tiếp quá trình crawl và xử lý dữ liệu
- **Quản Lý Database**: Lưu trữ có cấu trúc với thiết kế database quan hệ

## 📁 Cấu Trúc Project

```
car_price_prediction/
├── app/
│   ├── __init__.py                 # Cấu hình Flask app
│   ├── models.py                   # Models database
│   ├── routes.py                   # Routes và API endpoints
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css           # CSS tùy chỉnh
│   │   └── js/
│   │       ├── main.js             # Chức năng dashboard
│   │       └── predict.js          # Xử lý form dự đoán
│   ├── templates/
│   │   ├── index.html              # Dashboard chính
│   │   ├── predict.html            # Giao diện dự đoán giá
│   │   ├── logs.html               # Logs hoạt động
│   │   └── database_info.html      # Thống kê database
│   └── utils/
│       ├── crawler.py              # Web crawler thu thập dữ liệu
│       ├── preprocessor.py         # Làm sạch và xử lý dữ liệu
│       └── database.py             # Tiện ích database
├── data/
│   ├── raw/                        # Dữ liệu thô đã scrape
│   └── processed/                  # Dữ liệu đã làm sạch
├── src/
│   ├── models/                     # Mô hình ML đã huấn luyện
│   └── training/                   # Scripts huấn luyện mô hình
├── logs/                           # Logs ứng dụng
├── db__init.py                     # Khởi tạo database
├── run.py                          # Entry point ứng dụng
└── requirements.txt                # Dependencies Python
```

## 🛠️ Cài Đặt & Thiết Lập

### Yêu Cầu Hệ Thống

- Python 3.8+
- SQLite (có sẵn với Python)
- Trình duyệt web

### Các Bước Cài Đặt

1. **Clone repository**

   ```bash
   git clone <repository-url>
   cd car_price_prediction
   ```

2. **Cài đặt dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Khởi tạo database**

   ```bash
   python db__init.py
   ```

4. **Chạy ứng dụng**

   ```bash
   python run.py
   ```

5. **Truy cập ứng dụng**
   Mở trình duyệt và vào `http://localhost:5000`

## 🔧 Thư Viện Cần Thiết

```txt
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Migrate==4.0.5
requests==2.31.0
beautifulsoup4==4.12.2
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
xgboost==1.7.6
joblib==1.3.2
```

## 📊 Hướng Dẫn Sử Dụng

### 1. Quy Trình Xử Lý Dữ Liệu

#### Bước 1: Thu Thập Dữ Liệu (Crawl Data)

- Vào dashboard chính
- Thiết lập phạm vi trang (trang bắt đầu và trang kết thúc)
- Nhấn "Start Crawling" để bắt đầu thu thập dữ liệu
- Theo dõi tiến độ theo thời gian thực

#### Bước 2: Xử Lý Dữ Liệu (Preprocess Data)

- Nhấn "Start Preprocessing" để làm sạch dữ liệu đã crawl
- Hệ thống sẽ tự động sử dụng file dữ liệu thô mới nhất
- Dữ liệu đã xử lý sẽ được lưu để huấn luyện mô hình

#### Bước 3: Import vào Database

- Nhấn "Import to Database" để tạo các lựa chọn dropdown
- Bước này tạo dữ liệu có cấu trúc cho giao diện dự đoán

#### Bước 4: Huấn Luyện Mô Hình (Tùy chọn)

- Nhấn "Đào tạo mô hình" để huấn luyện lại các mô hình dự đoán
- Sử dụng dữ liệu đã xử lý mới nhất để cải thiện độ chính xác

### 2. Dự Đoán Giá Xe

1. **Vào Trang Dự Đoán**

   - Nhấn "Chuyển Đến Trang Dự Đoán Giá Xe" từ dashboard

2. **Điền Thông Tin Xe**

   - **Hãng Xe**: Chọn nhà sản xuất
   - **Dòng Xe**: Chọn model cụ thể (tự động cập nhật theo hãng)
   - **Năm Sản Xuất**: Năm sản xuất xe
   - **Số Km Đã Đi**: Số km đã di chuyển
   - **Nhiên Liệu**: Xăng, Dầu diesel, v.v.
   - **Hộp Số**: Số sàn hoặc Số tự động
   - **Xuất Xứ**: Trong nước hoặc Nhập khẩu
   - **Kiểu Dáng**: Sedan, SUV, Hatchback, v.v.
   - **Số Chỗ Ngồi**: Số ghế trong xe

3. **Nhận Kết Quả Dự Đoán**
   - Nhấn "Dự Đoán Giá" để nhận ước tính giá
   - Xem kết quả từ ba mô hình khác nhau
   - Xem giá dự đoán trung bình để có ước tính tốt nhất
