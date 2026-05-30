# 🏪 FashionStore - Hệ Thống Quản Lý Cửa Hàng Thời Trang

Chào mừng bạn đến với **FashionStore**! Đây là một ứng dụng máy tính (Desktop Application) hiện đại, mạnh mẽ được xây dựng bằng ngôn ngữ **Python** kết hợp với framework giao diện **PyQt5** và cơ sở dữ liệu **SQLite**. Hệ thống được thiết kế nhằm giúp các chủ cửa hàng thời trang quản lý sản phẩm, nhân viên, khách hàng, hóa đơn, khuyến mãi và báo cáo doanh thu một cách trực quan, tối ưu và bảo mật.

---

## 🚀 Các Tính Năng Nổi Bật

- **🔑 Đăng Nhập & Bảo Mật**: Xác thực tài khoản người dùng, mã hóa mật khẩu an toàn bằng công nghệ băm `bcrypt`.
- **📦 Quản Lý Sản Phẩm**: Thêm, sửa, xóa, tìm kiếm thông tin quần áo, size, màu sắc, số lượng tồn kho.
- **💼 Quản Lý Nhân Viên & Khách Hàng**: Theo dõi lịch làm việc, thông tin liên lạc và lịch sử mua sắm.
- **🧾 Quản Lý Hóa Đơn & Bán Hàng**: Tạo hóa đơn nhanh chóng, tính toán tự động các khoản giảm giá và thuế.
- **📊 Báo Cáo & Thống Kê Giao Diện Trực Quan**: 
  - Vẽ biểu đồ cột/tròn biểu diễn doanh thu và xu hướng mua sắm bằng thư viện `matplotlib`.
  - Phân tích dữ liệu sản phẩm bán chạy sử dụng thư viện `pandas`.
- **📂 Xuất Bản Dữ Liệu Chuyên Nghiệp**:
  - Xuất báo cáo doanh thu và danh sách sản phẩm ra file **Excel (`.xlsx`)** thông qua `openpyxl`.
  - Xuất hóa đơn, tài liệu định dạng **PDF** chuẩn mực thông qua `reportlab`.

---

## 🛠️ Công Nghệ Sử Dụng

Dự án tích hợp các thư viện Python mạnh mẽ sau:

| Thư viện | Phiên bản / Mục đích |
| :--- | :--- |
| **PyQt5** | Thiết kế giao diện đồ họa (GUI) desktop chất lượng cao, mượt mà |
| **matplotlib** | Vẽ biểu đồ thống kê, trực quan hóa dữ liệu doanh số |
| **pandas** | Xử lý dữ liệu lớn, hỗ trợ phân tích thông tin kinh doanh |
| **openpyxl** | Tạo và ghi dữ liệu ra các trang tính Excel |
| **reportlab** | Thiết kế và xuất bản hóa đơn, tài liệu định dạng PDF |
| **bcrypt** | Mã hóa một chiều mật khẩu để đảm bảo an toàn thông tin tài khoản |
| **Pillow** | Xử lý hình ảnh sản phẩm trong hệ thống |

---

## 📁 Cấu Trúc Thư Mục Dự Án

Dưới đây là sơ đồ tổ chức mã nguồn theo mô hình MVC (Model-View-Controller) giúp dễ dàng mở rộng và bảo trì:

```text
FashionStore/
│
├── main.py                 # File khởi chạy ứng dụng chính (Entry Point)
├── requirements.txt        # Danh sách thư viện cần cài đặt
├── config.py               # Các cấu hình chung toàn hệ thống
├── database.db             # File cơ sở dữ liệu SQLite cục bộ
│
├── database/               # Khởi tạo và quản lý cấu trúc bảng CSDL
│   └── init_db.py
│
├── ui/                     # Giao diện người dùng (Views - PyQt5)
│   ├── login_window.py
│   ├── main_window.py
│   └── ...
│
├── controllers/            # Điều khiển logic nghiệp vụ (Controllers)
│   ├── login_controller.py
│   └── ...
│
├── models/                 # Mô hình dữ liệu kết nối CSDL (Models)
├── modules/                # Các mô đun tính năng bổ sung
├── utils/                  # Hàm tiện ích dùng chung (Date, Format, ...)
├── assets/                 # Hình ảnh, icon, hình nền hệ thống
└── exports/                # Thư mục chứa các file báo cáo PDF/Excel đã xuất
```

---

## ⚙️ Hướng Dẫn Cài Đặt & Chạy Ứng Dụng

Hãy thực hiện theo các bước dưới đây để thiết lập môi trường và khởi động ứng dụng trên máy tính của bạn:

### 1. Chuẩn bị môi trường ảo (Virtual Environment)
Mở terminal tại thư mục gốc của dự án (`FashionStore`) và tạo môi trường ảo:
```bash
# Tạo môi trường ảo có tên là .venv
python -m venv .venv

# Kích hoạt môi trường ảo (Dành cho Windows)
.venv\Scripts\activate
```

### 2. Cài đặt các thư viện cần thiết
Cài đặt tất cả các dependencies từ file [requirements.txt](file:///c:/Users/Admin/PycharmProjects/FashionStore/requirements.txt):
```bash
Mở terminal: pip install -r requirements.txt
```

### 3. Chạy ứng dụng
Khởi chạy file [main.py](file:///c:/Users/Admin/PycharmProjects/FashionStore/main.py) để bắt đầu sử dụng phần mềm quản lý:
```bash
python main.py
```
### 4. Thông tin tài khoản 
tài khoản : admin
```bash
mật khẩu : 123456

mật khẩu để có thể vào trang khuyến mãi và trang nhân viên là : admin123
---

## 🤝 Hướng Dẫn Đóng Góp (Contributing)
1. **Fork** dự án này về tài khoản cá nhân của bạn.
2. Tạo một nhánh mới để phát triển tính năng (`git checkout -b feature/NewFeature`).
3. Ghi lại các thay đổi của bạn (`git commit -m 'Add some NewFeature'`).
4. **Push** lên nhánh của bạn (`git push origin feature/NewFeature`).
5. Tạo một **Pull Request** mới để chúng tôi phê duyệt.

Chúc bạn có trải nghiệm tuyệt vời cùng **FashionStore**! 💖
