from models.staff import Staff


class StaffService:

    @staticmethod
    def get_staff():

        return Staff.get_all()

    @staticmethod
    def add_staff(
            full_name,
            birth_date,
            phone,
            address,
            role,
            shift,
            salary,
            attendance_days,
            password="123456"
    ):

        Staff.create(
            full_name,
            birth_date,
            phone,
            address,
            role,
            shift,
            salary,
            attendance_days,
            password
        )

    @staticmethod
    def update_staff(
            staff_id,
            full_name,
            birth_date,
            phone,
            address,
            role,
            shift,
            salary,
            attendance_days,
            password="123456"
    ):

        Staff.update(
            staff_id,
            full_name,
            birth_date,
            phone,
            address,
            role,
            shift,
            salary,
            attendance_days,
            password
        )

    @staticmethod
    def delete_staff(staff_id):

        Staff.delete(staff_id)

    @staticmethod
    def search_staff(keyword):

        return Staff.search(keyword)

    @staticmethod
    def start_shift(staff_id, check_in_time):
        Staff.update_check_in(staff_id, check_in_time)

    @staticmethod
    def end_shift(staff_id, hours):
        Staff.add_hours(staff_id, hours)

    @staticmethod
    def reset_attendance(staff_id):
        Staff.reset_hours(staff_id)

    @staticmethod
    def export_payroll_excel():
        import os
        import sqlite3
        from config import DATABASE_NAME
        
        if not os.path.exists("exports/excel_reports"):
            os.makedirs("exports/excel_reports")

        conn = sqlite3.connect(DATABASE_NAME)
        try:
            import pandas as pd
            file_path = "exports/excel_reports/Bang_tinh_luong_nhan_vien.xlsx"
            
            # Lấy dữ liệu nhân viên
            df = pd.read_sql_query("SELECT * FROM staff", conn)
            
            # Tính toán lương thực tế cho từng nhân viên
            def calculate_salary(row):
                from models.attendance import AttendanceModel
                salary_base = float(row['salary'] or 0)
                unpaid_earnings = AttendanceModel.get_unpaid_earnings(row['id'])
                
                if salary_base > 100000:
                    return max(0.0, salary_base + unpaid_earnings)
                else:
                    return unpaid_earnings

            df['Luong_Thuc_Nhan'] = df.apply(calculate_salary, axis=1)
            
            # Đổi tên cột cho đẹp
            df_export = df.rename(columns={
                'id': 'Mã NV',
                'full_name': 'Họ Tên',
                'phone': 'Điện thoại',
                'role': 'Chức vụ',
                'salary': 'Lương cơ bản',
                'attendance_days': 'Số ngày công',
                'total_hours': 'Tổng giờ làm',
                'Luong_Thuc_Nhan': 'Lương thực nhận'
            })
            
            # Chỉ lấy các cột cần thiết
            cols = ['Mã NV', 'Họ Tên', 'Điện thoại', 'Chức vụ', 'Lương cơ bản', 'Số ngày công', 'Tổng giờ làm', 'Lương thực nhận']
            df_export = df_export[cols]
            
            df_export.to_excel(file_path, index=False)
            return file_path
        except ImportError:
            import csv
            file_path = "exports/excel_reports/Bang_tinh_luong_nhan_vien.csv"
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM staff")
            rows = cursor.fetchall()
            colnames = [d[0] for d in cursor.description]
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                w = csv.writer(f)
                w.writerow(colnames)
                w.writerows(rows)
            return file_path
        finally:
            conn.close()