"""
ReportTab — Giao diện Báo cáo & Thống kê
Thiết kế với Tab (Tổng quan | Lợi nhuận) + biểu đồ đa dạng.
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from config import *
from ui.widgets import *

def _kpi_card(title, value_widget, icon, color, bg):
    """KPI card hiện đại với icon + tiêu đề + giá trị"""
    card = QFrame()
    card.setObjectName("KpiCard")
    card.setStyleSheet(f"""
        QFrame#KpiCard {{
            background-color: #ffffff;
            border: 1.5px solid #cbd5e1;
            border-radius: 16px;
            border-left: 5px solid {color};
        }}
    """)
    
    # Thêm hiệu ứng bóng đổ cao cấp cho từng card chỉ số
    from PyQt5.QtGui import QColor
    from PyQt5.QtWidgets import QGraphicsDropShadowEffect
    shadow = QGraphicsDropShadowEffect(card)
    shadow.setBlurRadius(15)
    shadow.setOffset(0, 4)
    shadow.setColor(QColor(0, 0, 0, 15))
    card.setGraphicsEffect(shadow)
    
    lay = QVBoxLayout(card)
    lay.setContentsMargins(20, 16, 20, 16)
    lay.setSpacing(8)

    top_row = QHBoxLayout()
    t_lbl = QLabel(title)
    t_lbl.setStyleSheet(
        "color: #334155; font-size: 13px; font-weight: 800; "
        "font-family: 'Nunito', sans-serif; letter-spacing: 0.5px;"
    )
    ic_box = QFrame()
    ic_box.setFixedSize(36, 36)
    ic_box.setStyleSheet(
        f"background-color: {bg}; border-radius: 18px; border: none;"
    )
    ic_lay = QHBoxLayout(ic_box)
    ic_lay.setContentsMargins(0, 0, 0, 0)
    ic_lbl = QLabel(icon)
    ic_lbl.setAlignment(Qt.AlignCenter)
    ic_lbl.setStyleSheet(
        f"color: {color}; font-size: 18px; background: transparent; font-weight: bold;"
    )
    ic_lay.addWidget(ic_lbl)
    top_row.addWidget(t_lbl)
    top_row.addStretch()
    top_row.addWidget(ic_box)

    value_widget.setStyleSheet(
        "color: #0f172a; font-size: 26px; font-weight: 900; "
        "font-family: 'Nunito', sans-serif;"
    )
    lay.addLayout(top_row)
    lay.addWidget(value_widget)
    return card


def _kpi_group(title, cards):
    """Bọc các thẻ KPI vào một nhóm có tiêu đề"""
    group = QFrame()
    group.setStyleSheet(f"QFrame {{ background: transparent; border: none; }}")
    lay = QVBoxLayout(group)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(12)
    
    hdr = QLabel(title)
    hdr.setStyleSheet(f"color: #1e3a8a; font-size: 12px; font-weight: 900; text-transform: uppercase; letter-spacing: 1.5px;")
    lay.addWidget(hdr)
    
    row = QHBoxLayout()
    row.setSpacing(16)
    for c in cards:
        row.addWidget(c)
    lay.addLayout(row)
    return group


class ReportTab(QWidget):

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {BG_MAIN};")
        self.setup_ui()

    def setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(30, 25, 30, 25)
        root.setSpacing(20)

        # ── HEADER ──────────────────────────────────────────────────
        header = QHBoxLayout()
        title_vbox = QVBoxLayout()
        lbl_page = QLabel("PHÂN TÍCH & BÁO CÁO")
        lbl_page.setStyleSheet(f"color: {TEXT_DARK}; font-size: 20px; font-weight: 900; font-family: 'Nunito', sans-serif;")
        lbl_sub = QLabel("Theo dõi hiệu suất kinh doanh và lợi nhuận cửa hàng")
        lbl_sub.setStyleSheet(f"color: {TEXT_LIGHT}; font-size: 13px; font-weight: 600;")
        title_vbox.addWidget(lbl_page)
        title_vbox.addWidget(lbl_sub)
        
        self.btn_refresh = QPushButton(" 🔄  Làm mới dữ liệu")
        self.btn_refresh.setFixedHeight(40)
        self.btn_refresh.setCursor(Qt.PointingHandCursor)
        self.btn_refresh.setStyleSheet(f"""
            QPushButton {{
                background-color: #ffffff; color: {PRIMARY};
                border: 1.5px solid {PRIMARY}; border-radius: 10px;
                padding: 0 20px; font-weight: 800; font-size: 13px;
            }}
            QPushButton:hover {{ background-color: {PRIMARY_LIGHT}; }}
        """)

        self.btn_export = QPushButton(" 📥  Xuất Báo Cáo (Excel)")
        self.btn_export.setFixedHeight(40)
        self.btn_export.setCursor(Qt.PointingHandCursor)
        self.btn_export.setStyleSheet(f"""
            QPushButton {{
                background-color: {SUCCESS}; color: white;
                border: none; border-radius: 10px;
                padding: 0 20px; font-weight: 800; font-size: 13px;
            }}
            QPushButton:hover {{ background-color: #059669; }}
        """)

        header.addLayout(title_vbox)
        header.addStretch()
        header.addWidget(self.btn_refresh)
        header.addSpacing(10)
        header.addWidget(self.btn_export)
        root.addLayout(header)

        # ── KPI SECTION ──────────────────────────────────────────────
        kpi_main_layout = QVBoxLayout()
        kpi_main_layout.setSpacing(18)

        # Nhóm 1: Kết quả bán hàng
        self.lbl_revenue = QLabel("0 ₫")
        self.lbl_invoice = QLabel("0")
        self.lbl_refund = QLabel("0 ₫")
        
        sales_metrics = [
            _kpi_card("TỔNG DOANH THU", self.lbl_revenue, "💰", INFO, "#e0f2fe"),
            _kpi_card("TỔNG HÓA ĐƠN", self.lbl_invoice, "📄", PRIMARY, "#eff6ff"),
            _kpi_card("TIỀN HOÀN TRẢ", self.lbl_refund, "↩️", DANGER, "#fee2e2")
        ]

        # Nhóm 2: Hiệu quả tài chính
        self.lbl_cost = QLabel("0 ₫")
        self.lbl_profit = QLabel("0 ₫")
        self.lbl_margin = QLabel("0 %")
        
        finance_metrics = [
            _kpi_card("GIÁ VỐN HÀNG BÁN", self.lbl_cost, "📦", WARNING, "#fef3c7"),
            _kpi_card("LỢI NHUẬN GỘP", self.lbl_profit, "📈", SUCCESS, "#dcfce7"),
            _kpi_card("TỶ SUẤT LỢI NHUẬN", self.lbl_margin, "💹", PURPLE, "#f3e8ff")
        ]

        # Nhóm 3: Doanh thu theo thời gian
        self.lbl_revenue_today = QLabel("0 ₫")
        self.lbl_revenue_month = QLabel("0 ₫")
        self.lbl_revenue_year = QLabel("0 ₫")

        time_metrics = [
            _kpi_card("DOANH THU HÔM NAY", self.lbl_revenue_today, "📅", PRIMARY, "#eff6ff"),
            _kpi_card("THÁNG NÀY", self.lbl_revenue_month, "📆", INFO, "#e0f2fe"),
            _kpi_card("NĂM NAY", self.lbl_revenue_year, "⭐", PURPLE, "#f3e8ff")
        ]

        # Hàng 1 chứa Nhóm 1 và Nhóm 2
        row1 = QHBoxLayout()
        row1.setSpacing(25)
        row1.addWidget(_kpi_group("KẾT QUẢ BÁN HÀNG", sales_metrics), 1)
        row1.addWidget(_kpi_group("HIỆU QUẢ TÀI CHÍNH", finance_metrics), 1)
        kpi_main_layout.addLayout(row1)

        # Hàng 2 chứa Nhóm 3
        row2 = QHBoxLayout()
        row2.setSpacing(25)
        row2.addWidget(_kpi_group("DOANH THU THEO THỜI GIAN", time_metrics), 1)
        row2.addStretch(1)
        kpi_main_layout.addLayout(row2)
        
        root.addLayout(kpi_main_layout)

        # ── MAIN ANALYSIS TABS ───────────────────────────────────────
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {BORDER}; border-radius: 15px;
                background: white;
            }}
            QTabBar::tab {{
                background: transparent; color: {TEXT_LIGHT};
                padding: 12px 30px; margin-right: 5px;
                font-weight: 800; font-size: 14px;
                border-bottom: 3px solid transparent;
            }}
            QTabBar::tab:selected {{
                color: {PRIMARY}; border-bottom: 3px solid {PRIMARY};
            }}
            QTabBar::tab:hover:!selected {{
                color: {TEXT_MID};
            }}
        """)
        root.addWidget(self.tabs, 1)

        # === TAB 1: BIỂU ĐỒ & XU HƯỚNG ================================
        tab_visual = QWidget()
        vis_lay = QVBoxLayout(tab_visual)
        vis_lay.setContentsMargins(20, 20, 20, 20)
        vis_lay.setSpacing(20)

        # Bộ lọc chu kỳ thời gian
        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(0, 0, 0, 5)
        
        lbl_filter = QLabel("📅 XEM BÁO CÁO THEO:")
        lbl_filter.setStyleSheet(f"color: {TEXT_DARK}; font-size: 13px; font-weight: 800; font-family: 'Nunito', sans-serif;")
        filter_layout.addWidget(lbl_filter)
        
        self.combo_period = QComboBox()
        self.combo_period.addItems(["Từng đơn hàng", "Doanh thu theo Tuần", "Doanh thu theo Tháng", "Doanh thu theo Năm"])
        self.combo_period.setFixedWidth(220)
        self.combo_period.setFixedHeight(36)
        self.combo_period.setCursor(Qt.PointingHandCursor)
        self.combo_period.setStyleSheet(f"""
            QComboBox {{
                background-color: #ffffff;
                border: 1.5px solid {BORDER};
                border-radius: 8px;
                padding-left: 12px;
                font-weight: 700;
                color: {TEXT_DARK};
            }}
            QComboBox::drop-down {{
                border: none;
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
            }}
            QComboBox QAbstractItemView {{
                background-color: #ffffff;
                border: 1px solid {BORDER};
                selection-background-color: {PRIMARY_LIGHT};
                selection-color: {PRIMARY};
            }}
        """)
        filter_layout.addWidget(self.combo_period)
        filter_layout.addStretch()
        vis_lay.addLayout(filter_layout)

        # Hàng biểu đồ chính (Sắp xếp 3 biểu đồ song song trực quan, hiện đại)
        charts_row = QHBoxLayout()
        charts_row.setSpacing(20)

        # 1. Biểu đồ doanh thu (Area Chart)
        rev_box = QFrame()
        rev_box.setStyleSheet(f"background: #ffffff; border: 1px solid {BORDER}; border-radius: 12px;")
        rev_lay = QVBoxLayout(rev_box)
        rev_lay.setContentsMargins(15, 12, 15, 10)
        rev_lay.setSpacing(5)
        self.lbl_chart_rev_title = QLabel("📈 XU HƯỚNG DOANH THU THEO ĐƠN HÀNG")
        self.lbl_chart_rev_title.setStyleSheet(f"color: {PRIMARY_DARK}; font-size: 13px; font-weight: 800;")
        rev_lay.addWidget(self.lbl_chart_rev_title)
        self.figure_revenue = Figure(facecolor="#ffffff")
        self.canvas_revenue = FigureCanvasQTAgg(self.figure_revenue)
        rev_lay.addWidget(self.canvas_revenue)
        charts_row.addWidget(rev_box, 3) # Tỷ lệ 3

        # 2. Biểu đồ so sánh lợi nhuận ròng
        bar_box = QFrame()
        bar_box.setStyleSheet(f"background: #ffffff; border: 1px solid {BORDER}; border-radius: 12px;")
        bar_lay = QVBoxLayout(bar_box)
        bar_lay.setContentsMargins(15, 12, 15, 10)
        bar_lay.setSpacing(5)
        self.lbl_chart_bar_title = QLabel("📊 BIẾN ĐỘNG LỢI NHUẬN RÒNG")
        self.lbl_chart_bar_title.setStyleSheet(f"color: {PRIMARY_DARK}; font-size: 13px; font-weight: 800;")
        bar_lay.addWidget(self.lbl_chart_bar_title)
        self.figure_bar = Figure(facecolor="#ffffff")
        self.canvas_bar = FigureCanvasQTAgg(self.figure_bar)
        bar_lay.addWidget(self.canvas_bar)
        charts_row.addWidget(bar_box, 3) # Tỷ lệ 3

        # 3. Biểu đồ tròn cơ cấu
        pie_box = QFrame()
        pie_box.setStyleSheet(f"background: #ffffff; border: 1px solid {BORDER}; border-radius: 12px;")
        pie_lay = QVBoxLayout(pie_box)
        pie_lay.setContentsMargins(15, 12, 15, 10)
        pie_lay.setSpacing(5)
        pie_hdr = QLabel("🍩 CƠ CẤU DOANH THU")
        pie_hdr.setStyleSheet(f"color: {PRIMARY_DARK}; font-size: 13px; font-weight: 800;")
        pie_lay.addWidget(pie_hdr)
        self.figure_pie = Figure(facecolor="#ffffff")
        self.canvas_pie = FigureCanvasQTAgg(self.figure_pie)
        pie_lay.addWidget(self.canvas_pie)
        charts_row.addWidget(pie_box, 2) # Tỷ lệ 2
        
        vis_lay.addLayout(charts_row, 1)

        self.tabs.addTab(tab_visual, "  📈  PHÂN TÍCH XU HƯỚNG  ")

        # === TAB 2: CHI TIẾT SẢN PHẨM =================================
        tab_details = QWidget()
        det_lay = QHBoxLayout(tab_details)
        det_lay.setContentsMargins(20, 20, 20, 20)
        det_lay.setSpacing(25)

        # Bên trái: Danh sách Top sản phẩm & Tồn kho
        lists_col = QVBoxLayout()
        lists_col.setSpacing(20)

        # Top bán chạy
        top_box = QVBoxLayout()
        top_hdr = QLabel("🏆 TOP 5 SẢN PHẨM BÁN CHẠY")
        top_hdr.setStyleSheet(f"color: {SUCCESS}; font-size: 13px; font-weight: 900;")
        top_box.addWidget(top_hdr)
        self.tbl_top_selling = styled_table(["SẢN PHẨM", "ĐÃ BÁN", "DOANH THU"])
        self.tbl_top_selling.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tbl_top_selling.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tbl_top_selling.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        top_box.addWidget(self.tbl_top_selling)
        lists_col.addLayout(top_box)

        # Tồn kho thấp
        low_box = QVBoxLayout()
        low_hdr = QLabel("⚠️ SẢN PHẨM SẮP HẾT HÀNG")
        low_hdr.setStyleSheet(f"color: {WARNING}; font-size: 13px; font-weight: 900;")
        low_box.addWidget(low_hdr)
        self.tbl_low_stock = styled_table(["SẢN PHẨM", "TỒN", "MỨC"])
        self.tbl_low_stock.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tbl_low_stock.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tbl_low_stock.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        low_box.addWidget(self.tbl_low_stock)
        lists_col.addLayout(low_box)
        
        det_lay.addLayout(lists_col, 2)

        # Bên phải: Bảng lợi nhuận chi tiết
        profit_col = QVBoxLayout()
        prof_hdr = QLabel("💹 BẢNG KÊ LỢI NHUẬN CHI TIẾT THEO SẢN PHẨM")
        prof_hdr.setStyleSheet(f"color: {PRIMARY_DARK}; font-size: 13px; font-weight: 900;")
        profit_col.addWidget(prof_hdr)
        
        self.tbl_profit = styled_table(["SẢN PHẨM", "SL", "GIÁ BÁN", "GIÁ NHẬP", "DOANH THU", "GIÁ VỐN", "LỢI NHUẬN", "BIÊN (%)"])
        hdr = self.tbl_profit.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(1, 8):
            hdr.setSectionResizeMode(i, QHeaderView.ResizeToContents)
            
        profit_col.addWidget(self.tbl_profit)
        det_lay.addLayout(profit_col, 3)

        self.tabs.addTab(tab_details, "  📦  DỮ LIỆU CHI TIẾT  ")

        # === TAB 3: HÓA ĐƠN TRONG THÁNG ===============================
        tab_monthly_invoices = QWidget()
        m_lay = QVBoxLayout(tab_monthly_invoices)
        m_lay.setContentsMargins(20, 20, 20, 20)
        m_lay.setSpacing(15)

        # Thanh bộ lọc tháng
        m_filter_layout = QHBoxLayout()
        lbl_m_filter = QLabel("📅 CHỌN THÁNG XEM BÁO CÁO:")
        lbl_m_filter.setStyleSheet(f"color: {TEXT_DARK}; font-size: 13px; font-weight: 800; font-family: 'Nunito', sans-serif;")
        m_filter_layout.addWidget(lbl_m_filter)

        self.combo_report_month = QComboBox()
        self.combo_report_month.setFixedWidth(200)
        self.combo_report_month.setFixedHeight(36)
        self.combo_report_month.setCursor(Qt.PointingHandCursor)
        self.combo_report_month.setStyleSheet(self.combo_period.styleSheet())
        m_filter_layout.addWidget(self.combo_report_month)
        
        self.btn_export_month_invoices = QPushButton("📥 Xuất Excel Hóa Đơn Tháng")
        self.btn_export_month_invoices.setFixedHeight(36)
        self.btn_export_month_invoices.setCursor(Qt.PointingHandCursor)
        self.btn_export_month_invoices.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY}; color: white;
                border: none; border-radius: 8px;
                padding: 0 15px; font-weight: 800; font-size: 12px;
            }}
            QPushButton:hover {{ background-color: {PRIMARY_DARK}; }}
        """)
        m_filter_layout.addStretch()
        m_filter_layout.addWidget(self.btn_export_month_invoices)
        m_lay.addLayout(m_filter_layout)

        # KPI mini của tháng được chọn
        kpi_row = QHBoxLayout()
        kpi_row.setSpacing(15)
        
        self.lbl_month_rev = QLabel("0 ₫")
        self.lbl_month_cnt = QLabel("0 HĐ")
        self.lbl_month_prof = QLabel("0 ₫")
        
        kpi_row.addWidget(_kpi_card("DOANH THU THÁNG", self.lbl_month_rev, "💰", INFO, "#e0f2fe"))
        kpi_row.addWidget(_kpi_card("SỐ HÓA ĐƠN", self.lbl_month_cnt, "📄", PRIMARY, "#eff6ff"))
        kpi_row.addWidget(_kpi_card("LỢI NHUẬN THÁNG", self.lbl_month_prof, "📈", SUCCESS, "#dcfce7"))
        m_lay.addLayout(kpi_row)

        # Bảng danh sách hóa đơn trong tháng
        self.tbl_monthly_invoices = styled_table(["MÃ HĐ", "KHÁCH HÀNG", "TỔNG TIỀN", "PHƯƠNG THỨC TT", "THỜI GIAN TẠO", "TRẠNG THÁI", "THAO TÁC"])
        self.tbl_monthly_invoices.setColumnWidth(0, 80)
        self.tbl_monthly_invoices.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tbl_monthly_invoices.setColumnWidth(2, 120)
        self.tbl_monthly_invoices.setColumnWidth(3, 140)
        self.tbl_monthly_invoices.setColumnWidth(4, 180)
        self.tbl_monthly_invoices.setColumnWidth(5, 130)
        self.tbl_monthly_invoices.setColumnWidth(6, 120)
        
        m_lay.addWidget(self.tbl_monthly_invoices)

        self.tabs.addTab(tab_monthly_invoices, "  📋  HÓA ĐƠN TRONG THÁNG  ")

        # Placeholders
        self.lbl_products = QLabel()
        self.lbl_best_seller = QLabel()
