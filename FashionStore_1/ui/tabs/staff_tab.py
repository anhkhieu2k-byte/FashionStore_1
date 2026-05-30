from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from config import *
from ui.widgets import *


class StaffTab(QWidget):

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
        
        self.txt_search = search_bar("Tìm nhân viên theo tên...")
        self.txt_search.setMinimumWidth(300)
        toolbar.addWidget(self.txt_search, 1)  # Chiếm không gian còn lại
        
        self.btn_add = primary_btn("＋ Thêm", 42)
        self.btn_update = secondary_btn("✎ Cập nhật", 42)
        self.btn_delete = danger_btn("✕ Xóa", 42)
        
        # Thêm các nút chức năng mới
        self.btn_attendance = success_btn("🕒 Vào ca", 42)
        self.btn_end_shift = primary_btn("🏁 Kết thúc ca", 42)
        self.btn_end_shift.setStyleSheet(self.btn_end_shift.styleSheet().replace(PRIMARY, "#f59e0b")) # Màu cam Warning
        self.btn_history = primary_btn("📜 Lịch sử", 42)
        self.btn_history.setStyleSheet(self.btn_history.styleSheet().replace(PRIMARY, "#475569")) # Màu Slate 600
        self.btn_payroll = primary_btn("💰 Tính lương", 42)
        self.btn_payroll.setStyleSheet(self.btn_payroll.styleSheet().replace(PRIMARY, "#6366f1")) # Màu Indigo cho khác biệt
        
        self.btn_export_payroll = success_btn("📥 Xuất Excel", 42)
        self.btn_export_payroll.setFixedWidth(140)

        toolbar.addWidget(self.btn_add)
        toolbar.addWidget(self.btn_update)
        toolbar.addWidget(self.btn_delete)
        toolbar.addSpacing(20) # Tạo khoảng cách
        toolbar.addWidget(self.btn_attendance)
        toolbar.addWidget(self.btn_end_shift)
        toolbar.addWidget(self.btn_history)
        toolbar.addWidget(self.btn_payroll)
        toolbar.addWidget(self.btn_export_payroll)
        
        root.addLayout(toolbar)

        # ─── Vùng hiển thị Bảng ───────────────────────────────────────────
        card = QFrame()
        card.setStyleSheet(f"background:{BG_CARD}; border-radius: 12px; border: 1px solid {BORDER};")
        card_lay = QVBoxLayout(card)
        card_lay.setContentsMargins(16, 16, 16, 16)
        card_lay.setSpacing(0)

        self.table = styled_table(["MÃ NV", "HỌ TÊN", "NGÀY SINH", "ĐIỆN THOẠI", "ĐỊA CHỈ", "CHỨC VỤ", "CA LÀM", "LƯƠNG", "NGÀY CÔNG"])
        self.table.setColumnWidth(0, 70)
        self.table.setColumnWidth(1, 180)
        self.table.setColumnWidth(2, 110)
        self.table.setColumnWidth(3, 120)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)  # Địa chỉ co giãn
        self.table.setColumnWidth(5, 110)
        self.table.setColumnWidth(6, 90)
        self.table.setColumnWidth(7, 120)
        self.table.setColumnWidth(8, 100)
        
        card_lay.addWidget(self.table)
        root.addWidget(card)

        # Gỡ các input ảo thừa, giữ lại btn_search ảo nếu code cũ kết nối
        self.btn_search = QPushButton()
        self.btn_search.hide()
