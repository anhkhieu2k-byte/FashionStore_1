import sqlite3
import os
from config import DATABASE_NAME


class ReportService:

    @staticmethod
    def get_summary():
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Tổng doanh thu
        cursor.execute("SELECT SUM(total) FROM invoices")
        revenue = cursor.fetchone()[0] or 0

        # Tổng hóa đơn
        cursor.execute("SELECT COUNT(*) FROM invoices")
        total_invoices = cursor.fetchone()[0] or 0

        # Sản phẩm bán chạy nhất
        cursor.execute("""
            SELECT product_name, SUM(quantity) as total_sold
            FROM invoice_details
            GROUP BY product_name
            ORDER BY total_sold DESC
            LIMIT 1
        """)
        best_seller_row = cursor.fetchone()
        best_seller = best_seller_row[0] if best_seller_row else "---"

        # Tổng tiền trả hàng
        try:
            cursor.execute("SELECT SUM(refund_amount) FROM return_orders")
            total_refund = cursor.fetchone()[0] or 0
        except Exception:
            total_refund = 0

        cursor.execute("""
            SELECT SUM(id.quantity * CASE WHEN COALESCE(p.import_price, 0) > 0 THEN p.import_price ELSE id.price * 0.6 END)
            FROM invoice_details id
            LEFT JOIN products p ON (CASE WHEN INSTR(id.product_name, ' (') > 0 THEN SUBSTR(id.product_name, 1, INSTR(id.product_name, ' (') - 1) ELSE id.product_name END) = p.name
        """)
        total_cost = cursor.fetchone()[0] or 0

        import datetime
        today = datetime.date.today()
        today_str = today.strftime('%Y-%m-%d')
        month_str = today.strftime('%Y-%m')
        year_str = today.strftime('%Y')

        # Doanh thu hôm nay
        cursor.execute("SELECT SUM(total) FROM invoices WHERE created_at LIKE ?", (f"{today_str}%",))
        revenue_today = cursor.fetchone()[0] or 0

        # Doanh thu tháng này
        cursor.execute("SELECT SUM(total) FROM invoices WHERE created_at LIKE ?", (f"{month_str}%",))
        revenue_month = cursor.fetchone()[0] or 0

        # Doanh thu năm nay
        cursor.execute("SELECT SUM(total) FROM invoices WHERE created_at LIKE ?", (f"{year_str}%",))
        revenue_year = cursor.fetchone()[0] or 0

        profit = revenue - total_cost
        profit_margin = (profit / revenue * 100) if revenue > 0 else 0

        conn.close()
        return {
            "revenue": revenue,
            "total_invoices": total_invoices,
            "best_seller": best_seller,
            "total_refund": total_refund,
            "total_cost": total_cost,
            "profit": profit,
            "profit_margin": profit_margin,
            "revenue_today": revenue_today,
            "revenue_month": revenue_month,
            "revenue_year": revenue_year,
        }

    @staticmethod
    def get_top_selling():
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT product_name, SUM(quantity), SUM(subtotal)
            FROM invoice_details
            GROUP BY product_name
            ORDER BY SUM(quantity) DESC
            LIMIT 8
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_low_stock():
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT name, stock, 10 FROM products WHERE stock <= 10 LIMIT 8")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_profit_by_product():
        """Lợi nhuận chi tiết theo từng sản phẩm"""
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                id.product_name,
                SUM(id.quantity)                            AS so_luong,
                ROUND(AVG(id.price), 0)                    AS gia_ban,
                ROUND(AVG(CASE WHEN COALESCE(p.import_price, 0) > 0 THEN p.import_price ELSE id.price * 0.6 END), 0) AS gia_nhap,
                SUM(id.subtotal)                           AS doanh_thu,
                SUM(id.quantity * CASE WHEN COALESCE(p.import_price, 0) > 0 THEN p.import_price ELSE id.price * 0.6 END) AS gia_von,
                SUM(id.subtotal) - SUM(id.quantity * CASE WHEN COALESCE(p.import_price, 0) > 0 THEN p.import_price ELSE id.price * 0.6 END) AS loi_nhuan
            FROM invoice_details id
            LEFT JOIN products p ON (CASE WHEN INSTR(id.product_name, ' (') > 0 THEN SUBSTR(id.product_name, 1, INSTR(id.product_name, ' (') - 1) ELSE id.product_name END) = p.name
            GROUP BY id.product_name
            ORDER BY loi_nhuan DESC
        """)
        data = cursor.fetchall()
        conn.close()
        return data  # (name, qty, price, import, revenue, cost, profit)

    @staticmethod
    def get_profit_chart_data():
        """Lấy doanh thu + giá vốn theo từng hóa đơn (15 gần nhất) để vẽ biểu đồ lợi nhuận"""
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                i.id,
                i.total,
                COALESCE(SUM(id.quantity * CASE WHEN COALESCE(p.import_price, 0) > 0 THEN p.import_price ELSE id.price * 0.6 END), 0) AS cost
            FROM invoices i
            LEFT JOIN invoice_details id ON i.id = id.invoice_id
            LEFT JOIN products p ON (CASE WHEN INSTR(id.product_name, ' (') > 0 THEN SUBSTR(id.product_name, 1, INSTR(id.product_name, ' (') - 1) ELSE id.product_name END) = p.name
            GROUP BY i.id
            ORDER BY i.id DESC
            LIMIT 15
        """)
        data = cursor.fetchall()
        data.reverse()
        conn.close()
        return data  # (id, revenue, cost)

    @staticmethod
    def get_weekly_chart_data():
        import datetime
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        # Lấy tháng gần nhất có hóa đơn
        cursor.execute("SELECT strftime('%Y-%m', created_at) FROM invoices ORDER BY created_at DESC LIMIT 1")
        row = cursor.fetchone()
        if row and row[0]:
            target_month = row[0]
        else:
            target_month = datetime.date.today().strftime('%Y-%m')
            
        # Lấy tất cả hóa đơn trong tháng này
        cursor.execute("""
            SELECT 
                strftime('%d', i.created_at) AS day_str,
                i.total AS revenue,
                COALESCE(SUM(id.quantity * CASE WHEN COALESCE(p.import_price, 0) > 0 THEN p.import_price ELSE id.price * 0.6 END), 0) AS cost
            FROM invoices i
            LEFT JOIN invoice_details id ON i.id = id.invoice_id
            LEFT JOIN products p ON (CASE WHEN INSTR(id.product_name, ' (') > 0 THEN SUBSTR(id.product_name, 1, INSTR(id.product_name, ' (') - 1) ELSE id.product_name END) = p.name
            WHERE strftime('%Y-%m', i.created_at) = ?
            GROUP BY i.id
        """, (target_month,))
        
        invoices_data = cursor.fetchall()
        conn.close()
        
        # Định nghĩa 5 tuần
        weeks = {
            "Tuần 1": {"revenue": 0.0, "cost": 0.0},
            "Tuần 2": {"revenue": 0.0, "cost": 0.0},
            "Tuần 3": {"revenue": 0.0, "cost": 0.0},
            "Tuần 4": {"revenue": 0.0, "cost": 0.0},
            "Tuần 5": {"revenue": 0.0, "cost": 0.0}
        }
        
        for day_str, rev, cost in invoices_data:
            try:
                day = int(day_str)
            except ValueError:
                day = 1
                
            if day <= 7:
                w_key = "Tuần 1"
            elif day <= 14:
                w_key = "Tuần 2"
            elif day <= 21:
                w_key = "Tuần 3"
            elif day <= 28:
                w_key = "Tuần 4"
            else:
                w_key = "Tuần 5"
                
            weeks[w_key]["revenue"] += rev
            weeks[w_key]["cost"] += cost
            
        # Chuyển đổi thành dạng tuple list
        month_num = target_month.split("-")[1]
        
        result = []
        for w_name in ["Tuần 1", "Tuần 2", "Tuần 3", "Tuần 4", "Tuần 5"]:
            label = w_name
            result.append((label, weeks[w_name]["revenue"], weeks[w_name]["cost"]))
            
        return result

    @staticmethod
    def get_monthly_chart_data():
        import datetime
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        # Lấy năm gần nhất có hóa đơn
        cursor.execute("SELECT strftime('%Y', created_at) FROM invoices ORDER BY created_at DESC LIMIT 1")
        row = cursor.fetchone()
        if row and row[0]:
            target_year = row[0]
        else:
            target_year = str(datetime.date.today().year)
            
        cursor.execute("""
            SELECT 
                rev.month_str,
                rev.revenue,
                COALESCE(cst.cost, 0) AS cost
            FROM (
                SELECT strftime('%m', created_at) AS month_str, SUM(total) AS revenue
                FROM invoices
                WHERE strftime('%Y', created_at) = ?
                GROUP BY month_str
            ) rev
            LEFT JOIN (
                SELECT 
                    strftime('%m', i.created_at) AS month_str,
                    SUM(id.quantity * CASE WHEN COALESCE(p.import_price, 0) > 0 THEN p.import_price ELSE id.price * 0.6 END) AS cost
                FROM invoices i
                LEFT JOIN invoice_details id ON i.id = id.invoice_id
                LEFT JOIN products p ON (CASE WHEN INSTR(id.product_name, ' (') > 0 THEN SUBSTR(id.product_name, 1, INSTR(id.product_name, ' (') - 1) ELSE id.product_name END) = p.name
                WHERE strftime('%Y', i.created_at) = ?
                GROUP BY month_str
            ) cst ON rev.month_str = cst.month_str
        """, (target_year, target_year))
        
        db_data = cursor.fetchall()
        conn.close()
        
        months_dict = {f"{i:02d}": {"revenue": 0.0, "cost": 0.0} for i in range(1, 13)}
        for m_str, rev, cost in db_data:
            if m_str in months_dict:
                months_dict[m_str]["revenue"] = rev
                months_dict[m_str]["cost"] = cost
                
        result = []
        for i in range(1, 13):
            m_str = f"{i:02d}"
            label = f"T{i}"
            result.append((label, months_dict[m_str]["revenue"], months_dict[m_str]["cost"]))
            
        return result

    @staticmethod
    def get_yearly_chart_data():
        import datetime
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        # Lấy năm gần nhất có hóa đơn làm mốc kết thúc của 5 năm
        cursor.execute("SELECT strftime('%Y', created_at) FROM invoices ORDER BY created_at DESC LIMIT 1")
        row = cursor.fetchone()
        if row and row[0]:
            end_year = int(row[0])
        else:
            end_year = datetime.date.today().year
            
        start_year = end_year - 4
        years_list = [str(y) for y in range(start_year, end_year + 1)]
        
        cursor.execute("""
            SELECT 
                rev.year_str,
                rev.revenue,
                COALESCE(cst.cost, 0) AS cost
            FROM (
                SELECT strftime('%Y', created_at) AS year_str, SUM(total) AS revenue
                FROM invoices
                WHERE CAST(strftime('%Y', created_at) AS INTEGER) BETWEEN ? AND ?
                GROUP BY year_str
            ) rev
            LEFT JOIN (
                SELECT 
                    strftime('%Y', i.created_at) AS year_str,
                    SUM(id.quantity * CASE WHEN COALESCE(p.import_price, 0) > 0 THEN p.import_price ELSE id.price * 0.6 END) AS cost
                FROM invoices i
                LEFT JOIN invoice_details id ON i.id = id.invoice_id
                LEFT JOIN products p ON (CASE WHEN INSTR(id.product_name, ' (') > 0 THEN SUBSTR(id.product_name, 1, INSTR(id.product_name, ' (') - 1) ELSE id.product_name END) = p.name
                WHERE CAST(strftime('%Y', i.created_at) AS INTEGER) BETWEEN ? AND ?
                GROUP BY year_str
            ) cst ON rev.year_str = cst.year_str
        """, (start_year, end_year, start_year, end_year))
        
        db_data = cursor.fetchall()
        conn.close()
        
        years_dict = {y: {"revenue": 0.0, "cost": 0.0} for y in years_list}
        for y_str, rev, cost in db_data:
            if y_str in years_dict:
                years_dict[y_str]["revenue"] = rev
                years_dict[y_str]["cost"] = cost
                
        result = []
        for y in years_list:
            result.append((y, years_dict[y]["revenue"], years_dict[y]["cost"]))
            
        return result

    @staticmethod
    def get_chart_data():
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, total FROM invoices ORDER BY id DESC LIMIT 15")
        data = cursor.fetchall()
        data.reverse()
        conn.close()
        return data

    @staticmethod
    def get_available_months():
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT strftime('%Y-%m', created_at) FROM invoices ORDER BY created_at DESC")
        months = [row[0] for row in cursor.fetchall() if row[0]]
        conn.close()
        return months

    @staticmethod
    def get_available_years():
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT strftime('%Y', created_at) FROM invoices ORDER BY created_at DESC")
        years = [row[0] for row in cursor.fetchall() if row[0]]
        conn.close()
        return years

    @staticmethod
    def export_excel(selected_period=None):
        if not os.path.exists("exports/excel_reports"):
            os.makedirs("exports/excel_reports")

        conn = sqlite3.connect(DATABASE_NAME)
        try:
            import pandas as pd
            if selected_period and selected_period != "Tất cả":
                if len(selected_period) == 4: # Year
                    month_filter_invoices = f"WHERE strftime('%Y', created_at) = '{selected_period}'"
                    month_filter_details = f"WHERE strftime('%Y', i.created_at) = '{selected_period}'"
                    file_path = f"exports/excel_reports/Bao_cao_kinh_doanh_nam_{selected_period}.xlsx"
                else: # Month
                    month_filter_invoices = f"WHERE strftime('%Y-%m', created_at) = '{selected_period}'"
                    month_filter_details = f"WHERE strftime('%Y-%m', i.created_at) = '{selected_period}'"
                    file_path = f"exports/excel_reports/Bao_cao_kinh_doanh_{selected_period}.xlsx"
            else:
                month_filter_invoices = ""
                month_filter_details = ""
                file_path = "exports/excel_reports/Bao_cao_kinh_doanh.xlsx"

            with pd.ExcelWriter(file_path) as writer:
                # 1. Báo cáo theo tháng
                df_monthly = pd.read_sql_query(f"""
                    SELECT 
                        strftime('%Y-%m', i.created_at) AS Thang,
                        COUNT(i.id) AS So_Hoa_Don,
                        SUM(i.total) AS Tong_Doanh_Thu,
                        SUM(COALESCE(inv_cost.cost, 0)) AS Tong_Gia_Von,
                        SUM(i.total) - SUM(COALESCE(inv_cost.cost, 0)) AS Loi_Nhuan
                    FROM invoices i
                    LEFT JOIN (
                        SELECT 
                            id.invoice_id,
                            SUM(id.quantity * CASE WHEN COALESCE(p.import_price, 0) > 0 THEN p.import_price ELSE id.price * 0.6 END) AS cost
                        FROM invoice_details id
                        LEFT JOIN products p ON (CASE WHEN INSTR(id.product_name, ' (') > 0 THEN SUBSTR(id.product_name, 1, INSTR(id.product_name, ' (') - 1) ELSE id.product_name END) = p.name
                        GROUP BY id.invoice_id
                    ) inv_cost ON i.id = inv_cost.invoice_id
                    {month_filter_invoices}
                    GROUP BY Thang
                    ORDER BY Thang DESC
                """, conn)
                df_monthly.to_excel(writer, sheet_name='BaoCaoTheoThang', index=False)

                # 2. Tổng quan
                df_summary = pd.read_sql_query(f"""
                    SELECT
                        (SELECT SUM(total) FROM invoices {month_filter_invoices}) AS Tong_Doanh_Thu,
                        (SELECT SUM(id.quantity * CASE WHEN COALESCE(p.import_price, 0) > 0 THEN p.import_price ELSE id.price * 0.6 END)
                           FROM invoice_details id
                           LEFT JOIN products p ON (CASE WHEN INSTR(id.product_name, ' (') > 0 THEN SUBSTR(id.product_name, 1, INSTR(id.product_name, ' (') - 1) ELSE id.product_name END) = p.name
                           WHERE id.invoice_id IN (SELECT id FROM invoices {month_filter_invoices})) AS Tong_Gia_Von,
                        ((SELECT SUM(total) FROM invoices {month_filter_invoices}) -
                         (SELECT SUM(id.quantity * CASE WHEN COALESCE(p.import_price, 0) > 0 THEN p.import_price ELSE id.price * 0.6 END)
                           FROM invoice_details id
                           LEFT JOIN products p ON (CASE WHEN INSTR(id.product_name, ' (') > 0 THEN SUBSTR(id.product_name, 1, INSTR(id.product_name, ' (') - 1) ELSE id.product_name END) = p.name
                           WHERE id.invoice_id IN (SELECT id FROM invoices {month_filter_invoices}))) AS Loi_Nhuan
                """, conn)
                df_summary.to_excel(writer, sheet_name='TongQuan', index=False)

                # 3. Lợi nhuận chi tiết theo sản phẩm
                df_profit = pd.read_sql_query(f"""
                    SELECT
                        id.product_name AS San_Pham,
                        SUM(id.quantity) AS So_Luong,
                        ROUND(AVG(id.price), 0) AS Gia_Ban,
                        ROUND(AVG(CASE WHEN COALESCE(p.import_price, 0) > 0 THEN p.import_price ELSE id.price * 0.6 END), 0) AS Gia_Nhap,
                        SUM(id.subtotal) AS Doanh_Thu,
                        SUM(id.quantity * CASE WHEN COALESCE(p.import_price, 0) > 0 THEN p.import_price ELSE id.price * 0.6 END) AS Gia_Von,
                        SUM(id.subtotal) - SUM(id.quantity * CASE WHEN COALESCE(p.import_price, 0) > 0 THEN p.import_price ELSE id.price * 0.6 END) AS Loi_Nhuan
                    FROM invoice_details id
                    LEFT JOIN products p ON (CASE WHEN INSTR(id.product_name, ' (') > 0 THEN SUBSTR(id.product_name, 1, INSTR(id.product_name, ' (') - 1) ELSE id.product_name END) = p.name
                    JOIN invoices i ON id.invoice_id = i.id
                    {month_filter_details}
                    GROUP BY id.product_name
                    ORDER BY Loi_Nhuan DESC
                """, conn)
                df_profit.to_excel(writer, sheet_name='LoiNhuanChiTiet', index=False)

                # 4. Hóa đơn
                df_invoices = pd.read_sql_query(f"""
                    SELECT 
                        id AS "Mã HĐ",
                        customer_name AS "Khách hàng",
                        total AS "Tổng tiền",
                        payment_method AS "Phương thức TT",
                        discount_code AS "Mã giảm giá",
                        discount_amount AS "Số tiền giảm",
                        status AS "Trạng thái",
                        created_at AS "Thời gian"
                    FROM invoices 
                    {month_filter_invoices}
                    ORDER BY created_at DESC
                """, conn)
                df_invoices["Mã HĐ"] = df_invoices["Mã HĐ"].apply(lambda x: f"HD{x:03d}")
                df_invoices.to_excel(writer, sheet_name='HoaDon', index=False)

            return file_path
        except ImportError:
            import csv
            if selected_period and selected_period != "Tất cả":
                if len(selected_period) == 4:
                    file_path = f"exports/excel_reports/report_summary_nam_{selected_period}.csv"
                    query = "SELECT * FROM invoices WHERE strftime('%Y', created_at) = ?"
                else:
                    file_path = f"exports/excel_reports/report_summary_{selected_period}.csv"
                    query = "SELECT * FROM invoices WHERE strftime('%Y-%m', created_at) = ?"
                params = (selected_period,)
            else:
                file_path = "exports/excel_reports/report_summary.csv"
                query = "SELECT * FROM invoices"
                params = ()
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            colnames = [d[0] for d in cursor.description]
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                w = csv.writer(f)
                w.writerow(colnames)
                w.writerows(rows)
            return file_path
        finally:
            conn.close()

    @staticmethod
    def get_invoices_by_month(month):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, customer_name, total, payment_method, created_at, status 
            FROM invoices 
            WHERE strftime('%Y-%m', created_at) = ?
            ORDER BY created_at DESC
        """, (month,))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_monthly_summary(month):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        # Doanh thu tháng
        cursor.execute("SELECT SUM(total) FROM invoices WHERE strftime('%Y-%m', created_at) = ?", (month,))
        revenue = cursor.fetchone()[0] or 0
        
        # Số hóa đơn tháng
        cursor.execute("SELECT COUNT(*) FROM invoices WHERE strftime('%Y-%m', created_at) = ?", (month,))
        total_invoices = cursor.fetchone()[0] or 0
        
        # Giá vốn tháng
        cursor.execute("""
            SELECT SUM(id.quantity * CASE WHEN COALESCE(p.import_price, 0) > 0 THEN p.import_price ELSE id.price * 0.6 END)
            FROM invoice_details id
            LEFT JOIN products p ON (CASE WHEN INSTR(id.product_name, ' (') > 0 THEN SUBSTR(id.product_name, 1, INSTR(id.product_name, ' (') - 1) ELSE id.product_name END) = p.name
            WHERE id.invoice_id IN (SELECT id FROM invoices WHERE strftime('%Y-%m', created_at) = ?)
        """, (month,))
        total_cost = cursor.fetchone()[0] or 0
        
        profit = revenue - total_cost
        conn.close()
        return {
            "revenue": revenue,
            "total_invoices": total_invoices,
            "profit": profit
        }