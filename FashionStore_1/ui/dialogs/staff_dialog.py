"""
StaffDialog — Cửa sổ nổi (Popup) Thêm / Sửa Nhân viên
Thiết kế phẳng (Sky Blue), bo góc 16px sang trọng
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from config import *
from ui.widgets import primary_btn, secondary_btn


class StaffDialog(QDialog):

    def __init__(self, parent=None, staff_data=None):
        super().__init__(parent)
        self.staff_data = staff_data  # Tuples: (id, full_name, birth_date, phone, address, role, shift, salary, attendance_days)
        self.setWindowTitle("Thông tin Nhân viên" if staff_data else "Thêm Nhân viên Mới")
        self.setFixedSize(480, 660)
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
        if self.staff_data:
            self.load_data()

    def setup_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 28, 28, 28)
        lay.setSpacing(16)

        # Tiêu đề
        lbl_title = QLabel("CẬP NHẬT NHÂN VIÊN" if self.staff_data else "THÊM NHÂN VIÊN MỚI")
        lbl_title.setStyleSheet(f"color: {PRIMARY_DARK}; font-size: 18px; font-weight: 900; border-bottom: 2px solid {PRIMARY_LIGHT}; padding-bottom: 8px;")
        lay.addWidget(lbl_title)

        form = QGridLayout()
        form.setSpacing(14)

        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("Ví dụ: Đinh Thị Mai...")
        
        self.txt_birth = QLineEdit()
        self.txt_birth.setPlaceholderText("Ví dụ: 1995-03-15...")
        
        self.txt_phone = QLineEdit()
        self.txt_phone.setPlaceholderText("Ví dụ: 0945678901...")
        
        self.txt_address = QLineEdit()
        self.txt_address.setPlaceholderText("Ví dụ: Hà Nội...")
        
        self.cb_role = QComboBox()
        self.cb_role.addItems(["Nhân viên", "Quản lý", "Thu ngân", "Kho"])
        
        self.cb_shift = QComboBox()
        self.cb_shift.addItems(["Sáng", "Chiều", "Tối", "Cả ngày"])
        
        self.spn_salary = QSpinBox()
        self.spn_salary.setMaximum(999999999)
        self.spn_salary.setSingleStep(5000)
        self.spn_salary.setSuffix(" ₫")
        self.spn_salary.setValue(25000)
        
        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Mật khẩu vào/ra ca (mặc định: 123456)")
        
        self.spn_attendance = QSpinBox()
        self.spn_attendance.setMaximum(31)
        self.spn_attendance.setValue(0)

        def lbl(t): return QLabel(t)
        
        form.addWidget(lbl("Họ và tên:"), 0, 0)
        form.addWidget(self.txt_name, 0, 1)
        
        form.addWidget(lbl("Ngày sinh:"), 1, 0)
        form.addWidget(self.txt_birth, 1, 1)
        
        form.addWidget(lbl("Số điện thoại:"), 2, 0)
        form.addWidget(self.txt_phone, 2, 1)
        
        form.addWidget(lbl("Địa chỉ:"), 3, 0)
        form.addWidget(self.txt_address, 3, 1)
        
        form.addWidget(lbl("Chức vụ:"), 4, 0)
        form.addWidget(self.cb_role, 4, 1)
        
        form.addWidget(lbl("Ca làm việc:"), 5, 0)
        form.addWidget(self.cb_shift, 5, 1)
        
        form.addWidget(lbl("Mức lương:"), 6, 0)
        form.addWidget(self.spn_salary, 6, 1)
        
        self.lbl_salary_note = QLabel("(* > 100k là lương cố định, dưới 100k là lương/giờ)")
        self.lbl_salary_note.setStyleSheet("font-size: 11px; font-weight: normal; color: #64748b; font-style: italic; padding: 0;")
        form.addWidget(self.lbl_salary_note, 7, 1)
        
        form.addWidget(lbl("Mật khẩu:"), 8, 0)
        form.addWidget(self.txt_password, 8, 1)
        
        form.addWidget(lbl("Số ngày công:"), 9, 0)
        form.addWidget(self.spn_attendance, 9, 1)
        
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
        # staff_data = (id, full_name, birth_date, phone, address, role, shift, salary, attendance_days, check_in_time, total_hours, password)
        self.txt_name.setText(str(self.staff_data[1] if self.staff_data[1] is not None else ""))
        self.txt_birth.setText(str(self.staff_data[2] if self.staff_data[2] is not None else ""))
        self.txt_phone.setText(str(self.staff_data[3] if self.staff_data[3] is not None else ""))
        self.txt_address.setText(str(self.staff_data[4] if self.staff_data[4] is not None else ""))
        self.cb_role.setCurrentText(str(self.staff_data[5] if self.staff_data[5] is not None else ""))
        self.cb_shift.setCurrentText(str(self.staff_data[6] if self.staff_data[6] is not None else ""))
        self.spn_salary.setValue(int(float(self.staff_data[7])) if self.staff_data[7] is not None else 0)
        self.txt_password.setText(str(self.staff_data[11] if len(self.staff_data) > 11 and self.staff_data[11] is not None else "123456"))
        self.spn_attendance.setValue(int(self.staff_data[8]) if self.staff_data[8] is not None else 0)

    def get_data(self):
        return {
            "full_name": self.txt_name.text().strip(),
            "birth_date": self.txt_birth.text().strip(),
            "phone": self.txt_phone.text().strip(),
            "address": self.txt_address.text().strip(),
            "role": self.cb_role.currentText(),
            "shift": self.cb_shift.currentText(),
            "salary": float(self.spn_salary.value()),
            "password": self.txt_password.text().strip() or "123456",
            "attendance_days": int(self.spn_attendance.value())
        }
