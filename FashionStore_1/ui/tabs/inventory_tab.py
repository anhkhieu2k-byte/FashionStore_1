"""
InventoryTab — UI module Quản lý kho
Thiết kế phẳng (Flat UI), form ẩn (stub) để không crash controller.
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from config import *
from ui.widgets import *

class InventoryTab(QWidget):

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {BG_MAIN};")
        self.setup_ui()

    def setup_ui(self):
        root = QVBoxLayout()
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(20)
        self.setLayout(root)

        # ── Tiêu đề & Thanh công cụ ────────────────────────
        hdr_row = QHBoxLayout()
        title = QLabel("📦   Quản lý Kho hàng")
        title.setStyleSheet(f"color:{TEXT_DARK}; font-size:20px; font-weight:800; font-family:'Nunito',sans-serif;")
        
        self.txt_search = search_bar("Tìm sản phẩm trong kho...")
        self.txt_search.setFixedWidth(280)
        
        self.btn_search = primary_btn("🔍", 40)
        self.btn_search.setFixedWidth(44)
        
        self.btn_add = primary_btn("＋ Nhập hàng", 42)
        self.btn_update = secondary_btn("✎ Sửa lô", 42)
        self.btn_delete = danger_btn("✕ Xóa lô", 42)

        hdr_row.addWidget(title)
        hdr_row.addStretch()
        hdr_row.addWidget(self.txt_search)
        hdr_row.addWidget(self.btn_search)
        hdr_row.addSpacing(10)
        hdr_row.addWidget(self.btn_add)
        hdr_row.addWidget(self.btn_update)
        hdr_row.addWidget(self.btn_delete)
        
        root.addLayout(hdr_row)

        # ── Bảng dữ liệu ──────────────────────────────────
        card = QFrame()
        card.setStyleSheet(f"background:{BG_CARD}; border:1px solid {BORDER}; border-radius:12px;")
        card_lay = QVBoxLayout(card)
        card_lay.setContentsMargins(20, 20, 20, 20)
        
        self.table = styled_table(["ID", "TÊN SẢN PHẨM", "SIZE", "MÀU SẮC", "SỐ LƯỢNG", "TỐI THIỂU", "NHÀ CUNG CẤP", "GIÁ NHẬP"])
        self.table.setColumnWidth(0, 60)
        self.table.setColumnWidth(1, 180)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 90)
        self.table.setColumnWidth(5, 90)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch) # Nhà cung cấp dãn rộng
        self.table.setColumnWidth(7, 110)
        
        card_lay.addWidget(self.table)
        root.addWidget(card)
