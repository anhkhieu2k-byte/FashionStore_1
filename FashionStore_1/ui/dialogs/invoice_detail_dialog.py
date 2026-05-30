"""
InvoiceDetailDialog — Cửa sổ hiển thị chi tiết hóa đơn
Thiết kế phẳng cao cấp (Sky Blue), bo góc sang trọng.
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from config import *
from ui.widgets import primary_btn, secondary_btn, styled_table
from database.db_connect import get_connection

class InvoiceDetailDialog(QDialog):

    def __init__(self, parent=None, invoice_id=None, summary_data=None):
        super().__init__(parent)
        self.invoice_id = invoice_id
        # summary_data = (id_str, customer_name, total_str, payment_method, created_at)
        self.summary_data = summary_data 
        self.setWindowTitle(f"Chi tiết hóa đơn {summary_data[0]}" if summary_data else "Chi tiết hóa đơn")
        self.setFixedSize(720, 550)
        self.setStyleSheet(f"""
            QDialog {{ background-color: {BG_CARD}; border-radius: 16px; }}
            QLabel {{ font-family: 'Nunito', sans-serif; color: {TEXT_DARK}; }}
        """)
        self.setup_ui()
        self.invoice_data = self.fetch_invoice_data()
        self.update_header_info()
        self.load_details()

    def fetch_invoice_data(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM invoices WHERE id = ?", (self.invoice_id,))
        row = cursor.fetchone()
        conn.close()
        return row

    def update_header_info(self):
        if not self.invoice_data:
            return
        
        # row: (id, customer_name, total, payment_method, discount_code, discount_amount, created_at, status)
        data = self.invoice_data
        cust_name = data[1]
        total = data[2]
        pay_method = data[3]
        disc_code = data[4]
        disc_amount = data[5]
        created_at = data[6]
        status = data[7] if len(data) > 7 else "Đã thanh toán"
        
        self.lbl_cust.setText(str(cust_name))
        self.lbl_pay.setText(str(pay_method))
        self.lbl_total_val.setText(f"{total:,.0f} ₫")
        self.lbl_time.setText(f"Ngày tạo: {created_at}")
        
        # Cập nhật và trang trí trạng thái
        self.lbl_status.setText(str(status))
        if status == "Đã hoàn tiền":
            self.lbl_status.setStyleSheet("color: #ef4444; font-size: 14px; font-weight: 800;")
        elif status == "Hoàn tiền một phần":
            self.lbl_status.setStyleSheet("color: #f97316; font-size: 14px; font-weight: 800;")
        else:
            self.lbl_status.setStyleSheet("color: #059669; font-size: 14px; font-weight: 800;")
        
        if disc_code:
            self.lbl_disc.setText(f"{disc_code} (-{disc_amount:,.0f} ₫)")
            self.lbl_disc.setVisible(True)
            self.lbl_disc_title.setVisible(True)
        else:
            self.lbl_disc.setVisible(False)
            self.lbl_disc_title.setVisible(False)

    def setup_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(16)

        # ── Header ──────────────────────────────────────────────
        header = QHBoxLayout()
        lbl_title = QLabel(f"CHI TIẾT HÓA ĐƠN {self.summary_data[0]}")
        lbl_title.setStyleSheet(f"color: {PRIMARY_DARK}; font-size: 20px; font-weight: 900;")
        
        self.lbl_time = QLabel(f"Ngày tạo: {self.summary_data[4]}")
        self.lbl_time.setStyleSheet(f"color: {TEXT_MID}; font-size: 13px; font-weight: 600;")
        
        header.addWidget(lbl_title)
        header.addStretch()
        header.addWidget(self.lbl_time)
        lay.addLayout(header)

        # Đường kẻ ngang
        line = QFrame()
        line.setFixedHeight(2)
        line.setStyleSheet(f"background-color: {PRIMARY_LIGHT};")
        lay.addWidget(line)

        # ── Info box ────────────────────────────────────────────
        info_grid = QGridLayout()
        info_grid.setSpacing(10)
        
        def bold_lbl(text):
            l = QLabel(text)
            l.setStyleSheet("font-weight: 800; font-size: 14px;")
            return l

        def val_lbl(text, color=TEXT_DARK, size=14, bold=False):
            l = QLabel(text)
            w = "800" if bold else "500"
            l.setStyleSheet(f"color: {color}; font-size: {size}px; font-weight: {w};")
            return l

        info_grid.addWidget(bold_lbl("Khách hàng:"), 0, 0)
        self.lbl_cust = val_lbl(self.summary_data[1], bold=True)
        info_grid.addWidget(self.lbl_cust, 0, 1)
        
        info_grid.addWidget(bold_lbl("Phương thức TT:"), 1, 0)
        self.lbl_pay = val_lbl(self.summary_data[3])
        info_grid.addWidget(self.lbl_pay, 1, 1)

        info_grid.addWidget(bold_lbl("Trạng thái:"), 2, 0)
        self.lbl_status = val_lbl("Đã thanh toán", bold=True)
        info_grid.addWidget(self.lbl_status, 2, 1)

        info_grid.addWidget(bold_lbl("Tổng thanh toán:"), 0, 2)
        self.lbl_total_val = val_lbl(self.summary_data[2], color=SUCCESS, size=16, bold=True)
        info_grid.addWidget(self.lbl_total_val, 0, 3)
        
        self.lbl_disc_title = bold_lbl("Mã giảm giá:")
        self.lbl_disc = val_lbl("", color=PRIMARY, bold=True)
        info_grid.addWidget(self.lbl_disc_title, 1, 2)
        info_grid.addWidget(self.lbl_disc, 1, 3)

        lay.addLayout(info_grid)
        lay.addSpacing(6)

        # ── Table chi tiết sản phẩm ─────────────────────────────
        lbl_sub = QLabel("Danh sách mặt hàng:")
        lbl_sub.setStyleSheet(f"color: {TEXT_MID}; font-weight: 800; font-size: 13px; text-transform: uppercase;")
        lay.addWidget(lbl_sub)

        self.table = styled_table(["SẢN PHẨM", "SIZE", "MÀU SẮC", "SỐ LƯỢNG", "ĐƠN GIÁ", "THÀNH TIỀN"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setColumnWidth(1, 70)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 110)
        self.table.setColumnWidth(5, 120)
        lay.addWidget(self.table)

        # ── Nút bấm ─────────────────────────────────────────────
        btn_box = QHBoxLayout()
        self.btn_print = primary_btn("🖨 In hóa đơn", 42)
        self.btn_print.setStyleSheet("""
            QPushButton {
                background-color: #0284c7; color: white; border: none; border-radius: 8px;
                padding: 0 20px; font-weight: bold; font-size: 14px;
            }
            QPushButton:hover { background-color: #0369a1; }
        """)
        
        self.btn_close = secondary_btn("Đóng", 42)
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9; color: #334155; border: 1px solid #cbd5e1;
                border-radius: 8px; padding: 0 20px; font-weight: bold; font-size: 14px;
            }
            QPushButton:hover { background-color: #e2e8f0; color: #0f172a; }
        """)

        self.btn_print.clicked.connect(self.print_invoice)
        self.btn_close.clicked.connect(self.accept)

        btn_box.addWidget(self.btn_print)
        btn_box.addStretch()
        btn_box.addWidget(self.btn_close)
        lay.addLayout(btn_box)

    def parse_name_size_color(self, full_name):
        import re
        match = re.search(r'\s*\(([^)]+)\)\s*$', full_name)
        if match:
            content = match.group(1)
            clean_name = full_name[:match.start()].strip()
            
            size = "—"
            color = "—"
            
            parts = [p.strip() for p in content.split(",") if p.strip()]
            for part in parts:
                if "Size:" in part:
                    size = part.replace("Size:", "").strip()
                elif "Màu:" in part:
                    color = part.replace("Màu:", "").strip()
                else:
                    if part in ["S", "M", "L", "XL", "XXL", "F", "Freesize"] or part.isdigit():
                        size = part
                    else:
                        color = part
            return clean_name, size, color
            
        clean_name = full_name.strip()
        size = "—"
        color = "—"
        
        lower_name = clean_name.lower()
        for col in ["trắng", "đen", "xanh", "đỏ", "be", "kem", "xám", "vàng", "hồng", "tím"]:
            if col in lower_name:
                color = col.capitalize()
                if col == "xanh":
                    if "navy" in lower_name:
                        color = "Xanh navy"
                    elif "dương" in lower_name:
                        color = "Xanh dương"
                    elif "rêu" in lower_name:
                        color = "Xanh rêu"
                break
                
        return clean_name, size, color

    def load_details(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT product_name, quantity, price, subtotal
            FROM invoice_details
            WHERE invoice_id = ?
        """, (self.invoice_id,))
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(0)
        for r_idx, row in enumerate(rows):
            self.table.insertRow(r_idx)
            
            p_name = str(row[0])
            qty = int(row[1])
            price = float(row[2])
            subtotal = float(row[3])

            clean_name, size, color = self.parse_name_size_color(p_name)

            def item(text, align=Qt.AlignLeft):
                it = QTableWidgetItem(str(text))
                it.setTextAlignment(Qt.AlignVCenter | align)
                return it

            self.table.setItem(r_idx, 0, item(clean_name))
            self.table.setItem(r_idx, 1, item(size, Qt.AlignCenter))
            self.table.setItem(r_idx, 2, item(color, Qt.AlignCenter))
            self.table.setItem(r_idx, 3, item(qty, Qt.AlignCenter))
            self.table.setItem(r_idx, 4, item(f"{price:,.0f} ₫", Qt.AlignRight))
            self.table.setItem(r_idx, 5, item(f"{subtotal:,.0f} ₫", Qt.AlignRight))

    def generate_pdf_invoice(self):
        import os
        from PyQt5.QtPrintSupport import QPrinter
        from PyQt5.QtGui import QTextDocument

        # 1. Khởi tạo thư mục exports/invoices nếu chưa có
        export_dir = os.path.join(os.getcwd(), "exports", "invoices")
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)

        pdf_path = os.path.join(export_dir, f"invoice_{self.summary_data[0]}.pdf")

        # 2. Lấy chi tiết sản phẩm từ database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT product_name, quantity, price, subtotal
            FROM invoice_details
            WHERE invoice_id = ?
        """, (self.invoice_id,))
        rows = cursor.fetchall()
        conn.close()

        # 3. Thông tin chung từ hóa đơn gốc
        inv_id = self.invoice_data[0]
        cust_name = self.invoice_data[1]
        total = self.invoice_data[2]
        pay_method = self.invoice_data[3]
        disc_code = self.invoice_data[4]
        disc_amount = self.invoice_data[5]
        created_at = self.invoice_data[6]

        # 4. Tạo bảng sản phẩm dạng HTML
        table_rows_html = ""
        for idx, row in enumerate(rows):
            p_name = str(row[0])
            qty = int(row[1])
            price = float(row[2])
            subtotal = float(row[3])
            
            clean_name, size, color = self.parse_name_size_color(p_name)
            
            table_rows_html += f"""
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #e2e8f0; text-align: left;">{clean_name}</td>
                <td style="padding: 8px; border-bottom: 1px solid #e2e8f0; text-align: center;">{size}</td>
                <td style="padding: 8px; border-bottom: 1px solid #e2e8f0; text-align: center;">{color}</td>
                <td style="padding: 8px; border-bottom: 1px solid #e2e8f0; text-align: center;">{qty}</td>
                <td style="padding: 8px; border-bottom: 1px solid #e2e8f0; text-align: right;">{price:,.0f} ₫</td>
                <td style="padding: 8px; border-bottom: 1px solid #e2e8f0; text-align: right; font-weight: bold;">{subtotal:,.0f} ₫</td>
            </tr>
            """

        discount_section = ""
        if disc_code:
            discount_section = f"""
            <div style="margin-top: 10px; text-align: right; font-size: 14px; color: #475569;">
                Mã ưu đãi: <span style="font-weight: bold; color: #2563eb;">{disc_code}</span> &nbsp;&nbsp;|&nbsp;&nbsp; 
                Đã giảm: <span style="font-weight: bold; color: #ef4444;">-{disc_amount:,.0f} ₫</span>
            </div>
            """

        html_content = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: 'Nunito', 'Segoe UI', sans-serif;
                    color: #1e293b;
                    margin: 40px;
                }}
                .header {{
                    border-bottom: 3px solid #2563eb;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }}
                .title {{
                    font-size: 28px;
                    font-weight: 900;
                    color: #1e3a8a;
                    margin: 0;
                    text-transform: uppercase;
                }}
                .subtitle {{
                    font-size: 14px;
                    color: #64748b;
                    margin-top: 5px;
                }}
                .info-table {{
                    width: 100%;
                    margin-bottom: 30px;
                    font-size: 14px;
                }}
                .info-table td {{
                    padding: 4px 0;
                    vertical-align: top;
                }}
                .items-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 30px;
                    font-size: 13px;
                }}
                .items-table th {{
                    background-color: #eff6ff;
                    color: #1d4ed8;
                    font-weight: 800;
                    text-transform: uppercase;
                    padding: 10px 8px;
                    border-bottom: 2px solid #cbd5e1;
                    text-align: left;
                }}
                .total-box {{
                    background-color: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 8px;
                    padding: 15px 20px;
                    float: right;
                    width: 300px;
                    font-size: 15px;
                }}
                .footer {{
                    margin-top: 100px;
                    text-align: center;
                    border-top: 1px solid #cbd5e1;
                    padding-top: 20px;
                    font-size: 12px;
                    color: #64748b;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <table style="width: 100%;">
                    <tr>
                        <td>
                            <div class="title">FASHION STORE</div>
                            <div class="subtitle">Hệ thống Cửa hàng Thời trang Cao cấp</div>
                        </td>
                        <td style="text-align: right; vertical-align: bottom;">
                            <div style="font-size: 16px; font-weight: bold; color: #2563eb;">HÓA ĐƠN BÁN HÀNG</div>
                            <div style="font-size: 13px; color: #475569; margin-top: 4px;">Số hóa đơn: {self.summary_data[0]}</div>
                        </td>
                    </tr>
                </table>
            </div>

            <table class="info-table">
                <tr>
                    <td style="width: 50%;">
                        <strong>Khách hàng:</strong> {cust_name}<br>
                        <strong>Phương thức thanh toán:</strong> {pay_method}
                    </td>
                    <td style="width: 50%; text-align: right;">
                        <strong>Ngày tạo:</strong> {created_at}<br>
                        <strong>Trạng thái:</strong> Đã thanh toán
                    </td>
                </tr>
            </table>

            <table class="items-table">
                <thead>
                    <tr>
                        <th style="text-align: left; width: 40%;">Mặt hàng</th>
                        <th style="text-align: center; width: 10%;">Size</th>
                        <th style="text-align: center; width: 15%;">Màu</th>
                        <th style="text-align: center; width: 10%;">SL</th>
                        <th style="text-align: right; width: 12%;">Đơn giá</th>
                        <th style="text-align: right; width: 13%;">Thành tiền</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows_html}
                </tbody>
            </table>

            {discount_section}

            <div style="width: 100%; overflow: hidden; margin-top: 20px;">
                <div class="total-box">
                    <table style="width: 100%; border-spacing: 0 6px;">
                        <tr>
                            <td style="color: #64748b;">Tổng tiền hàng:</td>
                            <td style="text-align: right;">{total + disc_amount:,.0f} ₫</td>
                        </tr>
                        <tr>
                            <td style="color: #64748b;">Giảm giá:</td>
                            <td style="text-align: right; color: #ef4444;">-{disc_amount:,.0f} ₫</td>
                        </tr>
                        <tr style="font-size: 18px; font-weight: bold;">
                            <td style="color: #1e3a8a; padding-top: 8px; border-top: 1px solid #cbd5e1;">Tổng thanh toán:</td>
                            <td style="text-align: right; color: #10b981; padding-top: 8px; border-top: 1px solid #cbd5e1;">{total:,.0f} ₫</td>
                        </tr>
                    </table>
                </div>
            </div>

            <div class="footer">
                Cảm ơn quý khách đã mua sắm tại <strong>Fashion Store</strong>!<br>
                Hẹn gặp lại quý khách!
            </div>
        </body>
        </html>
        """

        # 5. Khởi tạo QPrinter để xuất PDF với tỉ lệ chuẩn và sắc nét
        printer = QPrinter(QPrinter.ScreenResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(pdf_path)
        
        # Thiết lập margins
        printer.setPageMargins(15, 15, 15, 15, QPrinter.Millimeter)

        doc = QTextDocument()
        doc.setHtml(html_content)
        doc.print_(printer)

        return pdf_path

    def print_invoice(self):
        import os
        try:
            pdf_path = self.generate_pdf_invoice()
            file_name = os.path.basename(pdf_path)
            
            # Popup thông báo xuất thành công và nút mở file nhanh
            msg = QMessageBox(self)
            msg.setWindowTitle("Xuất hóa đơn thành công")
            msg.setText(
                f"Đã xuất hóa đơn <b>{self.summary_data[0]}</b> thành file PDF thành công!<br><br>"
                f"<b>File:</b> {file_name}<br><b>Thư mục:</b> exports/invoices/"
            )
            msg.setIcon(QMessageBox.Information)
            
            btn_open = msg.addButton("Mở file PDF", QMessageBox.ActionRole)
            btn_ok = msg.addButton("Đóng", QMessageBox.AcceptRole)
            
            # Styles cho các nút
            btn_open.setStyleSheet("""
                QPushButton {
                    background-color: #0284c7; color: white; border: none; border-radius: 6px;
                    padding: 8px 20px; font-size: 13px; font-weight: bold; min-width: 90px;
                }
                QPushButton:hover { background-color: #0369a1; }
            """)
            btn_ok.setStyleSheet("""
                QPushButton {
                    background-color: #f1f5f9; color: #334155; border: 1px solid #cbd5e1;
                    border-radius: 6px; padding: 8px 20px; font-size: 13px; font-weight: bold; min-width: 80px;
                }
                QPushButton:hover { background-color: #e2e8f0; }
            """)
            msg.setStyleSheet("QMessageBox { background-color: white; } QLabel { color: #1e293b; font-size: 14px; }")
            
            msg.exec_()
            
            if msg.clickedButton() == btn_open:
                os.startfile(pdf_path)
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể xuất file PDF hóa đơn: {str(e)}")
