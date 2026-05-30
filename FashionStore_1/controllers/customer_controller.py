from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt
from utils.message_utils import show_warning, show_success, show_confirm
from modules.customers.customer_service import CustomerService
from ui.dialogs.customer_dialog import CustomerDialog
from ui.dialogs.invoice_detail_dialog import InvoiceDetailDialog


class CustomerController:

    def __init__(self, ui):
        self.ui = ui
        self._all_data = []

        self.load_customers()

        # Kết nối sự kiện nút
        self.ui.btn_add.clicked.connect(self.add_customer)
        self.ui.btn_update.clicked.connect(self.update_customer)
        self.ui.btn_delete.clicked.connect(self.delete_customer)

        # Kết nối thanh tìm kiếm
        self.ui.txt_search.textChanged.connect(self.search_customer)

        # Kết nối sự kiện chọn dòng khách hàng để xem chi tiết
        self.ui.table.itemSelectionChanged.connect(self.show_customer_detail)

        # Kết nối sự kiện click chọn hóa đơn trong lịch sử mua hàng của khách
        self.ui.table_history.cellClicked.connect(self.show_invoice_detail)

    def load_customers(self):
        self._all_data = CustomerService.get_customers()
        self._populate_table(self._all_data)

    def _populate_table(self, data):
        self.ui.table.setRowCount(0)
        for row_index, customer in enumerate(data):
            self.ui.table.insertRow(row_index)
            # customer = (id, full_name, phone, email, points, member_rank)
            for col_index in range(6):
                val = str(customer[col_index] if customer[col_index] is not None else "")
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignVCenter | (Qt.AlignCenter if col_index in [0, 2, 4, 5] else Qt.AlignLeft))
                self.ui.table.setItem(row_index, col_index, item)

    def add_customer(self):
        dlg = CustomerDialog(self.ui)
        if dlg.exec_() == CustomerDialog.Accepted:
            data = dlg.get_data()
            if not data["name"] or not data["phone"]:
                show_warning(self.ui, "Thiếu thông tin", "Vui lòng nhập ít nhất Họ tên và Số điện thoại!")
                return
            CustomerService.add_customer(
                data["name"],
                data["phone"],
                data["email"],
                data["points"],
                data["rank"]
            )
            show_success(self.ui, "Thành công", "Đã thêm khách hàng mới thành công!")
            self.load_customers()

    def update_customer(self):
        row = self.ui.table.currentRow()
        if row < 0:
            show_warning(self.ui, "Chưa chọn", "Vui lòng click chọn một khách hàng trong bảng để sửa!")
            return

        cust_id = int(self.ui.table.item(row, 0).text())
        # Tìm data gốc
        target_cust = next((c for c in self._all_data if c[0] == cust_id), None)
        if not target_cust:
            return

        dlg = CustomerDialog(self.ui, customer_data=target_cust)
        if dlg.exec_() == CustomerDialog.Accepted:
            data = dlg.get_data()
            if not data["name"] or not data["phone"]:
                show_warning(self.ui, "Thiếu thông tin", "Họ tên và Số điện thoại không được để trống!")
                return
            CustomerService.update_customer(
                cust_id,
                data["name"],
                data["phone"],
                data["email"],
                data["points"],
                data["rank"]
            )
            show_success(self.ui, "Thành công", "Cập nhật thông tin khách hàng thành công!")
            self.load_customers()

    def delete_customer(self):
        row = self.ui.table.currentRow()
        if row < 0:
            show_warning(self.ui, "Chưa chọn", "Vui lòng click chọn một khách hàng trong bảng để xóa!")
            return

        cust_id = int(self.ui.table.item(row, 0).text())
        cust_name = self.ui.table.item(row, 1).text()

        if show_confirm(self.ui, "Xác nhận xóa", f"Bạn có chắc muốn xóa vĩnh viễn khách hàng '{cust_name}' khỏi hệ thống?"):
            CustomerService.delete_customer(cust_id)
            show_success(self.ui, "Thành công", f"Đã xóa khách hàng '{cust_name}' khỏi hệ thống.")
            self.load_customers()

    def search_customer(self, keyword):
        kw = keyword.strip().lower()
        if not kw:
            self._populate_table(self._all_data)
            return

        # Tìm live trên danh sách đã tải (nhanh và tiện) hoặc gọi DB
        filtered = [
            c for c in self._all_data
            if kw in str(c[1]).lower() or kw in str(c[2]).lower()
        ]
        self._populate_table(filtered)

    def show_customer_detail(self):
        row = self.ui.table.currentRow()
        if row < 0:
            self.ui.detail_widget.hide()
            self.ui.lbl_placeholder.show()
            return

        try:
            cust_id = int(self.ui.table.item(row, 0).text())
            customer = next((c for c in self._all_data if c[0] == cust_id), None)
            if not customer:
                self.ui.detail_widget.hide()
                self.ui.lbl_placeholder.show()
                return

            # Cập nhật thông tin cơ bản
            self.ui.val_name.setText(str(customer[1]))
            self.ui.val_phone.setText(str(customer[2] or "N/A"))
            self.ui.val_email.setText(str(customer[3] or "N/A"))
            self.ui.val_rank.setText(f"🏅 {customer[5]}")
            self.ui.val_points.setText(f"✨ {customer[4]} điểm")

            # Lấy lịch sử mua hàng
            history = CustomerService.get_purchase_history(customer[1])
            total_spent = sum(float(h[1] or 0) for h in history)
            self.ui.lbl_spent_val.setText(f"{total_spent:,.0f} ₫")

            # Nạp vào bảng lịch sử đơn mua
            self.ui.table_history.setRowCount(0)
            for idx, inv in enumerate(history):
                self.ui.table_history.insertRow(idx)
                # inv = (id, total, payment_method, created_at)
                
                item_id = QTableWidgetItem(f"HD{inv[0]:03d}")
                item_id.setTextAlignment(Qt.AlignCenter)
                item_id.setData(Qt.UserRole, inv[0])
                self.ui.table_history.setItem(idx, 0, item_id)
                
                date_str = str(inv[3])
                if len(date_str) > 16:
                    date_str = date_str[:16]
                item_date = QTableWidgetItem(date_str)
                item_date.setTextAlignment(Qt.AlignCenter)
                self.ui.table_history.setItem(idx, 1, item_date)
                
                item_method = QTableWidgetItem(str(inv[2]))
                item_method.setTextAlignment(Qt.AlignCenter)
                self.ui.table_history.setItem(idx, 2, item_method)
                
                item_total = QTableWidgetItem(f"{float(inv[1] or 0):,.0f} ₫")
                item_total.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.ui.table_history.setItem(idx, 3, item_total)

            self.ui.lbl_placeholder.hide()
            self.ui.detail_widget.show()
        except Exception as e:
            print("Error displaying customer detail:", e)
            self.ui.detail_widget.hide()
            self.ui.lbl_placeholder.show()

    def show_invoice_detail(self, row, col):
        item_id = self.ui.table_history.item(row, 0)
        if not item_id:
            return
        
        real_id = item_id.data(Qt.UserRole)
        if real_id is None:
            return
            
        summary_data = (
            self.ui.table_history.item(row, 0).text(),  # Mã HĐ (HD002)
            self.ui.val_name.text(),                     # Khách hàng (Trần Văn Minh)
            self.ui.table_history.item(row, 3).text(),  # Tổng tiền (850,000 ₫)
            self.ui.table_history.item(row, 2).text(),  # Phương thức thanh toán (Chuyển khoản)
            self.ui.table_history.item(row, 1).text()   # Thời gian tạo (2026-05-15 05:32)
        )

        dlg = InvoiceDetailDialog(self.ui, invoice_id=real_id, summary_data=summary_data)
        dlg.exec_()