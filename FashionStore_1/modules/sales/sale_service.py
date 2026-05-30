from models.sale import Sale


class SalesService:

    @staticmethod
    def create_sale(
            customer_name,
            total,
            payment_method,
            cart_items,
            discount_code='',
            discount_amount=0
    ):

        invoice_id = Sale.create_invoice(
            customer_name,
            total,
            payment_method,
            discount_code,
            discount_amount
        )

        # Cập nhật số lượt đã dùng của mã giảm giá
        if discount_code:
            from modules.promotions.promotion_service import PromotionService
            PromotionService.increment_used_count(discount_code)

        for item in cart_items:

            Sale.add_invoice_detail(
                invoice_id,
                item["product_name"],
                item["quantity"],
                item["price"],
                item["subtotal"]
            )

            # Khấu trừ số lượng tồn kho sản phẩm sau khi bán thành công
            try:
                prod_id = item.get("product_id")
                from database.db_connect import get_connection
                conn = get_connection()
                cursor = conn.cursor()
                if prod_id:
                    cursor.execute("""
                        UPDATE products SET stock = max(0, stock - ?)
                        WHERE id = ?
                    """, (item["quantity"], prod_id))
                else:
                    prod_name = item["product_name"]
                    base_name = prod_name
                    if " (" in prod_name:
                        base_name = prod_name.split(" (")[0].strip()
                    cursor.execute("""
                        UPDATE products SET stock = max(0, stock - ?)
                        WHERE name = ?
                    """, (item["quantity"], base_name))
                conn.commit()
                conn.close()
            except Exception as e:
                print("Error deducting product stock on checkout:", e)

        # Tự động tính điểm tích lũy và cập nhật hạng thành viên
        if customer_name and customer_name != "Khách lẻ":
            try:
                from models.customer import Customer
                customer = Customer.get_by_name(customer_name)
                if customer:
                    cust_id = customer[0]
                    current_points = int(customer[4] or 0)
                    
                    # Quy tắc: 10,000 ₫ = 1 điểm tích lũy
                    earned_points = int(total // 10000)
                    new_points = current_points + earned_points
                    
                    # Xếp hạng thành viên
                    if new_points >= 500:
                        new_rank = "Kim cương"
                    elif new_points >= 300:
                        new_rank = "Vàng"
                    elif new_points >= 100:
                        new_rank = "Bạc"
                    else:
                        new_rank = "Đồng"
                        
                    Customer.update_points_and_rank(cust_id, new_points, new_rank)
            except Exception as e:
                print("Error updating customer points/rank at checkout:", e)

    @staticmethod
    def get_invoices():

        return Sale.get_invoices()

    @staticmethod
    def export_invoices_excel():
        import os
        from config import DATABASE_NAME
        import sqlite3
        
        if not os.path.exists("exports/excel_reports"):
            os.makedirs("exports/excel_reports")

        conn = sqlite3.connect(DATABASE_NAME)
        try:
            import pandas as pd
            file_path = "exports/excel_reports/lich_su_hoa_don.xlsx"
            
            # Lấy dữ liệu hóa đơn
            df = pd.read_sql_query("""
                SELECT 
                    id AS "Mã HĐ",
                    customer_name AS "Khách hàng",
                    total AS "Tổng tiền",
                    payment_method AS "Thanh toán",
                    discount_code AS "Mã giảm giá",
                    discount_amount AS "Số tiền giảm",
                    status AS "Trạng thái",
                    created_at AS "Thời gian"
                FROM invoices
                ORDER BY created_at DESC
            """, conn)
            
            # Định dạng cột Mã HĐ
            df["Mã HĐ"] = df["Mã HĐ"].apply(lambda x: f"HD{x:03d}")
            
            df.to_excel(file_path, index=False)
            return file_path
        except ImportError:
            import csv
            file_path = "exports/excel_reports/lich_su_hoa_don.csv"
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM invoices ORDER BY created_at DESC")
            rows = cursor.fetchall()
            colnames = [d[0] for d in cursor.description]
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                w = csv.writer(f)
                w.writerow(colnames)
                w.writerows(rows)
            return file_path
        finally:
            conn.close()