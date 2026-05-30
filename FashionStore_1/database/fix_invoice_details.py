import sqlite3
import os
import random

def fix_invoice_details():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fashion_store.db')
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get available products to use as dummy data
    cursor.execute("SELECT name, price FROM products")
    products = cursor.fetchall()
    if not products:
        products = [("Sản phẩm mặc định", 100000)]

    # Get all invoices
    cursor.execute("SELECT id, total FROM invoices")
    invoices = cursor.fetchall()

    for inv_id, total in invoices:
        # Check if invoice already has details
        cursor.execute("SELECT COUNT(*) FROM invoice_details WHERE invoice_id = ?", (inv_id,))
        count = cursor.fetchone()[0]
        
        if count == 0:
            print(f"Fixing invoice HD{inv_id:03d} with total {total:,.0f} ₫")
            
            # Simple logic to add 1 or 2 products that match the total
            # We'll just add one main product and one "Phụ kiện" to match the remaining balance
            p_name, p_price = random.choice(products)
            
            if total > p_price:
                # Add the main product
                qty = 1
                subtotal = p_price
                cursor.execute(
                    "INSERT INTO invoice_details(invoice_id, product_name, quantity, price, subtotal) VALUES(?,?,?,?,?)",
                    (inv_id, p_name, qty, p_price, subtotal)
                )
                
                # Add "Phụ kiện" for the rest
                rest = total - p_price
                if rest > 0:
                    cursor.execute(
                        "INSERT INTO invoice_details(invoice_id, product_name, quantity, price, subtotal) VALUES(?,?,?,?,?)",
                        (inv_id, "Phụ kiện đi kèm", 1, rest, rest)
                    )
            else:
                # Just add one entry with the full total
                cursor.execute(
                    "INSERT INTO invoice_details(invoice_id, product_name, quantity, price, subtotal) VALUES(?,?,?,?,?)",
                    (inv_id, p_name, 1, total, total)
                )

    conn.commit()
    conn.close()
    print("✅ All invoices have been updated with product details!")

if __name__ == "__main__":
    fix_invoice_details()
