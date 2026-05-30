from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from config import *
from ui.widgets import *


class ProductTab(QWidget):

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {BG_MAIN};")
        self.setup_ui()

    def setup_ui(self):
        root = QVBoxLayout()
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(20)
        self.setLayout(root)

        # ─── Thanh công cụ ─────────────────────────────────────────
        toolbar = QHBoxLayout()
        toolbar.setSpacing(12)
        
        self.txt_search = search_bar("Tìm sản phẩm...")
        self.txt_search.setMinimumWidth(220)
        toolbar.addWidget(self.txt_search, 1)

        self.cb_filter_category = QComboBox()
        self.cb_filter_category.setFixedHeight(40)
        self.cb_filter_category.setMinimumWidth(160)
        self.cb_filter_category.setStyleSheet(f"background:{BG_INPUT}; border:1px solid {BORDER}; border-radius:8px; padding:0 12px; font-size:14px; font-weight:bold; font-family:'Nunito',sans-serif;")
        toolbar.addWidget(self.cb_filter_category)
        
        self.btn_add = primary_btn("＋ Thêm", 40)
        self.btn_update = secondary_btn("✎ Cập nhật", 40)
        self.btn_delete = danger_btn("✕ Xóa", 40)
        
        toolbar.addWidget(self.btn_add)
        toolbar.addWidget(self.btn_update)
        toolbar.addWidget(self.btn_delete)
        
        root.addLayout(toolbar)

        # ─── Vùng Bảng ──────────────────────────────────────────────
        card = QFrame()
        card.setStyleSheet(f"background:{BG_CARD}; border-radius: 12px; border: 1px solid {BORDER};")
        card_lay = QVBoxLayout(card)
        card_lay.setContentsMargins(16, 16, 16, 16)
        card_lay.setSpacing(0)

        self.table = styled_table(["MÃ SP", "TÊN SẢN PHẨM", "DANH MỤC", "SIZE", "MÀU SẮC", "GIÁ NHẬP", "GIÁ BÁN", "TỒN KHO", "NHÀ CUNG CẤP", "MÔ TẢ"])
        self.table.setColumnWidth(0, 60)
        self.table.setColumnWidth(1, 180)
        self.table.setColumnWidth(2, 90)
        self.table.setColumnWidth(3, 80) # Size
        self.table.setColumnWidth(4, 90)
        self.table.setColumnWidth(5, 110) # Giá nhập
        self.table.setColumnWidth(6, 110) # Giá bán
        self.table.setColumnWidth(7, 80)  # Tồn kho
        self.table.setColumnWidth(8, 140) # Nhà cung cấp
        self.table.horizontalHeader().setSectionResizeMode(9, QHeaderView.Stretch) # Mô tả dãn rộng
        
        card_lay.addWidget(self.table)
        root.addWidget(card)
