from database.db_connect import get_connection


class Staff:

    @staticmethod
    def get_all():

        conn = get_connection()

        cursor = conn.cursor()

        # Tự động cập nhật cấu trúc bảng nếu thiếu cột (Migration)
        try:
            cursor.execute("SELECT check_in_time FROM staff LIMIT 1")
        except:
            cursor.execute("ALTER TABLE staff ADD COLUMN check_in_time TEXT")
            cursor.execute("ALTER TABLE staff ADD COLUMN total_hours REAL DEFAULT 0")
            conn.commit()

        try:
            cursor.execute("SELECT password FROM staff LIMIT 1")
        except:
            cursor.execute("ALTER TABLE staff ADD COLUMN password TEXT DEFAULT '123456'")
            conn.commit()

        cursor.execute("""
        SELECT * FROM staff
        """)

        data = cursor.fetchall()

        conn.close()

        return data

    @staticmethod
    def update_check_in(staff_id, check_in_time):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE staff SET check_in_time = ? WHERE id = ?", (check_in_time, staff_id))
        conn.commit()
        conn.close()

    @staticmethod
    def add_hours(staff_id, hours):
        conn = get_connection()
        cursor = conn.cursor()
        # Vừa tăng ngày công, vừa cộng dồn số giờ thực tế
        cursor.execute("UPDATE staff SET attendance_days = attendance_days + 1, total_hours = total_hours + ?, check_in_time = NULL WHERE id = ?", (hours, staff_id))
        conn.commit()
        conn.close()

    @staticmethod
    def reset_hours(staff_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE staff SET attendance_days = 0, total_hours = 0 WHERE id = ?", (staff_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def create(
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

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO staff(
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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            full_name,
            birth_date,
            phone,
            address,
            role,
            shift,
            salary,
            attendance_days,
            password
        ))

        conn.commit()

        conn.close()

    @staticmethod
    def update(
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

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        UPDATE staff
        SET
            full_name = ?,
            birth_date = ?,
            phone = ?,
            address = ?,
            role = ?,
            shift = ?,
            salary = ?,
            attendance_days = ?,
            password = ?
        WHERE id = ?
        """, (
            full_name,
            birth_date,
            phone,
            address,
            role,
            shift,
            salary,
            attendance_days,
            password,
            staff_id
        ))

        conn.commit()

        conn.close()

    @staticmethod
    def delete(staff_id):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM staff
        WHERE id = ?
        """, (staff_id,))

        conn.commit()

        conn.close()

    @staticmethod
    def search(keyword):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM staff
        WHERE full_name LIKE ?
        """, (f"%{keyword}%",))

        data = cursor.fetchall()

        conn.close()

        return data