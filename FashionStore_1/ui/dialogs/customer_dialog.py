"""
CustomerDialog — Cửa sổ nổi (Popup) Thêm / Sửa Khách hàng
Thiết kế phẳng (Sky Blue), bo góc 16px sang trọng
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from config import *
from ui.widgets import primary_btn, secondary_btn

class CustomerDialog(QDialog):

    def __init__(self, parent=None, customer_data=None):
        super().__init__(parent)
        self.customer_data = customer_data # Tuples: (id, name, phone, email, points, rank)
        self.setWindowTitle("Thông tin Khách hàng" if customer_data else "Thêm Khách hàng Mới")
        self.setFixedSize(450, 480)
        self.setStyleSheet(f"""
            QDialog {{ background-color: {BG_CARD}; border-radius: 16px; }}
            QLineEdit, QComboBox, QSpinBox {{
                background-color: {BG_INPUT}; border: 1.5px solid {BORDER};
                border-radius: 8px; padding: 8px; font-size: 14px; font-family: 'Nunito', sans-serif;
            }}
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{
                border-color: {PRIMARY}; background-color: #fff;
            }}
            QLabel {{ font-weight: bold; color: {TEXT_DARK}; font-family: 'Nunito', sans-serif; }}
        """)
        self.setup_ui()
        if self.customer_data:
            self.load_data()

    def setup_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 28, 28, 28)
        lay.setSpacing(16)

        # Tiêu đề
        lbl_title = QLabel("CẬP NHẬT KHÁCH HÀNG" if self.customer_data else "THÊM KHÁCH HÀNG MỚI")
        lbl_title.setStyleSheet(f"color: {PRIMARY_DARK}; font-size: 18px; font-weight: 900; border-bottom: 2px solid {PRIMARY_LIGHT}; padding-bottom: 8px;")
        lay.addWidget(lbl_title)

        form = QGridLayout()
        form.setSpacing(14)

        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("Ví dụ: Nguyễn Văn A...")
        
        self.txt_phone = QLineEdit()
        self.txt_phone.setPlaceholderText("Ví dụ: 0912345678...")
        
        self.txt_email = QLineEdit()
        self.txt_email.setPlaceholderText("Ví dụ: email@domain.com...")
        
        self.spn_points = QSpinBox()
        self.spn_points.setMaximum(999999); self.spn_points.setValue(0)
        
        self.cb_rank = QComboBox()
        self.cb_rank.addItems(["Thành viên", "Bạc", "Vàng", "Kim Cương"])

        def lbl(t): return QLabel(t)
        
        form.addWidget(lbl("Họ và tên:"), 0, 0); form.addWidget(self.txt_name, 0, 1)
        form.addWidget(lbl("Số điện thoại:"), 1, 0); form.addWidget(self.txt_phone, 1, 1)
        form.addWidget(lbl("Email:"), 2, 0); form.addWidget(self.txt_email, 2, 1)
        form.addWidget(lbl("Điểm tích lũy:"), 3, 0); form.addWidget(self.spn_points, 3, 1)
        form.addWidget(lbl("Hạng thành viên:"), 4, 0); form.addWidget(self.cb_rank, 4, 1)
        
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

    def load_data(self):
        # customer_data = (id, name, phone, email, points, rank)
        self.txt_name.setText(str(self.customer_data[1]))
        self.txt_phone.setText(str(self.customer_data[2]))
        self.txt_email.setText(str(self.customer_data[3] or ""))
        self.spn_points.setValue(int(self.customer_data[4]))
        self.cb_rank.setCurrentText(str(self.customer_data[5]))

    def get_data(self):
        return {
            "name": self.txt_name.text().strip(),
            "phone": self.txt_phone.text().strip(),
            "email": self.txt_email.text().strip(),
            "points": self.spn_points.value(),
            "rank": self.cb_rank.currentText()
        }
