"""
ReturnController — Xử lý nghiệp vụ Đổi/Trả hàng hóa toàn diện
Hỗ trợ linh hoạt cho phép đặc cách các hóa đơn cũ để thuận tiện demo/thử nghiệm.
"""
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from modules.returns.return_service import ReturnService
from config import PRIMARY, DANGER, SUCCESS, INFO, TEXT_MID, WARNING
from utils.message_utils import show_info, show_warning, show_error, show_success, show_confirm


# Giới hạn chuẩn là 3 ngày theo quy định
RETURN_DAYS_LIMIT = 3


class ReturnController:

    def __init__(self, ui, on_success=None):
        self.ui = ui
        self.on_success = on_success
        self._selected_product = None   # {"name":, "price":, "max_qty":}
        self._selected_invoice_id = None
        self._invoice_date = None       # datetime object
        self._all_products = []         # danh sách SP để đổi
        self._current_filter_type = None

        # ── Kết nối sự kiện ──────────────────────────────────
        # Nút tạo phiếu đổi trả
        if hasattr(self.ui, 'btn_create_return'):
            self.ui.btn_create_return.clicked.connect(self.show_create_return_form)

        # Bước 1
        self.ui.btn_lookup.clicked.connect(self.lookup_invoice)
        if hasattr(self.ui, 'cb_invoice_id') and self.ui.cb_invoice_id.lineEdit():
            self.ui.cb_invoice_id.lineEdit().returnPressed.connect(self.lookup_invoice)
        if hasattr(self.ui, 'txt_search_inv'):
            self.ui.txt_search_inv.textChanged.connect(self.on_search_invoice)
        self.ui.tbl_invoice_items.itemSelectionChanged.connect(self.on_item_selected)
        self.ui.btn_next.clicked.connect(self.go_to_step2)

        # Bước 2
        self.ui.btn_back.clicked.connect(self.go_to_step1)
        self.ui.cb_return_type.currentIndexChanged.connect(self.on_type_changed)
        self.ui.spn_qty.valueChanged.connect(self.update_refund_amount)
        self.ui.cb_new_product.currentIndexChanged.connect(self.on_new_product_changed)
        self.ui.btn_confirm.clicked.connect(self.confirm_return)
        self.ui.btn_clear.clicked.connect(self.clear_form)

        # Lịch sử & Bộ lọc
        self.ui.txt_search.textChanged.connect(self.search_history)
        
        if hasattr(self.ui, 'btn_filter_all'):
            self.ui.btn_filter_all.clicked.connect(lambda: self.filter_by_type(None))
        if hasattr(self.ui, 'btn_filter_exc'):
            self.ui.btn_filter_exc.clicked.connect(lambda: self.filter_by_type("EXCHANGE"))
        if hasattr(self.ui, 'btn_filter_ret'):
            self.ui.btn_filter_ret.clicked.connect(lambda: self.filter_by_type("REFUND"))

        self.ui.tbl_history.cellDoubleClicked.connect(self.show_return_detail)
        self.load_history()

    # ═══════════════════════════════════════════════════════════
    # BƯỚC 1
    # ═══════════════════════════════════════════════════════════

    def show_create_return_form(self):
        # Load danh sách hóa đơn 3 ngày gần đây vào cb_invoice_id
        if hasattr(self.ui, 'cb_invoice_id'):
            self.ui.cb_invoice_id.clear()
            self.ui.cb_invoice_id.addItem("— Chọn mã hóa đơn —")
            invoices = ReturnService.get_recent_invoices(100)
            for inv in invoices:
                # inv: id, customer_name, total, created_at
                created_str = str(inv[3])[:16] if inv[3] else "—"
                display = f"HD{inv[0]:03d} - {inv[1]} ({inv[2]:,.0f}₫) - {created_str}"
                self.ui.cb_invoice_id.addItem(display, inv[0])
                
        if hasattr(self.ui, 'return_dialog'):
            self.ui.return_dialog.exec_()

    def on_search_invoice(self, text):
        keyword = text.strip()
        if not hasattr(self.ui, 'cb_invoice_id'): return
        
        self.ui.cb_invoice_id.clear()
        self.ui.cb_invoice_id.addItem("— Chọn mã hóa đơn —")
        
        if keyword:
            invoices = ReturnService.search_invoices(keyword, 100)
        else:
            invoices = ReturnService.get_recent_invoices(100)
            
        for inv in invoices:
            created_str = str(inv[3])[:16] if inv[3] else "—"
            display = f"HD{inv[0]:03d} - {inv[1]} ({inv[2]:,.0f}₫) - {created_str}"
            self.ui.cb_invoice_id.addItem(display, inv[0])

    def go_to_step1(self):
        self.ui._step_stack.setCurrentIndex(0)
        if hasattr(self.ui, 'set_step'):
            self.ui.set_step(1)
        if hasattr(self.ui, 'lbl_step_info'):
            self.ui.lbl_step_info.setText("Bước 1/2: Tra cứu HĐ và Chọn SP")

    def go_to_step2(self):
        if self._selected_product is None:
            show_warning(
                self.ui, "Chưa chọn sản phẩm",
                "Vui lòng click chọn một sản phẩm từ danh sách mặt hàng của hoá đơn trước!"
            )
            return
        self._load_products_for_exchange()
        self._update_selected_info()
        self.update_refund_amount()
        self.ui._step_stack.setCurrentIndex(1)
        if hasattr(self.ui, 'set_step'):
            self.ui.set_step(2)
        if hasattr(self.ui, 'lbl_step_info'):
            self.ui.lbl_step_info.setText("Bước 2/2: Chọn Hình thức & Xác nhận")

    # ─────────────────────────────────────────────────
    # TRA CỨU HOÁ ĐƠN
    # ─────────────────────────────────────────────────
    def lookup_invoice(self):
        if hasattr(self.ui, 'cb_invoice_id'):
            # Thử lấy data từ item hiện tại
            inv_id_data = self.ui.cb_invoice_id.currentData()
            if inv_id_data is not None:
                raw = str(inv_id_data)
            else:
                # Nếu người dùng gõ text vào combobox
                raw = self.ui.cb_invoice_id.currentText().strip()
                # Xóa phần sau dấu gạch ngang nếu chọn mà data là None (do lỗi nào đó)
                if "-" in raw and raw.startswith("HD"):
                    raw = raw.split("-")[0].strip()
        else:
            raw = ""
            
        if not raw or raw == "— Chọn mã hóa đơn —":
            self._set_inv_info("⚠  Vui lòng nhập hoặc chọn mã hoá đơn cần tra cứu.", WARNING)
            return

        # Gọt bỏ tiền tố HD tự động
        clean_raw = raw.upper().replace("HD", "").strip()

        try:
            inv_id = int(clean_raw)
        except ValueError:
            self._set_inv_info("⚠  Mã hoá đơn phải là số nguyên (VD: 1, 2...).", WARNING)
            return

        try:
            invoice = ReturnService.get_invoice_info(inv_id)
        except Exception as e:
            show_error(self.ui, "Lỗi truy vấn", f"Lỗi DB khi tra cứu hóa đơn:\n{e}")
            return
        if not invoice:
            self._set_inv_info(f"✗  Không tìm thấy hoá đơn #{inv_id} trong hệ thống.", DANGER)
            self.ui.tbl_invoice_items.setRowCount(0)
            self._selected_invoice_id = None
            self._selected_product = None
            self.ui.btn_next.setEnabled(False)
            return

        # ── Kiểm tra thời hạn ──────────────────────────────────
        created_str = str(invoice[4])
        try:
            inv_date = datetime.strptime(created_str[:19], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            inv_date = datetime.now()

        self._invoice_date = inv_date
        delta = datetime.now() - inv_date

        # Xử lý nghiêm ngặt: Từ chối hóa đơn quá hạn
        if delta > timedelta(days=RETURN_DAYS_LIMIT):
            self._set_inv_info(f"⛔ Hoá đơn #{inv_id} quá hạn {RETURN_DAYS_LIMIT} ngày — Từ chối đổi/trả.", DANGER)
            show_error(
                self.ui, "Từ chối", 
                f"⛔ Hoá đơn #{inv_id} đã xuất cách đây {delta.days} ngày.\n"
                f"Vượt quá thời hạn {RETURN_DAYS_LIMIT} ngày quy định.\n"
                f"Yêu cầu đổi/trả bị từ chối!"
            )
            self.ui.tbl_invoice_items.setRowCount(0)
            self._selected_invoice_id = None
            self._selected_product = None
            self.ui.btn_next.setEnabled(False)
            return

        # ── HĐ hợp lệ ───────────────────────
        self._selected_invoice_id = inv_id
        days_str = f"Còn {RETURN_DAYS_LIMIT - delta.days} ngày"
        self._set_inv_info(
            f"✔ HĐ #{invoice[0]} | KH: {invoice[1]} | Tổng: {invoice[2]:,.0f} ₫ | Ngày mua: {inv_date.strftime('%d/%m/%Y %H:%M')} | {days_str}",
            SUCCESS
        )

        # Điền bảng chi tiết SP thuộc hóa đơn
        try:
            details = ReturnService.get_invoice_details(inv_id)
        except Exception as e:
            show_error(self.ui, "Lỗi truy vấn", f"Lỗi DB khi lấy chi tiết hóa đơn:\n{e}")
            return

        self.ui.tbl_invoice_items.setRowCount(0)
        for row_data in details:
            r = self.ui.tbl_invoice_items.rowCount()
            self.ui.tbl_invoice_items.insertRow(r)
            try:
                # sqlite3.Row hỗ trợ cả index lẫn key
                prod_name = str(row_data[1])          # product_name
                qty       = int(row_data[2])           # quantity
                price_val = float(row_data[3])         # price
                subtotal  = float(row_data[4])         # subtotal
            except Exception as e:
                print(f"[fill_table] parse row error: {e} | row={tuple(row_data)}")
                continue
            self.ui.tbl_invoice_items.setItem(r, 0, QTableWidgetItem(prod_name))
            self.ui.tbl_invoice_items.setItem(r, 1, QTableWidgetItem(str(qty)))
            self.ui.tbl_invoice_items.setItem(r, 2, QTableWidgetItem(f"{price_val:,.0f} ₫"))
            self.ui.tbl_invoice_items.setItem(r, 3, QTableWidgetItem(f"{subtotal:,.0f} ₫"))

        if self.ui.tbl_invoice_items.rowCount() == 0:
            self._set_inv_info("⚠ Hóa đơn này không có sản phẩm chi tiết.", WARNING)

        self._selected_product = None
        self.ui.btn_next.setEnabled(False)

    def _set_inv_info(self, text, color):
        self.ui.lbl_inv_info.setText(text)
        self.ui.lbl_inv_info.setStyleSheet(
            f"color:{color}; font-size:13px; background:transparent; padding:4px 0;"
            f"font-family:'Nunito','Segoe UI',sans-serif; font-weight:600;"
        )

    # ─────────────────────────────────────────────────
    # CHỌN SP TỪ BẢNG HĐ
    # ─────────────────────────────────────────────────
    def on_item_selected(self):
        try:
            selected = self.ui.tbl_invoice_items.selectedItems()
            if not selected:
                return
            row = selected[0].row()
            
            item_name  = self.ui.tbl_invoice_items.item(row, 0)
            item_qty   = self.ui.tbl_invoice_items.item(row, 1)
            item_price = self.ui.tbl_invoice_items.item(row, 2)
            if not item_name or not item_qty or not item_price:
                return
            
            name  = item_name.text().strip()
            qty   = int(item_qty.text().strip())
            price_text = item_price.text().replace(" ₫", "").replace(",", "").replace(".", "").strip()
            price = float(price_text)
            
            self._selected_product = {"name": name, "price": price, "max_qty": qty}
            self.ui.spn_qty.setMaximum(qty)
            self.ui.spn_qty.setValue(1)
            self.ui.btn_next.setEnabled(True)
            # Highlight dòng được chọn
            self._set_inv_info(
                f"✔ Đã chọn: {name}  |  Đơn giá: {price:,.0f} ₫  |  SL tối đa: {qty}",
                SUCCESS
            )
        except Exception as e:
            print(f"[on_item_selected] lỗi: {e}")
            show_warning(self.ui, "Lỗi phân tích dữ liệu", f"Không thể lấy dữ liệu sản phẩm từ bảng:\n{e}")

    # ═══════════════════════════════════════════════════════════
    # BƯỚC 2
    # ═══════════════════════════════════════════════════════════

    def _load_products_for_exchange(self):
        products = ReturnService.get_all_products()
        self._all_products = products
        self.ui.cb_new_product.blockSignals(True)
        self.ui.cb_new_product.clear()
        old_name = self._selected_product["name"] if self._selected_product else ""
        for p in products:
            if str(p[1]) != old_name:
                display = f"{p[1]} [Size:{p[3]}|Màu:{p[4]}|{p[5]:,.0f}₫|Tồn:{p[6]}]"
                self.ui.cb_new_product.addItem(display, p)
        self.ui.cb_new_product.blockSignals(False)
        self.on_new_product_changed(self.ui.cb_new_product.currentIndex())

    def _update_selected_info(self):
        if not self._selected_product:
            return
        sp = self._selected_product
        inv_date_str = self._invoice_date.strftime("%d/%m/%Y %H:%M") if self._invoice_date else "—"
        self.ui.lbl_selected_prod.setText(
            f"<b>Hóa đơn #{self._selected_invoice_id}</b> · "
            f"Mặt hàng: <b>{sp['name']}</b> · "
            f"Đơn giá: <b>{sp['price']:,.0f} ₫</b> · "
            f"SL tối đa: <b>{sp['max_qty']}</b> · "
            f"Xuất lúc: {inv_date_str}"
        )

    def on_type_changed(self, idx):
        is_exchange = (idx == 1)
        self.ui._new_prod_frame.setVisible(is_exchange)
        self.update_refund_amount()
        if is_exchange:
            self.on_new_product_changed(self.ui.cb_new_product.currentIndex())

    def on_new_product_changed(self, idx):
        prod_data = self.ui.cb_new_product.currentData()
        self.ui.cb_new_size.blockSignals(True)
        self.ui.cb_new_size.clear()
        self.ui.cb_new_color.blockSignals(True)
        self.ui.cb_new_color.clear()
        if prod_data:
            # size
            sizes_str = str(prod_data[3] or "")
            sizes = [s.strip() for s in sizes_str.split(",") if s.strip()]
            if sizes:
                for sz in sizes:
                    self.ui.cb_new_size.addItem(sz, sz)
            else:
                self.ui.cb_new_size.addItem("F", "F")
                
            # màu sắc
            colors_str = str(prod_data[4] or "")
            colors = [c.strip() for c in colors_str.split(",") if c.strip()]
            if colors:
                for cl in colors:
                    self.ui.cb_new_color.addItem(cl, cl)
            else:
                self.ui.cb_new_color.addItem("N/A", "N/A")
                
        self.ui.cb_new_size.blockSignals(False)
        self.ui.cb_new_color.blockSignals(False)
        self.update_refund_amount()

    def update_refund_amount(self):
        if self._selected_product is None:
            self.ui.lbl_refund_amount.setText("0 ₫")
            self.ui.lbl_diff.setText("")
            return

        qty = self.ui.spn_qty.value()
        old_price = self._selected_product["price"]
        is_exchange = (self.ui.cb_return_type.currentIndex() == 1)

        if not is_exchange:
            amount = old_price * qty
            self.ui.lbl_refund_amount.setText(f"{amount:,.0f} ₫")
            self.ui.lbl_diff.setText("")
        else:
            prod_data = self.ui.cb_new_product.currentData()
            if prod_data is None:
                self.ui.lbl_refund_amount.setText("0 ₫")
                self.ui.lbl_diff.setText("")
                return
            new_price = float(prod_data[5])
            diff = (new_price - old_price) * qty
            if diff > 0:
                self.ui.lbl_refund_amount.setText(f"Khách trả thêm: {diff:,.0f} ₫")
                self.ui.lbl_diff.setText(f"🔺 SP mới đắt hơn → Thu thêm khách {diff:,.0f} ₫")
                self.ui.lbl_diff.setStyleSheet(f"color:{WARNING}; font-size:13px; font-weight:700;")
            elif diff < 0:
                self.ui.lbl_refund_amount.setText(f"Hoàn lại khách: {abs(diff):,.0f} ₫")
                self.ui.lbl_diff.setText(f"🔻 SP mới rẻ hơn → Hoàn trả khách {abs(diff):,.0f} ₫")
                self.ui.lbl_diff.setStyleSheet(f"color:{SUCCESS}; font-size:13px; font-weight:700;")
            else:
                self.ui.lbl_refund_amount.setText("Không chênh lệch")
                self.ui.lbl_diff.setText("= Giá trị tương đương nhau")
                self.ui.lbl_diff.setStyleSheet(f"color:{TEXT_MID}; font-size:13px; font-weight:700;")

    # ─────────────────────────────────────────────────
    # XÁC NHẬN GIAO DỊCH
    # ─────────────────────────────────────────────────
    def confirm_return(self):
        if self._selected_invoice_id is None or self._selected_product is None:
            show_warning(self.ui, "Thiếu thông tin", "Vui lòng hoàn thành Bước 1 trước.")
            return

        qty          = self.ui.spn_qty.value()
        is_exchange  = (self.ui.cb_return_type.currentIndex() == 1)
        return_type  = "EXCHANGE" if is_exchange else "REFUND"
        reason_base  = self.ui.cb_reason.currentText()
        note         = self.ui.txt_note.text().strip()
        reason       = f"{reason_base}. {note}" if note else reason_base
        old_price    = self._selected_product["price"]
        old_name     = self._selected_product["name"]

        new_product_name = ""
        price_diff = 0.0
        summary_lines = []

        if is_exchange:
            prod_data = self.ui.cb_new_product.currentData()
            if prod_data is None:
                show_warning(self.ui, "Chưa chọn SP mới", "Vui lòng chọn sản phẩm mới để đổi!")
                return
            new_product_name = str(prod_data[1])
            selected_size = self.ui.cb_new_size.currentText().strip()
            selected_color = self.ui.cb_new_color.currentText().strip()
            
            parts = []
            if selected_size:
                parts.append(f"Size: {selected_size}")
            if selected_color:
                parts.append(f"Màu: {selected_color}")
            if parts:
                new_product_name = f"{new_product_name} ({', '.join(parts)})"
                
            new_price = float(prod_data[5])
            price_diff = (new_price - old_price) * qty

            summary_lines = [
                f"Hình thức:        Đổi sản phẩm",
                f"SP trả lại:       {old_name} ({old_price:,.0f} ₫)",
                f"SP mới xuất:      {new_product_name} ({new_price:,.0f} ₫)",
                f"Số lượng:         {qty}",
            ]
            if price_diff > 0:
                summary_lines.append(f"Khách trả thêm:   {price_diff:,.0f} ₫")
            elif price_diff < 0:
                summary_lines.append(f"Hoàn lại khách:   {abs(price_diff):,.0f} ₫")
            else:
                summary_lines.append("Không chênh lệch giá")
        else:
            refund = old_price * qty
            summary_lines = [
                f"Hình thức:        Trả hàng (hoàn tiền)",
                f"SP hoàn kho:      {old_name} ({old_price:,.0f} ₫)",
                f"Số lượng:         {qty}",
                f"Số tiền hoàn:     {refund:,.0f} ₫",
            ]

        summary_lines.append(f"\nLý do: {reason}")
        confirm_msg = "\n".join(summary_lines) + "\n\nXác nhận hoàn tất giao dịch này?"

        msg = QMessageBox(self.ui)
        msg.setWindowTitle("Xác nhận đổi trả")
        msg.setText(confirm_msg)
        msg.setIcon(QMessageBox.Question)
        btn_yes = msg.addButton("Đồng ý", QMessageBox.YesRole)
        btn_no = msg.addButton("Hủy bỏ", QMessageBox.NoRole)

        msg.setStyleSheet("QMessageBox { background-color: #ffffff; } QLabel { color: #0f172a; font-size: 14px; font-weight: bold; }")
        btn_yes.setStyleSheet("QPushButton { background-color: #059669; color: white; border: none; border-radius: 6px; padding: 8px 18px; font-weight: bold; min-width: 80px; } QPushButton:hover { background-color: #047857; }")
        btn_no.setStyleSheet("QPushButton { background-color: #f1f5f9; color: #334155; border: 1px solid #cbd5e1; padding: 8px 18px; font-weight: bold; min-width: 80px; } QPushButton:hover { background-color: #e2e8f0; color: #0f172a; }")
        msg.exec_()

        if msg.clickedButton() != btn_yes:
            return

        try:
            ReturnService.process_return(
                invoice_id       = self._selected_invoice_id,
                product_name     = old_name,
                quantity         = qty,
                price            = old_price,
                reason           = reason,
                return_type      = return_type,
                new_product_name = new_product_name,
                price_diff       = price_diff
            )
            if is_exchange:
                success_msg = f"Đổi hàng thành công!\n\n• Đã nhập lại kho: {old_name}\n• Đã xuất kho mới: {new_product_name}"
            else:
                refund = old_price * qty
                success_msg = f"Trả hàng thành công!\n\n• Đã hoàn kho: {old_name}\n• Hoàn tiền khách: {refund:,.0f} ₫"
            
            show_success(self.ui, "Hoàn tất", success_msg)
            self.clear_form()
            self.load_history()
            if self.on_success:
                self.on_success()
        except Exception as e:
            show_error(self.ui, "Lỗi hệ thống", f"Không thể xử lý giao dịch:\n{str(e)}")

    # ─────────────────────────────────────────────────
    # CLEAR FORM
    # ─────────────────────────────────────────────────
    def clear_form(self):
        if hasattr(self.ui, 'cb_invoice_id'):
            self.ui.cb_invoice_id.clearEditText()
        self._set_inv_info("Chưa có hoá đơn nào được chọn", TEXT_MID)
        self.ui.tbl_invoice_items.setRowCount(0)
        self.ui.txt_note.clear()
        if hasattr(self.ui, 'txt_search_inv'):
            self.ui.txt_search_inv.clear()
        self.ui.spn_qty.setValue(1)
        self.ui.lbl_refund_amount.setText("0 ₫")
        self.ui.lbl_diff.setText("")
        self.ui.btn_next.setEnabled(False)
        self._selected_product = None
        self._selected_invoice_id = None
        self._invoice_date = None
        
        if hasattr(self.ui, 'return_dialog'):
            self.ui.return_dialog.reject()
            
        self.go_to_step1()

    # ─────────────────────────────────────────────────
    # LỊCH SỬ & LỌC DỮ LIỆU
    # ─────────────────────────────────────────────────
    def filter_by_type(self, ret_type):
        self._current_filter_type = ret_type
        self.load_history(self.ui.txt_search.text().strip())

    def load_history(self, keyword=""):
        if keyword:
            rows = ReturnService.search_returns(keyword)
        else:
            rows = ReturnService.get_all_returns()

        self.ui.tbl_history.setRowCount(0)
        total_refund = 0
        total_exchange = 0

        for row_data in rows:
            rtype = row_data[9]
            
            # Lọc theo tab bộ lọc đang chọn (Hỗ trợ cả EXCHANGE/Đổi hàng và REFUND/Trả hàng)
            if self._current_filter_type:
                if self._current_filter_type == "EXCHANGE" and rtype not in ("EXCHANGE", "Đổi hàng"):
                    continue
                elif self._current_filter_type == "REFUND" and rtype not in ("REFUND", "Trả hàng"):
                    continue

            r = self.ui.tbl_history.rowCount()
            self.ui.tbl_history.insertRow(r)

            refund     = row_data[7]
            price_diff = row_data[6]
            is_ref = rtype in ("REFUND", "Trả hàng")
            is_exc = rtype in ("EXCHANGE", "Đổi hàng")

            type_label = "Trả hàng" if is_ref else "Đổi hàng"

            if is_ref:
                total_refund += refund
            else:
                total_exchange += 1

            if is_exc:
                diff_val = price_diff
                if diff_val > 0:
                    diff_str = f"+{diff_val:,.0f} ₫"
                elif diff_val < 0:
                    diff_str = f"-{abs(diff_val):,.0f} ₫"
                else:
                    diff_str = "—"
            else:
                diff_str = "—"

            cells = [
                f"GD{row_data[0]:03d}",
                f"HD{row_data[1]:03d}",
                str(row_data[2]),
                str(row_data[3]),
                f"{row_data[4]:,.0f} ₫",
                str(row_data[5]) if (row_data[5] and is_exc) else "—",
                diff_str,
                f"{refund:,.0f} ₫" if is_ref else "—",
                str(row_data[8]),
                type_label,
                str(row_data[10]),
            ]
            for col, val in enumerate(cells):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                # Lưu thông tin bổ sung vào UserRole của cột đầu tiên
                if col == 0:
                    item.setData(Qt.UserRole, {
                        "customer_name": row_data[11] or "N/A",
                        "phone": row_data[12] or "N/A",
                        "reason": row_data[8],
                        "new_product": row_data[5] or "—",
                        "price_diff": row_data[6],
                        "refund": row_data[7],
                        "qty": row_data[3]
                    })
                self.ui.tbl_history.setItem(r, col, item)

            type_item = self.ui.tbl_history.item(r, 9)
            if is_ref:
                type_item.setForeground(QColor(DANGER))
                type_item.setBackground(QColor("#fdf0ef"))
            else:
                type_item.setForeground(QColor(INFO))
                type_item.setBackground(QColor("#eaf4fb"))

        # Cập nhật số liệu thống kê tổng quan
        count = self.ui.tbl_history.rowCount()
        if hasattr(self.ui, 'lbl_stat_total'):
            self.ui.lbl_stat_total.setText(f"{count}")
        if hasattr(self.ui, 'lbl_stat_exc'):
            self.ui.lbl_stat_exc.setText(f"{total_exchange}")
        if hasattr(self.ui, 'lbl_stat_ref'):
            self.ui.lbl_stat_ref.setText(f"{total_refund:,.0f} ₫")

        # Fallback an toàn
        if hasattr(self.ui, 'lbl_total_count'):
            self.ui.lbl_total_count.setText(f"Tổng phiếu: {count}")
            self.ui.lbl_total_refund.setText(f"Tổng hoàn tiền: {total_refund:,.0f} ₫")
            self.ui.lbl_total_exchange.setText(f"Tổng đổi hàng: {total_exchange}")

    def search_history(self, keyword):
        self.load_history(keyword.strip())

    def show_return_detail(self, row, col):
        item = self.ui.tbl_history.item(row, 0)
        if not item: return
        
        extra = item.data(Qt.UserRole)
        if not extra: return
        
        # Lấy dữ liệu từ các cột hiển thị
        ma_gd = self.ui.tbl_history.item(row, 0).text()
        ma_hd = self.ui.tbl_history.item(row, 1).text()
        sp_cu = self.ui.tbl_history.item(row, 2).text()
        loai  = self.ui.tbl_history.item(row, 9).text()
        
        qty = extra.get('qty', 1)
        sp_moi = extra.get('new_product', '—')
        diff = extra.get('price_diff', 0)
        refund = extra.get('refund', 0)
        
        # Định dạng tiền tệ
        diff_str = f"{diff:,.0f} ₫" if diff != 0 else "0 ₫"
        refund_str = f"{refund:,.0f} ₫"
        
        msg = QMessageBox(self.ui)
        msg.setWindowTitle(f"Chi tiết {loai} - {ma_gd}")
        
        # Phần thông tin sản phẩm thay đổi tùy theo loại giao dịch
        if "Đổi" in loai:
            product_section = f"""
                <tr><td style='color: #64748b; padding: 6px 0;'>📤 Trả lại SP:</td><td style='font-weight: bold;'>{sp_cu}</td></tr>
                <tr><td style='color: #64748b; padding: 6px 0;'>📥 Nhận mới SP:</td><td style='font-weight: bold; color: #059669;'>{sp_moi}</td></tr>
                <tr><td style='color: #64748b; padding: 6px 0;'>🔢 Số lượng:</td><td style='font-weight: bold;'>{qty}</td></tr>
                <tr><td style='color: #64748b; padding: 6px 0;'>⚖️ Chênh lệch:</td><td style='font-weight: bold;'>{diff_str}</td></tr>
            """
        else:
            product_section = f"""
                <tr><td style='color: #64748b; padding: 6px 0;'>📤 Trả lại SP:</td><td style='font-weight: bold;'>{sp_cu}</td></tr>
                <tr><td style='color: #64748b; padding: 6px 0;'>🔢 Số lượng:</td><td style='font-weight: bold;'>{qty}</td></tr>
                <tr><td style='color: #64748b; padding: 6px 0;'>💰 Tiền hoàn:</td><td style='font-weight: bold; color: #ef4444;'>{refund_str}</td></tr>
            """

        detail_html = f"""
            <div style='min-width: 400px;'>
                <h3 style='color: #1d4ed8; margin-top: 0;'>📄 Thông tin phiếu {loai}</h3>
                <hr style='border: 0; border-top: 1px solid #e2e8f0; margin: 10px 0;'>
                <table style='width: 100%; font-size: 14px;'>
                    <tr><td style='color: #64748b; padding: 4px 0; width: 120px;'>Mã hóa đơn:</td><td style='font-weight: bold;'>{ma_hd}</td></tr>
                    <tr><td style='color: #64748b; padding: 4px 0;'>Khách hàng:</td><td style='font-weight: bold; color: #0f172a;'>{extra['customer_name']}</td></tr>
                    <tr><td style='color: #64748b; padding: 4px 0;'>Số điện thoại:</td><td style='font-weight: bold;'>{extra['phone']}</td></tr>
                    <tr><td colspan='2' style='padding: 8px 0;'><hr style='border: 0; border-top: 1px dashed #cbd5e1;'></td></tr>
                    {product_section}
                    <tr><td style='color: #64748b; padding: 12px 0 4px 0;' colspan='2'><b>Lý do chi tiết:</b></td></tr>
                    <tr><td style='background: #f8fafc; padding: 10px; border-radius: 6px; border: 1px solid #e2e8f0;' colspan='2'>{extra['reason']}</td></tr>
                </table>
            </div>
        """
        
        msg.setText(detail_html)
        msg.setIcon(QMessageBox.Information)
        
        ok_btn = msg.addButton("Đã rõ", QMessageBox.AcceptRole)
        from config import PRIMARY
        ok_btn.setStyleSheet(f"QPushButton {{ background-color: {PRIMARY}; color: white; border-radius: 8px; padding: 8px 30px; font-weight: 800; min-width: 100px; }} QPushButton:hover {{ background-color: #1e40af; }}")
        msg.setStyleSheet("QMessageBox { background-color: white; } QLabel { color: #1e293b; }")
        
        msg.exec_()
