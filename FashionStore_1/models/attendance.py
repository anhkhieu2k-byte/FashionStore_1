import sqlite3
from database.db_connect import get_connection

class AttendanceModel:
    @staticmethod
    def _migrate_db(cursor):
        # Đảm bảo bảng tồn tại
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                staff_id INTEGER,
                staff_name TEXT,
                check_in TEXT,
                check_out TEXT,
                hours REAL,
                earned REAL,
                is_paid INTEGER DEFAULT 0
            )
        """)
        # Kiểm tra và thêm cột is_paid nếu thiếu
        try:
            cursor.execute("SELECT is_paid FROM attendance_history LIMIT 1")
        except sqlite3.OperationalError:
            try:
                cursor.execute("ALTER TABLE attendance_history ADD COLUMN is_paid INTEGER DEFAULT 0")
            except Exception:
                pass

    @staticmethod
    def log_attendance(staff_id, staff_name, check_in, check_out, hours, earned):
        conn = get_connection()
        cursor = conn.cursor()
        
        AttendanceModel._migrate_db(cursor)
        conn.commit()
            
        cursor.execute("""
            INSERT INTO attendance_history (staff_id, staff_name, check_in, check_out, hours, earned, is_paid)
            VALUES (?, ?, ?, ?, ?, ?, 0)
        """, (staff_id, staff_name, check_in, check_out, hours, earned))
        
        conn.commit()
        conn.close()

    @staticmethod
    def get_history(staff_id=None):
        conn = get_connection()
        cursor = conn.cursor()
        
        AttendanceModel._migrate_db(cursor)
        conn.commit()
        
        if staff_id:
            cursor.execute("SELECT * FROM attendance_history WHERE staff_id = ? ORDER BY id DESC", (staff_id,))
        else:
            cursor.execute("SELECT * FROM attendance_history ORDER BY id DESC")
            
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_unpaid_earnings(staff_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        AttendanceModel._migrate_db(cursor)
        conn.commit()
        
        cursor.execute("SELECT SUM(earned) FROM attendance_history WHERE staff_id = ? AND is_paid = 0", (staff_id,))
        res = cursor.fetchone()
        conn.close()
        return float(res[0] or 0)

    @staticmethod
    def mark_as_paid(staff_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        AttendanceModel._migrate_db(cursor)
        conn.commit()
        
        cursor.execute("UPDATE attendance_history SET is_paid = 1 WHERE staff_id = ?", (staff_id,))
        conn.commit()
        conn.close()
