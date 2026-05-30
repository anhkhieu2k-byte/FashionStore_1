from database.db_connect import get_connection


class Customer:

    @staticmethod
    def get_all():

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM customers
        """)

        data = cursor.fetchall()

        conn.close()

        return data

    @staticmethod
    def create(
            full_name,
            phone,
            email,
            points,
            member_rank
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO customers(
            full_name,
            phone,
            email,
            points,
            member_rank
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            full_name,
            phone,
            email,
            points,
            member_rank
        ))

        conn.commit()

        conn.close()

    @staticmethod
    def update(
            customer_id,
            full_name,
            phone,
            email,
            points,
            member_rank
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        UPDATE customers
        SET
            full_name = ?,
            phone = ?,
            email = ?,
            points = ?,
            member_rank = ?
        WHERE id = ?
        """, (
            full_name,
            phone,
            email,
            points,
            member_rank,
            customer_id
        ))

        conn.commit()

        conn.close()

    @staticmethod
    def delete(customer_id):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM customers
        WHERE id = ?
        """, (customer_id,))

        conn.commit()

        conn.close()

    @staticmethod
    def search(keyword):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM customers
        WHERE full_name LIKE ? OR phone LIKE ?
        """, (f"%{keyword}%", f"%{keyword}%"))

        data = cursor.fetchall()

        conn.close()

        return data

    @staticmethod
    def get_purchase_history(customer_name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, total, payment_method, created_at FROM invoices
        WHERE customer_name = ?
        ORDER BY created_at DESC
        """, (customer_name,))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_by_name(full_name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE full_name = ?", (full_name,))
        row = cursor.fetchone()
        conn.close()
        return row

    @staticmethod
    def update_points_and_rank(customer_id, points, rank):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE customers
        SET points = ?, member_rank = ?
        WHERE id = ?
        """, (points, rank, customer_id))
        conn.commit()
        conn.close()