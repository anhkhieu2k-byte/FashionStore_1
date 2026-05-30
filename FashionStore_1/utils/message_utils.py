from PyQt5.QtWidgets import QMessageBox, QPushButton
from PyQt5.QtCore import Qt
from config import PRIMARY, SUCCESS, WARNING, DANGER

def show_info(parent, title, message):
    msg = QMessageBox(parent)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setIcon(QMessageBox.Information)
    msg.setStandardButtons(QMessageBox.NoButton)
    ok_btn = msg.addButton("Đã hiểu", QMessageBox.AcceptRole)
    _apply_style(msg, "#2563eb", ok_btn)
    msg.exec_()

def show_warning(parent, title, message):
    msg = QMessageBox(parent)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setIcon(QMessageBox.Warning)
    msg.setStandardButtons(QMessageBox.NoButton)
    ok_btn = msg.addButton("Đã hiểu", QMessageBox.AcceptRole)
    _apply_style(msg, "#f59e0b", ok_btn)
    msg.exec_()

def show_error(parent, title, message):
    msg = QMessageBox(parent)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setIcon(QMessageBox.Critical)
    msg.setStandardButtons(QMessageBox.NoButton)
    ok_btn = msg.addButton("Đóng", QMessageBox.AcceptRole)
    _apply_style(msg, "#dc2626", ok_btn)
    msg.exec_()

def show_success(parent, title, message):
    msg = QMessageBox(parent)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setIcon(QMessageBox.Information)
    msg.setStandardButtons(QMessageBox.NoButton)
    ok_btn = msg.addButton("Tuyệt vời", QMessageBox.AcceptRole)
    _apply_style(msg, "#10b981", ok_btn)
    msg.exec_()

def show_confirm(parent, title, message):
    msg = QMessageBox(parent)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setIcon(QMessageBox.Question)
    msg.setStandardButtons(QMessageBox.NoButton)
    
    btn_yes = msg.addButton("Đồng ý", QMessageBox.YesRole)
    btn_no = msg.addButton("Hủy bỏ", QMessageBox.NoRole)
    msg.setDefaultButton(btn_no)
    
    # Style trực tiếp cho nút Đồng ý (Màu xanh dương phẳng, chữ trắng như trong ảnh)
    btn_yes.setStyleSheet(f"""
        QPushButton {{
            background-color: #2563eb;
            color: #ffffff;
            border: none;
            border-radius: 6px;
            padding: 8px 24px;
            font-weight: bold;
            font-size: 13px;
            min-width: 100px;
        }}
        QPushButton:hover {{
            background-color: #1d4ed8;
        }}
    """)
    
    # Style trực tiếp cho nút Hủy bỏ (Màu xám)
    btn_no.setStyleSheet("""
        QPushButton {
            background-color: #f1f5f9;
            color: #475569;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            padding: 8px 24px;
            font-weight: bold;
            font-size: 13px;
            min-width: 100px;
        }
        QPushButton:hover {
            background-color: #e2e8f0;
            color: #0f172a;
        }
    """)
    
    # Style cho khung nền QMessageBox
    msg.setStyleSheet("""
        QMessageBox {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
        }
        QLabel {
            color: #1e293b;
            font-size: 14px;
            font-weight: 600;
            padding: 8px;
        }
    """)
    
    msg.exec_()
    return msg.clickedButton() == btn_yes

def _apply_style(msg, color, target_btn=None):
    # Định nghĩa màu sắc nút phẳng, không viền đen thô, đồng bộ 100% với ảnh của khách hàng
    btn_color = "#2563eb" # Mặc định là màu xanh dương thương hiệu
    btn_hover_color = "#1d4ed8"
    
    if color == "#dc2626": # Đỏ của lỗi
        btn_color = "#ef4444"
        btn_hover_color = "#dc2626"
    elif color == "#10b981": # Xanh của thành công
        btn_color = "#10b981"
        btn_hover_color = "#059669"
        
    # Định dạng khung nền hộp thoại trắng tinh tế, sạch sẽ
    msg.setStyleSheet("""
        QMessageBox {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
        }
        QLabel {
            color: #1e293b;
            font-size: 14px;
            font-weight: 600;
            padding: 8px;
        }
    """)
    
    if target_btn:
        target_btn.setCursor(Qt.PointingHandCursor)
        target_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {btn_color};
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 8px 24px;
                font-weight: bold;
                font-size: 13px;
                min-width: 90px;
            }}
            QPushButton:hover {{
                background-color: {btn_hover_color};
            }}
        """)
        
    for btn in msg.findChildren(QPushButton):
        btn.setCursor(Qt.PointingHandCursor)
