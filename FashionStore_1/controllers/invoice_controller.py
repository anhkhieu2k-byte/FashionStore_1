from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from utils.message_utils import show_success, show_error
from database.db_connect import get_connection
from ui.dialogs.invoice_detail_dialog import InvoiceDetailDialog
from modules.sales.sale_service import SalesService

class InvoiceController:

    def __init__(self, ui):
        self.ui = ui
        self.load_history()

        self.ui.btn_search.clicked.connect(self.search_history)
        self.ui.txt_search.returnPressed.connect(self.search_history)
        self.ui.table.cellClicked.connect(self.show_invoice_detail)
        
        # Kết nối nút Cập nhật (Refresh)
        if hasattr(self.ui, 'btn_refresh'):
            self.ui.btn_refresh.clicked.connect(lambda: self.load_history())

        # Kết nối nút Xuất Excel
        if hasattr(self.ui, 'btn_export'):
            self.ui.btn_export.clicked.connect(self.export_to_excel)

    def load_history(self, keyword=""):
        conn = get_connection()
        cursor = conn.cursor()

        if keyword:
            cursor.execute("""
                SELECT id, customer_name, total, payment_method, created_at, status
                FROM invoices 
                WHERE id LIKE ? OR customer_name LIKE ?
                ORDER BY id DESC
            """, (f"%{keyword}%", f"%{keyword}%"))
        else:
            cursor.execute("""
                SELECT id, customer_name, total, payment_method, created_at, status
                FROM invoices 
                ORDER BY id DESC
            """)
        
        data = cursor.fetchall()
        conn.close()

        self.ui.table.setRowCount(0)
        from PyQt5.QtGui import QColor
        for row_index, invoice in enumerate(data):
            self.ui.table.insertRow(row_index)

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
                
                # Trang trí màu sắc cho cột Trạng thái
                if col_index == 5:
                    if text == "Đã hoàn tiền":
                        item.setForeground(QColor("#ef4444")) # Đỏ
                        item.setBackground(QColor("#fdf0ef"))
                    elif text == "Hoàn tiền một phần":
                        item.setForeground(QColor("#f97316")) # Cam
                        item.setBackground(QColor("#fff7ed"))
                    else:
                        item.setForeground(QColor("#059669")) # Xanh lá
                        item.setBackground(QColor("#ecfdf5"))

                self.ui.table.setItem(row_index, col_index, item)
            
            # Thêm nút Xem chi tiết (Thao tác)
            btn_item = QTableWidgetItem("🔍 Xem chi tiết")
            btn_item.setForeground(Qt.blue)
            btn_item.setTextAlignment(Qt.AlignCenter)
            self.ui.table.setItem(row_index, 6, btn_item)

    def search_history(self):
        keyword = self.ui.txt_search.text()
        self.load_history(keyword)

    def show_invoice_detail(self, row, col):
        item_id = self.ui.table.item(row, 0)
        if not item_id:
            return
        
        real_id = item_id.data(Qt.UserRole)
        
        summary_data = (
            self.ui.table.item(row, 0).text(),
            self.ui.table.item(row, 1).text(),
            self.ui.table.item(row, 2).text(),
            self.ui.table.item(row, 3).text(),
            self.ui.table.item(row, 4).text()
        )

        dlg = InvoiceDetailDialog(self.ui, invoice_id=real_id, summary_data=summary_data)
        dlg.exec_()

    def export_to_excel(self):
        try:
            file_path = SalesService.export_invoices_excel()
            file_name = file_path.replace("\\", "/").split("/")[-1]
            show_success(
                self.ui, "Thành công",
                f"Đã xuất lịch sử hóa đơn thành công!<br><br>"
                f"<b>File:</b> {file_name}<br><b>Thư mục:</b> exports/excel_reports/"
            )
        except Exception as e:
            show_error(self.ui, "Lỗi", f"Không thể xuất file: {str(e)}")
