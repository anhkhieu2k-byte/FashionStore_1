from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QColor, QFont

from config import *

from ui.tabs.product_tab import ProductTab
from ui.tabs.customer_tab import CustomerTab
from ui.tabs.sales_tab import SalesTab
from ui.tabs.inventory_tab import InventoryTab
from ui.tabs.staff_tab import StaffTab
from ui.tabs.promotion_tab import PromotionTab
from ui.tabs.report_tab import ReportTab
from ui.tabs.return_tab import ReturnTab
from ui.tabs.invoice_tab import InvoiceTab

from controllers.product_controller import ProductController
from controllers.customer_controller import CustomerController
from controllers.sales_controller import SalesController
from controllers.inventory_controller import InventoryController
from controllers.staff_controller import StaffController
from controllers.promotion_controller import PromotionController
from controllers.report_controller import ReportController
from controllers.return_controller import ReturnController
from controllers.invoice_controller import InvoiceController


GLOBAL_STYLE = f"""
    QMainWindow {{ background-color: {BG_MAIN}; }}
    QWidget {{
        background-color: {BG_MAIN}; color: {TEXT_DARK};
        font-family: 'Nunito', 'Segoe UI', sans-serif; font-size: 14px;
    }}
    QLabel {{ color: {TEXT_DARK}; background-color: transparent; font-family: 'Nunito', 'Segoe UI', sans-serif; }}

    QLineEdit {{
        background-color: {BG_INPUT}; border: 1.5px solid {BORDER};
        border-radius: 10px; padding: 8px 12px; color: {TEXT_DARK}; font-size: 14px;
        font-family: 'Nunito', 'Segoe UI', sans-serif;
    }}
    QLineEdit:focus {{ border: 1.5px solid {PRIMARY}; background-color: #fff; }}

    QTextEdit {{
        background-color: {BG_INPUT}; border: 1.5px solid {BORDER};
        border-radius: 10px; padding: 8px; color: {TEXT_DARK};
        font-family: 'Nunito', 'Segoe UI', sans-serif;
    }}

    QComboBox {{
        background-color: {BG_INPUT}; border: 1.5px solid {BORDER};
        border-radius: 10px; padding: 7px 12px; color: {TEXT_DARK}; min-height: 36px;
        font-family: 'Nunito', 'Segoe UI', sans-serif;
    }}
    QComboBox:focus {{ border-color: {PRIMARY}; }}
    QComboBox::drop-down {{ border: none; width: 28px; }}
    QComboBox QAbstractItemView {{
        background-color: {BG_CARD}; border: 1px solid {BORDER}; color: {TEXT_DARK};
        selection-background-color: {PRIMARY}; selection-color: white;
        font-family: 'Nunito', 'Segoe UI', sans-serif;
    }}

    QPushButton {{
        background-color: {PRIMARY}; border: none; border-radius: 10px;
        padding: 10px 18px; color: white; font-weight: 800; font-size: 15px;
        font-family: 'Nunito', 'Segoe UI', sans-serif;
    }}
    QPushButton:hover {{ background-color: {PRIMARY_DARK}; }}
    QPushButton:pressed {{ background-color: {PRIMARY_DARK}; }}
    QPushButton:disabled {{ background-color: {BORDER}; color: {TEXT_LIGHT}; }}

    /* QMessageBox Styles */
    QMessageBox {{
        background-color: #ffffff;
    }}
    QMessageBox QLabel {{
        color: #1e293b;
        font-size: 15px;
        font-weight: 600;
        padding: 10px;
    }}
    QMessageBox QPushButton {{
        background-color: #2563eb !important;
        color: #ffffff !important;
        border: none;
        border-radius: 6px;
        padding: 8px 25px;
        font-weight: bold;
        font-size: 13px;
        min-width: 85px;
    }}
    QMessageBox QPushButton:hover {{
        background-color: #1d4ed8 !important;
    }}
    
    /* General Dialog Buttons */
    QDialog QPushButton {{
        background-color: #2563eb;
        color: #ffffff;
        border-radius: 6px;
        padding: 8px 20px;
        font-weight: bold;
    }}

    QTableWidget {{
        background-color: #ffffff; border: 1px solid {BORDER};
        border-radius: 12px; color: {TEXT_MID};
        font-family: 'Nunito', 'Segoe UI', sans-serif;
    }}
    QHeaderView::section {{
        background-color: #f0f7ff;
        color: #0369a1; padding: 12px;
        border: none; border-bottom: 1px solid {BORDER};
        font-weight: 800; font-size: 11px;
        font-family: 'Nunito', 'Segoe UI', sans-serif; text-transform: uppercase;
    }}

    QScrollBar:vertical {{ background: {BG_MAIN}; width: 7px; margin: 0px; border-radius: 4px; }}
    QScrollBar::handle:vertical {{ background: {BORDER_MED}; border-radius: 4px; min-height: 24px; }}
    QScrollBar::handle:vertical:hover {{ background: {PRIMARY}; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
    QScrollBar:horizontal {{ background: {BG_MAIN}; height: 7px; border-radius: 4px; }}
    QScrollBar::handle:horizontal {{ background: {BORDER_MED}; border-radius: 4px; }}

    QGroupBox {{
        border: 1px solid {BORDER}; border-radius: 10px; margin-top: 14px;
        padding-top: 14px; color: {TEXT_MID}; font-size: 12px;
        background-color: {BG_CARD};
        font-family: 'Nunito', 'Segoe UI', sans-serif;
    }}
    QGroupBox::title {{ color: {PRIMARY_DARK}; subcontrol-origin: margin; left: 12px; }}

    QDateEdit, QSpinBox, QDoubleSpinBox {{
        background-color: {BG_INPUT}; border: 1.5px solid {BORDER};
        border-radius: 10px; padding: 7px; color: {TEXT_DARK};
        font-family: 'Nunito', 'Segoe UI', sans-serif;
    }}

    QCheckBox {{ color: {TEXT_DARK}; spacing: 8px; font-family: 'Nunito', 'Segoe UI', sans-serif; }}
    QCheckBox::indicator {{ width: 17px; height: 17px; border: 2px solid {BORDER_MED}; border-radius: 5px; background: {BG_INPUT}; }}
    QCheckBox::indicator:checked {{ background-color: {PRIMARY}; border-color: {PRIMARY}; }}

    QTabWidget::pane {{ border: 1px solid {BORDER}; border-radius: 10px; background: {BG_CARD}; }}
    QTabBar::tab {{
        background-color: {BG_MAIN}; color: {TEXT_MID}; padding: 8px 22px;
        border-top-left-radius: 8px; border-top-right-radius: 8px; border: 1px solid {BORDER};
        margin-right: 2px; font-family: 'Nunito', 'Segoe UI', sans-serif;
    }}
    QTabBar::tab:selected {{ background-color: {PRIMARY}; color: white; border-color: {PRIMARY}; }}
    QTabBar::tab:hover:!selected {{ background-color: {PRIMARY_LIGHT}; color: {TEXT_DARK}; }}
"""

NAV_ACTIVE = f"""
    QPushButton {{
        background-color: {BG_SIDEBAR_ACT};
        color: white;
        text-align: left;
        padding-left: 21px;
        font-size: 15px;
        font-weight: 800;
        border: none;
        border-left: 4px solid {PRIMARY};
        border-radius: 0;
        font-family: 'Nunito', 'Segoe UI', sans-serif;
    }}
"""

NAV_NORMAL = f"""
    QPushButton {{
        background-color: transparent;
        color: #94a3b8;
        text-align: left;
        padding-left: 24px;
        font-size: 15px;
        font-weight: 600;
        border: none;
        border-radius: 0;
        font-family: 'Nunito', 'Segoe UI', sans-serif;
    }}
    QPushButton:hover {{
        background-color: #1e293b;
        color: white;
    }}
"""


class ClickableCard(QFrame):
    def __init__(self, title, subtitle, icon, color_hex, bg_light, callback, parent=None):
        super().__init__(parent)
        self.callback = callback
        self.setFixedHeight(85)
        self.setCursor(Qt.PointingHandCursor)
        self.default_style = f"""
            ClickableCard {{
                background-color: #ffffff;
                border: 1.5px solid #e2e8f0;
                border-radius: 14px;
            }}
        """
        self.hover_style = f"""
            ClickableCard {{
                background-color: {bg_light};
                border: 1.5px solid {color_hex};
                border-radius: 14px;
            }}
        """
        self.setStyleSheet(self.default_style)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(16, 12, 16, 12)
        lay.setSpacing(14)

        ic_frame = QFrame()
        ic_frame.setFixedSize(46, 46)
        ic_frame.setStyleSheet(f"background-color: {bg_light}; border-radius: 23px; border: none;")
        ic_lay = QHBoxLayout(ic_frame)
        ic_lay.setContentsMargins(0, 0, 0, 0)
        lbl_ic = QLabel(icon)
        lbl_ic.setAlignment(Qt.AlignCenter)
        lbl_ic.setStyleSheet(f"color: {color_hex}; font-size: 20px; font-weight: bold; background: transparent;")
        ic_lay.addWidget(lbl_ic)

        t_lay = QVBoxLayout()
        t_lay.setSpacing(2)
        t_lay.setAlignment(Qt.AlignVCenter)

        lbl_t = QLabel(title)
        lbl_t.setStyleSheet("color: #0f172a; font-size: 15px; font-weight: 800; background: transparent; font-family: 'Nunito', sans-serif;")

        lbl_sub = QLabel(subtitle)
        lbl_sub.setStyleSheet("color: #64748b; font-size: 12px; font-weight: 600; background: transparent; font-family: 'Nunito', sans-serif;")

        t_lay.addWidget(lbl_t)
        t_lay.addWidget(lbl_sub)

        lay.addWidget(ic_frame)
        lay.addLayout(t_lay)
        lay.addStretch()

        lbl_arr = QLabel("→")
        lbl_arr.setStyleSheet("color: #cbd5e1; font-size: 18px; font-weight: bold; background: transparent;")
        lay.addWidget(lbl_arr)
        self.lbl_arr = lbl_arr
        self.color_hex = color_hex

        # Thêm hiệu ứng bóng đổ mượt mà
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setOffset(0, 3)
        shadow.setColor(QColor(0, 0, 0, 10))
        self.setGraphicsEffect(shadow)

    def enterEvent(self, event):
        self.setStyleSheet(self.hover_style)
        self.lbl_arr.setStyleSheet(f"color: {self.color_hex}; font-size: 18px; font-weight: bold; background: transparent;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(self.default_style)
        self.lbl_arr.setStyleSheet("color: #cbd5e1; font-size: 18px; font-weight: bold; background: transparent;")
        super().leaveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.callback:
            self.callback()
        super().mouseReleaseEvent(event)


class PasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Xác thực quyền truy cập")
        self.setFixedWidth(400)
        self.setStyleSheet("background-color: white;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(18)
        
        lbl = QLabel("🔐 Vui lòng nhập mật khẩu quản trị để tiếp tục:")
        lbl.setStyleSheet("font-weight: 800; color: #1e293b; font-size: 14px;")
        lbl.setWordWrap(True)
        layout.addWidget(lbl)
        
        self.txt_pass = QLineEdit()
        self.txt_pass.setEchoMode(QLineEdit.Password)
        self.txt_pass.setFixedHeight(45)
        self.txt_pass.setPlaceholderText("Nhập mật khẩu tại đây...")
        self.txt_pass.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 0 15px;
                font-size: 16px;
                background-color: #f8fafc;
            }}
            QLineEdit:focus {{
                border-color: {PRIMARY};
                background-color: white;
            }}
        """)
        layout.addWidget(self.txt_pass)
        
        btns = QHBoxLayout()
        btns.setSpacing(12)
        
        self.btn_ok = QPushButton("Xác nhận")
        self.btn_ok.setFixedHeight(40)
        self.btn_ok.setCursor(Qt.PointingHandCursor)
        self.btn_ok.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY};
                color: white;
                border-radius: 8px;
                font-weight: 800;
                font-size: 14px;
            }}
            QPushButton:hover {{ background-color: {PRIMARY_DARK}; }}
        """)
        self.btn_ok.clicked.connect(self.accept)
        
        self.btn_cancel = QPushButton("Hủy bỏ")
        self.btn_cancel.setFixedHeight(40)
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #475569;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #e2e8f0; }
        """)
        self.btn_cancel.clicked.connect(self.reject)
        
        btns.addWidget(self.btn_cancel)
        btns.addWidget(self.btn_ok)
        layout.addLayout(btns)
        
        self.txt_pass.setFocus()
        
    def get_password(self):
        return self.txt_pass.text()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.current_active_btn = None
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(GLOBAL_STYLE)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central.setLayout(main_layout)

        # ─── SIDEBAR ────────────────────────────────────────────
        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet(f"QFrame {{ background: {BG_SIDEBAR}; border-right: 1px solid #1e293b; }}")
        sb_layout = QVBoxLayout()
        sb_layout.setContentsMargins(0, 0, 0, 0)
        sb_layout.setSpacing(4)
        sidebar.setLayout(sb_layout)

        # Logo
        logo_frame = QFrame()
        logo_frame.setFixedHeight(76)
        logo_frame.setStyleSheet("background: transparent; border-bottom: 1px solid #1e293b;")
        ll = QHBoxLayout()
        ll.setContentsMargins(20, 0, 20, 0)
        ic = QLabel("👗")
        ic.setStyleSheet("color:white; font-size:24px; background:transparent;")
        
        lt_col = QVBoxLayout()
        lt_col.setSpacing(0); lt_col.setAlignment(Qt.AlignVCenter)
        lt1 = QLabel("FashionStore")
        lt1.setStyleSheet("color:white; font-size:16px; font-weight:800; background:transparent; font-family:'Nunito',sans-serif;")
        lt2 = QLabel("QUẢN LÝ CỬA HÀNG")
        lt2.setStyleSheet("color:#94a3b8; font-size:9px; font-weight:700; background:transparent; font-family:'Nunito',sans-serif;")
        lt_col.addWidget(lt1); lt_col.addWidget(lt2)
        
        ll.addWidget(ic); ll.addSpacing(8); ll.addLayout(lt_col); ll.addStretch()
        logo_frame.setLayout(ll)
        sb_layout.addWidget(logo_frame)

        nav_hdr = QLabel("   ") # Tắt dòng chữ điều hướng để giống ảnh
        sb_layout.addWidget(nav_hdr)

        menu_items = [
            ("btn_dashboard", "▪", "Tổng quan",   0),
            ("btn_product",   "▪", "Sản phẩm",    1),
            ("btn_customer",  "▪", "Khách hàng",  2),
            ("btn_sales",     "▪", "Bán hàng",    3),
            ("btn_invoice",   "▪", "Lịch sử hóa đơn", 9),
            ("btn_return",    "▪", "Đổi / Trả hàng",   8),
            ("btn_inventory", "▪", "Kho hàng",    4),
            ("btn_staff",     "▪", "Nhân viên",   5),
            ("btn_promotion", "▪", "Khuyến mãi",  6),
            ("btn_report",    "▪", "Báo cáo",     7),
        ]

        for attr, icon, label, idx in menu_items:
            btn = QPushButton(f"   {icon}    {label}")
            btn.setFixedHeight(48)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(NAV_NORMAL)
            setattr(self, attr, btn)
            sb_layout.addWidget(btn)

        sb_layout.addStretch()

        self.btn_logout = QPushButton("  ⚙   Cài đặt / Đăng xuất")
        self.btn_logout.setFixedHeight(50)
        self.btn_logout.setCursor(Qt.PointingHandCursor)
        self.btn_logout.setStyleSheet(NAV_NORMAL)
        self.btn_logout.clicked.connect(self.logout)
        
        user_panel = QFrame()
        user_panel.setFixedHeight(64)
        user_panel.setStyleSheet("background: #0f172a; border-top: 1px solid #1e293b;")
        up_lay = QHBoxLayout(user_panel)
        up_lay.setContentsMargins(20, 0, 20, 0)
        ub_circle = QLabel("A")
        ub_circle.setFixedSize(32, 32)
        ub_circle.setAlignment(Qt.AlignCenter)
        ub_circle.setStyleSheet(f"background:{PRIMARY}; color:white; border-radius:16px; font-weight:bold; font-size:14px;")
        
        u_info = QVBoxLayout()
        u_info.setSpacing(0); u_info.setAlignment(Qt.AlignVCenter)
        u1 = QLabel("Admin")
        u1.setStyleSheet("color:white; font-size:13px; font-weight:700; font-family:'Nunito',sans-serif;")
        u2 = QLabel("Quản lý")
        u2.setStyleSheet("color:#94a3b8; font-size:11px; font-family:'Nunito',sans-serif;")
        u_info.addWidget(u1); u_info.addWidget(u2)
        up_lay.addWidget(ub_circle); up_lay.addSpacing(8); up_lay.addLayout(u_info); up_lay.addStretch()
        
        sb_layout.addWidget(self.btn_logout)
        sb_layout.addWidget(user_panel)

        # ─── CONTENT ────────────────────────────────────────────
        content = QWidget()
        content.setStyleSheet(f"background-color: {BG_MAIN};")
        cl = QVBoxLayout()
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(0)
        content.setLayout(cl)

        top_bar = QFrame()
        top_bar.setFixedHeight(64)
        top_bar.setStyleSheet(f"QFrame {{ background-color: #ffffff; border-bottom: 1px solid {BORDER}; }}")
        tbl = QHBoxLayout()
        tbl.setContentsMargins(24, 0, 24, 0)
        self.lbl_page = QLabel("Tổng quan")
        self.lbl_page.setStyleSheet(
            f"color:#1e293b; font-size:16px; font-weight:800; background:transparent;"
            f"font-family:'Nunito','Segoe UI',sans-serif;"
        )
        self.lbl_date = QLabel("📅 " + QDateTime.currentDateTime().toString("dddd, dd/MM/yyyy"))
        self.lbl_date.setStyleSheet(
            f"color:{TEXT_MID}; font-size:13px; background:transparent;"
            f"font-family:'Nunito','Segoe UI',sans-serif;"
        )

        ub_top = QHBoxLayout()
        ub_top.setSpacing(8)
        ub_top_circle = QLabel("A")
        ub_top_circle.setFixedSize(28, 28)
        ub_top_circle.setAlignment(Qt.AlignCenter)
        ub_top_circle.setStyleSheet(f"background:{PRIMARY}; color:white; border-radius:14px; font-weight:bold;")
        ub_top_txt = QLabel("Admin")
        ub_top_txt.setStyleSheet("color:#1e293b; font-weight:700; font-size:13px;")
        ub_top.addWidget(ub_top_circle); ub_top.addWidget(ub_top_txt)

        tbl.addWidget(self.lbl_page); tbl.addStretch()
        tbl.addWidget(self.lbl_date); tbl.addSpacing(24); tbl.addLayout(ub_top)
        top_bar.setLayout(tbl)
        cl.addWidget(top_bar)

        self.stack = QStackedWidget()
        self.stack.setStyleSheet(f"background-color: {BG_MAIN};")
        cl.addWidget(self.stack)
        self.stack.addWidget(self._build_dashboard())

        self.product_tab   = ProductTab()
        self.customer_tab  = CustomerTab()
        self.sales_tab     = SalesTab()
        self.inventory_tab = InventoryTab()
        self.staff_tab     = StaffTab()
        self.promotion_tab = PromotionTab()
        self.report_tab    = ReportTab()
        self.return_tab    = ReturnTab()
        self.invoice_tab   = InvoiceTab()

        for tab in [self.product_tab, self.customer_tab, self.sales_tab,
                    self.inventory_tab, self.staff_tab, self.promotion_tab,
                    self.report_tab, self.return_tab, self.invoice_tab]:
            self.stack.addWidget(tab)

        self.product_controller   = ProductController(self.product_tab)
        self.customer_controller  = CustomerController(self.customer_tab)
        
        # Kết nối SalesController với hàm refresh để cập nhật Lịch sử & Dashboard ngay lập tức
        self.sales_controller = SalesController(
            self.sales_tab, 
            on_success=lambda: (
                self.invoice_controller.load_history() if hasattr(self, 'invoice_controller') else None,
                self.refresh_dashboard()
            )
        )
        self.inventory_controller = InventoryController(self.inventory_tab)
        self.staff_controller     = StaffController(self.staff_tab)
        self.promotion_controller = PromotionController(self.promotion_tab)
        self.report_controller    = ReportController(self.report_tab)
        self.return_controller = ReturnController(
            self.return_tab,
            on_success=lambda: (
                self.invoice_controller.load_history() if hasattr(self, 'invoice_controller') else None,
                self.customer_controller.load_customers() if hasattr(self, 'customer_controller') else None,
                self.refresh_dashboard() if hasattr(self, 'refresh_dashboard') else None
            )
        )
        self.invoice_controller   = InvoiceController(self.invoice_tab)

        for attr, icon, label, idx in menu_items:
            btn = getattr(self, attr)
            btn.clicked.connect(lambda ch, i=idx, lbl=label, b=btn: self._navigate(i, lbl, b))

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)
        self._set_active(self.btn_dashboard)

    def _tick(self):
        self.lbl_clock.setText(QDateTime.currentDateTime().toString("hh:mm  dd/MM/yyyy"))

    def _navigate(self, index, label, btn):
        # Kiểm tra bảo mật cho trang Khuyến mãi (index 6)
        if index == 6:
            dialog = PasswordDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                password = dialog.get_password()
                ok = True
            else:
                return
            
            if ok and password == "admin123":
                # Mật khẩu đúng, cho phép vào
                pass
            elif not ok:
                # Người dùng nhấn Cancel, không làm gì cả
                return
            else:
                # Mật khẩu sai
                msg = QMessageBox(self)
                msg.setWindowTitle("Truy cập bị từ chối")
                msg.setText("Mật khẩu không chính xác!<br>Bạn không có quyền truy cập vào khu vực này.")
                msg.setIcon(QMessageBox.Critical)
                ok_btn = msg.addButton("Đã hiểu", QMessageBox.AcceptRole)
                ok_btn.setStyleSheet("QPushButton { background-color: #ef4444; color: white; border-radius: 8px; padding: 8px 20px; font-weight: bold; }")
                msg.exec_()
                return

        self.stack.setCurrentIndex(index)
        self.lbl_page.setText(label)
        self._set_active(btn)
        
        # Refresh dữ liệu cho các tab khi nhấn vào
        if index == 0: # Dashboard
            self.refresh_dashboard()
        elif index == 1: # Sản phẩm
            self.product_controller.load_products()
        elif index == 2: # Khách hàng
            self.customer_controller.load_customers()
        elif index == 3: # Bán hàng
            self.sales_controller.load_customers()
            self.sales_controller.load_products()
            self.sales_controller.load_promotions()
        elif index == 5: # Nhân viên
            self.staff_controller.load_staff()
        elif index == 6: # Khuyến mãi
            self.promotion_controller.load_promotions()
        elif index == 9: # Hóa đơn
            self.invoice_controller.load_history()

    def _set_active(self, btn):
        if self.current_active_btn and self.current_active_btn is not btn:
            self.current_active_btn.setStyleSheet(NAV_NORMAL)
        btn.setStyleSheet(NAV_ACTIVE)
        self.current_active_btn = btn

    def logout(self):
        reply = QMessageBox.question(
            self, "Xác nhận đăng xuất",
            "Bạn có muốn đăng xuất khỏi hệ thống không?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            from ui.login_window import LoginWindow
            from controllers.login_controller import LoginController
            self.login_window = LoginWindow()
            self.login_controller = LoginController(self.login_window)
            self.login_window.show()
            self.close()

    def _build_dashboard(self):
        w = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 26, 32, 26)
        layout.setSpacing(24)
        w.setLayout(layout)

        # 1. Bảng điều khiển Chào mừng (Hero Banner) với Gradient tuyệt đẹp
        banner = QFrame()
        banner.setObjectName("HeroBanner")
        banner.setFixedHeight(125)
        banner.setStyleSheet(f"""
            QFrame#HeroBanner {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e3a8a, stop:0.5 #2563eb, stop:1 #3b82f6);
                border-radius: 18px;
            }}
        """)
        # Hiệu ứng bóng đổ cho Banner
        b_shadow = QGraphicsDropShadowEffect(banner)
        b_shadow.setBlurRadius(20)
        b_shadow.setOffset(0, 6)
        b_shadow.setColor(QColor(37, 99, 235, 60))
        banner.setGraphicsEffect(b_shadow)

        bl = QHBoxLayout(banner)
        bl.setContentsMargins(32, 0, 32, 0)
        
        bv = QVBoxLayout()
        bv.setSpacing(6)
        bv.setAlignment(Qt.AlignVCenter)
        
        tag_frame = QFrame()
        tag_frame.setObjectName("TagFrame")
        tag_frame.setStyleSheet("QFrame#TagFrame { background-color: rgba(255, 255, 255, 0.2); border-radius: 6px; }")
        tag_lay = QHBoxLayout(tag_frame)
        tag_lay.setContentsMargins(10, 4, 10, 4)
        lbl_tag = QLabel("✨ PREMIUM SYSTEM")
        lbl_tag.setStyleSheet("color: #ffffff; font-size: 10px; font-weight: 900; letter-spacing: 1px; font-family: 'Nunito', sans-serif;")
        tag_lay.addWidget(lbl_tag)
        
        top_banner_row = QHBoxLayout()
        top_banner_row.addWidget(tag_frame)
        top_banner_row.addStretch()

        bt = QLabel("XIN CHÀO, QUẢN TRỊ VIÊN! 👋")
        bt.setStyleSheet("color: #ffffff; font-size: 22px; font-weight: 900; background: transparent; font-family: 'Nunito', sans-serif; letter-spacing: 0.5px;")
        
        bs = QLabel("Hệ thống Quản lý Bán lẻ & Chuỗi cửa hàng Thời trang Cao cấp • Hoạt động tối ưu")
        bs.setStyleSheet("color: #e0f2fe; font-size: 14px; font-weight: 600; background: transparent; font-family: 'Nunito', sans-serif;")
        
        bv.addLayout(top_banner_row)
        bv.addWidget(bt)
        bv.addWidget(bs)
        
        bi = QLabel("👑")
        bi.setStyleSheet("color: #bfdbfe; font-size: 64px; background: transparent;")
        bi.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        bl.addLayout(bv)
        bl.addStretch()
        bl.addWidget(bi)
        layout.addWidget(banner)

        # 2. Thẻ Thống kê KPI (Metric Cards) cao cấp
        cards_row = QHBoxLayout()
        cards_row.setSpacing(20)
        
        self.lbl_dash_prod = QLabel("0")
        self.lbl_dash_rev = QLabel("0 ₫")
        self.lbl_dash_cust = QLabel("0")
        self.lbl_dash_orders = QLabel("0")

        cards_data = [
            ("TỔNG SẢN PHẨM", self.lbl_dash_prod, PRIMARY, "◈", "#eff6ff", "Cập nhật danh mục"),
            ("DOANH THU ƯỚC TÍNH", self.lbl_dash_rev, INFO, "❖", "#e0f2fe", "▲ Tăng trưởng tốt"),
            ("KHÁCH HÀNG", self.lbl_dash_cust, SUCCESS, "▪", "#dcfce7", "Hoạt động tích cực"),
            ("ĐƠN BÁN HÀNG", self.lbl_dash_orders, WARNING, "▣", "#fef3c7", "Xử lý theo thời gian thực"),
        ]
        
        for title, lbl_val, color, icon, bg_light, sub_text in cards_data:
            card = QFrame()
            card.setObjectName("StatCard")
            card.setFixedHeight(135)
            card.setStyleSheet(f"""
                QFrame#StatCard {{
                    background-color: #ffffff;
                    border: 1px solid #e2e8f0;
                    border-radius: 16px;
                    border-top: 4px solid {color};
                }}
            """)
            
            c_shadow = QGraphicsDropShadowEffect(card)
            c_shadow.setBlurRadius(15)
            c_shadow.setOffset(0, 4)
            c_shadow.setColor(QColor(0, 0, 0, 10))
            card.setGraphicsEffect(c_shadow)

            cvl = QVBoxLayout(card)
            cvl.setContentsMargins(22, 16, 22, 16)
            cvl.setSpacing(6)
            
            row = QHBoxLayout()
            t_lbl = QLabel(title)
            t_lbl.setStyleSheet(f"color: #64748b; font-size: 11px; font-weight: 900; font-family: 'Nunito', sans-serif; letter-spacing: 0.5px;")
            
            ic_box = QFrame()
            ic_box.setObjectName("IconBox")
            ic_box.setFixedSize(34, 34)
            ic_box.setStyleSheet(f"QFrame#IconBox {{ background-color: {bg_light}; border-radius: 17px; border: none; }}")
            ic_lay = QHBoxLayout(ic_box)
            ic_lay.setContentsMargins(0, 0, 0, 0)
            ic_lbl = QLabel(icon)
            ic_lbl.setAlignment(Qt.AlignCenter)
            ic_lbl.setStyleSheet(f"color: {color}; font-size: 16px; font-weight: bold; background: transparent;")
            ic_lay.addWidget(ic_lbl)
            
            row.addWidget(t_lbl)
            row.addStretch()
            row.addWidget(ic_box)
            
            lbl_val.setStyleSheet("color: #0f172a; font-size: 26px; font-weight: 900; font-family: 'Nunito', sans-serif;")
            
            sub_lbl = QLabel(sub_text)
            sub_lbl.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: 700; font-family: 'Nunito', sans-serif;")
            
            cvl.addLayout(row)
            cvl.addWidget(lbl_val)
            cvl.addWidget(sub_lbl)
            cards_row.addWidget(card)
            
        layout.addLayout(cards_row)

        # 3. Lối tắt Nghiệp vụ (Quick Actions) dạng Thẻ Click (Clickable Cards)
        qa_hdr = QLabel("⚡ LỐI TẮT NGHIỆP VỤ NHANH")
        qa_hdr.setStyleSheet("color: #475569; font-size: 12px; font-weight: 900; background: transparent; letter-spacing: 1px; font-family: 'Nunito', sans-serif;")
        layout.addWidget(qa_hdr)

        qa_row = QHBoxLayout()
        qa_row.setSpacing(16)
        
        quick_actions = [
            ("Bán hàng nhanh", "Tạo đơn và thanh toán", "⊕", PRIMARY, "#eff6ff", lambda: self._quick_nav(3, "Bán hàng")),
            ("Quản lý sản phẩm", "Kiểm tra danh mục hàng", "◈", INFO, "#e0f2fe", lambda: self._quick_nav(1, "Sản phẩm")),
            ("Nhập xuất kho", "Kiểm soát lượng hàng tồn", "▣", SUCCESS, "#dcfce7", lambda: self._quick_nav(4, "Kho hàng")),
            ("Xem báo cáo", "Phân tích số liệu kinh doanh", "▦", WARNING, "#fef3c7", lambda: self._quick_nav(7, "Báo cáo")),
        ]
        
        for title, sub, ic, col, bg_l, cb in quick_actions:
            q_card = ClickableCard(title, sub, ic, col, bg_l, cb)
            qa_row.addWidget(q_card)
            
        layout.addLayout(qa_row)

        # 4. Khu vực Điều hành (Executive Panels) — Phân tích & Hướng dẫn
        grid_row = QHBoxLayout()
        grid_row.setSpacing(20)
        
        # Panel Trái: Thanh tiến trình hiệu suất
        perf_panel = QFrame()
        perf_panel.setObjectName("PerfPanel")
        perf_panel.setStyleSheet("QFrame#PerfPanel { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; }")
        p_shadow = QGraphicsDropShadowEffect(perf_panel)
        p_shadow.setBlurRadius(15)
        p_shadow.setOffset(0, 4)
        p_shadow.setColor(QColor(0, 0, 0, 8))
        perf_panel.setGraphicsEffect(p_shadow)
        
        pp_lay = QVBoxLayout(perf_panel)
        pp_lay.setContentsMargins(22, 18, 22, 18)
        pp_lay.setSpacing(12)
        
        pp_hdr = QLabel("📈 Hiệu suất Kinh doanh & Vận hành")
        pp_hdr.setStyleSheet("color: #0f172a; font-size: 14px; font-weight: 800; font-family: 'Nunito', sans-serif;")
        pp_lay.addWidget(pp_hdr)
        
        def make_progress_row(label_text, percent, color_hex):
            r_w = QWidget()
            r_lay = QVBoxLayout(r_w)
            r_lay.setContentsMargins(0, 0, 0, 0)
            r_lay.setSpacing(4)
            
            t_r = QHBoxLayout()
            l1 = QLabel(label_text)
            l1.setStyleSheet("color: #475569; font-size: 12px; font-weight: 600;")
            l2 = QLabel(f"{percent}%")
            l2.setStyleSheet(f"color: {color_hex}; font-size: 12px; font-weight: 800;")
            t_r.addWidget(l1); t_r.addStretch(); t_r.addWidget(l2)
            
            p_bar = QProgressBar()
            p_bar.setFixedHeight(8)
            p_bar.setTextVisible(False)
            p_bar.setValue(percent)
            p_bar.setStyleSheet(f"""
                QProgressBar {{
                    background-color: #f1f5f9;
                    border: none;
                    border-radius: 4px;
                }}
                QProgressBar::chunk {{
                    background-color: {color_hex};
                    border-radius: 4px;
                }}
            """)
            r_lay.addLayout(t_r)
            r_lay.addWidget(p_bar)
            return r_w

        pp_lay.addWidget(make_progress_row("Chỉ tiêu doanh số ngày", 85, PRIMARY))
        pp_lay.addWidget(make_progress_row("Tỷ lệ xử lý đơn hàng thành công", 98, SUCCESS))
        pp_lay.addWidget(make_progress_row("Sức chứa kho hàng hiện tại", 42, INFO))
        grid_row.addWidget(perf_panel)
        
        # Panel Phải: Trung tâm Hướng dẫn
        guide_panel = QFrame()
        guide_panel.setObjectName("GuidePanel")
        guide_panel.setStyleSheet("QFrame#GuidePanel { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; }")
        g_shadow = QGraphicsDropShadowEffect(guide_panel)
        g_shadow.setBlurRadius(15)
        g_shadow.setOffset(0, 4)
        g_shadow.setColor(QColor(0, 0, 0, 8))
        guide_panel.setGraphicsEffect(g_shadow)
        
        gp_lay = QVBoxLayout(guide_panel)
        gp_lay.setContentsMargins(22, 18, 22, 18)
        gp_lay.setSpacing(10)
        
        gp_hdr = QLabel("💡 Hướng dẫn Vận hành Cửa hàng")
        gp_hdr.setStyleSheet("color: #0f172a; font-size: 14px; font-weight: 800; font-family: 'Nunito', sans-serif;")
        gp_lay.addWidget(gp_hdr)
        
        guides = [
            ("<b>Quản lý Hàng hóa:</b> Theo dõi tồn kho tối thiểu để kịp thời nhập lô mới.", SUCCESS),
            ("<b>Khách hàng:</b> Hệ thống tự động tích điểm và chiết khấu theo hạng thành viên.", PRIMARY),
            ("<b>Đồng bộ Dữ liệu:</b> Mọi giao dịch được lưu trữ an toàn theo thời gian thực.", INFO)
        ]
        
        for text, col in guides:
            g_r = QHBoxLayout()
            g_r.setSpacing(10)
            dot = QLabel("✔")
            dot.setFixedSize(20, 20)
            dot.setAlignment(Qt.AlignCenter)
            dot.setStyleSheet(f"background-color: {col}15; color: {col}; border-radius: 10px; font-size: 10px; font-weight: bold;")
            lbl_desc = QLabel(text)
            lbl_desc.setWordWrap(True)
            lbl_desc.setStyleSheet("color: #475569; font-size: 12px; line-height: 1.4;")
            g_r.addWidget(dot); g_r.addWidget(lbl_desc); g_r.addStretch()
            gp_lay.addLayout(g_r)
            
        gp_lay.addStretch()
        grid_row.addWidget(guide_panel)
        
        layout.addLayout(grid_row)
        layout.addStretch()
        
        # Gọi cập nhật số liệu ngay lần đầu
        self.refresh_dashboard()
        
        return w

    def refresh_dashboard(self):
        try:
            from database.db_connect import get_connection
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(id) FROM products")
            p_cnt = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT SUM(total) FROM invoices")
            r_sum = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT COUNT(id) FROM customers")
            c_cnt = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT COUNT(id) FROM invoices")
            o_cnt = cursor.fetchone()[0] or 0
            
            conn.close()
            
            if hasattr(self, 'lbl_dash_prod'): self.lbl_dash_prod.setText(f"{p_cnt:,}")
            if hasattr(self, 'lbl_dash_rev'): self.lbl_dash_rev.setText(f"{r_sum:,.0f} ₫")
            if hasattr(self, 'lbl_dash_cust'): self.lbl_dash_cust.setText(f"{c_cnt:,}")
            if hasattr(self, 'lbl_dash_orders'): self.lbl_dash_orders.setText(f"{o_cnt:,}")
        except Exception:
            pass

    def _quick_nav(self, idx, page):
        btn_map = {
            0: self.btn_dashboard, 1: self.btn_product, 2: self.btn_customer,
            3: self.btn_sales, 4: self.btn_inventory, 5: self.btn_staff,
            6: self.btn_promotion, 7: self.btn_report, 8: self.btn_return,
            9: self.btn_invoice
        }
        self._navigate(idx, page, btn_map[idx])
