from models.return_order import ReturnOrder
from models.product import Product


class ReturnService:

    @staticmethod
    def process_return(invoice_id, product_name, quantity, price, reason, return_type,
                       new_product_name='', price_diff=0.0):
        """
        Xử lý đổi/trả:
        REFUND: Tạo phiếu trả, hoàn kho sản phẩm cũ, hoàn tiền = price * qty
        EXCHANGE: Tạo phiếu đổi, hoàn kho cũ, trừ kho mới, tính chênh lệch
        """
        # Hoàn kho sản phẩm cũ (cả REFUND và EXCHANGE)
        ReturnOrder.restore_stock(product_name, quantity)

        if return_type == 'EXCHANGE' and new_product_name:
            # Trừ kho sản phẩm mới
            ok = ReturnOrder.deduct_stock(new_product_name, quantity)
            if not ok:
                raise ValueError(
                    f"Sản phẩm '{new_product_name}' không đủ tồn kho để đổi!"
                )

        rid = ReturnOrder.create(
            invoice_id=invoice_id,
            product_name=product_name,
            quantity=quantity,
            price=price,
            reason=reason,
            return_type=return_type,
            new_product_name=new_product_name,
            price_diff=price_diff
        )

        # Cập nhật hóa đơn và tính lại tiền nếu là giao dịch Trả hàng (REFUND)
        if return_type in ('REFUND', 'Trả hàng'):
            from database.db_connect import get_connection
            conn = get_connection()
            cursor = conn.cursor()
            try:
                # 1. Tìm và giảm trừ số lượng sản phẩm cũ trong chi tiết hóa đơn
                cursor.execute("""
                    SELECT id, quantity, price FROM invoice_details
                    WHERE invoice_id = ? AND product_name = ?
                """, (invoice_id, product_name))
                detail_row = cursor.fetchone()
                if detail_row:
                    detail_id, orig_qty, orig_price = detail_row
                    new_qty = max(0, orig_qty - quantity)
                    new_subtotal = new_qty * orig_price
                    cursor.execute("""
                        UPDATE invoice_details
                        SET quantity = ?, subtotal = ?
                        WHERE id = ?
                    """, (new_qty, new_subtotal, detail_id))

                # 2. Tính toán lại tổng tiền hóa đơn sau khi giảm trừ sản phẩm trả
                cursor.execute("""
                    SELECT SUM(subtotal) FROM invoice_details
                    WHERE invoice_id = ?
                """, (invoice_id,))
                sum_subtotal = cursor.fetchone()[0] or 0.0

                # Lấy số tiền giảm giá gốc của hóa đơn
                cursor.execute("""
                    SELECT discount_amount FROM invoices
                    WHERE id = ?
                """, (invoice_id,))
                discount_amount = cursor.fetchone()[0] or 0.0

                new_total = max(0.0, sum_subtotal - discount_amount)

                # 3. Xác định trạng thái note mới cho hóa đơn dựa trên số lượng sản phẩm còn lại
                cursor.execute("""
                    SELECT SUM(quantity) FROM invoice_details
                    WHERE invoice_id = ?
                """, (invoice_id,))
                total_qty_remaining = cursor.fetchone()[0] or 0

                if total_qty_remaining == 0:
                    status_note = "Đã hoàn tiền"
                else:
                    status_note = "Hoàn tiền một phần"

                # Cập nhật tổng tiền và trạng thái của hóa đơn
                cursor.execute("""
                    UPDATE invoices
                    SET total = ?, status = ?
                    WHERE id = ?
                """, (new_total, status_note, invoice_id))

                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                conn.close()

        return rid

    @staticmethod
    def get_all_returns():
        return ReturnOrder.get_all()

    @staticmethod
    def search_returns(keyword):
        return ReturnOrder.search(keyword)

    @staticmethod
    def get_invoice_info(invoice_id):
        return ReturnOrder.get_invoice(invoice_id)

    @staticmethod
    def get_invoice_details(invoice_id):
        return ReturnOrder.get_invoice_details(invoice_id)

    @staticmethod
    def get_recent_invoices(limit=50):
        return ReturnOrder.get_recent_invoices(limit)

    @staticmethod
    def search_invoices(keyword, limit=50):
        return ReturnOrder.search_invoices(keyword, limit)

    @staticmethod
    def get_all_products():
        """Lấy danh sách sản phẩm để chọn khi đổi hàng."""
        return Product.get_all()
