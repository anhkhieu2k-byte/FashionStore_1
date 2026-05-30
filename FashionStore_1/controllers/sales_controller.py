from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from modules.sales.sale_service import SalesService
from modules.products.product_service import ProductService
from modules.customers.customer_service import CustomerService
from modules.promotions.promotion_service import PromotionService
from ui.dialogs.customer_dialog import CustomerDialog
from config import *
from utils.message_utils import show_info, show_warning, show_error, show_success


class SalesController:

    def __init__(self, ui, on_success=None):
        self.ui = ui
        self.on_success = on_success
        self.cart_items = []
        self.total = 0
        self._discount_amount = 0
        self._all_customers = []

        # Load dữ liệu ban đầu
        self.load_products()
        self.load_customers()
        self.load_promotions()

        # Kết nối sự kiện
        self.ui.btn_add_cart.clicked.connect(self.add_to_cart)
        self.ui.btn_checkout.clicked.connect(self.checkout)
        self.ui.btn_clear_cart.clicked.connect(self.clear_cart)
        self.ui.txt_prod_search.textChanged.connect(self.filter_products)
        self.ui.product_list.cellClicked.connect(self.on_product_select)

        # Kết nối tìm kiếm khách hàng inline
        if hasattr(self.ui, 'txt_cust_search'):
            self.ui.txt_cust_search.textChanged.connect(self.filter_customers)

        # Kết nối mã giảm giá
        if hasattr(self.ui, 'btn_apply_disc'):
            self.ui.btn_apply_disc.clicked.connect(self.apply_discount)
        if hasattr(self.ui, 'cb_discount'):
            self.ui.cb_discount.currentTextChanged.connect(self.apply_discount)
            
        # Nút thêm khách hàng
        if hasattr(self.ui, 'btn_add_customer'):
            self.ui.btn_add_customer.clicked.connect(self.show_add_customer_dialog)

    # ─────────────────────────────────────────────────
    # CẬP NHẬT TỔNG TIỀN & MÃ GIẢM GIÁ
    # ─────────────────────────────────────────────────
    def _update_total_display(self):
        final_total = max(0, self.total - self._discount_amount)
        self.ui.lbl_total.setText(f"{final_total:,.0f} VNĐ")
        if hasattr(self.ui, 'lbl_disc_info'):
            if self._discount_amount > 0:
                self.ui.lbl_disc_info.setText(f"Đã giảm: -{self._discount_amount:,.0f} ₫")
            else:
                self.ui.lbl_disc_info.setText("")

    def apply_discount(self):
        code = self.ui.cb_discount.currentData()
        if not code:
            self._discount_amount = 0
            self._update_total_display()
            return

        # 1. Kiểm tra mã trong database
        promo = PromotionService.get_by_code(code)
        
        if promo:
            # promo = (id, code, discount_percent, min_order_value, start_date, end_date, quantity, used_count)
            discount_percent = promo[2]
            min_val = promo[3] or 0
            limit_qty = promo[6] or 999
            used_qty = promo[7] or 0
            
            # Kiểm tra thời hạn áp dụng thực tế
            from datetime import date
            try:
                today = date.today()
                
                def parse_dt(d_str):
                    if not d_str: return None
                    d_str = str(d_str).strip().replace('/', '-')
                    from datetime import datetime
                    for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
                        try: return datetime.strptime(d_str, fmt).date()
                        except ValueError: continue
                    return None

                start_dt = parse_dt(promo[4])
                end_dt = parse_dt(promo[5])
                
                if start_dt and today < start_dt:
                    show_warning(self.ui, "Chưa áp dụng", f"Mã giảm giá '{code}' chưa đến thời gian bắt đầu sử dụng!")
                    self._discount_amount = 0
                    self.ui.cb_discount.setCurrentIndex(0)
                    self._update_total_display()
                    return
                
                if end_dt and today > end_dt:
                    show_warning(self.ui, "Đã hết hạn", f"Mã giảm giá '{code}' đã hết hạn sử dụng!")
                    self._discount_amount = 0
                    self.ui.cb_discount.setCurrentIndex(0)
                    self._update_total_display()
                    return
            except Exception as e:
                print("Lỗi kiểm tra hạn sử dụng:", e)

            # Kiểm tra giới hạn số lượng mã
            if used_qty >= limit_qty:
                show_warning(self.ui, "Hết lượt", f"Mã giảm giá '{code}' đã hết số lượt sử dụng!")
                self._discount_amount = 0
                self._update_total_display()
                return

            # Kiểm tra xem khách này đã dùng mã này chưa
            cust_name = self.ui.cb_customer.currentData()
            if cust_name and cust_name != "Khách lẻ":
                usage_count = PromotionService.check_customer_usage(cust_name, code)
                if usage_count >= 1:
                    show_warning(self.ui, "Đã sử dụng", f"Khách hàng {cust_name} đã sử dụng mã này trước đó!")
                    self._discount_amount = 0
                    self._update_total_display()
                    return

            if self.total < min_val:
                msg = QMessageBox(self.ui)
                msg.setWindowTitle("Không đủ điều kiện")
                msg.setText(f"Mã này yêu cầu đơn hàng tối thiểu {min_val:,.0f} ₫")
                msg.setIcon(QMessageBox.Warning)
                ok_btn = msg.addButton("Đã hiểu", QMessageBox.AcceptRole)
                ok_btn.setCursor(Qt.PointingHandCursor)
                
                # Style cho hộp thoại và nút
                msg.setStyleSheet("QMessageBox { background-color: white; } QLabel { color: #1e293b; font-size: 14px; }")
                ok_btn.setStyleSheet(f"QPushButton {{ background-color: {PRIMARY}; color: white; border-radius: 6px; padding: 6px 20px; font-weight: bold; min-width: 80px; }} QPushButton:hover {{ background-color: {PRIMARY_DARK}; }}")
                
                msg.exec_()
                
                self._discount_amount = 0
                self._update_total_display()
                return

            # Tính toán giảm giá (giả định discount_percent là % nếu < 100, ngược lại là số tiền mặt)
            if discount_percent < 1: # ví dụ 0.1 cho 10%
                self._discount_amount = self.total * discount_percent
            elif discount_percent <= 100: # ví dụ 10 cho 10%
                self._discount_amount = self.total * (discount_percent / 100)
            else: # Nếu > 100 thì coi là số tiền mặt
                self._discount_amount = discount_percent
                
            msg = QMessageBox(self.ui)
            msg.setWindowTitle("Thành công")
            msg.setText(f"Áp dụng mã ưu đãi '{code}' thành công!")
            msg.setIcon(QMessageBox.Information)
            
            ok_btn = msg.addButton("Tuyệt vời", QMessageBox.AcceptRole)
            from config import SUCCESS
            ok_btn.setStyleSheet(f"QPushButton {{ background-color: {SUCCESS}; color: white; border-radius: 8px; padding: 8px 25px; font-weight: 800; min-width: 100px; }} QPushButton:hover {{ background-color: #059669; }}")
            msg.setStyleSheet("QMessageBox { background-color: white; } QLabel { color: #1e293b; font-size: 14px; }")
            msg.exec_()
        
        else:
            msg = QMessageBox(self.ui)
            msg.setWindowTitle("Mã không hợp lệ")
            msg.setText("Mã giảm giá không chính xác hoặc đã hết hạn!")
            msg.setIcon(QMessageBox.Critical)
            ok_btn = msg.addButton("Đóng", QMessageBox.AcceptRole)
            ok_btn.setStyleSheet("QPushButton { background-color: #ef4444; color: white; border-radius: 6px; padding: 6px 20px; font-weight: bold; }")
            msg.exec_()
            
            self._discount_amount = 0
            self.ui.cb_discount.setCurrentIndex(0)

        self._update_total_display()

    # ─────────────────────────────────────────────────
    # LOAD sản phẩm vào bảng chọn
    # ─────────────────────────────────────────────────
    def load_products(self, keyword=""):
        if keyword:
            data = ProductService.search_product(keyword)
        else:
            data = ProductService.get_products()

        self.ui.product_list.setRowCount(0)
        for row_idx, product in enumerate(data):
            self.ui.product_list.insertRow(row_idx)
            # id, name, category, size, color, price
            for col_idx, val in enumerate(product[:6]):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter if col_idx in [0, 2, 3, 4] else Qt.AlignLeft)
                self.ui.product_list.setItem(row_idx, col_idx, item)

    def filter_products(self, keyword):
        self.load_products(keyword)

    def on_product_select(self, row, col):
        size_str = self.ui.product_list.item(row, 3).text()
        sizes = [s.strip() for s in size_str.split(",") if s.strip()]
        self.ui.cb_size.clear()
        if sizes:
            self.ui.cb_size.addItems(sizes)
        else:
            self.ui.cb_size.addItem("Freesize")

        color_str = self.ui.product_list.item(row, 4).text()
        colors = [c.strip() for c in color_str.split(",") if c.strip()]
        self.ui.cb_color.clear()
        if colors:
            self.ui.cb_color.addItems(colors)
        else:
            self.ui.cb_color.addItem("N/A")

    # ─────────────────────────────────────────────────
    # LOAD & TÌM KIẾM mã giảm giá
    # ─────────────────────────────────────────────────
    def load_promotions(self):
        if not hasattr(self.ui, 'cb_discount'):
            return
            
        self.ui.cb_discount.clear()
        self.ui.cb_discount.addItem("— Chọn mã giảm giá —", None)
        
        # Load từ DB
        promos = PromotionService.get_promotions()
        
        from datetime import date
        today = date.today()
        
        def parse_dt(d_str):
            if not d_str: return None
            d_str = str(d_str).strip().replace('/', '-')
            from datetime import datetime
            for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
                try: return datetime.strptime(d_str, fmt).date()
                except ValueError: continue
            return None

        for p in promos:
            # p = (id, code, discount_percent, min_order_value, start_date, end_date, quantity, used_count)
            display_days = ""
            try:
                start_dt = parse_dt(p[4])
                end_dt = parse_dt(p[5])
                
                if start_dt and today < start_dt:
                    days_until = (start_dt - today).days
                    display_days = f" - Chưa bắt đầu (Còn {days_until} ngày)"
                elif end_dt:
                    if today <= end_dt:
                        delta = (end_dt - today).days
                        if delta > 0:
                            display_days = f" - Còn {delta} ngày"
                        elif delta == 0:
                            display_days = " - Hết hạn hôm nay"
                    else:
                        delta = (today - end_dt).days
                        display_days = f" - Hết hạn ({delta} ngày trước)"
                else:
                    display_days = " - Vô thời hạn"
            except Exception:
                pass
                
            display = f"{p[1]} (Giảm {p[2]:.0f}{'%' if p[2] <= 100 else '₫'}{display_days})"
            self.ui.cb_discount.addItem(display, p[1])

    # ─────────────────────────────────────────────────
    # LOAD & TÌM KIẾM khách hàng
    # ─────────────────────────────────────────────────
    def load_customers(self):
        self._all_customers = CustomerService.get_customers()
        self.filter_customers("")

    def filter_customers(self, keyword):
        kw = keyword.strip().lower()
        self.ui.cb_customer.clear()
        self.ui.cb_customer.addItem("— Khách lẻ (không chọn) —", None)
        for c in self._all_customers:
            # c = (id, full_name, phone, email, points, member_rank)
            name_str = str(c[1] or "").lower()
            phone_str = str(c[2] or "").lower()
            if kw in name_str or kw in phone_str:
                display = f"{c[1]}  ({c[2]})"
                self.ui.cb_customer.addItem(display, c[1])

    def show_add_customer_dialog(self):
        dialog = CustomerDialog(self.ui)
        if dialog.exec_():
            data = dialog.get_data()
            if not data['name']:
                show_warning(self.ui, "Lỗi", "Vui lòng nhập tên khách hàng!")
                return
            
            try:
                CustomerService.add_customer(
                    data['name'], data['phone'], data['email'], 
                    data['points'], data['rank']
                )
                show_success(self.ui, "Thành công", "Đã thêm khách hàng mới!")
                self.load_customers()
                
                # Cố gắng chọn khách hàng vừa thêm
                idx = self.ui.cb_customer.findData(data['name'])
                if idx >= 0:
                    self.ui.cb_customer.setCurrentIndex(idx)
                    
            except Exception as e:
                show_error(self.ui, "Lỗi", f"Lỗi khi thêm: {str(e)}")

    # ─────────────────────────────────────────────────
    # THÊM VÀO GIỎ
    # ─────────────────────────────────────────────────
    def add_to_cart(self):
        row = self.ui.product_list.currentRow()
        if row < 0:
            show_warning(self.ui, "Chú ý", "Vui lòng chọn một sản phẩm từ danh sách!")
            return

        prod_id_text = self.ui.product_list.item(row, 0).text()
        try:
            prod_id = int(prod_id_text)
        except ValueError:
            show_warning(self.ui, "Lỗi", "Mã sản phẩm không hợp lệ!")
            return

        product = ProductService.get_by_id(prod_id)
        if not product:
            show_error(self.ui, "Lỗi", "Không tìm thấy sản phẩm trong hệ thống!")
            return

        db_stock = int(product[6] or 0)
        current_cart_qty = sum(item["quantity"] for item in self.cart_items if item.get("product_id") == prod_id)
        quantity = self.ui.spin_qty.value()

        if current_cart_qty + quantity > db_stock:
            show_warning(
                self.ui,
                "Hết hàng/Thiếu hàng",
                f"Không thể thêm sản phẩm vào giỏ hàng!<br>"
                f"Tồn kho hiện tại: <b>{db_stock}</b><br>"
                f"Đã có trong giỏ: <b>{current_cart_qty}</b><br>"
                f"Số lượng yêu cầu thêm: <b>{quantity}</b>"
            )
            return

        base_name = self.ui.product_list.item(row, 1).text()
        selected_size = self.ui.cb_size.currentText()
        selected_color = self.ui.cb_color.currentText()
        
        parts = []
        if selected_size:
            parts.append(selected_size)
        if selected_color and selected_color != "N/A":
            parts.append(selected_color)
            
        if parts:
            product_name = f"{base_name} ({', '.join(parts)})"
        else:
            product_name = base_name
        price_text = self.ui.product_list.item(row, 5).text()

        try:
            price = float(price_text)
        except ValueError:
            show_warning(self.ui, "Lỗi", "Giá sản phẩm không hợp lệ!")
            return

        subtotal = quantity * price
        self.total += subtotal

        item_data = {
            "product_id": prod_id,
            "product_name": product_name,
            "quantity": quantity,
            "price": price,
            "subtotal": subtotal
        }
        self.cart_items.append(item_data)

        # Thêm vào bảng giỏ hàng
        r = self.ui.cart_table.rowCount()
        self.ui.cart_table.insertRow(r)

        def tbl_item(text, align=Qt.AlignCenter):
            it = QTableWidgetItem(str(text))
            it.setTextAlignment(align)
            return it

        self.ui.cart_table.setItem(r, 0, tbl_item(product_name, Qt.AlignLeft | Qt.AlignVCenter))
        self.ui.cart_table.setItem(r, 1, tbl_item(quantity))
        self.ui.cart_table.setItem(r, 2, tbl_item(f"{price:,.0f}đ"))
        self.ui.cart_table.setItem(r, 3, tbl_item(f"{subtotal:,.0f}đ"))

        btn_del = QPushButton("✕")
        btn_del.setFixedSize(32, 28)
        btn_del.setCursor(Qt.PointingHandCursor)
        btn_del.setStyleSheet("""
            QPushButton { background:#fee2e2; color:#ef4444; border:none; border-radius:6px;
                          font-size:13px; font-weight:bold; }
            QPushButton:hover { background:#fecaca; }
        """)
        btn_del.clicked.connect(lambda _, row_idx=r: self.remove_item(row_idx))
        self.ui.cart_table.setCellWidget(r, 4, btn_del)

        # Tính lại chiết khấu nếu có theo %
        if self.ui.cb_discount.currentIndex() > 0:
            self.apply_discount() # tự gọi lại hàm áp mã để cập nhật theo total mới
        else:
            self._update_total_display()

        self.ui.spin_qty.setValue(1)

    # ─────────────────────────────────────────────────
    # XÓA 1 SẢN PHẨM KHỎI GIỎ
    # ─────────────────────────────────────────────────
    def remove_item(self, row):
        if row >= len(self.cart_items):
            return
        subtotal = self.cart_items[row]["subtotal"]
        self.total -= subtotal
        self.cart_items.pop(row)
        self.ui.cart_table.removeRow(row)
        
        # Cập nhật lại các row index liên kết cho các nút xóa phía sau
        for r_idx in range(self.ui.cart_table.rowCount()):
            btn = self.ui.cart_table.cellWidget(r_idx, 4)
            if btn:
                btn.disconnect()
                btn.clicked.connect(lambda _, idx=r_idx: self.remove_item(idx))

        if self.ui.cb_discount.currentIndex() > 0:
            self.apply_discount()
        else:
            self._update_total_display()

    # ─────────────────────────────────────────────────
    # XÓA TOÀN BỘ GIỎ
    # ─────────────────────────────────────────────────
    def clear_cart(self):
        self.cart_items.clear()
        self.total = 0
        self._discount_amount = 0
        self.ui.cart_table.setRowCount(0)
        if hasattr(self.ui, 'cb_discount'):
            self.ui.cb_discount.setCurrentIndex(0)
        self._update_total_display()

    # ─────────────────────────────────────────────────
    # THANH TOÁN
    # ─────────────────────────────────────────────────
    def checkout(self):
        if not self.cart_items:
            show_warning(self.ui, "Chú ý", "Giỏ hàng đang trống!")
            return

        # Kiểm tra tồn kho trước khi thanh toán
        for item in self.cart_items:
            prod_id = item.get("product_id")
            if prod_id:
                product = ProductService.get_by_id(prod_id)
                if not product:
                    show_error(self.ui, "Lỗi", f"Không tìm thấy sản phẩm '{item['product_name']}' trong hệ thống!")
                    return
                db_stock = int(product[6] or 0)
                total_qty_in_cart = sum(i["quantity"] for i in self.cart_items if i.get("product_id") == prod_id)
                if total_qty_in_cart > db_stock:
                    show_warning(
                        self.ui,
                        "Hết hàng/Thiếu hàng",
                        f"Không thể thanh toán do sản phẩm <b>{item['product_name']}</b> không đủ tồn kho!<br>"
                        f"Tồn kho hiện tại: <b>{db_stock}</b><br>"
                        f"Tổng số lượng trong giỏ: <b>{total_qty_in_cart}</b>"
                    )
                    return

        customer_name = self.ui.cb_customer.currentData()
        if customer_name is None:
            customer_name = "Khách lẻ"

        payment_method = self.ui.cb_payment.currentText()
        final_total = max(0, self.total - self._discount_amount)
        
        # Lấy mã giảm giá đã sử dụng (nếu có)
        discount_code = self.ui.cb_discount.currentData() if self.ui.cb_discount.currentIndex() > 0 else ""

        SalesService.create_sale(
            customer_name,
            final_total,
            payment_method,
            self.cart_items,
            discount_code=discount_code,
            discount_amount=self._discount_amount
        )

        disc_str = f"\nChiết khấu: -{self._discount_amount:,.0f} ₫" if self._discount_amount > 0 else ""
        
        show_success(
            self.ui, 
            "Thành công", 
            f"Thanh toán thành công!<br>"
            f"Khách hàng: <b>{customer_name}</b><br>"
            f"Tổng tiền giỏ: {self.total:,.0f} ₫{disc_str}<br>"
            f"--------------------------<br>"
            f"<font color='#10b981' size='4'>CẦN THANH TOÁN: {final_total:,.0f} VNĐ</font>"
        )

        self.clear_cart()
        if self.on_success:
            self.on_success()
