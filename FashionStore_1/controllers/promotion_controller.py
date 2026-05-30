from PyQt5.QtWidgets import *
from modules.promotions.promotion_service import PromotionService
from utils.message_utils import show_info, show_warning, show_error, show_success


def to_display_date(date_str):
    """
    Converts YYYY-MM-DD (from DB) to DD-MM-YYYY (for UI display).
    If it is already in DD-MM-YYYY or invalid format, returns it as is.
    """
    if not date_str:
        return ""
    date_str = str(date_str).strip().replace('/', '-')
    try:
        parts = date_str.split('-')
        if len(parts) == 3:
            if len(parts[0]) == 4: # YYYY-MM-DD
                return f"{parts[2]}-{parts[1]}-{parts[0]}"
    except Exception:
        pass
    return date_str


def to_db_date(date_str):
    """
    Converts DD-MM-YYYY (from UI input) to YYYY-MM-DD (for DB saving).
    Also supports input in YYYY-MM-DD format.
    Raises ValueError if the input is not a valid date format.
    """
    if not date_str:
        return ""
    date_str = str(date_str).strip().replace('/', '-')
    try:
        parts = date_str.split('-')
        if len(parts) == 3:
            if len(parts[2]) == 4: # DD-MM-YYYY
                d, m, y = int(parts[0]), int(parts[1]), int(parts[2])
                from datetime import date
                date(y, m, d)
                return f"{y:04d}-{m:02d}-{d:02d}"
            elif len(parts[0]) == 4: # YYYY-MM-DD
                y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
                from datetime import date
                date(y, m, d)
                return f"{y:04d}-{m:02d}-{d:02d}"
    except Exception:
        pass
    raise ValueError(f"Ngày '{date_str}' không hợp lệ hoặc sai định dạng (vui lòng dùng DD-MM-YYYY)")



class PromotionController:

    def __init__(self, ui):

        self.ui = ui

        self.load_promotions()

        self.ui.btn_add.clicked.connect(
            self.add_promotion
        )

        self.ui.btn_update.clicked.connect(
            self.update_promotion
        )

        self.ui.btn_delete.clicked.connect(
            self.delete_promotion
        )

        self.ui.btn_search.clicked.connect(
            self.search_promotion
        )

        self.ui.table.cellClicked.connect(
            self.select_row
        )

    def load_promotions(self):

        data = PromotionService.get_promotions()

        self.ui.table.setRowCount(0)

        for row_index, promotion in enumerate(data):

            self.ui.table.insertRow(row_index)

            for col_index, item in enumerate(promotion):
                # Hiển thị số tiền VNĐ cho dễ đọc
                val = str(item)
                if col_index == 3:
                    try: val = f"{float(item):,.0f}"
                    except: pass
                elif col_index in [4, 5]:
                    val = to_display_date(val)
                
                self.ui.table.setItem(
                    row_index,
                    col_index,
                    QTableWidgetItem(val)
                )

            # Thêm cột "Còn lại" tính số ngày theo ngày thực tế
            try:
                from datetime import date, datetime
                today = date.today()
                
                def parse_dt(d_str):
                    if not d_str: return None
                    d_str = str(d_str).strip().replace('/', '-')
                    for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
                        try: return datetime.strptime(d_str, fmt).date()
                        except ValueError: continue
                    return None

                start_dt = parse_dt(promotion[4])
                end_dt = parse_dt(promotion[5])
                
                remaining_str = ""
                if start_dt and today < start_dt:
                    days_until = (start_dt - today).days
                    remaining_str = f"Chưa bắt đầu ({days_until} ngày)"
                elif end_dt:
                    if today <= end_dt:
                        delta = (end_dt - today).days
                        if delta > 0:
                            remaining_str = f"Còn {delta} ngày"
                        elif delta == 0:
                            remaining_str = "Hết hạn hôm nay"
                    else:
                        delta = (today - end_dt).days
                        remaining_str = f"Hết hạn ({delta} ngày trước)"
                else:
                    remaining_str = "Vô thời hạn"
                    
                self.ui.table.setItem(
                    row_index,
                    8,
                    QTableWidgetItem(remaining_str)
                )
            except Exception as e:
                print("Lỗi tính số ngày còn lại:", e)

    def add_promotion(self):
        try:
            qty = int(self.ui.txt_quantity.text() or 999)
            PromotionService.add_promotion(
                self.ui.txt_code.text(),
                float(self.ui.txt_discount.text()),
                float(self.ui.txt_min_order.text()),
                to_db_date(self.ui.txt_start.text()),
                to_db_date(self.ui.txt_end.text()),
                qty
            )

            show_success(
                self.ui,
                "Success",
                "Thêm khuyến mãi thành công"
            )

            self.load_promotions()
            self.clear_inputs()
        except Exception as e:
            show_error(self.ui, "Lỗi", f"Dữ liệu không hợp lệ: {str(e)}")

    def update_promotion(self):
        try:
            row = self.ui.table.currentRow()
            if row < 0:
                return

            promotion_id = int(self.ui.table.item(row, 0).text())
            qty = int(self.ui.txt_quantity.text() or 999)

            PromotionService.update_promotion(
                promotion_id,
                self.ui.txt_code.text(),
                float(self.ui.txt_discount.text()),
                float(self.ui.txt_min_order.text()),
                to_db_date(self.ui.txt_start.text()),
                to_db_date(self.ui.txt_end.text()),
                qty
            )

            show_success(
                self.ui,
                "Success",
                "Cập nhật thành công"
            )

            self.load_promotions()
            self.clear_inputs()
        except Exception as e:
            show_error(self.ui, "Lỗi", f"Lỗi cập nhật: {str(e)}")

    def delete_promotion(self):

        row = self.ui.table.currentRow()

        if row < 0:
            show_warning(self.ui, "Chưa chọn", "Vui lòng chọn một chương trình khuyến mãi để xóa!")
            return

        promotion_id = int(self.ui.table.item(row, 0).text())
        code_name = self.ui.table.item(row, 1).text()

        msg = QMessageBox(self.ui)
        msg.setWindowTitle("Xác nhận xóa")
        msg.setText(f"Bạn có chắc chắn muốn xóa mã khuyến mãi '{code_name}' không?")
        msg.setIcon(QMessageBox.Question)

        btn_yes = msg.addButton("Đồng ý xóa", QMessageBox.YesRole)
        btn_no = msg.addButton("Hủy bỏ", QMessageBox.NoRole)
        msg.setDefaultButton(btn_no)

        msg.setStyleSheet("""
            QMessageBox { background-color: #ffffff; }
            QLabel { color: #0f172a; font-size: 14px; font-weight: bold; }
        """)

        btn_yes.setStyleSheet("""
            QPushButton {
                background-color: #dc2626; color: white; border: none;
                border-radius: 6px; padding: 8px 18px; font-size: 13px; font-weight: bold; min-width: 80px;
            }
            QPushButton:hover { background-color: #b91c1c; }
        """)

        btn_no.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9; color: #334155; border: 1px solid #cbd5e1;
                padding: 8px 18px; font-size: 13px; font-weight: bold; min-width: 80px;
            }
            QPushButton:hover { background-color: #e2e8f0; color: #0f172a; }
        """)

        msg.exec_()

        if msg.clickedButton() == btn_yes:
            PromotionService.delete_promotion(promotion_id)
            show_success(self.ui, "Success", f"Đã xóa mã khuyến mãi '{code_name}'.")
            self.load_promotions()
            self.clear_inputs()

    def search_promotion(self):

        keyword = self.ui.txt_search.text()

        data = PromotionService.search_promotion(
            keyword
        )

        self.ui.table.setRowCount(0)

        for row_index, promotion in enumerate(data):

            self.ui.table.insertRow(row_index)

            for col_index, item in enumerate(promotion):
                val = str(item)
                if col_index == 3:
                    try: val = f"{float(item):,.0f}"
                    except: pass
                elif col_index in [4, 5]:
                    val = to_display_date(val)

                self.ui.table.setItem(
                    row_index,
                    col_index,
                    QTableWidgetItem(val)
                )

            # Thêm cột "Còn lại" tính số ngày theo ngày thực tế
            try:
                from datetime import date, datetime
                today = date.today()
                
                def parse_dt(d_str):
                    if not d_str: return None
                    d_str = str(d_str).strip().replace('/', '-')
                    for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
                        try: return datetime.strptime(d_str, fmt).date()
                        except ValueError: continue
                    return None

                start_dt = parse_dt(promotion[4])
                end_dt = parse_dt(promotion[5])
                
                remaining_str = ""
                if start_dt and today < start_dt:
                    days_until = (start_dt - today).days
                    remaining_str = f"Chưa bắt đầu ({days_until} ngày)"
                elif end_dt:
                    if today <= end_dt:
                        delta = (end_dt - today).days
                        if delta > 0:
                            remaining_str = f"Còn {delta} ngày"
                        elif delta == 0:
                            remaining_str = "Hết hạn hôm nay"
                    else:
                        delta = (today - end_dt).days
                        remaining_str = f"Hết hạn ({delta} ngày trước)"
                else:
                    remaining_str = "Vô thời hạn"
                    
                self.ui.table.setItem(
                    row_index,
                    8,
                    QTableWidgetItem(remaining_str)
                )
            except Exception as e:
                print("Lỗi tính số ngày còn lại:", e)

    def select_row(self, row):
        self.ui.txt_code.setText(self.ui.table.item(row, 1).text())
        self.ui.txt_discount.setText(self.ui.table.item(row, 2).text())
        
        # Xử lý format tiền khi lấy ngược lại từ bảng
        order_val = self.ui.table.item(row, 3).text().replace(",", "")
        self.ui.txt_min_order.setText(order_val)
        
        self.ui.txt_start.setText(self.ui.table.item(row, 4).text())
        self.ui.txt_end.setText(self.ui.table.item(row, 5).text())
        
        # Thêm hiển thị số lượng khi chọn dòng
        if self.ui.table.columnCount() > 6:
            self.ui.txt_quantity.setText(self.ui.table.item(row, 6).text())

    def clear_inputs(self):
        self.ui.txt_code.clear()
        self.ui.txt_discount.clear()
        self.ui.txt_min_order.clear()
        self.ui.txt_start.clear()
        self.ui.txt_end.clear()
        self.ui.txt_quantity.clear()