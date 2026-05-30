from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from config import *
from ui.widgets import *


class PromotionTab(QWidget):

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {BG_MAIN};")
        self.setup_ui()

    def setup_ui(self):
        root = QVBoxLayout()
        root.setContentsMargins(26, 22, 26, 22)
        root.setSpacing(16)
        self.setLayout(root)

        root.addWidget(page_title("◆   Quản lý Khuyến mãi"))

        card = form_card()
        card_lay = QVBoxLayout()
        card_lay.setContentsMargins(20, 16, 20, 16)
        card_lay.setSpacing(14)

        sr = QHBoxLayout(); sr.setSpacing(10)
        self.txt_search = search_bar("Tìm mã voucher...")
        self.btn_search = primary_btn("  Tìm kiếm", 40)
        self.btn_search.setFixedWidth(120)
        sr.addWidget(self.txt_search); sr.addWidget(self.btn_search)
        card_lay.addLayout(sr)
        card_lay.addWidget(divider())
        card_lay.addWidget(section_label("THÔNG TIN KHUYẾN MÃI"))

        grid = QGridLayout(); grid.setSpacing(12); grid.setContentsMargins(0, 4, 0, 0)

        self.txt_code      = field_input("Mã voucher  (vd: SUMMER20)")
        self.txt_discount  = field_input("% Giảm giá  (vd: 20)")
        self.txt_min_order = field_input("Giá trị đơn tối thiểu (VNĐ)")
        self.txt_start     = field_input("Ngày bắt đầu  (DD-MM-YYYY)")
        self.txt_end       = field_input("Ngày kết thúc  (DD-MM-YYYY)")
        self.txt_quantity  = field_input("Số lượng mã (Số lần dùng)")

        def lbl(t): return section_label(t)

        grid.addWidget(lbl("Mã voucher"),       0, 0); grid.addWidget(self.txt_code,      0, 1)
        grid.addWidget(lbl("% Giảm giá"),       0, 2); grid.addWidget(self.txt_discount,  0, 3)
        grid.addWidget(lbl("Đơn tối thiểu"),    1, 0); grid.addWidget(self.txt_min_order, 1, 1)
        grid.addWidget(lbl("Ngày bắt đầu"),     1, 2); grid.addWidget(self.txt_start,     1, 3)
        grid.addWidget(lbl("Ngày kết thúc"),    2, 0); grid.addWidget(self.txt_end,       2, 1)
        grid.addWidget(lbl("Số lượng mã"),      2, 2); grid.addWidget(self.txt_quantity,  2, 3)
        card_lay.addLayout(grid)
        card_lay.addWidget(divider())

        btn_row = QHBoxLayout(); btn_row.setSpacing(10)
        self.btn_add    = primary_btn("＋  Thêm mới")
        self.btn_update = secondary_btn("✎  Cập nhật")
        self.btn_delete = danger_btn("✕  Xóa")
        btn_row.addWidget(self.btn_add); btn_row.addWidget(self.btn_update)
        btn_row.addWidget(self.btn_delete); btn_row.addStretch()
        card_lay.addLayout(btn_row)

        card.setLayout(card_lay)
        root.addWidget(card)

        self.table = styled_table(["ID", "Mã Voucher", "% Giảm", "Đơn tối thiểu", "Bắt đầu", "Kết thúc", "Giới hạn", "Đã dùng", "Còn lại"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setColumnWidth(0, 48)
        self.table.setColumnWidth(6, 80)
        self.table.setColumnWidth(7, 80)
        self.table.setColumnWidth(8, 120)
        root.addWidget(self.table)
