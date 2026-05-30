from PyQt5.QtWidgets import QTableWidgetItem, QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QHeaderView, QLabel, QPushButton, QComboBox, QLineEdit
from PyQt5.QtCore import Qt
from utils.message_utils import show_info, show_warning, show_error, show_success, show_confirm
from modules.staff.staff_service import StaffService
from ui.dialogs.staff_dialog import StaffDialog
from models.attendance import AttendanceModel


def verify_staff_password(parent, staff_name, correct_password):
    dialog = QDialog(parent)
    dialog.setWindowTitle("Xác nhận mật khẩu")
    dialog.setFixedSize(380, 200)
    dialog.setStyleSheet("""
        QDialog { background-color: #ffffff; border-radius: 12px; }
        QLabel { font-size: 14px; color: #1e293b; }
        QLineEdit { background-color: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 6px; padding: 8px; font-size: 14px; }
        QLineEdit:focus { border-color: #2563eb; background-color: #ffffff; }
    """)
    
    layout = QVBoxLayout(dialog)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(12)
    
    lbl = QLabel(f"Nhập mật khẩu của <b>{staff_name}</b> để xác nhận:")
    layout.addWidget(lbl)
    
    txt_pwd = QLineEdit()
    txt_pwd.setEchoMode(QLineEdit.Password)
    txt_pwd.setPlaceholderText("Mật khẩu của bạn...")
    layout.addWidget(txt_pwd)
    
    btn_box = QHBoxLayout()
    btn_ok = QPushButton("Xác nhận")
    btn_ok.setCursor(Qt.PointingHandCursor)
    btn_ok.setStyleSheet("QPushButton { background-color: #2563eb; color: white; border: none; border-radius: 6px; padding: 8px 20px; font-weight: bold; } QPushButton:hover { background-color: #1d4ed8; }")
    
    btn_cancel = QPushButton("Hủy")
    btn_cancel.setCursor(Qt.PointingHandCursor)
    btn_cancel.setStyleSheet("QPushButton { background-color: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; border-radius: 6px; padding: 8px 20px; font-weight: bold; } QPushButton:hover { background-color: #e2e8f0; }")
    
    btn_box.addStretch()
    btn_box.addWidget(btn_cancel)
    btn_box.addWidget(btn_ok)
    layout.addLayout(btn_box)
    
    btn_ok.clicked.connect(dialog.accept)
    btn_cancel.clicked.connect(dialog.reject)
    
    if dialog.exec_() == QDialog.Accepted:
        entered = txt_pwd.text().strip()
        if entered == str(correct_password or ""):
            return True
        else:
            show_error(parent, "Sai mật khẩu", "Mật khẩu bạn nhập không chính xác!")
            return False
    return False


class StaffController:

    def __init__(self, ui):
        self.ui = ui
        self._all_staff = []

        self.load_staff()

        # Kết nối các nút thao tác
        self.ui.btn_add.clicked.connect(self.add_staff)
        self.ui.btn_update.clicked.connect(self.update_staff)
        self.ui.btn_delete.clicked.connect(self.delete_staff)
        self.ui.btn_attendance.clicked.connect(self.mark_attendance)
        self.ui.btn_end_shift.clicked.connect(self.end_shift)
        self.ui.btn_history.clicked.connect(self.show_history)
        self.ui.btn_payroll.clicked.connect(self.calculate_payroll)
        self.ui.btn_export_payroll.clicked.connect(self.export_payroll)

        # Kết nối tìm kiếm trực tiếp
        self.ui.txt_search.textChanged.connect(self.search_staff)

    def load_staff(self):
        self._all_staff = StaffService.get_staff()
        self._populate_table(self._all_staff)

    def _populate_table(self, data):
        self.ui.table.setRowCount(0)
        for row_index, staff in enumerate(data):
            self.ui.table.insertRow(row_index)
            # staff = (id, full_name, birth_date, phone, address, role, shift, salary, attendance_days, check_in_time, total_hours)
            role = str(staff[5] or "").lower()
            salary_base = float(staff[7] or 0)
            total_hours = float(staff[10] or 0) # Cột mới thứ 11

            for col_index in range(9):
                if col_index == 7:  # Cột Lương
                    if salary_base > 100000:
                        # Lương cố định tự nhập
                        display_val = salary_base
                    else:
                        # Lương theo giờ -> lấy tổng thu nhập thực tế từ lịch sử (đã trừ phạt)
                        from models.attendance import AttendanceModel
                        display_val = AttendanceModel.get_unpaid_earnings(staff[0])
                    val_str = f"{display_val:,.0f} ₫"
                elif col_index == 8: # Cột Ngày công - Hiển thị số ngày hoặc số giờ làm
                    if salary_base > 100000:
                        # Lương cố định -> hiển thị số ngày công
                        val_str = f"{int(staff[8] or 0)} ngày"
                    else:
                        # Lương theo giờ -> hiển thị số giờ làm
                        val_str = f"{total_hours:.2f} h"
                else:
                    val = staff[col_index]
                    val_str = str(val if val is not None else "")

                item = QTableWidgetItem(val_str)
                item.setTextAlignment(Qt.AlignVCenter | (Qt.AlignCenter if col_index in [0, 2, 3, 5, 6, 7, 8] else Qt.AlignLeft))
                self.ui.table.setItem(row_index, col_index, item)

    def search_staff(self, keyword=None):
        kw = self.ui.txt_search.text().strip().lower()
        if not kw:
            self._populate_table(self._all_staff)
            return

        filtered = [
            s for s in self._all_staff
            if kw in str(s[1] or "").lower() or kw in str(s[3] or "").lower()
        ]
        self._populate_table(filtered)

    def _check_admin_permission(self):
        from ui.main_window import PasswordDialog
        from utils.message_utils import show_error
        
        dialog = PasswordDialog(self.ui)
        if dialog.exec_() == QDialog.Accepted:
            password = dialog.get_password()
            if password == "admin123":
                return True
            else:
                show_error(self.ui, "Truy cập bị từ chối", "Mật khẩu không chính xác!<br>Bạn không có quyền thực hiện hành động này.")
                return False
        return False

    def add_staff(self):
        if not self._check_admin_permission():
            return
            
        dlg = StaffDialog(self.ui)
        if dlg.exec_() == QDialog.Accepted:
            data = dlg.get_data()
            if not data["full_name"]:
                show_warning(self.ui, "Thiếu thông tin", "Vui lòng nhập họ và tên nhân viên!")
                return
            StaffService.add_staff(
                data["full_name"],
                data["birth_date"],
                data["phone"],
                data["address"],
                data["role"],
                data["shift"],
                data["salary"],
                data["attendance_days"],
                data["password"]
            )
            show_success(self.ui, "Thành công", "Đã thêm nhân viên mới thành công!")
            self.load_staff()

    def update_staff(self):
        row = self.ui.table.currentRow()
        if row < 0:
            show_warning(self.ui, "Chưa chọn", "Vui lòng click chọn một nhân viên trong bảng để sửa thông tin!")
            return

        if not self._check_admin_permission():
            return

        staff_id = int(self.ui.table.item(row, 0).text())
        target_staff = next((s for s in self._all_staff if s[0] == staff_id), None)
        if not target_staff:
            return

        dlg = StaffDialog(self.ui, staff_data=target_staff)
        if dlg.exec_() == QDialog.Accepted:
            data = dlg.get_data()
            if not data["full_name"]:
                show_warning(self.ui, "Thiếu thông tin", "Họ và tên nhân viên không được để trống!")
                return
            StaffService.update_staff(
                staff_id,
                data["full_name"],
                data["birth_date"],
                data["phone"],
                data["address"],
                data["role"],
                data["shift"],
                data["salary"],
                data["attendance_days"],
                data["password"]
            )
            show_success(self.ui, "Thành công", "Cập nhật thông tin nhân viên thành công!")
            self.load_staff()

    def delete_staff(self):
        row = self.ui.table.currentRow()
        if row < 0:
            show_warning(self.ui, "Chưa chọn", "Vui lòng click chọn một nhân viên trong bảng để xóa!")
            return

        if not self._check_admin_permission():
            return

        staff_id = int(self.ui.table.item(row, 0).text())
        staff_name = self.ui.table.item(row, 1).text()

        if show_confirm(self.ui, "Xác nhận xóa", f"Bạn có chắc chắn muốn xóa nhân viên '{staff_name}' khỏi hệ thống không?"):
            StaffService.delete_staff(staff_id)
            show_success(self.ui, "Thành công", f"Đã xóa nhân viên '{staff_name}' khỏi hệ thống.")
            self.load_staff()

    def mark_attendance(self):
        row = self.ui.table.currentRow()
        if row < 0:
            show_warning(self.ui, "Chưa chọn", "Vui lòng chọn nhân viên muốn vào ca!")
            return

        staff_id = int(self.ui.table.item(row, 0).text())
        staff_name = self.ui.table.item(row, 1).text()
        
        staff_data = next((s for s in self._all_staff if s[0] == staff_id), None)
        if not staff_data:
            return
            
        if staff_data[9]: # check_in_time
            show_warning(self.ui, "Lỗi", "Nhân viên này hiện đang trong ca làm việc rồi!")
            return
            
        # Xác thực mật khẩu nhân viên
        correct_password = staff_data[11] if len(staff_data) > 11 else "123456"
        if not verify_staff_password(self.ui, staff_name, correct_password):
            return # Sai mật khẩu hoặc hủy bỏ
        
        from datetime import datetime
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        StaffService.start_shift(staff_id, now_str)
        show_success(self.ui, "Vào ca làm việc", f"Nhân viên <b>{staff_name}</b> đã vào ca lúc: <br>{now_str}")
        self.load_staff()

    def end_shift(self):
        row = self.ui.table.currentRow()
        if row < 0:
            show_warning(self.ui, "Chưa chọn", "Vui lòng chọn nhân viên muốn kết thúc ca!")
            return

        staff_id = int(self.ui.table.item(row, 0).text())
        staff_name = self.ui.table.item(row, 1).text()
        
        staff_data = next((s for s in self._all_staff if s[0] == staff_id), None)
        if not staff_data or not staff_data[9]: # check_in_time
            show_warning(self.ui, "Lỗi", "Nhân viên này chưa thực hiện 'Vào ca'!")
            return
            
        # Xác thực mật khẩu nhân viên
        correct_password = staff_data[11] if len(staff_data) > 11 else "123456"
        if not verify_staff_password(self.ui, staff_name, correct_password):
            return # Sai mật khẩu hoặc hủy bỏ
        
        from datetime import datetime
        check_in = datetime.strptime(staff_data[9], "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        duration = now - check_in
        hours = duration.total_seconds() / 3600 # Quy đổi ra giờ (có số lẻ)
        
        # Xác định số giờ quy định của ca làm việc
        shift_name = str(staff_data[6] or "").lower()
        if "sáng" in shift_name or "sang" in shift_name:
            target_hours = 4.0
        elif "chiều" in shift_name or "chieu" in shift_name:
            target_hours = 4.0
        elif "tối" in shift_name or "toi" in shift_name:
            target_hours = 4.0
        elif "cả ngày" in shift_name or "ca ngay" in shift_name:
            target_hours = 8.0
        else:
            target_hours = 4.0  # Mặc định ca khác là 4h
            
        is_early = hours < target_hours
        salary_base = float(staff_data[7] or 0)
        
        penalty = 0
        if is_early:
            missing_hours = target_hours - hours
            penalty = missing_hours * 30000  # Phạt 30.000đ/giờ thiếu
            
            warning_msg = (
                f"<b>CẢNH BÁO: KẾT THÚC CA SỚM HƠN QUY ĐỊNH!</b><br><br>"
                f"Nhân viên: <b>{staff_name}</b> làm ca: <b>{staff_data[6]}</b> ({target_hours} giờ).<br>"
                f"• Thời gian đã làm: <b>{hours:.2f} giờ</b> (Thiếu {missing_hours:.2f} giờ).<br>"
                f"• Tiền phạt tự động: <font color='#ef4444'><b>-{penalty:,.0f} ₫</b></font> (30.000₫/giờ thiếu).<br><br>"
                f"Bạn có muốn xác nhận kết thúc ca sớm và chấp nhận bị phạt không?"
            )
            if not show_confirm(self.ui, "Kết thúc ca sớm", warning_msg):
                return  # Người dùng chọn Hủy bỏ -> Hủy kết thúc ca!

        # Tính toán tiền lương và tiền phạt thực nhận của ca này
        if salary_base > 100000:
            # Lương cố định -> Không tính lương theo giờ, nhưng có thể bị trừ phạt trực tiếp vào lương
            shift_pay = -penalty
            StaffService.end_shift(staff_id, hours)
            
            if penalty > 0:
                msg_text = (
                    f"<b>NHÂN VIÊN: {staff_name.upper()} (LƯƠNG CỐ ĐỊNH)</b><br><br>"
                    f"Vào ca: {staff_data[9]}<br>"
                    f"Kết thúc: {now.strftime('%H:%M:%S')}<br>"
                    f"Thời gian làm: <b>{hours:.2f} giờ</b> (Thiếu {target_hours - hours:.2f} giờ)<br>"
                    f"Tiền phạt kết thúc sớm: <font color='#ef4444'><b>-{penalty:,.0f} ₫</b></font><br>"
                    f"<i>(Tiền phạt sẽ tự động khấu trừ khi chốt lương định kỳ)</i>"
                )
            else:
                msg_text = f"<b>NHÂN VIÊN: {staff_name.upper()}</b><br>Ca làm việc đã kết thúc thành công."
        else:
            # Lương theo giờ
            hourly_rate = salary_base if salary_base > 0 else 25000
            earned_raw = hours * hourly_rate
            shift_pay = max(0, earned_raw - penalty)
            StaffService.end_shift(staff_id, hours)
            
            penalty_str = f"<br>Tiền phạt kết thúc sớm: <font color='#ef4444'><b>-{penalty:,.0f} VNĐ</b></font>" if penalty > 0 else ""
            msg_text = (
                f"<b>NHÂN VIÊN: {staff_name.upper()}</b><br><br>"
                f"Vào ca: {staff_data[9]}<br>"
                f"Kết thúc: {now.strftime('%H:%M:%S')}<br>"
                f"Thời gian làm: <b>{hours:.2f} giờ</b> (Yêu cầu {target_hours} giờ)<br>"
                f"Lương ca làm: {earned_raw:,.0f} VNĐ{penalty_str}<br>"
                f"--------------------------<br>"
                f"Thực nhận ca này: <font color='#f59e0b'><b>{shift_pay:,.0f} VNĐ</b></font>"
            )

        # Ghi vào lịch sử chấm công cho TẤT CẢ nhân viên
        AttendanceModel.log_attendance(
            staff_id, staff_name, staff_data[9], now.strftime("%Y-%m-%d %H:%M:%S"), hours, shift_pay
        )
        
        show_info(self.ui, "Kết thúc ca làm việc", msg_text)
        self.load_staff()

    def show_history(self):
        row = self.ui.table.currentRow()
        staff_id = None
        if row >= 0:
            staff_id = int(self.ui.table.item(row, 0).text())
            
        dialog = QDialog(self.ui)
        dialog.setWindowTitle("Lịch sử chấm công")
        dialog.resize(950, 550)
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Tiêu đề & Chọn nhân viên
        header_layout = QHBoxLayout()
        
        title = QLabel("LỊCH SỬ CHẤM CÔNG")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e293b;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        lbl_filter = QLabel("Nhân viên:")
        lbl_filter.setStyleSheet("font-size: 13px; font-weight: bold; color: #475569;")
        header_layout.addWidget(lbl_filter)
        
        cb_staff = QComboBox()
        cb_staff.setStyleSheet("""
            QComboBox { 
                background-color: white; 
                border: 1px solid #cbd5e1; 
                border-radius: 6px; 
                padding: 6px 12px; 
                font-size: 13px; 
                color: #1e293b; 
                min-width: 220px; 
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView { background-color: white; border: 1px solid #cbd5e1; selection-background-color: #eff6ff; selection-color: #2563eb; }
        """)
        
        # Nạp danh sách nhân viên vào dropdown
        cb_staff.addItem("Tất cả nhân viên", None)
        all_staff_list = StaffService.get_staff()
        selected_index = 0
        for idx, s in enumerate(all_staff_list):
            cb_staff.addItem(s[1], s[0])
            if staff_id == s[0]:
                selected_index = idx + 1
                
        cb_staff.setCurrentIndex(selected_index)
        header_layout.addWidget(cb_staff)
        
        layout.addLayout(header_layout)
        
        # Bảng dữ liệu
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["ID", "Nhân viên", "Vào ca", "Kết thúc", "Số giờ", "Thu nhập"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setAlternatingRowColors(True)
        table.setStyleSheet("""
            QTableWidget { background-color: white; border-radius: 8px; border: 1px solid #e2e8f0; color: #334155; }
            QHeaderView::section { background-color: #f8fafc; font-weight: bold; padding: 12px; border: none; border-bottom: 2px solid #e2e8f0; color: #1e293b; }
        """)
        layout.addWidget(table)
        
        def update_table():
            curr_staff_id = cb_staff.currentData()
            curr_staff_name = cb_staff.currentText()
            title.setText(f"LỊCH SỬ CHẤM CÔNG: {curr_staff_name.upper()}")
            
            history_data = AttendanceModel.get_history(curr_staff_id)
            table.setRowCount(0)
            if not history_data:
                table.insertRow(0)
                no_data_item = QTableWidgetItem("Chưa có lịch sử làm việc nào được ghi nhận.")
                no_data_item.setTextAlignment(Qt.AlignCenter)
                table.setItem(0, 1, no_data_item)
                table.setSpan(0, 1, 1, 5)
            else:
                for h in history_data:
                    r = table.rowCount()
                    table.insertRow(r)
                    
                    id_item = QTableWidgetItem(str(h[0]))
                    id_item.setTextAlignment(Qt.AlignCenter)
                    
                    name_item = QTableWidgetItem(str(h[2]))
                    name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    
                    in_item = QTableWidgetItem(str(h[3]))
                    in_item.setTextAlignment(Qt.AlignCenter)
                    
                    out_item = QTableWidgetItem(str(h[4]))
                    out_item.setTextAlignment(Qt.AlignCenter)
                    
                    hours_item = QTableWidgetItem(f"{h[5]:.2f} h")
                    hours_item.setTextAlignment(Qt.AlignCenter)
                    
                    earned_item = QTableWidgetItem(f"{h[6]:,.0f} ₫")
                    earned_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    
                    table.setItem(r, 0, id_item)
                    table.setItem(r, 1, name_item)
                    table.setItem(r, 2, in_item)
                    table.setItem(r, 3, out_item)
                    table.setItem(r, 4, hours_item)
                    table.setItem(r, 5, earned_item)
                    
        cb_staff.currentIndexChanged.connect(update_table)
        update_table()  # Chạy lần đầu để nạp dữ liệu
        
        btn_close = QPushButton("Đóng cửa sổ")
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.setStyleSheet("QPushButton { background-color: #475569; color: white; border-radius: 6px; padding: 12px; font-weight: bold; font-size: 13px; } QPushButton:hover { background-color: #1e293b; }")
        btn_close.clicked.connect(dialog.accept)
        layout.addWidget(btn_close)
        
        dialog.exec_()

    def calculate_payroll(self):
        row = self.ui.table.currentRow()
        if row < 0:
            show_warning(self.ui, "Chưa chọn", "Vui lòng chọn nhân viên muốn tính lương!")
            return

        staff_name = self.ui.table.item(row, 1).text()
        staff_id = int(self.ui.table.item(row, 0).text())
        
        # Tìm nhân viên trong list data gốc
        staff_data = next((s for s in self._all_staff if s[0] == staff_id), None)
        if not staff_data:
            return
            
        # staff_data = (id, full_name, birth_date, phone, address, role, shift, salary, attendance_days, check_in_time, total_hours)
        role = str(staff_data[5] or "").lower()
        salary_base = float(staff_data[7] or 0)
        total_hours = float(staff_data[10] or 0)
        
        # Logic tính lương thực tế
        from models.attendance import AttendanceModel
        unpaid_earnings = AttendanceModel.get_unpaid_earnings(staff_id)
        
        if salary_base > 100000:
            final_salary = max(0.0, salary_base + unpaid_earnings) # unpaid_earnings chứa tổng các khoản phạt (số âm)
            formula_desc = f"Lương cố định: {salary_base:,.0f} ₫<br>Khấu trừ tiền phạt: <font color='#ef4444'>{unpaid_earnings:,.0f} ₫</font>"
            days_info = f"Số ngày công: {staff_data[8]} ngày"
        else:
            final_salary = unpaid_earnings
            formula_desc = f"Tổng lương thực lĩnh từ các ca làm việc (đã khấu trừ các khoản phạt)"
            days_info = f"Tổng số giờ tích lũy: {total_hours:.2f} h"
        
        msg_text = (
            f"<b>NHÂN VIÊN: {staff_name.upper()}</b><br>"
            f"Chức vụ: {staff_data[5]}<br><br>"
            f"{days_info}<br>"
            f"{formula_desc}<br>"
            f"--------------------------<br>"
            f"<font color='#6366f1' size='4'>THỰC NHẬN: {final_salary:,.0f} VNĐ</font>"
        )
        
        if show_confirm(self.ui, "Bảng tính lương", msg_text + "<br><br>Bạn có muốn chốt lương và reset ngày công không?"):
            StaffService.reset_attendance(staff_id)
            AttendanceModel.mark_as_paid(staff_id) # Đánh dấu các ca đã làm là đã trả lương
            show_success(self.ui, "Thành công", f"Đã chốt lương và reset ngày công cho {staff_name}.")
            self.load_staff()

    def export_payroll(self):
        try:
            file_path = StaffService.export_payroll_excel()
            file_name = file_path.replace("\\", "/").split("/")[-1]
            show_success(
                self.ui, "Thành công",
                f"Đã xuất bảng tính lương nhân viên thành công!<br><br>"
                f"<b>File:</b> {file_name}<br><b>Thư mục:</b> exports/excel_reports/"
            )
        except Exception as e:
            show_error(self.ui, "Lỗi", f"Không thể xuất file: {str(e)}")