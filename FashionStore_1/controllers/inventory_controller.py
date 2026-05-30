from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt
from utils.message_utils import show_warning, show_success, show_confirm
from modules.inventory.inventory_service import InventoryService
from ui.dialogs.inventory_dialog import InventoryDialog


class InventoryController:

    def __init__(self, ui):
        self.ui = ui
        self._all_data = []

        self.load_inventory()

        # Kết nối sự kiện nút
        self.ui.btn_add.clicked.connect(self.add_inventory)
        self.ui.btn_update.clicked.connect(self.update_inventory)
        self.ui.btn_delete.clicked.connect(self.delete_inventory)

        # Kết nối thanh tìm kiếm
        self.ui.btn_search.clicked.connect(self.search_inventory)
        self.ui.txt_search.returnPressed.connect(self.search_inventory)
        self.ui.txt_search.textChanged.connect(self._live_search)

    def load_inventory(self):
        self._all_data = InventoryService.get_inventory()
        self._populate_table(self._all_data)

    def _populate_table(self, data):
        self.ui.table.setRowCount(0)
        for row_index, item in enumerate(data):
            self.ui.table.insertRow(row_index)
            # item = (id, product_name, quantity, min_quantity, supplier_name, import_price, size, color)
            
            qty = int(item[2])
            min_qty = int(item[3])
            
            mapping = {
                0: item[0],  # ID
                1: item[1],  # Tên SP
                2: item[6] if len(item) > 6 and item[6] else "—",  # Size
                3: item[7] if len(item) > 7 and item[7] else "—",  # Màu sắc
                4: item[2],  # Số lượng
                5: item[3],  # Tối thiểu
                6: item[4],  # Nhà cung cấp
                7: item[5]   # Giá nhập
            }

            for col_index in range(8):
                val = mapping.get(col_index, "")
                if col_index == 7: # Giá nhập
                    val_str = f"{float(val or 0):,.0f} ₫"
                else:
                    val_str = str(val if val is not None else "")

                tbl_item = QTableWidgetItem(val_str)
                tbl_item.setTextAlignment(Qt.AlignVCenter | (Qt.AlignCenter if col_index in [0, 2, 3, 4, 5, 7] else Qt.AlignLeft))

                # Highlight đỏ nếu số lượng tồn kho <= mức cảnh báo tối thiểu
                if col_index == 4 and qty <= min_qty:
                    tbl_item.setForeground(Qt.red)
                    # Thêm ký hiệu cảnh báo trực quan
                    tbl_item.setText(f"⚠️ {val_str}")

                self.ui.table.setItem(row_index, col_index, tbl_item)

    def add_inventory(self):
        dlg = InventoryDialog(self.ui)
        if dlg.exec_() == InventoryDialog.Accepted:
            data = dlg.get_data()
            if not data["product_name"]:
                show_warning(self.ui, "Thiếu thông tin", "Vui lòng nhập tên mặt hàng cần nhập kho!")
                return
            
            InventoryService.add_inventory(
                data["product_name"],
                data["quantity"],
                data["min_quantity"],
                data["supplier_name"],
                data["import_price"]
            )
            show_success(self.ui, "Thành công", f"Đã nhập kho lô hàng '{data['product_name']}' thành công!")
            self.load_inventory()

    def update_inventory(self):
        row = self.ui.table.currentRow()
        if row < 0:
            show_warning(self.ui, "Chưa chọn", "Vui lòng click chọn một lô hàng trong bảng để cập nhật!")
            return

        inv_id = int(self.ui.table.item(row, 0).text())
        target_item = next((i for i in self._all_data if i[0] == inv_id), None)
        if not target_item:
            return

        dlg = InventoryDialog(self.ui, item_data=target_item)
        if dlg.exec_() == InventoryDialog.Accepted:
            data = dlg.get_data()
            if not data["product_name"]:
                show_warning(self.ui, "Thiếu thông tin", "Tên mặt hàng không được để trống!")
                return

            InventoryService.update_inventory(
                inv_id,
                data["product_name"],
                data["quantity"],
                data["min_quantity"],
                data["supplier_name"],
                data["import_price"]
            )
            show_success(self.ui, "Thành công", "Cập nhật lô hàng thành công!")
            self.load_inventory()

    def delete_inventory(self):
        row = self.ui.table.currentRow()
        if row < 0:
            show_warning(self.ui, "Chưa chọn", "Vui lòng click chọn một lô hàng trong bảng để xóa!")
            return

        inv_id = int(self.ui.table.item(row, 0).text())
        prod_name = self.ui.table.item(row, 1).text().replace("⚠️ ", "")

        if show_confirm(self.ui, "Xác nhận xóa", f"Bạn có chắc chắn muốn xóa bản ghi nhập kho của '{prod_name}' không?"):
            InventoryService.delete_inventory(inv_id)
            show_success(self.ui, "Thành công", f"Đã xóa thành công lô hàng '{prod_name}'.")
            self.load_inventory()

    def search_inventory(self):
        kw = self.ui.txt_search.text().strip()
        if not kw:
            self.load_inventory()
            return
        data = InventoryService.search_inventory(kw)
        self._populate_table(data)

    def _live_search(self, text):
        kw = text.strip().lower()
        if not kw:
            self._populate_table(self._all_data)
            return
        filtered = [
            i for i in self._all_data
            if kw in str(i[1]).lower() or kw in str(i[4] or "").lower()
        ]
        self._populate_table(filtered)