"""
Shared UI helper utilities
Font: Nunito | Bo góc nhẹ | Giao diện phẳng sáng sủa (giống ảnh)
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from config import *


def page_title(text):
    lbl = QLabel(text)
    lbl.setStyleSheet(
        f"color:{TEXT_DARK}; font-size:18px; font-weight:800; background:transparent;"
        f"font-family:'Nunito',sans-serif;"
    )
    return lbl


def section_label(text):
    lbl = QLabel(text)
    lbl.setStyleSheet(
        f"color:{TEXT_MID}; font-size:13px; background:transparent;"
        f"font-weight:700; font-family:'Nunito',sans-serif;"
    )
    return lbl


def form_card():
    f = QFrame()
    f.setStyleSheet(f"""
        QFrame {{
            background:{BG_CARD};
            border: 1px solid {BORDER};
            border-radius: 12px;
        }}
    """)
    return f


def search_bar(placeholder="Tìm kiếm..."):
    txt = QLineEdit()
    txt.setPlaceholderText("🔍  " + placeholder)
    txt.setFixedHeight(40)
    txt.setStyleSheet(f"""
        QLineEdit {{
            background:{BG_INPUT}; border:1px solid {BORDER};
            border-radius:8px; padding:0 14px; color:{TEXT_DARK}; font-size:13px;
            font-family:'Nunito',sans-serif;
        }}
        QLineEdit:focus {{ border-color:{PRIMARY}; }}
    """)
    return txt


def primary_btn(text, height=42):
    btn = QPushButton(text)
    btn.setFixedHeight(height)
    btn.setCursor(Qt.PointingHandCursor)
    btn.setStyleSheet(f"""
        QPushButton {{
            background:{PRIMARY}; color:white; border:none; border-radius:10px;
            font-size:15px; font-weight:800; padding:0 18px;
            font-family:'Nunito',sans-serif;
        }}
        QPushButton:hover {{ background:{PRIMARY_DARK}; }}
    """)
    return btn


def secondary_btn(text, height=42):
    btn = QPushButton(text)
    btn.setFixedHeight(height)
    btn.setCursor(Qt.PointingHandCursor)
    btn.setStyleSheet(f"""
        QPushButton {{
            background:{BG_INPUT}; color:{TEXT_MID};
            border:1.5px solid {BORDER_MED};
            border-radius:10px; font-size:15px; font-weight:800; padding:0 18px;
            font-family:'Nunito',sans-serif;
        }}
        QPushButton:hover {{ background:#f8fafc; color:{TEXT_DARK}; border-color:{PRIMARY}; }}
    """)
    return btn


def danger_btn(text, height=42):
    btn = QPushButton(text)
    btn.setFixedHeight(height)
    btn.setCursor(Qt.PointingHandCursor)
    btn.setStyleSheet(f"""
        QPushButton {{
            background:{DANGER}; color:white; border:none;
            border-radius:10px; font-size:15px; font-weight:800; padding:0 18px;
            font-family:'Nunito',sans-serif;
        }}
        QPushButton:hover {{ background:#dc2626; }}
    """)
    return btn


def success_btn(text, height=42):
    btn = QPushButton(text)
    btn.setFixedHeight(height)
    btn.setCursor(Qt.PointingHandCursor)
    btn.setStyleSheet(f"""
        QPushButton {{
            background:{SUCCESS}; color:white; border:none;
            border-radius:10px; font-size:15px; font-weight:800; padding:0 18px;
            font-family:'Nunito',sans-serif;
        }}
        QPushButton:hover {{ background:#059669; }}
    """)
    return btn


def action_btn(action_type="edit"):
    """ Nút hành động nhỏ trong bảng (Sửa/Xóa) """
    btn = QPushButton()
    btn.setFixedSize(30, 30)
    btn.setCursor(Qt.PointingHandCursor)
    if action_type == "edit":
        btn.setText("✎")
        btn.setStyleSheet(f"""
            QPushButton {{ background:{WARNING}; color:white; border:none; border-radius:6px; font-size:14px; }}
            QPushButton:hover {{ background:#d97706; }}
        """)
    else:
        btn.setText("🗑")
        btn.setStyleSheet(f"""
            QPushButton {{ background:{DANGER}; color:white; border:none; border-radius:6px; font-size:14px; }}
            QPushButton:hover {{ background:#dc2626; }}
        """)
    return btn


def divider():
    f = QFrame()
    f.setFixedHeight(1)
    f.setStyleSheet(f"background:{BORDER};")
    return f


def styled_table(columns):
    tbl = QTableWidget()
    tbl.setColumnCount(len(columns))
    tbl.setHorizontalHeaderLabels(columns)
    tbl.setAlternatingRowColors(True)
    tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
    tbl.setEditTriggers(QAbstractItemView.NoEditTriggers)
    tbl.verticalHeader().setVisible(False)
    tbl.setShowGrid(False)
    tbl.setStyleSheet(f"""
        QTableWidget {{
            background: {BG_CARD}; border: 1.5px solid {BORDER}; border-radius: 12px;
            color: {TEXT_DARK}; font-family: 'Nunito', sans-serif; font-size: 13px;
            alternate-background-color: #f8fafc;
        }}
        QTableWidget::item {{ 
            padding: 10px 15px;
            border-bottom: 1.5px solid #f1f5f9; 
        }}
        QTableWidget::item:selected {{ 
            background: {PRIMARY_LIGHT}; color: {PRIMARY_DARK}; 
            font-weight: bold;
        }}
        QHeaderView::section {{
            background: #e2e8f0; color: #0f172a; padding: 12px;
            border: none; border-bottom: 2.5px solid {BORDER};
            font-weight: 900; font-size: 12px; text-transform: uppercase;
            font-family: 'Nunito', sans-serif;
        }}
    """)
    return tbl


def field_input(placeholder, height=40):
    txt = QLineEdit()
    txt.setPlaceholderText(placeholder)
    txt.setFixedHeight(height)
    txt.setStyleSheet(f"""
        QLineEdit {{
            background:{BG_INPUT}; border:1px solid {BORDER};
            border-radius:8px; padding:0 12px; color:{TEXT_DARK};
            font-size:13px; font-family:'Nunito',sans-serif;
        }}
        QLineEdit:focus {{ border-color:{PRIMARY}; }}
    """)
    return txt


def status_badge(text, color, bg):
    lbl = QLabel(f"● {text}")
    lbl.setAlignment(Qt.AlignCenter)
    lbl.setStyleSheet(f"""
        QLabel {{
            background:{bg}; color:{color};
            border-radius:12px; font-size:11px; font-weight:700;
            padding:4px 10px; font-family:'Nunito',sans-serif;
        }}
    """)
    return lbl


def stat_card(title, value, color, icon):
    """ Thẻ thống kê màu sắc (như tab Báo cáo / Đổi trả) """
    card = QFrame()
    card.setFixedHeight(100)
    card.setStyleSheet(f"""
        QFrame {{
            background:{color}; border-radius:12px;
        }}
    """)
    lay = QVBoxLayout(card)
    lay.setContentsMargins(20, 16, 20, 16)
    
    top = QHBoxLayout()
    t_lbl = QLabel(title.upper())
    t_lbl.setStyleSheet("color:rgba(255,255,255,0.8); font-size:11px; font-weight:800; font-family:'Nunito',sans-serif;")
    ic_lbl = QLabel(icon)
    ic_lbl.setStyleSheet("color:rgba(255,255,255,0.4); font-size:24px;")
    top.addWidget(t_lbl); top.addStretch(); top.addWidget(ic_lbl)
    
    v_lbl = QLabel(value)
    v_lbl.setStyleSheet("color:white; font-size:22px; font-weight:800; font-family:'Nunito',sans-serif;")
    
    lay.addLayout(top)
    lay.addWidget(v_lbl)
    lay.addStretch()
    return card, v_lbl
