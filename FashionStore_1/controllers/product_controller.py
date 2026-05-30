from PyQt5.QtWidgets import QTableWidgetItem, QDialog
from PyQt5.QtCore import Qt
from utils.message_utils import show_info, show_warning, show_error, show_success, show_confirm
from modules.products.product_service import ProductService
from ui.dialogs.product_dialog import ProductDialog

class ProductController:

    def __init__(self, ui):
        self.ui = ui
        self._all_products = []
        self.load_products()

        # Kết nối các nút thao tác
        self.ui.btn_add.clicked.connect(self.add_product)
        self.ui.btn_update.clicked.connect(self.update_product)
        self.ui.btn_delete.clicked.connect(self.delete_product)

        # Kết nối sự kiện lọc
        self.ui.txt_search.textChanged.connect(self.filter_list)
        self.ui.cb_filter_category.currentIndexChanged.connect(self.filter_list)

    def load_products(self):
        self._all_products = ProductService.get_products()
        
        categories = sorted(list({str(p[2]).strip() for p in self._all_products if p[2]}))
        
        self.ui.cb_filter_category.blockSignals(True)
        self.ui.cb_filter_category.clear()
        self.ui.cb_filter_category.addItem("📂 Tất cả danh mục", "")
        for cat in categories:
            if cat:
                self.ui.cb_filter_category.addItem(f"📁 {cat}", cat)
        self.ui.cb_filter_category.blockSignals(False)

        self.filter_list()

    def _populate_table(self, data):
        self.ui.table.setRowCount(0)
        for row_index, product in enumerate(data):
            self.ui.table.insertRow(row_index)
            # product = (id, name, category, size, color, price, stock, description, import_price, supplier_name)
            
            # Mapping columns: 
            # 0: id, 1: name, 2: category, 3: size, 4: color, 5: import_price, 6: price, 7: stock, 8: supplier_name, 9: description
            mapping = {
                0: product[0], # ID
                1: product[1], # Name
                2: product[2], # Cat
                3: product[3], # Size
                4: product[4], # Color
                5: product[8] if len(product) > 8 else 0, # Import Price
                6: product[5], # Price
                7: product[6], # Stock
                8: product[9] if len(product) > 9 else "", # Supplier Name
                9: product[7]  # Desc
            }

            for col_index in range(10):
                val = mapping.get(col_index, "")
                if col_index in [5, 6]: # Giá nhập & Giá bán
                    val_str = f"{float(val or 0):,.0f} ₫"
                else:
                    val_str = str(val if val is not None else "")

                item = QTableWidgetItem(val_str)
                item.setTextAlignment(Qt.AlignVCenter | (Qt.AlignCenter if col_index in [0, 2, 3, 4, 5, 6, 7, 8] else Qt.AlignLeft))
                self.ui.table.setItem(row_index, col_index, item)

    def filter_list(self):
        kw = self.ui.txt_search.text().strip().lower()
        selected_cat = self.ui.cb_filter_category.currentData() or ""

        filtered = []
        for p in self._all_products:
            match_kw = kw in str(p[1]).lower() or kw in str(p[7] or "").lower()
            match_cat = (not selected_cat) or (str(p[2]).strip() == selected_cat)
            
            if match_kw and match_cat:
                filtered.append(p)

        self._populate_table(filtered)

    def add_product(self):
        dlg = ProductDialog(self.ui)
        if dlg.exec_() == QDialog.Accepted:
            data = dlg.get_data()
            if not data["name"]:
                show_warning(self.ui, "Thiếu thông tin", "Vui lòng điền tên sản phẩm!")
                return
            ProductService.add_product(
                data["name"],
                data["category"],
                data["size"],
                data["color"],
                data["price"],
                data["stock"],
                data["description"],
                data["import_price"],
                data["supplier_name"]
            )
            show_success(self.ui, "Thành công", "Đã thêm sản phẩm mới vào danh mục!")
            self.load_products()

    def update_product(self):
        row = self.ui.table.currentRow()
        if row < 0:
            show_warning(self.ui, "Chưa chọn", "Vui lòng click chọn một sản phẩm trong bảng để sửa đổi!")
            return

        prod_id = int(self.ui.table.item(row, 0).text())
        target_prod = next((p for p in self._all_products if p[0] == prod_id), None)
        if not target_prod:
            return

        dlg = ProductDialog(self.ui, product_data=target_prod)
        if dlg.exec_() == QDialog.Accepted:
            data = dlg.get_data()
            ProductService.update_product(
                prod_id,
                data["name"],
                data["category"],
                data["size"],
                data["color"],
                data["price"],
                data["stock"],
                data["description"],
                data["import_price"],
                data["supplier_name"]
            )
            show_success(self.ui, "Thành công", "Cập nhật thông tin sản phẩm thành công!")
            self.load_products()

    def delete_product(self):
        row = self.ui.table.currentRow()
        if row < 0:
            show_warning(self.ui, "Chưa chọn", "Vui lòng click chọn một sản phẩm trong bảng để xóa!")
            return

        prod_id = int(self.ui.table.item(row, 0).text())
        prod_name = self.ui.table.item(row, 1).text()

        if show_confirm(self.ui, "Xác nhận xóa", f"Bạn có chắc chắn muốn xóa vĩnh viễn sản phẩm '{prod_name}' khỏi hệ thống?"):
            ProductService.delete_product(prod_id)
            show_success(self.ui, "Thành công", f"Đã xóa sản phẩm '{prod_name}'.")
            self.load_products()