from database.db_connect import get_connection


def init_database():

    conn = get_connection()
    cursor = conn.cursor()

    # ACCOUNTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password BLOB,
            role TEXT
        )
    """)

    # PRODUCTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            size TEXT,
            color TEXT,
            price REAL,
            stock INTEGER,
            description TEXT,
            import_price REAL DEFAULT 0,
            supplier_name TEXT DEFAULT ''
        )
    """)

    # Migration for products table
    try:
        cursor.execute("SELECT import_price FROM products LIMIT 1")
    except Exception:
        cursor.execute("ALTER TABLE products ADD COLUMN import_price REAL DEFAULT 0")
        conn.commit()

    try:
        cursor.execute("SELECT supplier_name FROM products LIMIT 1")
    except Exception:
        cursor.execute("ALTER TABLE products ADD COLUMN supplier_name TEXT DEFAULT ''")
        conn.commit()

    # CUSTOMERS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            phone TEXT,
            email TEXT,
            points INTEGER DEFAULT 0,
            member_rank TEXT DEFAULT 'Dong'
        )
    """)

    # INVOICES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            total REAL,
            payment_method TEXT,
            discount_code TEXT DEFAULT '',
            discount_amount REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT (datetime('now', 'localtime'))
        )
    """)

    # INVOICE DETAILS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoice_details(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER,
            product_name TEXT,
            quantity INTEGER,
            price REAL,
            subtotal REAL
        )
    """)

    # SUPPLIERS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            address TEXT
        )
    """)

    # INVENTORY
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            quantity INTEGER,
            min_quantity INTEGER,
            supplier_name TEXT,
            import_price REAL
        )
    """)

    # STAFF
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS staff(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            birth_date TEXT,
            phone TEXT,
            address TEXT,
            role TEXT,
            shift TEXT,
            salary REAL,
            attendance_days INTEGER DEFAULT 0,
            check_in_time TEXT,
            total_hours REAL DEFAULT 0
        )
    """)

    # PROMOTIONS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS promotions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT,
            discount_percent REAL,
            min_order_value REAL,
            start_date TEXT,
            end_date TEXT,
            quantity INTEGER DEFAULT 999,
            used_count INTEGER DEFAULT 0
        )
    """)

    # RETURN ORDERS — thêm new_product_name & price_diff cho đổi hàng
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS return_orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER,
            product_name TEXT,
            quantity INTEGER,
            price REAL,
            refund_amount REAL,
            new_product_name TEXT DEFAULT '',
            price_diff REAL DEFAULT 0,
            reason TEXT,
            return_type TEXT,
            created_at TIMESTAMP DEFAULT (datetime('now', 'localtime'))
        )
    """)

    # Migration: thêm cột mới vào bảng cũ nếu chưa có
    try:
        cursor.execute("ALTER TABLE return_orders ADD COLUMN new_product_name TEXT DEFAULT ''")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE return_orders ADD COLUMN price_diff REAL DEFAULT 0")
    except Exception:
        pass

    # Migration for invoices table: thêm discount_code & discount_amount
    try:
        cursor.execute("ALTER TABLE invoices ADD COLUMN discount_code TEXT DEFAULT ''")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE invoices ADD COLUMN discount_amount REAL DEFAULT 0")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE invoices ADD COLUMN status TEXT DEFAULT 'Đã thanh toán'")
    except Exception:
        pass

    # Migration for promotions: thêm quantity & used_count
    try:
        cursor.execute("ALTER TABLE promotions ADD COLUMN quantity INTEGER DEFAULT 999")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE promotions ADD COLUMN used_count INTEGER DEFAULT 0")
    except Exception:
        pass

    # Bảng lịch sử chấm công
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_id INTEGER,
            staff_name TEXT,
            check_in TEXT,
            check_out TEXT,
            hours REAL,
            earned REAL,
            FOREIGN KEY (staff_id) REFERENCES staff (id)
        )
    """)

    # Auto-fill missing import prices (set to 60% of sale price)
    cursor.execute("UPDATE products SET import_price = price * 0.6 WHERE import_price IS NULL OR import_price = 0")

    conn.commit()
    conn.close()
    print("Database initialized!")
