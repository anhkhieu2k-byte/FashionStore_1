from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from utils.settings import load_login


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Fashion Store — Đăng nhập")
        self.resize(980, 620)
        self.setMinimumSize(800, 520)
        self.setStyleSheet(
            "QWidget { background-color: #f0f7fc; "
            "font-family: 'Nunito', 'Segoe UI', sans-serif; }"
        )

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        # ── LEFT PANEL (brand) ───────────────────────────────────
        left = QFrame()
        left.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 #0f3d5c, stop:0.5 #14527a, stop:1 #0a2d44);
            }
        """)
        ll = QVBoxLayout()
        ll.setAlignment(Qt.AlignCenter)
        ll.setSpacing(14)
        ll.setContentsMargins(50, 60, 50, 60)
        left.setLayout(ll)

        logo_icon = QLabel("✿")
        logo_icon.setAlignment(Qt.AlignCenter)
        logo_icon.setStyleSheet("color: #56b4e9; font-size: 56px; background: transparent;")

        logo_text = QLabel("FASHION STORE")
        logo_text.setAlignment(Qt.AlignCenter)
        logo_text.setStyleSheet(
            "color: #e8f4fd; font-size: 26px; font-weight: 800; background: transparent;"
            "letter-spacing: 2px; font-family: 'Nunito', 'Segoe UI', sans-serif;"
        )

        slogan = QLabel("Quản lý cửa hàng thời trang\nchuyên nghiệp & hiệu quả")
        slogan.setWordWrap(True)
        slogan.setAlignment(Qt.AlignCenter)
        slogan.setStyleSheet("color: #64748b; font-size: 14px; line-height: 1.6; background: transparent;")

        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background: rgba(86,180,233,0.25);")

        features = [
            ("◈", "Quản lý sản phẩm & kho hàng"),
            ("⊕", "Bán hàng & xuất hóa đơn"),
            ("▦", "Báo cáo & thống kê doanh thu"),
        ]

        ll.addWidget(logo_icon)
        ll.addWidget(logo_text)
        ll.addSpacing(4)
        ll.addWidget(slogan)
        ll.addSpacing(16)
        ll.addWidget(divider)
        ll.addSpacing(16)

        for icon, text in features:
            row = QHBoxLayout()
            row.setSpacing(10)
            ic_lbl = QLabel(icon)
            ic_lbl.setStyleSheet("color: #56b4e9; font-size: 14px; background: transparent;")
            ic_lbl.setFixedWidth(22)
            tx_lbl = QLabel(text)
            tx_lbl.setStyleSheet("color: #94a3b8; font-size: 13px; background: transparent;")
            row.addWidget(ic_lbl)
            row.addWidget(tx_lbl)
            row.addStretch()
            ll.addLayout(row)

        # ── RIGHT PANEL (form) ───────────────────────────────────
        right = QFrame()
        right.setStyleSheet("QFrame { background-color: #ffffff; }")
        rl = QVBoxLayout()
        rl.setContentsMargins(68, 0, 68, 0)
        rl.setAlignment(Qt.AlignCenter)
        rl.setSpacing(0)
        right.setLayout(rl)

        title = QLabel("Đăng nhập")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            "color: #0f172a; font-size: 26px; font-weight: bold; padding-bottom: 6px; background: transparent;"
        )

        subtitle = QLabel("Nhập thông tin tài khoản để tiếp tục")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #94a3b8; font-size: 13px; padding-bottom: 30px; background: transparent;")

        # Username
        lbl_user = QLabel("Tên đăng nhập")
        lbl_user.setStyleSheet("color: #475569; font-size: 13px; font-weight: 600; padding-bottom: 6px; background: transparent;")

        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("Nhập tên đăng nhập")
        self.txt_username.setFixedHeight(46)
        self.txt_username.setStyleSheet("""
            QLineEdit {
                background-color: #f4faff; border: 1.5px solid #d0e9f7;
                border-radius: 10px; padding: 0 14px; color: #0d2333; font-size: 14px;
                font-family: 'Nunito', 'Segoe UI', sans-serif;
            }
            QLineEdit:focus { border-color: #56b4e9; background-color: #ffffff; }
        """)

        # Password
        lbl_pass = QLabel("Mật khẩu")
        lbl_pass.setStyleSheet("color: #475569; font-size: 13px; font-weight: 600; padding-top: 16px; padding-bottom: 6px; background: transparent;")

        pw_row = QHBoxLayout()
        pw_row.setSpacing(8)

        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Nhập mật khẩu")
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.setFixedHeight(46)
        self.txt_password.setStyleSheet("""
            QLineEdit {
                background-color: #f4faff; border: 1.5px solid #d0e9f7;
                border-radius: 10px; padding: 0 14px; color: #0d2333; font-size: 14px;
                font-family: 'Nunito', 'Segoe UI', sans-serif;
            }
            QLineEdit:focus { border-color: #56b4e9; background-color: #ffffff; }
        """)

        self.btn_toggle_pw = QPushButton("👁")
        self.btn_toggle_pw.setFixedSize(46, 46)
        self.btn_toggle_pw.setCursor(Qt.PointingHandCursor)
        self.btn_toggle_pw.setStyleSheet("""
            QPushButton { background-color: #f4faff; border: 1.5px solid #d0e9f7;
                          border-radius: 10px; color: #7faec9; font-size: 16px; }
            QPushButton:hover { background-color: #e8f4fd; border-color: #56b4e9; }
        """)
        self.btn_toggle_pw.clicked.connect(self.toggle_password)
        pw_row.addWidget(self.txt_password)
        pw_row.addWidget(self.btn_toggle_pw)

        # Options row
        options_row = QHBoxLayout()
        self.chk_remember = QCheckBox("Ghi nhớ đăng nhập")
        self.chk_remember.setStyleSheet("""
            QCheckBox { color: #3d6278; font-size: 13px; background: transparent;
                        font-family: 'Nunito', 'Segoe UI', sans-serif; }
            QCheckBox::indicator { width: 17px; height: 17px; border: 2px solid #b0d8f0;
                                   border-radius: 5px; background: #f4faff; }
            QCheckBox::indicator:checked { background: #56b4e9; border-color: #56b4e9; }
        """)
        options_row.addWidget(self.chk_remember)
        options_row.addStretch()

        # Login button
        self.btn_login = QPushButton("Đăng nhập")
        self.btn_login.setFixedHeight(50)
        self.btn_login.setCursor(Qt.PointingHandCursor)
        self.btn_login.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #56b4e9, stop:1 #3a9fd4);
                border-radius: 10px; color: white;
                font-size: 15px; font-weight: 800; margin-top: 6px;
                font-family: 'Nunito', 'Segoe UI', sans-serif;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #3a9fd4, stop:1 #2186b8);
            }
            QPushButton:pressed { background-color: #2186b8; }
        """)

        self.lbl_status = QLabel("")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.lbl_status.setStyleSheet(
            "color: #ef4444; font-size: 13px; background: transparent; padding-top: 8px;"
        )

        rl.addWidget(title)
        rl.addWidget(subtitle)
        rl.addWidget(lbl_user)
        rl.addWidget(self.txt_username)
        rl.addWidget(lbl_pass)
        rl.addLayout(pw_row)
        rl.addSpacing(14)
        rl.addLayout(options_row)
        rl.addSpacing(18)
        rl.addWidget(self.btn_login)
        rl.addWidget(self.lbl_status)

        main_layout.addWidget(left, 1)
        main_layout.addWidget(right, 1)

        try:
            saved = load_login()
            if saved:
                self.txt_username.setText(saved.get("username", ""))
                self.txt_password.setText(saved.get("password", ""))
                self.chk_remember.setChecked(True)
        except Exception:
            pass

    def toggle_password(self):
        if self.txt_password.echoMode() == QLineEdit.Password:
            self.txt_password.setEchoMode(QLineEdit.Normal)
            self.btn_toggle_pw.setText("🙈")
        else:
            self.txt_password.setEchoMode(QLineEdit.Password)
            self.btn_toggle_pw.setText("👁")
