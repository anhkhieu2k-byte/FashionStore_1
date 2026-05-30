"""
ProductDialog — Cửa sổ nổi (Popup) Thêm / Sửa Sản phẩm
Thiết kế phẳng (Sky Blue), hỗ trợ mặc định size "S, M, L, XL, XXL"
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QEvent
from config import *
from ui.widgets import primary_btn, secondary_btn

class ProductDialog(QDialog):

    def __init__(self, parent=None, product_data=None):
        super().__init__(parent)
        self.product_data = product_data # (id, name, cat, size, color, price, stock, desc, import_price)
        self.setWindowTitle("Thông tin Sản phẩm" if product_data else "Thêm Sản phẩm Mới")
        self.setFixedSize(500, 720)
        self.setStyleSheet(f"""
            QDialog {{ background-color: {BG_CARD}; border-radius: 16px; }}
            QLineEdit, QTextEdit, QComboBox, QSpinBox {{
                background-color: {BG_INPUT}; border: 1.5px solid {BORDER};
                border-radius: 8px; padding: 8px; font-size: 14px; font-family: 'Nunito', sans-serif;
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {{
                border-color: {PRIMARY}; background-color: #fff;
            }}
            QLabel {{ font-weight: bold; color: {TEXT_DARK}; font-family: 'Nunito', sans-serif; }}
        """)
        self.setup_ui()
        if self.product_data:
            self.load_data()

    def setup_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 28, 28, 28)
        lay.setSpacing(16)

        # Tiêu đề
        lbl_title = QLabel("CẬP NHẬT SẢN PHẨM" if self.product_data else "THÊM SẢN PHẨM MỚI")
        lbl_title.setStyleSheet(f"color: {PRIMARY_DARK}; font-size: 18px; font-weight: 900; border-bottom: 2px solid {PRIMARY_LIGHT}; padding-bottom: 8px;")
        lay.addWidget(lbl_title)

        form = QGridLayout()
        form.setSpacing(12)

        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("Ví dụ: Áo thun cổ tròn cao cấp...")
        
        self.cb_category = QComboBox()
        self.cb_category.addItems(["Áo", "Quần", "Váy", "Áo khoác", "Giày", "Phụ kiện"])
        
        self.txt_size = QLineEdit()
        self.txt_size.setText("S, M, L, XL, XXL")
        
        self.txt_color = QLineEdit()
        self.txt_color.setPlaceholderText("Ví dụ: Đen, Trắng, Đỏ, Xanh rêu (ngăn cách bằng dấu phẩy)...")

        self.spn_import_price = QSpinBox()
        self.spn_import_price.setMaximum(999999999); self.spn_import_price.setSingleStep(10000)
        self.spn_import_price.setSuffix(" ₫")
        
        self.spn_price = QSpinBox()
        self.spn_price.setMaximum(999999999); self.spn_price.setSingleStep(10000)
        self.spn_price.setSuffix(" ₫")
        
        self.spn_stock = QSpinBox()
        self.spn_stock.setMaximum(99999); self.spn_stock.setValue(10)
 
        self.cb_supplier = QComboBox()
        self.cb_supplier.setEditable(True)
        self.load_suppliers_into_combo()
        self.cb_supplier.installEventFilter(self)
        self.cb_supplier.lineEdit().installEventFilter(self)
 
        self.txt_desc = QTextEdit()
        self.txt_desc.setFixedHeight(80)
        self.txt_desc.setPlaceholderText("Mô tả chi tiết chất liệu, kiểu dáng...")
 
        def lbl(t): return QLabel(t)
        
        form.addWidget(lbl("Tên sản phẩm:"), 0, 0); form.addWidget(self.txt_name, 0, 1)
        form.addWidget(lbl("Danh mục:"), 1, 0); form.addWidget(self.cb_category, 1, 1)
        form.addWidget(lbl("Kích cỡ (ngăn cách bằng dấu phẩy):"), 2, 0); form.addWidget(self.txt_size, 2, 1)
        form.addWidget(lbl("Màu sắc (ngăn cách bằng dấu phẩy):"), 3, 0); form.addWidget(self.txt_color, 3, 1)
        form.addWidget(lbl("Giá nhập (Vốn):"), 4, 0); form.addWidget(self.spn_import_price, 4, 1)
        form.addWidget(lbl("Giá bán:"), 5, 0); form.addWidget(self.spn_price, 5, 1)
        form.addWidget(lbl("Tồn kho ban đầu:"), 6, 0); form.addWidget(self.spn_stock, 6, 1)
        form.addWidget(lbl("Nhà cung cấp:"), 7, 0); form.addWidget(self.cb_supplier, 7, 1)
        form.addWidget(lbl("Mô tả:"), 8, 0); form.addWidget(self.txt_desc, 8, 1)
        
        lay.addLayout(form)
        lay.addStretch()

        # Nút bấm
        btn_box = QHBoxLayout()
        self.btn_save = primary_btn("Lưu thông tin", 42)
        self.btn_cancel = secondary_btn("Hủy bỏ", 42)
        
        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        
        btn_box.addStretch()
        btn_box.addWidget(self.btn_cancel)
        btn_box.addWidget(self.btn_save)
        lay.addLayout(btn_box)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                self.cb_supplier.showPopup()
        return super().eventFilter(watched, event)

    def load_suppliers_into_combo(self):
        try:
            from models.supplier import Supplier
            suppliers_data = Supplier.get_all()
            self.cb_supplier.clear()
            for s in suppliers_data:
                # s = (id, name, phone, address)
                self.cb_supplier.addItem(s[1], s[1])
            self.cb_supplier.lineEdit().setPlaceholderText("-- Chọn hoặc tự nhập nhà cung cấp --")
            self.cb_supplier.setCurrentIndex(-1)
        except Exception as e:
            print("Error loading suppliers:", e)

    def load_data(self):
        # self.product_data = (id, name, cat, size, color, price, stock, desc, import_price, supplier_name)
        self.txt_name.setText(str(self.product_data[1]))
        self.cb_category.setCurrentText(str(self.product_data[2]))
        self.txt_size.setText(str(self.product_data[3]))
        self.txt_color.setText(str(self.product_data[4]))
        self.spn_price.setValue(int(self.product_data[5]))
        self.spn_stock.setValue(int(self.product_data[6]))
        self.txt_desc.setText(str(self.product_data[7] or ""))
        if len(self.product_data) > 8:
            self.spn_import_price.setValue(int(self.product_data[8] or 0))
        if len(self.product_data) > 9:
            supp = str(self.product_data[9] or "").strip()
            if supp:
                self.cb_supplier.setCurrentText(supp)
            else:
                self.cb_supplier.setCurrentIndex(-1)

    def get_data(self):
        return {
            "name": self.txt_name.text().strip(),
            "category": self.cb_category.currentText(),
            "size": self.txt_size.text().strip(),
            "color": self.txt_color.text().strip(),
            "import_price": self.spn_import_price.value(),
            "price": self.spn_price.value(),
            "stock": self.spn_stock.value(),
            "supplier_name": self.cb_supplier.currentText().strip(),
            "description": self.txt_desc.toPlainText().strip()
        }
