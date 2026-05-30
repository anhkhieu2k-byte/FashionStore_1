"""
InventoryDialog — Popup Thêm / Sửa Hàng Tồn Kho
Thiết kế phẳng, sang trọng, đầy đủ validate
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from config import *
from ui.widgets import primary_btn, secondary_btn

class InventoryDialog(QDialog):

    def __init__(self, parent=None, item_data=None):
        super().__init__(parent)
        self.item_data = item_data  # Tuples: (id, product_name, quantity, min_quantity, supplier_name, import_price)
        self.setWindowTitle("Thông tin Nhập kho" if item_data else "Nhập Lô Hàng Mới")
        self.setFixedSize(460, 500)
        self.setStyleSheet(f"""
            QDialog {{ background-color: {BG_CARD}; border-radius: 16px; }}
            QLineEdit, QSpinBox, QDoubleSpinBox {{
                background-color: {BG_INPUT}; border: 1.5px solid {BORDER};
                border-radius: 8px; padding: 8px; font-size: 14px; font-family: 'Nunito', sans-serif;
            }}
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
                border-color: {PRIMARY}; background-color: #fff;
            }}
            QLabel {{ font-weight: bold; color: {TEXT_DARK}; font-family: 'Nunito', sans-serif; }}
        """)
        self.setup_ui()
        if self.item_data:
            self.load_data()

    def setup_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 28, 28, 28)
        lay.setSpacing(16)

        # Tiêu đề
        lbl_title = QLabel("CẬP NHẬT LÔ HÀNG" if self.item_data else "NHẬP LÔ HÀNG MỚI")
        lbl_title.setStyleSheet(f"color: {PRIMARY_DARK}; font-size: 18px; font-weight: 900; border-bottom: 2px solid {PRIMARY_LIGHT}; padding-bottom: 8px;")
        lay.addWidget(lbl_title)

        form = QGridLayout()
        form.setSpacing(14)

        self.txt_product = QLineEdit()
        self.txt_product.setPlaceholderText("Tên mặt hàng nhập...")
        
        self.spn_qty = QSpinBox()
        self.spn_qty.setMaximum(999999); self.spn_qty.setValue(10)
        
        self.spn_min_qty = QSpinBox()
        self.spn_min_qty.setMaximum(999999); self.spn_min_qty.setValue(5)
        
        self.txt_supplier = QLineEdit()
        self.txt_supplier.setPlaceholderText("Tên nhà cung cấp / đối tác...")
        
        self.spn_price = QDoubleSpinBox()
        self.spn_price.setMaximum(9999999999); self.spn_price.setDecimals(0); self.spn_price.setSuffix(" ₫")
        self.spn_price.setValue(100000)

        def lbl(t): return QLabel(t)
        
        form.addWidget(lbl("Tên sản phẩm:"), 0, 0); form.addWidget(self.txt_product, 0, 1)
        form.addWidget(lbl("Số lượng nhập:"), 1, 0); form.addWidget(self.spn_qty, 1, 1)
        form.addWidget(lbl("SL cảnh báo tối thiểu:"), 2, 0); form.addWidget(self.spn_min_qty, 2, 1)
        form.addWidget(lbl("Nhà cung cấp:"), 3, 0); form.addWidget(self.txt_supplier, 3, 1)
        form.addWidget(lbl("Giá nhập (VNĐ):"), 4, 0); form.addWidget(self.spn_price, 4, 1)
        
        lay.addLayout(form)
        lay.addStretch()

        # Nút bấm
        btn_box = QHBoxLayout()
        self.btn_save = primary_btn("Lưu lô hàng", 42)
        self.btn_cancel = secondary_btn("Hủy bỏ", 42)
        
        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        
        btn_box.addStretch()
        btn_box.addWidget(self.btn_cancel)
        btn_box.addWidget(self.btn_save)
        lay.addLayout(btn_box)

    def load_data(self):
        # item_data = (id, product_name, quantity, min_quantity, supplier_name, import_price)
        self.txt_product.setText(str(self.item_data[1]))
        self.spn_qty.setValue(int(self.item_data[2]))
        self.spn_min_qty.setValue(int(self.item_data[3]))
        self.txt_supplier.setText(str(self.item_data[4] or ""))
        self.spn_price.setValue(float(self.item_data[5]))

    def get_data(self):
        return {
            "product_name": self.txt_product.text().strip(),
            "quantity": self.spn_qty.value(),
            "min_quantity": self.spn_min_qty.value(),
            "supplier_name": self.txt_supplier.text().strip(),
            "import_price": self.spn_price.value()
        }
