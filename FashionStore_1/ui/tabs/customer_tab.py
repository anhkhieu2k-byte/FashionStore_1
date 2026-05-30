from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from config import *
from ui.widgets import *


class CustomerTab(QWidget):

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
        
        self.txt_search = search_bar("Tìm theo tên, SĐT...")
        self.txt_search.setMinimumWidth(300)
        toolbar.addWidget(self.txt_search, 1)
        
        self.btn_add = primary_btn("＋ Thêm", 42)
        self.btn_update = secondary_btn("✎ Cập nhật", 42)
        self.btn_delete = danger_btn("✕ Xóa", 42)
        
        toolbar.addWidget(self.btn_add)
        toolbar.addWidget(self.btn_update)
        toolbar.addWidget(self.btn_delete)
        
        root.addLayout(toolbar)

        # ─── Split Layout (Table bên trái, Chi tiết bên phải) ───────
        main_content = QHBoxLayout()
        main_content.setSpacing(16)
        
        # 📄 Bên trái: Danh sách Khách hàng
        left_card = QFrame()
        left_card.setStyleSheet(f"background:{BG_CARD}; border-radius: 12px; border: 1px solid {BORDER};")
        left_lay = QVBoxLayout(left_card)
        left_lay.setContentsMargins(16, 16, 16, 16)
        left_lay.setSpacing(0)

        self.table = styled_table(["MÃ KH", "HỌ TÊN", "ĐIỆN THOẠI", "EMAIL", "ĐIỂM TÍCH LŨY", "HẠNG THÀNH VIÊN"])
        self.table.setColumnWidth(0, 70)
        self.table.setColumnWidth(1, 160)
        self.table.setColumnWidth(2, 110)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch) # Email co giãn
        self.table.setColumnWidth(4, 110)
        self.table.setColumnWidth(5, 120)
        
        left_lay.addWidget(self.table)
        main_content.addWidget(left_card, 3) # chiếm tỉ lệ 3 phần

        # 🔍 Bên phải: Chi tiết Khách hàng
        self.right_card = QFrame()
        self.right_card.setStyleSheet(f"background:{BG_CARD}; border-radius: 12px; border: 1px solid {BORDER};")
        self.right_lay = QVBoxLayout(self.right_card)
        self.right_lay.setContentsMargins(20, 20, 20, 20)
        self.right_lay.setSpacing(16)
        
        # Placeholder khi chưa chọn khách hàng
        self.lbl_placeholder = QLabel("🔍 Chọn một khách hàng trong danh sách\nđể xem chi tiết lịch sử đơn mua")
        self.lbl_placeholder.setAlignment(Qt.AlignCenter)
        self.lbl_placeholder.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {TEXT_LIGHT}; line-height: 1.5;")
        self.right_lay.addWidget(self.lbl_placeholder, 1)
        
        # Widget chứa nội dung chi tiết (ẩn mặc định)
        self.detail_widget = QWidget()
        detail_lay = QVBoxLayout(self.detail_widget)
        detail_lay.setContentsMargins(0, 0, 0, 0)
        detail_lay.setSpacing(14)
        
        # Tiêu đề chi tiết
        self.lbl_detail_title = QLabel("CHI TIẾT KHÁCH HÀNG")
        self.lbl_detail_title.setStyleSheet(f"color: {PRIMARY_DARK}; font-size: 16px; font-weight: bold; border-bottom: 2px solid {PRIMARY_LIGHT}; padding-bottom: 8px;")
        detail_lay.addWidget(self.lbl_detail_title)
        
        # Grid Thông tin cơ bản
        info_grid = QGridLayout()
        info_grid.setSpacing(8)
        
        def create_info_lbl(t, val=False):
            l = QLabel(t)
            l.setStyleSheet(f"font-weight: {'bold' if not val else 'normal'}; color: {TEXT_DARK if not val else '#333'}; font-size: 13px;")
            return l

        self.val_name = create_info_lbl("", val=True)
        self.val_phone = create_info_lbl("", val=True)
        self.val_email = create_info_lbl("", val=True)
        self.val_rank = create_info_lbl("", val=True)
        self.val_points = create_info_lbl("", val=True)
        
        info_grid.addWidget(create_info_lbl("Họ tên:"), 0, 0); info_grid.addWidget(self.val_name, 0, 1)
        info_grid.addWidget(create_info_lbl("Điện thoại:"), 1, 0); info_grid.addWidget(self.val_phone, 1, 1)
        info_grid.addWidget(create_info_lbl("Email:"), 2, 0); info_grid.addWidget(self.val_email, 2, 1)
        info_grid.addWidget(create_info_lbl("Hạng / Điểm:"), 3, 0)
        
        # Hạng và điểm nằm trên cùng một hàng
        rank_points_lay = QHBoxLayout()
        rank_points_lay.setSpacing(8)
        rank_points_lay.addWidget(self.val_rank)
        rank_points_lay.addWidget(self.val_points)
        rank_points_lay.addStretch()
        info_grid.addLayout(rank_points_lay, 3, 1)
        
        detail_lay.addLayout(info_grid)
        
        # KPI Card: Tổng chi tiêu
        self.spent_card = QFrame()
        self.spent_card.setStyleSheet(f"background-color: #ffffff; border: 1.5px dashed {PRIMARY}; border-radius: 10px;")
        spent_lay = QVBoxLayout(self.spent_card)
        spent_lay.setContentsMargins(12, 12, 12, 12)
        spent_lay.setSpacing(4)
        
        lbl_spent_title = QLabel("TỔNG SỐ TIỀN ĐÃ MUA HÀNG")
        lbl_spent_title.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {TEXT_LIGHT}; letter-spacing: 0.5px;")
        lbl_spent_title.setAlignment(Qt.AlignCenter)
        
        self.lbl_spent_val = QLabel("0 ₫")
        self.lbl_spent_val.setStyleSheet(f"font-size: 20px; font-weight: 900; color: {PRIMARY_DARK};")
        self.lbl_spent_val.setAlignment(Qt.AlignCenter)
        
        spent_lay.addWidget(lbl_spent_title)
        spent_lay.addWidget(self.lbl_spent_val)
        detail_lay.addWidget(self.spent_card)
        
        # Tiêu đề Lịch sử mua hàng
        lbl_history_title = QLabel("⌛ Lịch sử đơn mua hàng")
        lbl_history_title.setStyleSheet(f"font-size: 13px; font-weight: bold; color: {TEXT_DARK}; margin-top: 8px;")
        detail_lay.addWidget(lbl_history_title)
        
        # Bảng Lịch sử mua hàng
        self.table_history = styled_table(["MÃ HĐ", "NGÀY MUA", "HÌNH THỨC", "TỔNG TIỀN"])
        self.table_history.setColumnWidth(0, 60)
        self.table_history.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch) # Ngày mua co giãn
        self.table_history.setColumnWidth(2, 90)
        self.table_history.setColumnWidth(3, 100)
        self.table_history.setFixedHeight(180) # Hạn chế chiều cao bảng lịch sử để cân đối
        detail_lay.addWidget(self.table_history)
        
        self.right_lay.addWidget(self.detail_widget)
        self.detail_widget.hide() # Ẩn mặc định khi chưa chọn
        
        main_content.addWidget(self.right_card, 2) # chiếm tỉ lệ 2 phần
        root.addLayout(main_content)
        
        # Gỡ các input ảo thừa
        self.btn_search = QPushButton(); self.btn_search.hide()
