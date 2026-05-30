from database.db_connect import get_connection


class Promotion:

    @staticmethod
    def get_all():

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM promotions
        """)

        data = cursor.fetchall()

        conn.close()

        return data

    @staticmethod
    def create(
            code,
            discount_percent,
            min_order_value,
            start_date,
            end_date,
            quantity=999
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO promotions(
            code,
            discount_percent,
            min_order_value,
            start_date,
            end_date,
            quantity
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            code,
            discount_percent,
            min_order_value,
            start_date,
            end_date,
            quantity
        ))

        conn.commit()

        conn.close()

    @staticmethod
    def update(
            promotion_id,
            code,
            discount_percent,
            min_order_value,
            start_date,
            end_date,
            quantity=999
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        UPDATE promotions
        SET
            code = ?,
            discount_percent = ?,
            min_order_value = ?,
            start_date = ?,
            end_date = ?,
            quantity = ?
        WHERE id = ?
        """, (
            code,
            discount_percent,
            min_order_value,
            start_date,
            end_date,
            quantity,
            promotion_id
        ))

        conn.commit()

        conn.close()

    @staticmethod
    def delete(promotion_id):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM promotions
        WHERE id = ?
        """, (promotion_id,))

        conn.commit()

        conn.close()

    @staticmethod
    def search(keyword):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM promotions
        WHERE code LIKE ?
        """, (f"%{keyword}%",))

        data = cursor.fetchall()

        conn.close()

        return data

    @staticmethod
    def get_by_code(code):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM promotions WHERE UPPER(code) = UPPER(?)", (code,))
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def check_customer_usage(customer_name, code):
        if not customer_name or customer_name == "Khách lẻ":
            return 0
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM invoices 
            WHERE customer_name = ? AND discount_code = ?
        """, (customer_name, code))
        count = cursor.fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def increment_used_count(code):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE promotions 
            SET used_count = COALESCE(used_count, 0) + 1 
            WHERE UPPER(code) = UPPER(?)
        """, (code,))
        conn.commit()
        conn.close()