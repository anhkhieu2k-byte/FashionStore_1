from database.db_connect import get_connection


class Inventory:

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT i.id, i.product_name, i.quantity, i.min_quantity, i.supplier_name, i.import_price, p.size, p.color
        FROM inventory i
        LEFT JOIN products p ON i.product_name = p.name
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def create(
            product_name,
            quantity,
            min_quantity,
            supplier_name,
            import_price
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO inventory(
            product_name,
            quantity,
            min_quantity,
            supplier_name,
            import_price
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            product_name,
            quantity,
            min_quantity,
            supplier_name,
            import_price
        ))

        conn.commit()

        conn.close()

    @staticmethod
    def update(
            inventory_id,
            product_name,
            quantity,
            min_quantity,
            supplier_name,
            import_price
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        UPDATE inventory
        SET
            product_name = ?,
            quantity = ?,
            min_quantity = ?,
            supplier_name = ?,
            import_price = ?
        WHERE id = ?
        """, (
            product_name,
            quantity,
            min_quantity,
            supplier_name,
            import_price,
            inventory_id
        ))

        conn.commit()

        conn.close()

    @staticmethod
    def delete(inventory_id):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM inventory
        WHERE id = ?
        """, (inventory_id,))

        conn.commit()

        conn.close()

    @staticmethod
    def search(keyword):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT i.id, i.product_name, i.quantity, i.min_quantity, i.supplier_name, i.import_price, p.size, p.color
        FROM inventory i
        LEFT JOIN products p ON i.product_name = p.name
        WHERE i.product_name LIKE ?
        """, (f"%{keyword}%",))
        data = cursor.fetchall()
        conn.close()
        return data