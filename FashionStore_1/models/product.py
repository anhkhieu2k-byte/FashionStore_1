from database.db_connect import get_connection

class Product:
    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_by_id(product_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def create(name, category, size, color, price, stock, description, import_price=0, supplier_name=""):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO products(name, category, size, color, price, stock, description, import_price, supplier_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, category, size, color, price, stock, description, import_price, supplier_name))
        conn.commit()
        conn.close()

    @staticmethod
    def update(product_id, name, category, size, color, price, stock, description, import_price=0, supplier_name=""):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE products
        SET name = ?, category = ?, size = ?, color = ?, price = ?, stock = ?, description = ?, import_price = ?, supplier_name = ?
        WHERE id = ?
        """, (name, category, size, color, price, stock, description, import_price, supplier_name, product_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(product_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def search(keyword):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE name LIKE ?", (f"%{keyword}%",))
        data = cursor.fetchall()
        conn.close()
        return data