from database.db_connect import get_connection

class Sale:

    @staticmethod
    def create_invoice(
            customer_name,
            total,
            payment_method,
            discount_code='',
            discount_amount=0
    ):
        import datetime
        local_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO invoices(
            customer_name,
            total,
            payment_method,
            discount_code,
            discount_amount,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            customer_name,
            total,
            payment_method,
            discount_code,
            discount_amount,
            local_time
        ))

        invoice_id = cursor.lastrowid

        conn.commit()

        conn.close()

        return invoice_id

    @staticmethod
    def add_invoice_detail(
            invoice_id,
            product_name,
            quantity,
            price,
            subtotal
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO invoice_details(
            invoice_id,
            product_name,
            quantity,
            price,
            subtotal
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            invoice_id,
            product_name,
            quantity,
            price,
            subtotal
        ))

        conn.commit()

        conn.close()

    @staticmethod
    def get_invoices():

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM invoices
        ORDER BY id DESC
        """)

        data = cursor.fetchall()

        conn.close()

        return data