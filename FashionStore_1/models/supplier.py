from database.db_connect import get_connection

class Supplier:
    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM suppliers")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_or_create(name):
        name = name.strip()
        if not name:
            return None
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM suppliers WHERE UPPER(name) = UPPER(?)", (name,))
        row = cursor.fetchone()
        if row:
            conn.close()
            return row
        else:
            cursor.execute("INSERT INTO suppliers(name, phone, address) VALUES (?, ?, ?)", (name, "", ""))
            conn.commit()
            cursor.execute("SELECT * FROM suppliers WHERE name = ?", (name,))
            new_row = cursor.fetchone()
            conn.close()
            return new_row
