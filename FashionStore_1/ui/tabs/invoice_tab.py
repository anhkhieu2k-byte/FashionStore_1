"""
InvoiceTab — UI module Quản lý Hóa đơn / Lịch sử đơn hàng
Thiết kế phẳng (Flat UI).
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from config import *
from ui.widgets import *

class InvoiceTab(QWidget):

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
        title = QLabel("📋   Lịch sử Hóa đơn")
        title.setStyleSheet(f"color:{TEXT_DARK}; font-size:20px; font-weight:800; font-family:'Nunito',sans-serif;")
        
        self.txt_search = search_bar("Tìm mã HĐ, tên KH...")
        self.txt_search.setFixedWidth(280)
        
        self.btn_search = primary_btn("🔍", 40)
        self.btn_search.setFixedWidth(44)
        
        self.btn_export = success_btn("📥 Xuất Excel", 40)
        self.btn_export.setFixedWidth(130)
        
        self.btn_refresh = secondary_btn("🔄 Cập nhật", 40)
        self.btn_refresh.setFixedWidth(120)

        hdr_row.addWidget(title)
        hdr_row.addStretch()
        hdr_row.addWidget(self.txt_search)
        hdr_row.addWidget(self.btn_search)
        hdr_row.addSpacing(10)
        hdr_row.addWidget(self.btn_refresh)
        hdr_row.addSpacing(5)
        hdr_row.addWidget(self.btn_export)
        
        root.addLayout(hdr_row)

        # ── Bảng dữ liệu ──────────────────────────────────
        card = QFrame()
        card.setStyleSheet(f"background:{BG_CARD}; border:1px solid {BORDER}; border-radius:12px;")
        card_lay = QVBoxLayout(card)
        card_lay.setContentsMargins(20, 20, 20, 20)
        
        self.table = styled_table(["MÃ HĐ", "KHÁCH HÀNG", "TỔNG TIỀN", "PHƯƠNG THỨC TT", "THỜI GIAN TẠO", "TRẠNG THÁI", "THAO TÁC"])
        self.table.setColumnWidth(0, 80)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch) # Khách hàng co giãn
        self.table.setColumnWidth(2, 120)
        self.table.setColumnWidth(3, 140)
        self.table.setColumnWidth(4, 180) # Thời gian tạo
        self.table.setColumnWidth(5, 130) # Trạng thái
        self.table.setColumnWidth(6, 120) # Thao tác
        
        card_lay.addWidget(self.table)
        root.addWidget(card)
