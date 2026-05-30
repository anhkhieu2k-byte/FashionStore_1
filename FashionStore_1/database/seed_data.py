"""
Seed dữ liệu mẫu: sản phẩm + khách hàng + kho + nhân viên
Chạy 1 lần từ thư mục gốc: python database/seed_data.py
"""
import sqlite3, sys, os
from datetime import datetime, timedelta
import bcrypt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATABASE_NAME

# Xóa file db cũ nếu có để reset ID về 1
db_path = DATABASE_NAME
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print(f"[INFO] Deleted old database file: {db_path}")
    except Exception as e:
        print(f"[WARNING] Could not delete old database file: {e}")

from database.init_db import init_database
init_database()

conn = sqlite3.connect(DATABASE_NAME)
c = conn.cursor()

# ─────────────────── ACCOUNTS ───────────────────
hashed_password = bcrypt.hashpw("123456".encode(), bcrypt.gensalt())
c.execute("INSERT INTO accounts(username, password, role) VALUES (?, ?, ?)", ("admin", hashed_password, "Admin"))
print("[OK] Admin account 'admin' with password '123456' created.")

# ─────────────────── PRODUCTS (50 products) ───────────────────
products = [
    ("Áo thun trắng cổ tròn", "Áo", "S, M, L, XL, XXL", "Trắng, Đen, Xám, Kem", 250000, 45, "Áo thun cotton thoáng mát", 120000, "Công ty May Mặc Hà Nội"),
    ("Quần jeans xanh", "Quần", "S, M, L, XL, XXL", "Xanh đậm, Xanh nhạt, Đen", 350000, 30, "Quần jeans cao cấp co giãn", 180000, "Xưởng Jean Việt"),
    ("Váy hoa mùa hè", "Váy", "S, M, L, XL, XXL", "Đỏ hoa, Xanh hoa, Vàng hoa", 650000, 18, "Váy voan lụa nhẹ nhàng", 350000, "Thời Trang Hè VN"),
    ("Áo khoác nhẹ", "Áo khoác", "S, M, L, XL, XXL", "Đen, Xám, Xanh rêu", 550000, 12, "Áo gió cản gió bụi nhẹ", 300000, "Công ty May Mặc Hà Nội"),
    ("Áo polo nam", "Áo", "S, M, L, XL, XXL", "Xanh navy, Trắng, Đen, Xám", 420000, 25, "Áo thun polo nam lịch lãm", 220000, "Xưởng Áo Thun SG"),
    ("Giày sneaker trắng", "Giày", "39, 40, 41, 42, 43", "Trắng, Đen, Trắng đen", 680000, 8, "Sneaker da thật mềm êm", 400000, "Giày Da Nhập Khẩu"),
    ("Đầm maxi boho", "Váy", "S, M, L, XL, XXL", "Be, Kem, Nâu", 780000, 15, "Đầm dáng dài phóng khoáng", 420000, "Thời Trang Hè VN"),
    ("Quần short thể thao", "Quần", "S, M, L, XL, XXL", "Xám, Đen, Xanh dương", 280000, 40, "Quần đùi thoáng mát năng động", 140000, "Xưởng Áo Thun SG"),
    ("Áo sơ mi trắng", "Áo", "S, M, L, XL", "Trắng", 320000, 50, "Sơ mi dài tay cotton công sở", 160000, "Công ty May Mặc Hà Nội"),
    ("Áo sơ mi caro", "Áo", "S, M, L, XL", "Đỏ đen, Xanh navy, Xám", 340000, 35, "Sơ mi flannel ấm áp trẻ trung", 170000, "Công ty May Mặc Hà Nội"),
    ("Quần kaki nam", "Quần", "29, 30, 31, 32, 33", "Be, Nâu, Đen, Xanh rêu", 390000, 25, "Quần kaki ống đứng thời trang", 200000, "Xưởng Jean Việt"),
    ("Quần jogger thể thao", "Quần", "M, L, XL, XXL", "Đen, Xám đậm, Xám nhạt", 300000, 40, "Quần nỉ bo gấu thể thao", 150000, "Xưởng Áo Thun SG"),
    ("Váy chữ A cá tính", "Váy", "S, M, L", "Đen, Nâu, Kem", 290000, 20, "Chân váy chữ A tôn dáng", 145000, "Thời Trang Hè VN"),
    ("Váy xếp ly tennis", "Váy", "S, M, L", "Trắng, Đen, Hồng", 270000, 22, "Chân váy xếp ly phong cách Hàn Quốc", 130000, "Thời Trang Hè VN"),
    ("Áo len mỏng", "Áo khoác", "Free Size", "Hồng phân, Kem, Be, Xanh mint", 380000, 15, "Áo len tăm mỏng cho mùa thu", 190000, "Công ty May Mặc Hà Nội"),
    ("Áo hoodie nỉ", "Áo khoác", "M, L, XL, XXL", "Đen, Xám, Vàng chanh", 450000, 18, "Áo hoodie vải nỉ bông ấm áp", 230000, "Xưởng Áo Thun SG"),
    ("Giày sandal cao gót", "Giày", "35, 36, 37, 38, 39", "Đen, Kem, Bạc", 490000, 12, "Giày sandal 7 phân tôn dáng", 250000, "Giày Da Nhập Khẩu"),
    ("Giày lười nam da lộn", "Giày", "39, 40, 41, 42, 43", "Nâu, Đen, Xanh than", 850000, 10, "Giày loafer chất da lộn mềm mại", 450000, "Giày Da Nhập Khẩu"),
    ("Kính mát thời trang", "Phụ kiện", "Free Size", "Đen, Trà, Gọng vàng", 220000, 60, "Kính mát chống tia UV", 100000, "Giày Da Nhập Khẩu"),
    ("Thắt lưng da nam", "Phụ kiện", "Free Size", "Đen, Nâu", 350000, 50, "Thắt lưng da bò thật nguyên tấm", 160000, "Giày Da Nhập Khẩu"),
    ("Mũ lưỡi trai thêu chữ", "Phụ kiện", "Free Size", "Đen, Trắng, Đỏ, Vàng", 150000, 80, "Nón kết cotton thêu chữ nổi", 60000, "Xưởng Áo Thun SG"),
    ("Túi xách da nữ", "Phụ kiện", "Free Size", "Đen, Trắng, Hồng pastel", 580000, 15, "Túi xách tay nữ da PU cao cấp", 280000, "Thời Trang Hè VN"),
    ("Áo len cổ lọ", "Áo", "S, M, L", "Trắng, Đen, Đỏ đô, Xám", 390000, 20, "Áo len ôm cổ lọ giữ nhiệt", 195000, "Công ty May Mặc Hà Nội"),
    ("Áo croptop thun gân", "Áo", "S, M, L", "Trắng, Đen, Cam đất", 180000, 55, "Croptop ôm body trẻ trung", 80000, "Xưởng Áo Thun SG"),
    ("Quần tây âu nam", "Quần", "28, 29, 30, 31, 32", "Đen, Xám đậm, Xanh đen", 450000, 30, "Quần tây phom slimfit đứng dáng", 220000, "Xưởng Jean Việt"),
    ("Quần ống rộng nữ", "Quần", "S, M, L, XL", "Đen, Trắng, Kem, Nâu", 320000, 40, "Quần vải ống suông dài tôn dáng", 150000, "Thời Trang Hè VN"),
    ("Đầm dạ hội đuôi cá", "Váy", "S, M, L", "Đỏ, Đen, Trắng", 1200000, 6, "Đầm tiệc đuôi cá quyến rũ", 650000, "Thời Trang Hè VN"),
    ("Áo khoác phao béo", "Áo khoác", "M, L, XL, XXL", "Đen, Xanh rêu, Đỏ ấm", 890000, 10, "Áo phao siêu nhẹ siêu ấm ngày đông", 480000, "Công ty May Mặc Hà Nội"),
    ("Áo cardigan len", "Áo khoác", "Free Size", "Be, Kem, Xanh nhạt", 420000, 25, "Áo khoác cardigan dáng lửng vintage", 210000, "Công ty May Mặc Hà Nội"),
    ("Dép lê bánh mì", "Giày", "36, 37, 38, 39, 40", "Hồng, Trắng, Kem, Đen", 190000, 50, "Dép lê bánh mì đi trong nhà dạo phố", 80000, "Giày Da Nhập Khẩu"),
    ("Vớ/Tất cổ cao cotton", "Phụ kiện", "Free Size", "Trắng, Đen, Xám", 35000, 200, "Tất dệt kim mềm mịn thấm mồ hôi tốt", 12000, "Xưởng Áo Thun SG"),
    ("Mũ len quả bông", "Phụ kiện", "Free Size", "Hồng, Be, Kem", 120000, 45, "Nón len ấm áp có quả bông xinh xắn", 50000, "Công ty May Mặc Hà Nội"),
    ("Áo ba lỗ thể thao", "Áo", "M, L, XL, XXL", "Đen, Trắng, Xám", 150000, 70, "Áo thun sát nách mát mẻ", 70000, "Xưởng Áo Thun SG"),
    ("Quần short jean nữ", "Quần", "S, M, L", "Xanh nhạt, Xanh đậm, Đen", 280000, 35, "Short bò cá tính trẻ trung", 130000, "Xưởng Jean Việt"),
    ("Áo trễ vai điệu đà", "Áo", "S, M, L", "Trắng, Hoa nhí, Đen", 290000, 22, "Áo trễ vai voan mát cho mùa hè", 140000, "Thời Trang Hè VN"),
    ("Áo khoác dạ dáng dài", "Áo khoác", "S, M, L", "Nâu tây, Đen, Kem", 1150000, 8, "Măng tô dạ ấm áp thanh lịch", 600000, "Công ty May Mặc Hà Nội"),
    ("Giày chelsea boot nam", "Giày", "39, 40, 41, 42, 43", "Đen, Nâu", 950000, 12, "Giày bốt da bò nam phong cách", 500000, "Giày Da Nhập Khẩu"),
    ("Khăn choàng cổ len", "Phụ kiện", "Free Size", "Đỏ, Nâu, Xám, Be", 250000, 40, "Khăn quàng cổ giữ ấm tua rua", 110000, "Công ty May Mặc Hà Nội"),
    ("Áo Blazer Hàn Quốc", "Áo khoác", "S, M, L, XL", "Đen, Be, Xám chuột", 590000, 20, "Blazer phom rộng chuẩn Hàn", 290000, "Công ty May Mặc Hà Nội"),
    ("Quần lửng culottes", "Quần", "S, M, L, XL", "Đen, Kem, Xanh rêu", 260000, 30, "Quần culottes chất đũi cực mát", 120000, "Thời Trang Hè VN"),
    ("Đầm ren công chúa", "Váy", "S, M, L", "Trắng, Hồng nhạt", 850000, 12, "Đầm ren xòe điệu đà cho bé gái", 420000, "Thời Trang Hè VN"),
    ("Giày búp bê nữ", "Giày", "35, 36, 37, 38, 39", "Đen, Kem, Đỏ", 380000, 25, "Giày búp bê da mềm êm chân dạo phố", 180000, "Giày Da Nhập Khẩu"),
    ("Ví cầm tay nữ nhỏ gọn", "Phụ kiện", "Free Size", "Đen, Kem, Hồng", 180000, 45, "Ví đựng tiền mini sang trọng", 80000, "Thời Trang Hè VN"),
    ("Áo gile len", "Áo", "M, L, XL", "Kem, Xám, Nâu", 320000, 28, "Áo gile len dệt phối sơ mi cực đẹp", 150000, "Xưởng Áo Thun SG"),
    ("Quần legging thun co giãn", "Quần", "S, M, L, XL", "Đen, Xám", 180000, 60, "Quần thun ôm tập gym dạo phố", 80000, "Xưởng Áo Thun SG"),
    ("Bộ quần áo nỉ nam", "Áo khoác", "M, L, XL, XXL", "Đen, Xám, Xanh than", 650000, 18, "Bộ quần áo nỉ hoodie giữ ấm cực tốt", 320000, "Xưởng Áo Thun SG"),
    ("Chân váy bò dáng dài", "Váy", "S, M, L", "Xanh nhạt, Đen", 340000, 22, "Chân váy jean xẻ tà sau trẻ trung", 160000, "Xưởng Jean Việt"),
    ("Giày thể thao tập gym", "Giày", "36, 37, 38, 39, 40, 41, 42", "Đen, Xám, Trắng hồng", 550000, 20, "Giày chạy bộ thể thao êm nhẹ", 270000, "Giày Da Nhập Khẩu"),
    ("Mũ nồi dạ nữ", "Phụ kiện", "Free Size", "Đen, Kem, Đỏ", 160000, 30, "Mũ beret chất dạ sang chảnh", 70000, "Thời Trang Hè VN"),
    ("Áo khoác bò denim", "Áo khoác", "M, L, XL", "Xanh bạc, Đen", 480000, 15, "Áo denim jacket bụi bặm phong cách", 240000, "Xưởng Jean Việt")
]

c.executemany(
    "INSERT INTO products(name,category,size,color,price,stock,description,import_price,supplier_name) VALUES(?,?,?,?,?,?,?,?,?)",
    products
)
print(f"[OK] Seeded {len(products)} products successfully.")

# ─────────────────── CUSTOMERS (20 customers) ───────────────────
customers = [
    ("Nguyễn Thị Lan", "0901234567", "lan@email.com", 343, "Vàng"),
    ("Trần Văn Minh", "0912345678", "minh@email.com", 85, "Đồng"),
    ("Lê Thị Hoa", "0923456789", "hoa@email.com", 120, "Bạc"),
    ("Phạm Quốc Hùng", "0934567890", "hung@email.com", 42, "Đồng"),
    ("Nguyễn Văn An", "0981112223", "an.nguyen@email.com", 560, "Vàng"),
    ("Trần Thị Bình", "0982223334", "binh.tran@email.com", 15, "Đồng"),
    ("Phạm Văn Cường", "0983334445", "cuong.pham@email.com", 230, "Bạc"),
    ("Lê Thị Dung", "0984445556", "dung.le@email.com", 1200, "Kim cương"),
    ("Hoàng Văn Em", "0985556667", "em.hoang@email.com", 50, "Đồng"),
    ("Nguyễn Thị Phương", "0986667778", "phuong.nguyen@email.com", 310, "Bạc"),
    ("Bùi Tấn Tài", "0987778889", "tai.bui@email.com", 890, "Vàng"),
    ("Ngô Thanh Vân", "0988889990", "van.ngo@email.com", 1500, "Kim cương"),
    ("Lâm Quốc Bảo", "0989990001", "bao.lam@email.com", 75, "Đồng"),
    ("Đặng Ngọc Hân", "0971112222", "han.dang@email.com", 450, "Vàng"),
    ("Trương Minh Thuận", "0972223333", "thuan.truong@email.com", 180, "Bạc"),
    ("Phan Thanh Thảo", "0973334444", "thao.phan@email.com", 90, "Đồng"),
    ("Vũ Hoàng Nam", "0974445555", "nam.vu@email.com", 620, "Vàng"),
    ("Đỗ Kim Liên", "0975556666", "lien.do@email.com", 25, "Đồng"),
    ("Trịnh Xuân Bách", "0976667777", "bach.trinh@email.com", 110, "Bạc"),
    ("Nguyễn Bảo Châu", "0977778888", "chau.nguyen@email.com", 2200, "Kim cương")
]

c.executemany(
    "INSERT INTO customers(full_name,phone,email,points,member_rank) VALUES(?,?,?,?,?)",
    customers
)
print(f"[OK] Seeded {len(customers)} customers successfully.")

# ─────────────────── STAFF (10 staff members) ───────────────────
staff = [
    ("Đinh Thị Mai", "1995-03-15", "0945678901", "Hà Nội", "Quản lý", "Sáng", 12000000, 22, None, 0.0),
    ("Vũ Tuấn Anh", "1998-07-22", "0956789012", "Hà Nội", "Nhân viên", "Chiều", 25000, 20, None, 80.0),
    ("Hoàng Minh Tuấn", "2000-01-01", "0967890123", "Hà Nội", "Nhân viên bán hàng", "Cả ngày", 25000, 1, None, 9.0),
    ("Phạm Thanh Hà", "1997-11-12", "0971234567", "Hải Phòng", "Nhân viên thu ngân", "Sáng", 25000, 18, None, 72.0),
    ("Trần Quốc Bảo", "1999-05-30", "0982345678", "Bắc Ninh", "Nhân viên kho", "Chiều", 25000, 15, None, 60.0),
    ("Lê Ngọc Trinh", "1996-08-18", "0934567891", "Hà Nội", "Nhân viên bán hàng", "Chiều", 25000, 21, None, 84.0),
    ("Nguyễn Hữu Đạt", "1994-04-25", "0905678912", "Nam Định", "Nhân viên kho", "Sáng", 25000, 19, None, 76.0),
    ("Vũ Hoàng Yến", "2001-09-05", "0916789023", "Hà Nội", "Nhân viên bán hàng", "Sáng", 25000, 22, None, 88.0),
    ("Đặng Anh Tú", "1993-12-10", "0927890134", "Hà Nội", "Quản lý kho", "Cả ngày", 10000000, 20, None, 160.0),
    ("Nguyễn Thùy Linh", "2002-02-28", "0938901245", "Hà Nam", "Nhân viên thu ngân", "Chiều", 25000, 16, None, 64.0)
]

c.executemany(
    "INSERT INTO staff(full_name,birth_date,phone,address,role,shift,salary,attendance_days,check_in_time,total_hours) VALUES(?,?,?,?,?,?,?,?,?,?)",
    staff
)
print(f"[OK] Seeded {len(staff)} staff members successfully.")

# ─────────────────── ATTENDANCE HISTORY GENERATOR ───────────────────
def generate_attendance_history():
    records = []
    hourly_staffs = [
        (2, "Vũ Tuấn Anh", "Chiều", 25000, 80.0),
        (3, "Hoàng Minh Tuấn", "Cả ngày", 25000, 9.0),
        (4, "Phạm Thanh Hà", "Sáng", 25000, 72.0),
        (5, "Trần Quốc Bảo", "Chiều", 25000, 60.0),
        (6, "Lê Ngọc Trinh", "Chiều", 25000, 84.0),
        (7, "Nguyễn Hữu Đạt", "Sáng", 25000, 76.0),
        (8, "Vũ Hoàng Yến", "Sáng", 25000, 88.0),
        (10, "Nguyễn Thùy Linh", "Chiều", 25000, 64.0)
    ]
    
    start_date = datetime(2026, 5, 18)
    
    for s_id, name, shift_name, hourly_rate, t_hours in hourly_staffs:
        if s_id == 3:
            records.append((3, "Hoàng Minh Tuấn", "2026-05-18 08:00:00", "2026-05-18 17:00:00", 9.0, 225000.0))
            continue
            
        shift_duration = 4.0
        if "sáng" in shift_name.lower():
            check_in_hour = 8
            check_out_hour = 12
        elif "chiều" in shift_name.lower():
            check_in_hour = 13
            check_out_hour = 17
        else:
            check_in_hour = 18
            check_out_hour = 22
            
        num_shifts = int(t_hours / shift_duration)
        for i in range(num_shifts):
            shift_date = start_date - timedelta(days=i)
            if shift_date.weekday() == 6:
                shift_date = shift_date - timedelta(days=1)
                
            in_str = shift_date.replace(hour=check_in_hour, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")
            out_str = shift_date.replace(hour=check_out_hour, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")
            earned = shift_duration * hourly_rate
            records.append((s_id, name, in_str, out_str, shift_duration, earned))
            
    return records

attendance_history = generate_attendance_history()

c.executemany(
    "INSERT INTO attendance_history(staff_id,staff_name,check_in,check_out,hours,earned) VALUES(?,?,?,?,?,?)",
    attendance_history
)
print(f"[OK] Seeded {len(attendance_history)} detailed shift attendance history records successfully.")

# ─────────────────── INVENTORY (50 items matching products) ───────────────────
inventory = []
for p in products:
    name = p[0]
    stock_qty = p[5]
    imp_price = p[7]
    supplier = p[8]
    min_qty = max(5, stock_qty // 4)
    inventory.append((name, stock_qty, min_qty, supplier, imp_price))

c.executemany(
    "INSERT INTO inventory(product_name,quantity,min_quantity,supplier_name,import_price) VALUES(?,?,?,?,?)",
    inventory
)
print(f"[OK] Seeded {len(inventory)} inventory entries successfully.")

# ─────────────────── SUPPLIERS ───────────────────
suppliers = [
    ("Công ty May Mặc Hà Nội", "0243123456", "KCN Bắc Thăng Long, Hà Nội"),
    ("Xưởng Jean Việt",        "0987654321", "Quận 12, TP. Hồ Chí Minh"),
    ("Thời Trang Hè VN",       "0911223344", "Hải Châu, Đà Nẵng"),
    ("Xưởng Áo Thun SG",       "0933445566", "Tân Bình, TP. Hồ Chí Minh"),
    ("Giày Da Nhập Khẩu",      "0909112233", "Đống Đa, Hà Nội"),
]

c.executemany(
    "INSERT INTO suppliers(name,phone,address) VALUES(?,?,?)",
    suppliers
)
print(f"[OK] Seeded {len(suppliers)} suppliers successfully.")

# ─────────────────── PROMOTIONS ───────────────────
promotions = [
    ("SUMMER20",  20.0, 500000,  "2026-05-01", "2026-08-31"),
    ("WELCOME10", 10.0, 200000,  "2026-01-01", "2026-12-31"),
    ("VIP30",     30.0, 1500000, "2026-05-01", "2026-06-30"),
]

c.executemany(
    "INSERT INTO promotions(code,discount_percent,min_order_value,start_date,end_date) VALUES(?,?,?,?,?)",
    promotions
)
print(f"[OK] Seeded {len(promotions)} promotions successfully.")

# ─────────────────── DYNAMIC INVOICES GENERATOR (Multiple per Customer matching Points) ───────────────────
# Sinh nhiều hóa đơn cho từng khách hàng, tổng số tiền tiêu khớp 100% với số điểm tích lũy (10,000 đ = 1 điểm)
# Các hóa đơn được phân bổ đều đặn từ ngày 01 đến ngày 18 tháng 5 năm 2026 giúp biểu đồ tab Báo cáo cực kỳ đẹp mắt
def generate_invoices_for_all_customers():
    # 20 khách hàng tương ứng trong bảng customers kèm điểm phân hạng
    customer_list = [
        ("Nguyễn Thị Lan", 343),
        ("Trần Văn Minh", 85),
        ("Lê Thị Hoa", 120),
        ("Phạm Quốc Hùng", 42),
        ("Nguyễn Văn An", 560),
        ("Trần Thị Bình", 15),
        ("Phạm Văn Cường", 230),
        ("Lê Thị Dung", 1200),
        ("Hoàng Văn Em", 50),
        ("Nguyễn Thị Phương", 310),
        ("Bùi Tấn Tài", 890),
        ("Ngô Thanh Vân", 1500),
        ("Lâm Quốc Bảo", 75),
        ("Đặng Ngọc Hân", 450),
        ("Trương Minh Thuận", 180),
        ("Phan Thanh Thảo", 90),
        ("Vũ Hoàng Nam", 620),
        ("Đỗ Kim Liên", 25),
        ("Trịnh Xuân Bách", 110),
        ("Nguyễn Bảo Châu", 2200)
    ]
    
    start_date = datetime(2026, 5, 1)
    
    for cust_idx, (c_name, points) in enumerate(customer_list):
        # 10,000 đ tiêu dùng = 1 điểm tích lũy
        target_spent = points * 10000
        if target_spent <= 0:
            continue
            
        # Xác định số lượng hóa đơn cho khách hàng này dựa trên tổng số tiền tiêu
        if target_spent <= 300000:
            num_invoices = 2
            shares = [0.6, 0.4]
        elif target_spent <= 1500000:
            num_invoices = 2
            shares = [0.55, 0.45]
        elif target_spent <= 5000000:
            num_invoices = 3
            shares = [0.4, 0.35, 0.25]
        else:
            num_invoices = 4
            shares = [0.35, 0.28, 0.22, 0.15]
            
        # Chia nhỏ số tiền tiêu cho từng hóa đơn
        invoice_targets = []
        accumulated = 0
        for i in range(num_invoices - 1):
            share_amount = int(target_spent * shares[i])
            # Tròn tiền chẵn nghìn cho thực tế
            share_amount = (share_amount // 1000) * 1000
            invoice_targets.append(share_amount)
            accumulated += share_amount
        invoice_targets.append(target_spent - accumulated) # Hóa đơn cuối nhận phần còn lại
        
        for inv_idx, T in enumerate(invoice_targets):
            if T <= 0:
                continue
                
            # Tạo ngày ngẫu nhiên/tuần hoàn phân phối đều từ 1/5 đến 18/5/2026
            day_offset = (cust_idx * 3 + inv_idx) % 18
            inv_date = start_date + timedelta(days=day_offset, hours=9 + (inv_idx * 3) % 10, minutes=(cust_idx * 7) % 60)
            date_str = inv_date.strftime("%Y-%m-%d %H:%M:%S")
            
            # Chọn phương thức thanh toán tuần hoàn
            pm_methods = ["Tiền mặt", "Chuyển khoản", "Thẻ"]
            payment_method = pm_methods[(cust_idx + inv_idx) % len(pm_methods)]
            
            # Lấy 2 sản phẩm tuần hoàn từ danh sách 50 sản phẩm
            p1_idx = (cust_idx * 3 + inv_idx) % 50
            p2_idx = (cust_idx * 3 + inv_idx + 13) % 50
            
            p1 = products[p1_idx]
            p2 = products[p2_idx]
            
            # Tính toán số lượng sản phẩm để raw_total >= T
            qty1 = 1
            qty2 = 1
            raw_total = p1[4] * qty1 + p2[4] * qty2
            
            while raw_total < T:
                if p1[4] <= p2[4]:
                    qty1 += 1
                else:
                    qty2 += 1
                raw_total = p1[4] * qty1 + p2[4] * qty2
                
            # Số tiền giảm giá để net_total = T đúng bằng raw_total - T
            discount_amount = raw_total - T
            discount_code = ""
            if discount_amount > 0:
                discount_code = "VIP_TRIAN" if T >= 500000 else "MEMBER_SALE"
                
            # Thêm hóa đơn
            c.execute("""
                INSERT INTO invoices(customer_name, total, payment_method, discount_code, discount_amount, created_at, status)
                VALUES (?, ?, ?, ?, ?, ?, 'Đã thanh toán')
            """, (c_name, T, payment_method, discount_code, discount_amount, date_str))
            
            inv_id = c.lastrowid
            
            # Thêm chi tiết cho sản phẩm 1
            sizes1 = [s.strip() for s in p1[2].split(",")]
            colors1 = [col.strip() for col in p1[3].split(",")]
            size1 = sizes1[inv_idx % len(sizes1)]
            color1 = colors1[(inv_idx + 1) % len(colors1)]
            full_name1 = f"{p1[0]} ({size1}, {color1})"
            subtotal1 = qty1 * p1[4]
            c.execute("""
                INSERT INTO invoice_details(invoice_id, product_name, quantity, price, subtotal)
                VALUES (?, ?, ?, ?, ?)
            """, (inv_id, full_name1, qty1, p1[4], subtotal1))
            
            # Thêm chi tiết cho sản phẩm 2
            sizes2 = [s.strip() for s in p2[2].split(",")]
            colors2 = [col.strip() for col in p2[3].split(",")]
            size2 = sizes2[(inv_idx + 2) % len(sizes2)]
            color2 = colors2[(inv_idx + 3) % len(colors2)]
            full_name2 = f"{p2[0]} ({size2}, {color2})"
            subtotal2 = qty2 * p2[4]
            c.execute("""
                INSERT INTO invoice_details(invoice_id, product_name, quantity, price, subtotal)
                VALUES (?, ?, ?, ?, ?)
            """, (inv_id, full_name2, qty2, p2[4], subtotal2))

generate_invoices_for_all_customers()
print("[OK] Seeded multiple unique invoices per customer (perfectly matching their points) successfully.")

# ─────────────────── RETURN ORDERS ───────────────────
# Đảm bảo Hóa đơn ID = 2 có phiếu đổi trả hàng hợp lệ
c.execute("""
    INSERT INTO return_orders(invoice_id, product_name, quantity, price, refund_amount, new_product_name, price_diff, reason, return_type) 
    VALUES (2, 'Váy hoa mùa hè (S, Đỏ hoa)', 1, 650000, 0.0, 'Đầm maxi boho (M, Be)', 130000, 'Đổi size', 'EXCHANGE')
""")
print("[OK] Seeded return order successfully.")

conn.commit()
conn.close()
print("\n[SUCCESS] Seed data completed! Database is fully populated with 50 products, 20 customers (with multiple invoices matching their rank points), and 10 staff members.")
