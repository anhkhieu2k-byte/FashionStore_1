from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from utils.message_utils import show_success, show_error
from modules.reports.report_service import ReportService
from config import PRIMARY, PRIMARY_DARK, TEXT_DARK, TEXT_MID, SUCCESS, WARNING, DANGER, INFO, PURPLE


# Matplotlib colour palette
_COL_REVENUE = "#2563eb"
_COL_COST    = "#f59e0b"
_COL_PROFIT  = "#10b981"


class ReportController:

    def __init__(self, ui):
        self.ui = ui
        self.refresh_data()
        self.ui.btn_refresh.clicked.connect(self.refresh_data)
        self.ui.btn_export.clicked.connect(self.export_excel)
        self.ui.combo_period.currentIndexChanged.connect(self.on_period_changed)
        
        # Connect new monthly invoices tab signals
        self.ui.combo_report_month.currentIndexChanged.connect(self.load_monthly_invoices)
        self.ui.btn_export_month_invoices.clicked.connect(self.export_selected_month_invoices)
        self.ui.tbl_monthly_invoices.cellClicked.connect(self.show_invoice_detail)

    def on_period_changed(self):
        self.load_overview_chart()
        self.load_profit_charts()

    # ── public ────────────────────────────────────────────────────────
    def refresh_data(self):
        self.load_summary()
        self.load_overview_chart()
        self.load_overview_tables()
        self.load_profit_charts()
        self.load_profit_table()
        self.populate_months()
        self.load_monthly_invoices()

    # ── KPI Cards ─────────────────────────────────────────────────────
    def load_summary(self):
        data = ReportService.get_summary()
        self.ui.lbl_revenue.setText(f"{data['revenue']:,.0f} ₫")
        self.ui.lbl_cost.setText(f"{data['total_cost']:,.0f} ₫")
        self.ui.lbl_profit.setText(f"{data['profit']:,.0f} ₫")
        self.ui.lbl_margin.setText(f"{data['profit_margin']:.1f} %")
        self.ui.lbl_invoice.setText(str(data['total_invoices']))
        self.ui.lbl_refund.setText(f"{data['total_refund']:,.0f} ₫")
        self.ui.lbl_revenue_today.setText(f"{data['revenue_today']:,.0f} ₫")
        self.ui.lbl_revenue_month.setText(f"{data['revenue_month']:,.0f} ₫")
        self.ui.lbl_revenue_year.setText(f"{data['revenue_year']:,.0f} ₫")

        # Color-code profit
        color = SUCCESS if data['profit'] >= 0 else DANGER
        self.ui.lbl_profit.setStyleSheet(
            f"color: {color}; font-size: 22px; font-weight: 900; font-family: 'Nunito', sans-serif;"
        )
        self.ui.lbl_margin.setStyleSheet(
            f"color: {color}; font-size: 22px; font-weight: 900; font-family: 'Nunito', sans-serif;"
        )

    # ── Tab 1 – Overview ──────────────────────────────────────────────
    def load_overview_chart(self):
        idx = self.ui.combo_period.currentIndex()
        if idx == 0:
            self.ui.lbl_chart_rev_title.setText("📈 XU HƯỚNG DOANH THU THEO ĐƠN HÀNG")
            chart_data = ReportService.get_chart_data() # (id, total)
            labels = [str(item[0]) for item in chart_data]
            totals = [item[1] for item in chart_data]
        elif idx == 1:
            self.ui.lbl_chart_rev_title.setText("📈 XU HƯỚNG DOANH THU THEO TUẦN")
            chart_data = ReportService.get_weekly_chart_data() # (period, revenue, cost)
            labels = [str(item[0]) for item in chart_data]
            totals = [item[1] for item in chart_data]
        elif idx == 2:
            self.ui.lbl_chart_rev_title.setText("📈 XU HƯỚNG DOANH THU THEO THÁNG")
            chart_data = ReportService.get_monthly_chart_data() # (period, revenue, cost)
            labels = [str(item[0]) for item in chart_data]
            totals = [item[1] for item in chart_data]
        else:
            self.ui.lbl_chart_rev_title.setText("📈 XU HƯỚNG DOANH THU THEO NĂM")
            chart_data = ReportService.get_yearly_chart_data() # (period, revenue, cost)
            labels = [str(item[0]) for item in chart_data]
            totals = [item[1] for item in chart_data]

        fig = self.ui.figure_revenue
        fig.clear()
        fig.patch.set_facecolor("#ffffff")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#ffffff")

        from matplotlib.ticker import FuncFormatter
        def currency_formatter(x, pos=None):
            if x >= 1_000_000:
                return f'{x/1_000_000:.1f}M'
            if x >= 1_000:
                return f'{x/1_000:.0f}K'
            return f'{x:,.0f}'

        if labels:
            ax.plot(labels, totals, color=_COL_REVENUE, linewidth=4,
                    marker='o', markersize=9,
                    markerfacecolor=PRIMARY_DARK, markeredgecolor='white',
                    markeredgewidth=2.5,
                    label="Doanh thu")
            ax.fill_between(labels, totals, alpha=0.1, color=_COL_REVENUE)

            # Thêm nhãn giá trị ngay trên các điểm mốc biểu đồ để nhìn cực rõ
            if len(labels) <= 12:
                for i, val in enumerate(totals):
                    ax.annotate(f"{currency_formatter(val)} ₫", (labels[i], totals[i]),
                                textcoords="offset points", xytext=(0, 10), ha='center',
                                fontsize=9, fontweight='black', color='#1e293b')

        ax.yaxis.set_major_formatter(FuncFormatter(currency_formatter))
        
        # Tăng kích thước tick labels để dễ nhìn hơn rất nhiều
        ax.tick_params(colors='#475569', labelsize=10)
        
        # Định dạng text nhãn trục trục hoành và tung
        for label in ax.get_xticklabels():
            label.set_fontsize(10)
            label.set_fontweight('bold')
            label.set_color('#475569')
        for label in ax.get_yticklabels():
            label.set_fontsize(10)
            label.set_fontweight('bold')
            label.set_color('#475569')
            
        if len(labels) > 6:
            ax.tick_params(axis='x', rotation=25)
            
        for spine in ax.spines.values():
            spine.set_visible(False)
            
        # Grid nét đứt tinh tế
        ax.grid(True, axis='y', color="#e2e8f0", linestyle='--', linewidth=0.8, alpha=0.7)
        
        # Tăng lề để không bị đè chữ
        fig.subplots_adjust(left=0.12, right=0.95, top=0.88, bottom=0.2)
        
        # Thiết lập khoảng biên cho trục Y để nhãn không bị tràn viền trên
        if totals:
            max_y = max(totals)
            ax.set_ylim(0, max_y * 1.25 if max_y > 0 else 1)
            
        self.ui.canvas_revenue.draw()

    def load_overview_tables(self):
        # Tồn kho thấp
        low_stock = ReportService.get_low_stock()
        self.ui.tbl_low_stock.setRowCount(0)
        for row, item in enumerate(low_stock):
            self.ui.tbl_low_stock.insertRow(row)
            for col, val in enumerate(item):
                cell = QTableWidgetItem(str(val))
                cell.setTextAlignment(Qt.AlignCenter)
                self.ui.tbl_low_stock.setItem(row, col, cell)
                if col == 1 and int(val) <= 5:
                    cell.setForeground(QColor(DANGER))

        # Top bán chạy
        top_selling = ReportService.get_top_selling()
        self.ui.tbl_top_selling.setRowCount(0)
        for row, item in enumerate(top_selling):
            self.ui.tbl_top_selling.insertRow(row)
            self.ui.tbl_top_selling.setItem(row, 0, QTableWidgetItem(str(item[0])))
            qty = QTableWidgetItem(f"{item[1]}")
            qty.setTextAlignment(Qt.AlignCenter)
            self.ui.tbl_top_selling.setItem(row, 1, qty)
            rev = QTableWidgetItem(f"{item[2]:,.0f} ₫")
            rev.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.ui.tbl_top_selling.setItem(row, 2, rev)

    # ── Tab 2 – Profit ────────────────────────────────────────────────
    def load_profit_charts(self):
        idx = self.ui.combo_period.currentIndex()
        if idx == 0:
            self.ui.lbl_chart_bar_title.setText("📊 BIẾN ĐỘNG LỢI NHUẬN RÒNG")
            data = ReportService.get_profit_chart_data()   # (id, revenue, cost)
            labels = [str(d[0]) for d in data]
            revenues = [d[1] for d in data]
            costs = [d[2] for d in data]
        elif idx == 1:
            self.ui.lbl_chart_bar_title.setText("📊 LỢI NHUẬN RÒNG THEO TUẦN")
            data = ReportService.get_weekly_chart_data()   # (period, revenue, cost)
            labels = [str(d[0]) for d in data]
            revenues = [d[1] for d in data]
            costs = [d[2] for d in data]
        elif idx == 2:
            self.ui.lbl_chart_bar_title.setText("📊 LỢI NHUẬN RÒNG THEO THÁNG")
            data = ReportService.get_monthly_chart_data()   # (period, revenue, cost)
            labels = [str(d[0]) for d in data]
            revenues = [d[1] for d in data]
            costs = [d[2] for d in data]
        else:
            self.ui.lbl_chart_bar_title.setText("📊 LỢI NHUẬN RÒNG THEO NĂM")
            data = ReportService.get_yearly_chart_data()   # (period, revenue, cost)
            labels = [str(d[0]) for d in data]
            revenues = [d[1] for d in data]
            costs = [d[2] for d in data]

        if not labels:
            return

        x = range(len(labels))

        # --- Profit Bar Chart ---
        fig_bar = self.ui.figure_bar
        fig_bar.clear()
        fig_bar.patch.set_facecolor("#ffffff")
        ax = fig_bar.add_subplot(111)
        ax.set_facecolor("#ffffff")

        # Calculate Net Profit for each order/period
        net_profits = [r - c for r, c in zip(revenues, costs)]
        
        # Color: Green if positive, Red if negative
        bar_colors = [_COL_PROFIT if p >= 0 else "#ef4444" for p in net_profits]

        # Tăng chiều rộng cột lên 0.55 và bo góc hoặc thiết kế thanh mảnh hơn
        ax.bar(x, net_profits, width=0.55, color=bar_colors, alpha=0.9, edgecolor='none')

        ax.set_xticks(list(x))
        ax.set_xticklabels(labels)
        
        from matplotlib.ticker import FuncFormatter
        def currency_formatter(x, pos=None):
            if abs(x) >= 1_000_000: return f'{x/1_000_000:.1f}M'
            if abs(x) >= 1_000: return f'{x/1_000:.0f}K'
            return f'{x:,.0f}'
            
        ax.yaxis.set_major_formatter(FuncFormatter(currency_formatter))
        
        # Hiển thị số liệu trực quan trên đầu/dưới chân mỗi cột bar để nhìn rõ 100%
        if len(labels) <= 12:
            for i, val in enumerate(net_profits):
                if val != 0:
                    offset = 8 if val >= 0 else -16
                    va_dir = 'bottom' if val >= 0 else 'top'
                    text_color = '#065f46' if val >= 0 else '#991b1b'
                    ax.annotate(f"{currency_formatter(val)} ₫", 
                                (i, val),
                                textcoords="offset points", xytext=(0, offset), ha='center',
                                fontsize=9, fontweight='black', color=text_color)

        # Định dạng font chữ của ticks cho rõ nét hơn
        ax.tick_params(colors='#475569', labelsize=10)
        for label in ax.get_xticklabels():
            label.set_fontsize(10)
            label.set_fontweight('bold')
            label.set_color('#475569')
        for label in ax.get_yticklabels():
            label.set_fontsize(10)
            label.set_fontweight('bold')
            label.set_color('#475569')

        if len(labels) > 6:
            ax.tick_params(axis='x', rotation=25)

        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.axhline(0, color='#94a3b8', linewidth=1.2, alpha=0.8) # Zero line đậm nét hơn
        ax.grid(True, axis='y', color="#e2e8f0", linestyle='--', linewidth=0.8, alpha=0.7)
        
        # Nới rộng biên Y để chừa khoảng trống cho nhãn text trên cột
        if net_profits:
            min_y, max_y = min(net_profits), max(net_profits)
            span = max_y - min_y
            if span == 0: span = 100000
            ax.set_ylim(min_y - 0.25 * span, max_y + 0.25 * span)
            
        fig_bar.subplots_adjust(left=0.12, right=0.95, top=0.88, bottom=0.2)
        self.ui.canvas_bar.draw()

        # --- Donut chart ---
        summary = ReportService.get_summary()
        total_rev  = summary['revenue']
        total_cost = summary['total_cost']
        total_prof = summary['profit']

        fig_pie = self.ui.figure_pie
        fig_pie.clear()
        fig_pie.patch.set_facecolor("#ffffff")
        ax2 = fig_pie.add_subplot(111)

        if total_rev > 0:
            sizes  = [max(total_cost, 0), max(total_prof, 0)]
            labels_pie = ["Giá vốn", "Lợi nhuận"]
            colors_pie = [_COL_COST, _COL_PROFIT]
            
            # Use only non-zero values for pie
            filtered_data = [(s, l, c) for s, l, c in zip(sizes, labels_pie, colors_pie) if s > 0]
            if filtered_data:
                s_vals, l_vals, c_vals = zip(*filtered_data)
                
                # Donut với viền dày hơn, màu sắc sang xịn
                wedges, texts = ax2.pie(
                    s_vals, labels=None, colors=c_vals, autopct=None,
                    startangle=90,
                    wedgeprops=dict(width=0.35, edgecolor='white', linewidth=3)
                )
                
                # Hiển thị số liệu tổng doanh thu ngay tại tâm của Donut Chart
                total_text = f"Tổng cộng\n{currency_formatter(total_rev)} ₫"
                ax2.text(0, 0, total_text, ha='center', va='center',
                         fontsize=11, fontweight='black', color='#0f172a',
                         linespacing=1.4)
                
                # Tính toán tỷ lệ phần trăm và hiển thị kèm theo chú thích Legend bên phải
                total_vals = sum(s_vals)
                legend_labels = []
                for l, s in zip(l_vals, s_vals):
                    pct = (s / total_vals * 100) if total_vals else 0
                    legend_labels.append(f"{l}: {s:,.0f} ₫ ({pct:.1f}%)")
                
                ax2.legend(
                    wedges, legend_labels,
                    loc="upper center",
                    bbox_to_anchor=(0.5, -0.05),
                    ncol=1,
                    frameon=False,
                    fontsize=9.5
                )
                
            else:
                ax2.text(0.5, 0.5, "Không có dữ liệu", ha='center', va='center', fontsize=11, fontweight='bold')
        else:
            ax2.text(0.5, 0.5, "Chưa có doanh thu", ha='center', va='center', color=TEXT_MID, fontsize=11, fontweight='bold')
            
        ax2.set_axis_off()
        fig_pie.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.28)
        self.ui.canvas_pie.draw()

    def load_profit_table(self):
        data = ReportService.get_profit_by_product()
        tbl = self.ui.tbl_profit
        tbl.setRowCount(0)
        for row_idx, item in enumerate(data):
            name, qty, price, imp_price, revenue, cost, profit = item
            margin = (profit / revenue * 100) if revenue else 0

            tbl.insertRow(row_idx)

            def _cell(text, align=Qt.AlignCenter):
                c = QTableWidgetItem(str(text))
                c.setTextAlignment(align)
                return c

            # Cols: ["SẢN PHẨM", "SL", "GIÁ BÁN", "GIÁ NHẬP", "DOANH THU", "GIÁ VỐN", "LỢI NHUẬN", "BIÊN (%)"]
            tbl.setItem(row_idx, 0, _cell(name, Qt.AlignLeft | Qt.AlignVCenter))
            tbl.setItem(row_idx, 1, _cell(f"{qty}"))
            tbl.setItem(row_idx, 2, _cell(f"{price:,.0f} ₫", Qt.AlignRight | Qt.AlignVCenter))
            tbl.setItem(row_idx, 3, _cell(f"{imp_price:,.0f} ₫", Qt.AlignRight | Qt.AlignVCenter))
            tbl.setItem(row_idx, 4, _cell(f"{revenue:,.0f} ₫", Qt.AlignRight | Qt.AlignVCenter))
            tbl.setItem(row_idx, 5, _cell(f"{cost:,.0f} ₫", Qt.AlignRight | Qt.AlignVCenter))

            profit_cell = _cell(f"{profit:,.0f} ₫", Qt.AlignRight | Qt.AlignVCenter)
            profit_cell.setForeground(QColor(_COL_PROFIT if profit >= 0 else "#ef4444"))
            tbl.setItem(row_idx, 6, profit_cell)

            margin_cell = _cell(f"{margin:.1f} %")
            margin_cell.setForeground(QColor(_COL_PROFIT if margin >= 30 else (
                "#f59e0b" if margin >= 10 else "#ef4444")))
            tbl.setItem(row_idx, 7, margin_cell)

    # ── Export ────────────────────────────────────────────────────────
    def export_excel(self):
        try:
            # Định nghĩa QDialog tùy chỉnh trực tiếp để hiển thị 2 nút bấm cực kỳ trực quan
            from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
            from PyQt5.QtCore import Qt

            class ReportTypeDialog(QDialog):
                def __init__(self, parent=None):
                    super().__init__(parent)
                    self.setWindowTitle("Chọn Loại Báo Cáo")
                    self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
                    self.selected_type = None
                    
                    # Layout chính
                    layout = QVBoxLayout()
                    layout.setContentsMargins(24, 24, 24, 24)
                    layout.setSpacing(20)
                    
                    # Nhãn mô tả
                    label = QLabel("Vui lòng chọn loại báo cáo bạn muốn xuất:")
                    label.setStyleSheet("color: #1e293b; font-size: 14px; font-weight: 600; margin-bottom: 5px;")
                    layout.addWidget(label)
                    
                    # Layout chứa 2 nút bấm
                    btn_layout = QHBoxLayout()
                    btn_layout.setSpacing(16)
                    
                    # Nút báo cáo theo Tháng
                    self.btn_month = QPushButton("📅 Báo cáo theo Tháng")
                    self.btn_month.setStyleSheet("""
                        QPushButton {
                            background-color: #0284c7;
                            color: #ffffff;
                            border: none;
                            border-radius: 8px;
                            padding: 14px 22px;
                            font-size: 13px;
                            font-weight: bold;
                            min-width: 160px;
                        }
                        QPushButton:hover {
                            background-color: #0369a1;
                        }
                    """)
                    self.btn_month.clicked.connect(self.choose_month)
                    btn_layout.addWidget(self.btn_month)
                    
                    # Nút báo cáo theo Năm
                    self.btn_year = QPushButton("📆 Báo cáo theo Năm")
                    self.btn_year.setStyleSheet("""
                        QPushButton {
                            background-color: #0d9488;
                            color: #ffffff;
                            border: none;
                            border-radius: 8px;
                            padding: 14px 22px;
                            font-size: 13px;
                            font-weight: bold;
                            min-width: 160px;
                        }
                        QPushButton:hover {
                            background-color: #0f766e;
                        }
                    """)
                    self.btn_year.clicked.connect(self.choose_year)
                    btn_layout.addWidget(self.btn_year)
                    
                    layout.addLayout(btn_layout)
                    
                    # Nút Hủy ở dưới
                    cancel_layout = QHBoxLayout()
                    cancel_layout.addStretch()
                    self.btn_cancel = QPushButton("Hủy")
                    self.btn_cancel.setStyleSheet("""
                        QPushButton {
                            background-color: #f1f5f9;
                            color: #475569;
                            border: 1px solid #cbd5e1;
                            border-radius: 6px;
                            padding: 6px 16px;
                            font-size: 12px;
                            font-weight: 600;
                            min-width: 70px;
                        }
                        QPushButton:hover {
                            background-color: #e2e8f0;
                        }
                    """)
                    self.btn_cancel.clicked.connect(self.reject)
                    cancel_layout.addWidget(self.btn_cancel)
                    layout.addLayout(cancel_layout)
                    
                    self.setLayout(layout)
                    self.setStyleSheet("background-color: #ffffff;")
                    
                def choose_month(self):
                    self.selected_type = "Báo cáo theo Tháng"
                    self.accept()
                    
                def choose_year(self):
                    self.selected_type = "Báo cáo theo Năm"
                    self.accept()

            # Hiển thị Custom Dialog
            type_dialog = ReportTypeDialog(self.ui)
            if not type_dialog.exec_():
                return
            selected_type = type_dialog.selected_type
            
            # Khởi tạo style chung cho combobox tiếp theo
            sub_dialog_style = """
                QInputDialog {
                    background-color: #ffffff;
                }
                QLabel {
                    color: #1e293b;
                    font-size: 13px;
                    font-weight: 600;
                }
                QComboBox {
                    background-color: #f8fafc;
                    border: 2px solid #cbd5e1;
                    border-radius: 6px;
                    padding: 8px 12px;
                    color: #0f172a;
                    font-size: 13px;
                    min-width: 280px;
                }
                QPushButton {
                    background-color: #0284c7;
                    color: #ffffff;
                    border: 2px solid #0284c7;
                    border-radius: 6px;
                    padding: 8px 18px;
                    font-size: 13px;
                    font-weight: bold;
                    min-width: 90px;
                }
                QPushButton:hover {
                    background-color: #0369a1;
                    border-color: #0369a1;
                }
            """
            
            from PyQt5.QtWidgets import QInputDialog
            if selected_type == "Báo cáo theo Tháng":
                months = ReportService.get_available_months()
                if not months:
                    show_error(self.ui, "Lỗi", "Chưa có dữ liệu hóa đơn nào để xuất báo cáo!")
                    return
                options = ["Tất cả các tháng"] + months
                
                dialog = QInputDialog(self.ui)
                dialog.setWindowTitle("Chọn Tháng Báo Cáo")
                dialog.setLabelText("Vui lòng chọn tháng bạn muốn xuất báo cáo Excel:")
                dialog.setComboBoxItems(options)
                dialog.setComboBoxEditable(False)
                dialog.setStyleSheet(sub_dialog_style)
                
                if not dialog.exec_():
                    return
                selected = dialog.textValue()
                
                if selected == "Tất cả các tháng":
                    # Xuất báo cáo tổng hợp
                    file_path = ReportService.export_excel(None)
                    file_name = file_path.replace("\\", "/").split("/")[-1]
                    
                    # Xuất báo cáo riêng lẻ cho từng tháng
                    for m in months:
                        ReportService.export_excel(m)
                    
                    months_str = ", ".join(months)
                    show_success(
                        self.ui, "Thành công",
                        f"Đã xuất báo cáo thành công!<br><br>"
                        f"• Báo cáo tổng hợp: <b>{file_name}</b><br>"
                        f"• Báo cáo riêng từng tháng: <b>{months_str}</b><br><br>"
                        f"<b>Thư mục:</b> exports/excel_reports/"
                    )
                else:
                    file_path = ReportService.export_excel(selected)
                    file_name = file_path.replace("\\", "/").split("/")[-1]
                    show_success(
                        self.ui, "Thành công",
                        f"Đã xuất báo cáo thành công cho <b>{selected}</b>!<br><br>"
                        f"<b>File:</b> {file_name}<br><b>Thư mục:</b> exports/excel_reports/"
                    )
            else: # Báo cáo theo Năm
                years = ReportService.get_available_years()
                if not years:
                    show_error(self.ui, "Lỗi", "Chưa có dữ liệu hóa đơn nào để xuất báo cáo!")
                    return
                options = ["Tất cả các năm"] + years
                
                dialog = QInputDialog(self.ui)
                dialog.setWindowTitle("Chọn Năm Báo Cáo")
                dialog.setLabelText("Vui lòng chọn năm bạn muốn xuất báo cáo Excel:")
                dialog.setComboBoxItems(options)
                dialog.setComboBoxEditable(False)
                dialog.setStyleSheet(sub_dialog_style)
                
                if not dialog.exec_():
                    return
                selected = dialog.textValue()
                
                if selected == "Tất cả các năm":
                    # Xuất báo cáo tổng hợp
                    file_path = ReportService.export_excel(None)
                    file_name = file_path.replace("\\", "/").split("/")[-1]
                    
                    # Xuất báo cáo riêng lẻ cho từng năm
                    for y in years:
                        ReportService.export_excel(y)
                    
                    years_str = ", ".join(years)
                    show_success(
                        self.ui, "Thành công",
                        f"Đã xuất báo cáo thành công!<br><br>"
                        f"• Báo cáo tổng hợp: <b>{file_name}</b><br>"
                        f"• Báo cáo riêng từng năm: <b>{years_str}</b><br><br>"
                        f"<b>Thư mục:</b> exports/excel_reports/"
                    )
                else:
                    file_path = ReportService.export_excel(selected)
                    file_name = file_path.replace("\\", "/").split("/")[-1]
                    show_success(
                        self.ui, "Thành công",
                        f"Đã xuất báo cáo thành công cho năm <b>{selected}</b>!<br><br>"
                        f"<b>File:</b> {file_name}<br><b>Thư mục:</b> exports/excel_reports/"
                    )
        except Exception as e:
            show_error(self.ui, "Lỗi", f"Không thể xuất file: {str(e)}")

    def populate_months(self):
        self.ui.combo_report_month.blockSignals(True)
        self.ui.combo_report_month.clear()
        months = ReportService.get_available_months()
        self.ui.combo_report_month.addItems(months)
        self.ui.combo_report_month.blockSignals(False)

    def load_monthly_invoices(self):
        month = self.ui.combo_report_month.currentText()
        if not month:
            self.ui.tbl_monthly_invoices.setRowCount(0)
            self.ui.lbl_month_rev.setText("0 ₫")
            self.ui.lbl_month_cnt.setText("0 HĐ")
            self.ui.lbl_month_prof.setText("0 ₫")
            return
            
        # Load mini KPIs
        monthly_summary = ReportService.get_monthly_summary(month)
        self.ui.lbl_month_rev.setText(f"{monthly_summary['revenue']:,.0f} ₫")
        self.ui.lbl_month_cnt.setText(f"{monthly_summary['total_invoices']} HĐ")
        self.ui.lbl_month_prof.setText(f"{monthly_summary['profit']:,.0f} ₫")
        
        # Color-code monthly profit
        color = SUCCESS if monthly_summary['profit'] >= 0 else DANGER
        self.ui.lbl_month_prof.setStyleSheet(
            f"color: {color}; font-size: 26px; font-weight: 900; font-family: 'Nunito', sans-serif;"
        )
        
        # Load Table
        invoices = ReportService.get_invoices_by_month(month)
        self.ui.tbl_monthly_invoices.setRowCount(0)
        from PyQt5.QtGui import QColor
        for row_index, invoice in enumerate(invoices):
            self.ui.tbl_monthly_invoices.insertRow(row_index)
            
            status_val = str(invoice[5]) if (len(invoice) > 5 and invoice[5]) else "Đã thanh toán"
            
            # Format data
            cells = [
                f"HD{invoice[0]:03d}",
                str(invoice[1]),
                f"{invoice[2]:,.0f} ₫",
                str(invoice[3]),
                str(invoice[4]),
                status_val
            ]
            
            for col_index, text in enumerate(cells):
                item = QTableWidgetItem(text)
                if col_index in [0, 3, 4, 5]:
                    item.setTextAlignment(Qt.AlignCenter)
                elif col_index == 2:
                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                else:
                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                    
                if col_index == 0:
                    item.setData(Qt.UserRole, invoice[0])
                    
                # Decoration
                if col_index == 5:
                    if text == "Đã hoàn tiền":
                        item.setForeground(QColor("#ef4444"))
                        item.setBackground(QColor("#fdf0ef"))
                    elif text == "Hoàn tiền một phần":
                        item.setForeground(QColor("#f97316"))
                        item.setBackground(QColor("#fff7ed"))
                    else:
                        item.setForeground(QColor("#059669"))
                        item.setBackground(QColor("#ecfdf5"))
                        
                self.ui.tbl_monthly_invoices.setItem(row_index, col_index, item)
                
            # Detail button
            btn_item = QTableWidgetItem("🔍 Xem chi tiết")
            btn_item.setForeground(Qt.blue)
            btn_item.setTextAlignment(Qt.AlignCenter)
            self.ui.tbl_monthly_invoices.setItem(row_index, 6, btn_item)

    def show_invoice_detail(self, row, col):
        item_id = self.ui.tbl_monthly_invoices.item(row, 0)
        if not item_id:
            return
            
        real_id = item_id.data(Qt.UserRole)
        
        summary_data = (
            self.ui.tbl_monthly_invoices.item(row, 0).text(),
            self.ui.tbl_monthly_invoices.item(row, 1).text(),
            self.ui.tbl_monthly_invoices.item(row, 2).text(),
            self.ui.tbl_monthly_invoices.item(row, 3).text(),
            self.ui.tbl_monthly_invoices.item(row, 4).text()
        )
        
        from ui.dialogs.invoice_detail_dialog import InvoiceDetailDialog
        dlg = InvoiceDetailDialog(self.ui, invoice_id=real_id, summary_data=summary_data)
        dlg.exec_()

    def export_selected_month_invoices(self):
        month = self.ui.combo_report_month.currentText()
        if not month:
            show_error(self.ui, "Lỗi", "Không có tháng nào được chọn!")
            return
            
        try:
            file_path = ReportService.export_excel(month)
            file_name = file_path.replace("\\", "/").split("/")[-1]
            show_success(
                self.ui, "Thành công",
                f"Đã xuất báo cáo và hóa đơn thành công cho <b>{month}</b>!<br><br>"
                f"<b>File:</b> {file_name}<br><b>Thư mục:</b> exports/excel_reports/"
            )
        except Exception as e:
            show_error(self.ui, "Lỗi", f"Không thể xuất file: {str(e)}")
