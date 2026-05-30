"""
SalesTab — UI module Bán hàng (Point of Sale)
Giao diện được thiết kế tối ưu cho thao tác thu ngân (POS Layout).
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from config import *
from ui.widgets import *

def _card():
    f = QFrame()
    f.setStyleSheet(f"background:{BG_CARD}; border:1px solid {BORDER}; border-radius:12px;")
    return f

class SalesTab(QWidget):

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {BG_MAIN};")
        self.setup_ui()

    def setup_ui(self):
        root = QVBoxLayout()
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(16)
        self.setLayout(root)

        body = QHBoxLayout()
        body.setSpacing(16)
        root.addLayout(body)

        # ═══ CỘT TRÁI (65%): TÌM KIẾM & CHỌN SẢN PHẨM ════════════════
        left_col = QVBoxLayout()
        left_col.setSpacing(16)
        body.addLayout(left_col, 55)

        prod_card = _card()
        prod_lay = QVBoxLayout(prod_card)
        prod_lay.setContentsMargins(20, 20, 20, 20)
        prod_lay.setSpacing(16)
        
        # Thanh tìm kiếm to rõ ràng
        search_row = QHBoxLayout()
        lbl_icon = QLabel("🛍️")
        lbl_icon.setStyleSheet("font-size: 24px; background: transparent;")
        
        self.txt_prod_search = QLineEdit()
        self.txt_prod_search.setPlaceholderText("Nhập tên hoặc mã sản phẩm để tìm kiếm nhanh...")
        self.txt_prod_search.setFixedHeight(48)
        self.txt_prod_search.setStyleSheet(f"""
            QLineEdit {{
                background:{BG_INPUT}; border:2px solid {PRIMARY_LIGHT}; border-radius:12px;
                padding:8px 16px; font-size:15px; color:{TEXT_DARK}; font-family:'Nunito',sans-serif;
            }}
            QLineEdit:focus {{ border-color:{PRIMARY}; background:#fff; }}
        """)
        
        search_row.addWidget(lbl_icon)
        search_row.addWidget(self.txt_prod_search, 1)
        prod_lay.addLayout(search_row)

        # Bảng sản phẩm
        self.product_list = styled_table(["MÃ SP", "TÊN SẢN PHẨM", "DANH MỤC", "SIZE", "MÀU SẮC", "GIÁ BÁN"])
        self.product_list.setColumnWidth(0, 50)
        self.product_list.setColumnWidth(1, 180) # Tên sản phẩm nhỏ lại theo đúng yêu cầu
        self.product_list.setColumnWidth(2, 80)
        self.product_list.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch) # Để cột Size co giãn lấp đầy
        self.product_list.setColumnWidth(4, 80)
        self.product_list.setColumnWidth(5, 100)
        
        # Tăng chiều cao hàng cho dễ bấm
        self.product_list.verticalHeader().setDefaultSectionSize(48)
        self.product_list.setStyleSheet(self.product_list.styleSheet() + f"""
            QTableWidget::item {{ padding: 8px; font-size: 14px; }}
        """)
        prod_lay.addWidget(self.product_list)

        # Khung Thêm vào giỏ
        add_row = QHBoxLayout()
        
        lbl_size = QLabel("Size:")
        lbl_size.setStyleSheet(f"color:{TEXT_DARK}; font-size:15px; font-weight:800; font-family:'Nunito',sans-serif;")
        self.cb_size = QComboBox()
        self.cb_size.setFixedHeight(46)
        self.cb_size.setFixedWidth(80)
        self.cb_size.setStyleSheet(f"background:{BG_INPUT}; border:2px solid {BORDER}; border-radius:8px; font-size:15px; font-weight:bold; font-family:'Nunito',sans-serif; padding-left:12px;")

        lbl_color = QLabel("Màu:")
        lbl_color.setStyleSheet(f"color:{TEXT_DARK}; font-size:15px; font-weight:800; font-family:'Nunito',sans-serif;")
        self.cb_color = QComboBox()
        self.cb_color.setFixedHeight(46)
        self.cb_color.setFixedWidth(100)
        self.cb_color.setStyleSheet(f"background:{BG_INPUT}; border:2px solid {BORDER}; border-radius:8px; font-size:15px; font-weight:bold; font-family:'Nunito',sans-serif; padding-left:12px;")

        lbl_qty = QLabel("Số lượng:")
        lbl_qty.setStyleSheet(f"color:{TEXT_DARK}; font-size:15px; font-weight:800; font-family:'Nunito',sans-serif;")
        self.spin_qty = QSpinBox()
        self.spin_qty.setMinimum(1); self.spin_qty.setMaximum(999)
        self.spin_qty.setFixedHeight(46); self.spin_qty.setFixedWidth(80)
        self.spin_qty.setStyleSheet(f"background:{BG_INPUT}; border:2px solid {BORDER}; border-radius:8px; font-size:18px; font-weight:bold; font-family:'Nunito',sans-serif;")
        self.spin_qty.setAlignment(Qt.AlignCenter)
        
        self.btn_add_cart = QPushButton("➕ THÊM VÀO GIỎ HÀNG")
        self.btn_add_cart.setFixedHeight(46)
        self.btn_add_cart.setCursor(Qt.PointingHandCursor)
        self.btn_add_cart.setStyleSheet(f"""
            QPushButton {{
                background:{PRIMARY}; color:white; border-radius:8px; font-size:15px; font-weight:800; font-family:'Nunito',sans-serif;
            }}
            QPushButton:hover {{ background:{PRIMARY_DARK}; }}
        """)
        
        add_row.addStretch()
        add_row.addWidget(lbl_size)
        add_row.addWidget(self.cb_size)
        add_row.addSpacing(16)
        add_row.addWidget(lbl_color)
        add_row.addWidget(self.cb_color)
        add_row.addSpacing(16)
        add_row.addWidget(lbl_qty)
        add_row.addWidget(self.spin_qty)
        add_row.addSpacing(16)
        add_row.addWidget(self.btn_add_cart)
        prod_lay.addLayout(add_row)

        left_col.addWidget(prod_card)

        # ═══ CỘT PHẢI (35%): GIỎ HÀNG & THANH TOÁN ════════════════
        right_col = QVBoxLayout()
        right_col.setSpacing(16)
        body.addLayout(right_col, 45)

        cart_card = _card()
        cart_lay = QVBoxLayout(cart_card)
        cart_lay.setContentsMargins(20, 20, 20, 20)
        cart_lay.setSpacing(16)

        # Khung Khách hàng & Tìm kiếm inline
        cust_row = QHBoxLayout()
        cust_lbl = QLabel("👤 Khách Hàng:")
        cust_lbl.setStyleSheet(f"color:{TEXT_MID}; font-size:13px; font-weight:800; font-family:'Nunito',sans-serif;")
        
        self.txt_cust_search = QLineEdit()
        self.txt_cust_search.setPlaceholderText("🔍 Tìm tên, SĐT...")
        self.txt_cust_search.setFixedHeight(36)
        self.txt_cust_search.setStyleSheet(f"background:{BG_INPUT}; border:1px solid {BORDER}; border-radius:6px; padding:0 8px; font-size:13px; font-family:'Nunito',sans-serif;")
        
        cust_row.addWidget(cust_lbl); cust_row.addSpacing(10); cust_row.addWidget(self.txt_cust_search)
        cart_lay.addLayout(cust_row)
        
        cb_cust_row = QHBoxLayout()
        self.cb_customer = QComboBox()
        self.cb_customer.setFixedHeight(42)
        self.cb_customer.setStyleSheet(f"background:{BG_INPUT}; border:1px solid {BORDER}; border-radius:8px; padding:6px 12px; font-size:14px; font-weight:bold; font-family:'Nunito',sans-serif;")
        
        self.btn_add_customer = QPushButton("➕ Thêm mới")
        self.btn_add_customer.setFixedHeight(42)
        self.btn_add_customer.setCursor(Qt.PointingHandCursor)
        self.btn_add_customer.setStyleSheet(f"""
            QPushButton {{
                background:{SUCCESS}; color:white; border-radius:8px; 
                font-size:14px; font-weight:bold; padding: 0 12px;
            }}
            QPushButton:hover {{ background:#059669; }}
        """)
        self.btn_add_customer.setToolTip("Thêm khách hàng mới vào hệ thống")
        
        cb_cust_row.addWidget(self.cb_customer, 1)
        cb_cust_row.addWidget(self.btn_add_customer)
        cart_lay.addLayout(cb_cust_row)
        
        cart_lay.addWidget(divider())

        # Tiêu đề Giỏ hàng
        ch = QHBoxLayout()
        lbl_cart = QLabel("🛒 Giỏ Hàng")
        lbl_cart.setStyleSheet(f"color:{PRIMARY_DARK}; font-size:16px; font-weight:900; font-family:'Nunito',sans-serif;")
        self.btn_clear_cart = secondary_btn("✕ Làm mới", 36)
        ch.addWidget(lbl_cart); ch.addStretch(); ch.addWidget(self.btn_clear_cart)
        cart_lay.addLayout(ch)

        # Bảng giỏ hàng
        self.cart_table = styled_table(["SẢN PHẨM", "SL", "ĐƠN GIÁ", "T.TIỀN", ""])
        self.cart_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.cart_table.setColumnWidth(1, 50)
        self.cart_table.setColumnWidth(2, 110)
        self.cart_table.setColumnWidth(3, 110)
        self.cart_table.setColumnWidth(4, 45)
        self.cart_table.verticalHeader().setDefaultSectionSize(45)
        cart_lay.addWidget(self.cart_table, 1) # Thêm stretch factor 1 để bảng giỏ hàng mở rộng tối đa

        # Chọn phương thức TT
        pay_lbl = QLabel("💳 Phương thức thanh toán:")
        pay_lbl.setStyleSheet(f"color:{TEXT_MID}; font-size:13px; font-weight:800; font-family:'Nunito',sans-serif;")
        cart_lay.addWidget(pay_lbl)
        
        self.cb_payment = QComboBox()
        self.cb_payment.addItems(["Tiền mặt", "Chuyển khoản", "Thẻ tín dụng"])
        self.cb_payment.setFixedHeight(42)
        self.cb_payment.setStyleSheet(f"background:{BG_INPUT}; border:1px solid {BORDER}; border-radius:8px; padding:6px 12px; font-size:14px; font-family:'Nunito',sans-serif;")
        cart_lay.addWidget(self.cb_payment)

        # Khung Mã giảm giá
        disc_row = QHBoxLayout()
        self.cb_discount = QComboBox()
        self.cb_discount.setFixedHeight(40)
        self.cb_discount.setStyleSheet(f"background:{BG_INPUT}; border:1px solid {BORDER}; border-radius:8px; padding:0 10px; font-size:13px; font-weight:bold; font-family:'Nunito',sans-serif;")
        
        self.btn_apply_disc = primary_btn("Áp dụng", 40)
        disc_row.addWidget(self.cb_discount, 1); disc_row.addWidget(self.btn_apply_disc)
        cart_lay.addLayout(disc_row)

        # Nhãn hiển thị thông tin giảm giá
        self.lbl_disc_info = QLabel("")
        self.lbl_disc_info.setAlignment(Qt.AlignRight)
        self.lbl_disc_info.setStyleSheet(f"color:{SUCCESS}; font-size:13px; font-weight:800; font-family:'Nunito',sans-serif;")
        cart_lay.addWidget(self.lbl_disc_info)

        # Khung Tổng tiền to đùng
        tot_frame = QFrame()
        tot_frame.setStyleSheet(f"QFrame {{ background:{PRIMARY}; border:none; border-radius:12px; }}")
        tot_lay = QVBoxLayout(tot_frame)
        tot_lay.setContentsMargins(20, 16, 20, 16)
        tot_lay.setSpacing(4)
        
        t_lbl = QLabel("TỔNG CẦN THANH TOÁN")
        t_lbl.setAlignment(Qt.AlignCenter)
        t_lbl.setStyleSheet("color:rgba(255,255,255,0.8); font-size:13px; font-weight:800; font-family:'Nunito',sans-serif;")
        
        self.lbl_total = QLabel("0 ₫")
        self.lbl_total.setAlignment(Qt.AlignCenter)
        self.lbl_total.setStyleSheet("color:white; font-size:36px; font-weight:900; font-family:'Nunito',sans-serif;")
        
        tot_lay.addWidget(t_lbl)
        tot_lay.addWidget(self.lbl_total)
        cart_lay.addWidget(tot_frame)

        # Nút thanh toán khổng lồ
        self.btn_checkout = QPushButton("THANH TOÁN NGAY (F9)")
        self.btn_checkout.setFixedHeight(60)
        self.btn_checkout.setCursor(Qt.PointingHandCursor)
        self.btn_checkout.setStyleSheet(f"""
            QPushButton {{
                background:{SUCCESS}; color:white; border-radius:12px; font-size:18px; font-weight:900; font-family:'Nunito',sans-serif; letter-spacing: 1px;
            }}
            QPushButton:hover {{ background:#059669; }}
        """)
        cart_lay.addWidget(self.btn_checkout)

        right_col.addWidget(cart_card)
