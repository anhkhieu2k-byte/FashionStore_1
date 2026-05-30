from database.db_connect import get_connection


class ReturnOrder:

    @staticmethod
    def create(invoice_id, product_name, quantity, price, reason, return_type,
               new_product_name='', price_diff=0.0):
        """
        Tạo phiếu đổi/trả.
        - return_type: 'REFUND' hoặc 'EXCHANGE'
        - refund_amount: số tiền hoàn (= price * qty nếu trả; = 0 hoặc âm nếu đổi)
        - price_diff: chênh lệch giá (new_price - old_price) * qty (âm = hoàn lại, dương = thu thêm)
        """
        import datetime
        local_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        refund_amount = price * quantity if return_type == 'REFUND' else 0.0
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO return_orders(
                invoice_id, product_name, quantity, price,
                refund_amount, new_product_name, price_diff, reason, return_type,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            invoice_id,
            product_name,
            quantity,
            price,
            refund_amount,
            new_product_name,
            price_diff,
            reason,
            return_type,
            local_time
        ))
        rid = cursor.lastrowid
        conn.commit()
        conn.close()
        return rid

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                ro.id, ro.invoice_id, ro.product_name, ro.quantity, ro.price,
                ro.new_product_name, ro.price_diff, ro.refund_amount,
                ro.reason, ro.return_type, ro.created_at,
                inv.customer_name, cust.phone
            FROM return_orders ro
            LEFT JOIN invoices inv ON ro.invoice_id = inv.id
            LEFT JOIN customers cust ON inv.customer_name = cust.full_name
            ORDER BY ro.id DESC
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def search(keyword):
        conn = get_connection()
        cursor = conn.cursor()
        kw = f"%{keyword}%"
        cursor.execute("""
            SELECT 
                ro.id, ro.invoice_id, ro.product_name, ro.quantity, ro.price,
                ro.new_product_name, ro.price_diff, ro.refund_amount,
                ro.reason, ro.return_type, ro.created_at,
                inv.customer_name, cust.phone
            FROM return_orders ro
            LEFT JOIN invoices inv ON ro.invoice_id = inv.id
            LEFT JOIN customers cust ON inv.customer_name = cust.full_name
            WHERE ro.product_name LIKE ?
               OR ro.new_product_name LIKE ?
               OR ro.reason LIKE ?
               OR CAST(ro.invoice_id AS TEXT) LIKE ?
               OR inv.customer_name LIKE ?
               OR cust.phone LIKE ?
            ORDER BY ro.id DESC
        """, (kw, kw, kw, kw, kw, kw))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_invoice_details(invoice_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, product_name, quantity, price, subtotal
            FROM invoice_details
            WHERE invoice_id = ?
        """, (invoice_id,))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_invoice(invoice_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, customer_name, total, payment_method, created_at
            FROM invoices WHERE id = ?
        """, (invoice_id,))
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def get_recent_invoices(limit=50):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, customer_name, total, created_at
            FROM invoices ORDER BY id DESC LIMIT ?
        """, (limit,))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def search_invoices(keyword, limit=50):
        conn = get_connection()
        cursor = conn.cursor()
        kw = f"%{keyword}%"
        cursor.execute("""
            SELECT i.id, i.customer_name, i.total, i.created_at
            FROM invoices i
            LEFT JOIN customers c ON i.customer_name = c.full_name
            WHERE CAST(i.id AS TEXT) LIKE ?
               OR i.customer_name LIKE ?
               OR c.phone LIKE ?
            GROUP BY i.id
            ORDER BY i.id DESC
            LIMIT ?
        """, (kw, kw, kw, limit))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def restore_stock(product_name, quantity):
        """Hoàn tồn kho sản phẩm cũ (khi trả / đổi)."""
        base_name = product_name
        if " (" in product_name:
            base_name = product_name.split(" (")[0].strip()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE products SET stock = stock + ?
            WHERE name = ?
        """, (quantity, base_name))
        conn.commit()
        conn.close()

    @staticmethod
    def deduct_stock(product_name, quantity):
        """Trừ tồn kho sản phẩm mới (khi đổi hàng)."""
        base_name = product_name
        if " (" in product_name:
            base_name = product_name.split(" (")[0].strip()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE products SET stock = stock - ?
            WHERE name = ? AND stock >= ?
        """, (quantity, base_name, quantity))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0
