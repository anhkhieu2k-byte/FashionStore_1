import sys
import os
import sqlite3
from datetime import datetime

# Reconfigure stdout to avoid UnicodeEncodeError on Windows
sys.stdout.reconfigure(encoding='utf-8')

# Add project path to sys.path so we can import modules
sys.path.append(r"c:\Users\Admin\PycharmProjects\FashionStore")

from database.db_connect import get_connection

# 1. Imports from system modules
from modules.sales.sale_service import SalesService
from modules.returns.return_service import ReturnService
from modules.reports.report_service import ReportService
from modules.staff.staff_service import StaffService
from models.customer import Customer
from models.attendance import AttendanceModel
from models.promotion import Promotion

def get_product_stock(product_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT stock FROM products WHERE name = ?", (product_name,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def get_customer_data(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT points, member_rank FROM customers WHERE full_name = ?", (name,))
    row = cursor.fetchone()
    conn.close()
    return row if row else None

def run_all_tests():
    print("="*60)
    print("🧪 BẮT ĐẦU CHẠY THỬ NGHIỆM LIÊN THÔNG TOÀN BỘ LOGIC HỆ THỐNG")
    print("="*60)

    # Dữ liệu mẫu dùng cho thử nghiệm
    customer_name = "Phạm Minh Đức"
    product_a = "Áo thun trắng cổ tròn"
    product_b = "Quần jeans xanh"
    promo_code = "TESTPROMO"

    # Reset/chuẩn bị dữ liệu mẫu trong cơ sở dữ liệu
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Đảm bảo Khách hàng thử nghiệm tồn tại và có điểm tích lũy ban đầu là 0
    cursor.execute("DELETE FROM customers WHERE full_name = ?", (customer_name,))
    cursor.execute("INSERT INTO customers (full_name, phone, points, member_rank) VALUES (?, '0987654321', 0, 'Đồng')", (customer_name,))
    
    # 2. Đảm bảo sản phẩm thử nghiệm có tồn kho ban đầu chuẩn
    cursor.execute("UPDATE products SET stock = 50 WHERE name = ?", (product_a,))
    cursor.execute("UPDATE products SET stock = 30 WHERE name = ?", (product_b,))
    
    # 3. Đảm bảo mã giảm giá hoạt động
    cursor.execute("DELETE FROM promotions WHERE code = ?", (promo_code,))
    cursor.execute("""
        INSERT INTO promotions (code, discount_percent, min_order_value, start_date, end_date, quantity, used_count)
        VALUES (?, 10, 50000, '2026-01-01', '2026-12-31', 100, 0)
    """, (promo_code,))
    
    conn.commit()
    conn.close()

    print("\n🟢 [Bước 1: Chuẩn bị dữ liệu]")
    print(f"  - Đã khởi tạo khách hàng: '{customer_name}' | Điểm: 0 | Hạng: Đồng")
    print(f"  - Đặt lại tồn kho '{product_a}' = 50, '{product_b}' = 30")
    print(f"  - Khởi tạo mã giảm giá: '{promo_code}' (Giảm 10%, HSD: cả năm 2026)")

    # 4. Kiểm tra luồng Mua hàng (Checkout)
    print("\n🟢 [Bước 2: Kiểm tra luồng Bán Hàng - Mua Hàng]")
    cart = [
        {"product_name": f"{product_a} (S, Trắng)", "quantity": 3, "price": 100000.0, "subtotal": 300000.0}
    ]
    total_before_discount = 300000.0
    discount_amount = 30000.0 # 10%
    final_total = total_before_discount - discount_amount

    print(f"  - Khách hàng '{customer_name}' mua 3 cái '{product_a} (S, Trắng)' trị giá 300.000đ")
    print(f"  - Áp dụng mã giảm giá '{promo_code}' (Giảm {discount_amount:,.0f}đ)")
    
    SalesService.create_sale(
        customer_name=customer_name,
        total=final_total,
        payment_method="Tiền mặt",
        cart_items=cart,
        discount_code=promo_code,
        discount_amount=discount_amount
    )

    # Kiểm tra tồn kho sau khi mua hàng
    stock_a_after = get_product_stock(product_a)
    print(f"  ➔ Tồn kho '{product_a}' còn: {stock_a_after} (Mong đợi: 47)")
    assert stock_a_after == 47, "Lỗi logic: Giảm trừ tồn kho khi bán hàng sai!"

    # Kiểm tra điểm tích lũy và xếp hạng thành viên (Quy tắc: 10,000 ₫ = 1 điểm tích lũy)
    cust_data = get_customer_data(customer_name)
    expected_points = int(final_total // 10000) # 270k // 10000 = 27 điểm
    print(f"  ➔ Khách hàng nhận được: {cust_data[0]} điểm tích lũy | Hạng thành viên: {cust_data[1]}")
    assert cust_data[0] == expected_points, f"Lỗi logic: Tính điểm tích lũy sai! Nhận {cust_data[0]}, mong đợi {expected_points}"
    assert cust_data[1] == "Đồng", f"Lỗi logic: Hệ tính phân hạng thành viên sai! Nhận {cust_data[1]}, mong đợi Đồng"

    # Kiểm tra số lần sử dụng mã giảm giá tăng lên
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT used_count FROM promotions WHERE code = ?", (promo_code,))
    promo_used = cursor.fetchone()[0]
    conn.close()
    print(f"  ➔ Số lần dùng mã '{promo_code}': {promo_used} (Mong đợi: 1)")
    assert promo_used == 1, "Lỗi logic: Chưa cập nhật số lượt đã dùng của mã ưu đãi!"

    # Lấy mã hóa đơn vừa sinh ra
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM invoices ORDER BY id DESC LIMIT 1")
    invoice_id = cursor.fetchone()[0]
    conn.close()
    print(f"  ➔ Mã hóa đơn vừa tạo: HD{invoice_id:03d}")

    # 5. Kiểm tra luồng Đổi trả hàng (Exchange & Refund)
    print("\n🟢 [Bước 3: Kiểm tra luồng Đổi Hàng - Trả Hàng]")
    
    # 5a. Đổi 1 chiếc Áo thun trắng (product_a) lấy 1 chiếc Quần jeans xanh (product_b)
    print(f"  - Tiến hành ĐỔI HÀNG: Đổi 1 chiếc '{product_a} (S, Trắng)' lấy 1 chiếc '{product_b} (M, Xanh nhạt)'")
    ReturnService.process_return(
        invoice_id=invoice_id,
        product_name=f"{product_a} (S, Trắng)",
        quantity=1,
        price=100000.0,
        reason="Đổi mẫu",
        return_type="EXCHANGE",
        new_product_name=f"{product_b} (M, Xanh nhạt)",
        price_diff=0.0
    )

    stock_a_exc = get_product_stock(product_a)
    stock_b_exc = get_product_stock(product_b)
    print(f"  ➔ Tồn kho '{product_a}' sau đổi: {stock_a_exc} (Mong đợi: 48 - được cộng trả 1 chiếc)")
    print(f"  ➔ Tồn kho '{product_b}' sau đổi: {stock_b_exc} (Mong đợi: 29 - bị giảm đi 1 chiếc mới lấy)")
    assert stock_a_exc == 48, "Lỗi logic đổi hàng: Chưa cộng lại tồn kho sản phẩm cũ!"
    assert stock_b_exc == 29, "Lỗi logic đổi hàng: Chưa khấu trừ tồn kho sản phẩm mới đổi!"

    # 5b. Trả hàng hoàn tiền 1 chiếc Áo thun trắng còn lại
    print(f"  - Tiến hành TRẢ HÀNG HOÀN TIỀN: Trả lại 1 chiếc '{product_a} (S, Trắng)' lấy lại tiền")
    ReturnService.process_return(
        invoice_id=invoice_id,
        product_name=f"{product_a} (S, Trắng)",
        quantity=1,
        price=100000.0,
        reason="Không vừa ý",
        return_type="REFUND"
    )

    stock_a_ref = get_product_stock(product_a)
    print(f"  ➔ Tồn kho '{product_a}' sau hoàn tiền: {stock_a_ref} (Mong đợi: 49 - được cộng trả thêm 1 chiếc)")
    assert stock_a_ref == 49, "Lỗi logic trả hàng hoàn tiền: Chưa cộng trả tồn kho sản phẩm hoàn trả!"

    # 6. Kiểm tra phân hệ Báo cáo kinh doanh (Reporting)
    print("\n🟢 [Bước 4: Kiểm tra luồng Báo cáo doanh thu & Lợi nhuận]")
    months = ReportService.get_available_months()
    print(f"  - Các tháng có dữ liệu báo cáo: {months}")
    assert len(months) > 0, "Lỗi logic: Không lấy được danh sách tháng khả dụng!"

    # Chạy thử xuất báo cáo Excel
    report_file = ReportService.export_excel("2026-05")
    print(f"  ➔ Đã xuất file báo cáo tháng tại: {report_file}")
    assert os.path.exists(report_file), "Lỗi xuất báo cáo: Không tạo được tệp Excel báo cáo!"

    # 7. Kiểm tra phân hệ Nhân sự & Chấm công (Staff & Attendance)
    print("\n🟢 [Bước 5: Kiểm tra luồng Chấm công & Tính lương nhân viên]")
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM staff WHERE full_name = 'Trần Thu Trang'")
    cursor.execute("""
        INSERT INTO staff (full_name, role, shift, salary, attendance_days, total_hours)
        VALUES ('Trần Thu Trang', 'Nhân viên bán hàng', 'Ca Sáng', 20000, 0, 0.0)
    """)
    conn.commit()
    
    cursor.execute("SELECT id FROM staff WHERE full_name = 'Trần Thu Trang'")
    staff_id = cursor.fetchone()[0]
    conn.close()
    
    print(f"  - Đã thêm nhân viên thử nghiệm: 'Trần Thu Trang' (ID: {staff_id}, Lương: 20.000đ/giờ, ca quy định: 4h)")

    # 7b. Vào ca (Check-in) lúc 4.5 giờ trước để thử nghiệm
    from datetime import datetime, timedelta
    check_in_time = (datetime.now() - timedelta(hours=4.5)).strftime("%Y-%m-%d %H:%M:%S")
    StaffService.start_shift(staff_id, check_in_time)
    print(f"  - Đã vào ca làm việc lúc: {check_in_time}")

    # 7c. Chốt ca làm việc (Check-out) - làm được 4.5 giờ
    # Không bị phạt vì ca quy định chỉ là 4h
    hours_worked = 4.5
    shift_pay = hours_worked * 20000 # 90.000đ
    StaffService.end_shift(staff_id, hours_worked)
    
    AttendanceModel.log_attendance(
        staff_id, "Trần Thu Trang", check_in_time, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), hours_worked, shift_pay
    )
    print(f"  ➔ Kết thúc ca thành công! Số giờ tích lũy: {hours_worked} giờ | Lương ca này: {shift_pay:,.0f}đ")

    # 7d. Tính toán bảng lương và Reset công
    unpaid_earnings = AttendanceModel.get_unpaid_earnings(staff_id)
    print(f"  ➔ Lương chưa trả thực nhận: {unpaid_earnings:,.0f}đ (Mong đợi: 90.000đ)")
    assert unpaid_earnings == 90000, f"Lỗi logic tính lương: Tính sai lương ca làm! Nhận {unpaid_earnings}, mong đợi 90000"

    # Chốt lương & Reset ngày công
    StaffService.reset_attendance(staff_id)
    AttendanceModel.mark_as_paid(staff_id)
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT total_hours FROM staff WHERE id = ?", (staff_id,))
    reset_hours = cursor.fetchone()[0]
    conn.close()
    print(f"  ➔ Số giờ làm của nhân viên sau khi chốt công: {reset_hours} (Mong đợi: 0)")
    assert reset_hours == 0, "Lỗi logic chốt công: Chưa reset tổng số giờ tích lũy của nhân viên!"

    # Dọn dẹp dữ liệu test nhân viên và khách hàng để tránh làm rác database
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM staff WHERE id = ?", (staff_id,))
    cursor.execute("DELETE FROM attendance_history WHERE staff_id = ?", (staff_id,))
    cursor.execute("DELETE FROM customers WHERE full_name = ?", (customer_name,))
    conn.commit()
    conn.close()

    print("\n" + "="*60)
    print("🎉 TẤT CẢ CÁC BƯỚC KIỂM THỬ HỆ THỐNG ĐÃ THÀNH CÔNG VÀ CHUẨN XÁC 100%!")
    print("="*60)

if __name__ == "__main__":
    run_all_tests()
