"""
ReturnTab — Trang Đổi / Trả Hàng
Giao diện sạch, đơn giản, dễ dùng, có ScrollArea.
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor
from config import *
from ui.widgets import *


# ─── helpers ────────────────────────────────────────────────────────────────

def _card(parent_lay, title="", icon=""):
    """Card trắng có tiêu đề + gạch ngang."""
    frame = QFrame()
    frame.setObjectName("rtCard")
    frame.setStyleSheet(
        "QFrame#rtCard{background:#fff;border:1px solid #e2e8f0;border-radius:12px;}"
    )
    vl = QVBoxLayout(frame)
    vl.setContentsMargins(22, 18, 22, 18)
    vl.setSpacing(12)
    if title:
        row = QHBoxLayout()
        lbl = QLabel(f"{icon}  {title}" if icon else title)
        lbl.setStyleSheet(
            f"color:{TEXT_DARK};font-size:14px;font-weight:800;"
            "font-family:'Nunito',sans-serif;"
        )
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet(f"background:{BORDER};border:none;")
        row.addWidget(lbl)
        row.addStretch()
        vl.addLayout(row)
        vl.addWidget(sep)
    parent_lay.addWidget(frame)
    return frame, vl


def _lbl(text, color=None, size=13, bold=700):
    l = QLabel(text)
    l.setStyleSheet(
        f"color:{color or TEXT_MID};font-size:{size}px;font-weight:{bold};"
        "font-family:'Nunito',sans-serif;background:transparent;"
    )
    return l


def _combo_style(cb):
    cb.setStyleSheet(f"""
        QComboBox{{background:#fff;border:1.5px solid {BORDER};border-radius:8px;
            padding:0 12px;font-size:13px;color:{TEXT_DARK};
            font-family:'Nunito',sans-serif;}}
        QComboBox:focus{{border-color:{PRIMARY};}}
        QComboBox::drop-down{{border:none;width:28px;}}
        QComboBox QAbstractItemView{{background:#fff;border:1px solid {BORDER};
            selection-background-color:{PRIMARY_LIGHT};selection-color:{PRIMARY_DARK};
            font-family:'Nunito',sans-serif;}}
    """)


def _input_style(widget, h=40):
    widget.setFixedHeight(h)
    widget.setStyleSheet(f"""
        QLineEdit{{background:#fff;border:1.5px solid {BORDER};border-radius:8px;
            padding:0 14px;color:{TEXT_DARK};font-size:13px;
            font-family:'Nunito',sans-serif;}}
        QLineEdit:focus{{border-color:{PRIMARY};background:#fafcff;}}
    """)


def _mini_stat(title, value, color, icon):
    card = QFrame()
    card.setFixedHeight(84)
    card.setStyleSheet(f"QFrame{{background:{color};border-radius:10px;}}")
    hl = QHBoxLayout(card)
    hl.setContentsMargins(16, 12, 16, 12)
    hl.setSpacing(12)
    ic = QLabel(icon)
    ic.setStyleSheet("font-size:24px;color:rgba(255,255,255,0.3);")
    vl = QVBoxLayout()
    vl.setSpacing(2)
    v = QLabel(value)
    v.setStyleSheet("color:white;font-size:19px;font-weight:900;font-family:'Nunito',sans-serif;")
    t = QLabel(title.upper())
    t.setStyleSheet("color:rgba(255,255,255,0.75);font-size:10px;font-weight:800;font-family:'Nunito',sans-serif;")
    vl.addWidget(v); vl.addWidget(t)
    hl.addWidget(ic); hl.addLayout(vl); hl.addStretch()
    return card, v


def _step_indicator(n, label, active):
    w = QWidget()
    hl = QHBoxLayout(w)
    hl.setContentsMargins(0, 0, 0, 0)
    hl.setSpacing(8)
    num = QLabel(str(n))
    if active:
        num.setStyleSheet(
            f"background:{PRIMARY};color:white;border-radius:11px;"
            "font-size:12px;font-weight:800;padding:2px 8px;"
            "font-family:'Nunito',sans-serif;"
        )
    else:
        num.setStyleSheet(
            "background:#e2e8f0;color:#94a3b8;border-radius:11px;"
            "font-size:12px;font-weight:800;padding:2px 8px;"
            "font-family:'Nunito',sans-serif;"
        )
    txt = QLabel(label)
    txt.setStyleSheet(
        f"color:{TEXT_DARK if active else TEXT_LIGHT};"
        f"font-size:13px;font-weight:{'800' if active else '600'};"
        "font-family:'Nunito',sans-serif;background:transparent;"
    )
    hl.addWidget(num); hl.addWidget(txt)
    return w, num, txt


def _btn(text, h=40, bg=None, fg="white", border=None, hover=None):
    btn = QPushButton(text)
    btn.setFixedHeight(h)
    btn.setCursor(Qt.PointingHandCursor)
    bg    = bg    or PRIMARY
    hover = hover or PRIMARY_DARK
    border_css = f"border:1.5px solid {border};" if border else "border:none;"
    btn.setStyleSheet(f"""
        QPushButton{{background:{bg};color:{fg};{border_css}border-radius:9px;
            font-size:13px;font-weight:800;padding:0 20px;
            font-family:'Nunito',sans-serif;}}
        QPushButton:hover{{background:{hover};}}
        QPushButton:disabled{{background:#cbd5e1;color:#94a3b8;border:none;}}
    """)
    return btn


# ─── main widget ────────────────────────────────────────────────────────────

class ReturnTab(QWidget):

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background:{BG_MAIN};")
        self._setup_ui()

    # ────────────────────────────────────────────────────────────────────────
    def _setup_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Scroll area bao toàn bộ nội dung
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea{background:transparent;border:none;}")

        inner = QWidget()
        inner.setStyleSheet(f"background:{BG_MAIN};")
        root = QVBoxLayout(inner)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        scroll.setWidget(inner)
        outer.addWidget(scroll)

        # ── 1. Header ────────────────────────────────────────────────────
        self._build_header(root)

        # ── 2. Stat cards ────────────────────────────────────────────────
        self._build_stats(root)

        # ── 3. Khu vực xử lý (Popup Dialog) ─────────────────────────────
        self._build_process_card()

        # ── 4. Lịch sử ──────────────────────────────────────────────────
        self._build_history_card(root)

        # fallback labels (tương thích controller cũ)
        self.lbl_total_count    = QLabel("")
        self.lbl_total_refund   = QLabel("")
        self.lbl_total_exchange = QLabel("")
        for lb in (self.lbl_total_count, self.lbl_total_refund, self.lbl_total_exchange):
            lb.setVisible(False)
            root.addWidget(lb)

    # ── Header ──────────────────────────────────────────────────────────────
    def _build_header(self, root):
        hl = QHBoxLayout()
        col = QVBoxLayout()
        col.setSpacing(3)
        col.addWidget(_lbl("Đổi / Trả Hàng", TEXT_DARK, 21, 900))
        col.addWidget(_lbl("Tra cứu hóa đơn và xử lý yêu cầu đổi hoặc trả sản phẩm",
                           TEXT_LIGHT, 13, 400))
        hl.addLayout(col)
        hl.addStretch()
        
        self.btn_create_return = _btn("➕ Tạo phiếu đổi trả", 42, SUCCESS, "white")
        hl.addWidget(self.btn_create_return)
        
        root.addLayout(hl)

    # ── Stat cards ──────────────────────────────────────────────────────────
    def _build_stats(self, root):
        hl = QHBoxLayout()
        hl.setSpacing(12)
        c1, self.lbl_stat_total = _mini_stat("Tổng giao dịch", "0",  INFO,    "🔄")
        c2, self.lbl_stat_exc   = _mini_stat("Đổi hàng",       "0",  PRIMARY, "🔁")
        c3, self.lbl_stat_ret   = _mini_stat("Trả hàng",       "0",  DANGER,  "📦")
        c4, self.lbl_stat_ref   = _mini_stat("Tổng hoàn tiền", "0 ₫", SUCCESS, "💰")
        for c in (c1, c2, c3, c4):
            hl.addWidget(c)
        root.addLayout(hl)

    # ── Process Dialog (Popup) ────────────────────────────────────────────────────────
    def _build_process_card(self):
        self.return_dialog = QDialog(self)
        self.return_dialog.setWindowTitle("Tạo Phiếu Đổi / Trả")
        self.return_dialog.setFixedSize(720, 750)
        self.return_dialog.setStyleSheet(f"""
            QDialog {{ background-color: {BG_CARD}; border-radius: 16px; }}
            QLabel {{ font-family: 'Nunito', sans-serif; }}
        """)
        
        pl = QVBoxLayout(self.return_dialog)
        pl.setContentsMargins(28, 28, 28, 28)
        pl.setSpacing(14)
        
        lbl_title = QLabel("TẠO PHIẾU ĐỔI / TRẢ")
        lbl_title.setStyleSheet(f"color: {PRIMARY_DARK}; font-size: 18px; font-weight: 900; border-bottom: 2px solid {PRIMARY_LIGHT}; padding-bottom: 8px;")
        pl.addWidget(lbl_title)

        # --- Step bar
        sb = QHBoxLayout()
        sb.setSpacing(0)
        self._sn1, self._sl1, self._st1 = _step_indicator(1, "Tra cứu hóa đơn", True)
        self._sn2, self._sl2, self._st2 = _step_indicator(2, "Xác nhận xử lý",  False)
        arr = QLabel("›")
        arr.setStyleSheet(f"color:{TEXT_LIGHT};font-size:20px;padding:0 10px;background:transparent;")
        arr.setAlignment(Qt.AlignCenter)
        sb.addWidget(self._sn1); sb.addWidget(arr); sb.addWidget(self._sn2); sb.addStretch()
        pl.addLayout(sb)

        # --- Policy
        pol = QLabel(
            "📌  Hóa đơn phải trong vòng <b>3 ngày</b> kể từ ngày xuất. "
            "Sản phẩm cần giữ nguyên tem mác. Chênh lệch tiền tính tự động."
        )
        pol.setWordWrap(True)
        pol.setStyleSheet(
            "background:#f0fdf4;color:#166534;border:1px solid #bbf7d0;"
            "border-radius:8px;padding:9px 14px;font-size:12px;"
            "font-family:'Nunito',sans-serif;"
        )
        pl.addWidget(pol)

        # --- Stack
        self._step_stack = QStackedWidget()
        self._build_step1(self._step_stack)
        self._build_step2(self._step_stack)
        pl.addWidget(self._step_stack)

    # ── Step 1 ──────────────────────────────────────────────────────────────
    def _build_step1(self, stack):
        pg = QWidget()
        vl = QVBoxLayout(pg)
        vl.setContentsMargins(0, 8, 0, 0)
        vl.setSpacing(10)

        # Lọc / Tìm kiếm hóa đơn
        filter_lay = QHBoxLayout()
        filter_lay.setSpacing(8)
        self.txt_search_inv = QLineEdit()
        self.txt_search_inv.setPlaceholderText("🔍  Tìm theo mã HĐ, Tên KH, Số điện thoại...")
        _input_style(self.txt_search_inv, 42)
        filter_lay.addWidget(self.txt_search_inv)
        vl.addLayout(filter_lay)

        # Search row
        sr = QHBoxLayout()
        sr.setSpacing(8)
        lbl_id = _lbl("Chọn hóa đơn:", TEXT_MID, 13, 700)
        lbl_id.setFixedWidth(100)

        self.cb_invoice_id = QComboBox()
        self.cb_invoice_id.setFixedHeight(42)
        _combo_style(self.cb_invoice_id)
        # Bỏ setEditable để user click vào là hiện dropdown ngay
        
        self.btn_lookup = _btn("🔍  Tra cứu / Kiểm tra", 42)
        self.btn_lookup.setFixedWidth(180)

        sr.addWidget(lbl_id)
        sr.addWidget(self.cb_invoice_id, 1)
        sr.addWidget(self.btn_lookup)
        vl.addLayout(sr)

        # Info label
        self.lbl_inv_info = QLabel("Nhập mã hóa đơn rồi nhấn Tra cứu để xem chi tiết.")
        self.lbl_inv_info.setStyleSheet(
            f"color:{TEXT_LIGHT};font-size:12px;font-style:italic;"
            "font-family:'Nunito',sans-serif;background:transparent;"
        )
        vl.addWidget(self.lbl_inv_info)

        # Table gợi ý click
        hint = _lbl("👆  Click vào dòng sản phẩm để chọn mặt hàng cần đổi/trả:", TEXT_MID, 12, 600)
        vl.addWidget(hint)

        self.tbl_invoice_items = styled_table(
            ["Tên sản phẩm", "SL mua", "Đơn giá", "Thành tiền"]
        )
        self.tbl_invoice_items.setFixedHeight(220)
        self.tbl_invoice_items.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tbl_invoice_items.setColumnWidth(1, 80)
        self.tbl_invoice_items.setColumnWidth(2, 120)
        self.tbl_invoice_items.setColumnWidth(3, 130)
        self.tbl_invoice_items.verticalHeader().setDefaultSectionSize(45)
        self.tbl_invoice_items.setStyleSheet(self.tbl_invoice_items.styleSheet() + "QTableWidget::item { padding: 8px; font-size: 14px; }")
        vl.addWidget(self.tbl_invoice_items)

        # Next button
        self.btn_next = _btn("Tiếp tục  →", 42)
        self.btn_next.setFixedWidth(150)
        self.btn_next.setEnabled(False)
        vl.addWidget(self.btn_next, alignment=Qt.AlignRight)

        stack.addWidget(pg)

    # ── Step 2 ──────────────────────────────────────────────────────────────
    def _build_step2(self, stack):
        pg = QWidget()
        vl = QVBoxLayout(pg)
        vl.setContentsMargins(0, 8, 0, 0)
        vl.setSpacing(12)

        # Selected product banner
        self.lbl_selected_prod = QLabel("—")
        self.lbl_selected_prod.setWordWrap(True)
        self.lbl_selected_prod.setStyleSheet(f"""
            background:#f0f7ff;border-left:4px solid {PRIMARY};
            padding:10px 16px;color:{TEXT_DARK};font-size:13px;
            font-family:'Nunito',sans-serif;border-radius:6px;
        """)
        vl.addWidget(self.lbl_selected_prod)

        # --- 2-column form grid
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(3, 1)

        # Hình thức
        self.cb_return_type = QComboBox()
        self.cb_return_type.addItems(["Trả hàng (hoàn tiền)", "Đổi hàng (lấy hàng khác)"])
        self.cb_return_type.setFixedHeight(40)
        _combo_style(self.cb_return_type)

        # Số lượng
        self.spn_qty = QSpinBox()
        self.spn_qty.setMinimum(1); self.spn_qty.setMaximum(999)
        self.spn_qty.setFixedHeight(40)
        self.spn_qty.setStyleSheet(f"""
            QSpinBox{{background:#fff;border:1.5px solid {BORDER};border-radius:8px;
                padding:0 10px;font-size:14px;font-weight:700;color:{TEXT_DARK};
                font-family:'Nunito',sans-serif;}}
            QSpinBox:focus{{border-color:{PRIMARY};}}
        """)

        grid.addWidget(_lbl("Hình thức xử lý:"), 0, 0)
        grid.addWidget(self.cb_return_type, 0, 1)
        grid.addWidget(_lbl("Số lượng:"), 0, 2)
        grid.addWidget(self.spn_qty, 0, 3)

        # Lý do
        self.cb_reason = QComboBox()
        self.cb_reason.addItems([
            "Sản phẩm bị lỗi NSX", "Không vừa size",
            "Đổi màu sắc khác", "Khách hàng đổi ý", "Lý do khác"
        ])
        self.cb_reason.setFixedHeight(40)
        _combo_style(self.cb_reason)

        # Ghi chú
        self.txt_note = QLineEdit()
        self.txt_note.setPlaceholderText("Ghi chú thêm về tình trạng hàng...")
        _input_style(self.txt_note, 40)

        grid.addWidget(_lbl("Lý do:"), 1, 0)
        grid.addWidget(self.cb_reason, 1, 1)
        grid.addWidget(_lbl("Ghi chú:"), 1, 2)
        grid.addWidget(self.txt_note, 1, 3)

        vl.addLayout(grid)

        # --- Chọn sản phẩm mới (chỉ hiện khi Đổi hàng)
        self._new_prod_frame = QFrame()
        self._new_prod_frame.setStyleSheet(
            f"background:#f8fafc;border:1px solid {BORDER};border-radius:8px;"
        )
        np_vl = QVBoxLayout(self._new_prod_frame)
        np_vl.setContentsMargins(14, 10, 14, 10)
        np_vl.setSpacing(6)
        np_vl.addWidget(_lbl("Chọn sản phẩm mới muốn đổi sang:", TEXT_DARK, 13, 700))
        self.cb_new_product = QComboBox()
        self.cb_new_product.setFixedHeight(40)
        _combo_style(self.cb_new_product)
        np_vl.addWidget(self.cb_new_product)
        
        # Thêm ô chọn size và màu sắc
        attr_lay = QHBoxLayout()
        attr_lay.setSpacing(12)
        
        attr_lay.addWidget(_lbl("Chọn Size:", TEXT_DARK, 13, 700))
        self.cb_new_size = QComboBox()
        self.cb_new_size.setFixedHeight(36)
        self.cb_new_size.setFixedWidth(100)
        _combo_style(self.cb_new_size)
        attr_lay.addWidget(self.cb_new_size)
        
        attr_lay.addWidget(_lbl("Chọn Màu:", TEXT_DARK, 13, 700))
        self.cb_new_color = QComboBox()
        self.cb_new_color.setFixedHeight(36)
        self.cb_new_color.setFixedWidth(120)
        _combo_style(self.cb_new_color)
        attr_lay.addWidget(self.cb_new_color)
        
        attr_lay.addStretch()
        np_vl.addLayout(attr_lay)

        self.lbl_diff = QLabel()
        self.lbl_diff.setStyleSheet(
            f"color:{TEXT_MID};font-size:12px;font-family:'Nunito',sans-serif;"
            "background:transparent;"
        )
        np_vl.addWidget(self.lbl_diff)
        vl.addWidget(self._new_prod_frame)
        self._new_prod_frame.setVisible(False)

        # --- Refund banner
        rf = QFrame()
        rf.setStyleSheet(
            "background:#fffbeb;border:1.5px dashed #f59e0b;border-radius:10px;"
        )
        rf_hl = QHBoxLayout(rf)
        rf_hl.setContentsMargins(18, 12, 18, 12)
        rf_hl.addWidget(_lbl("Tổng tiền hoàn lại / thu thêm:", "#b45309", 13, 700))
        rf_hl.addStretch()
        self.lbl_refund_amount = QLabel("0 ₫")
        self.lbl_refund_amount.setStyleSheet(
            "color:#d97706;font-size:22px;font-weight:900;"
            "font-family:'Nunito',sans-serif;background:transparent;"
        )
        rf_hl.addWidget(self.lbl_refund_amount)
        vl.addWidget(rf)

        # --- Action buttons
        br = QHBoxLayout()
        br.setSpacing(10)
        self.btn_back = _btn("← Quay lại", 42, "#f1f5f9", TEXT_MID, BORDER_MED, "#e2e8f0")
        self.btn_clear = _btn("Hủy bỏ", 42, "#fff1f2", DANGER, "#fecdd3", "#ffe4e6")
        self.btn_confirm = _btn("✔  Xác nhận hoàn tất", 42, "#059669", "white", None, "#047857")
        br.addWidget(self.btn_back)
        br.addWidget(self.btn_clear)
        br.addStretch()
        br.addWidget(self.btn_confirm)
        vl.addLayout(br)

        stack.addWidget(pg)

    # ── History card ────────────────────────────────────────────────────────
    def _build_history_card(self, root):
        _, hl = _card(root, "Lịch Sử Đổi / Trả", "📄")

        # Filter row
        fr = QHBoxLayout()
        fr.setSpacing(8)

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍  Tìm theo mã HĐ, tên khách hàng hoặc mã phiếu...")
        _input_style(self.txt_search, 38)

        self.btn_filter_all = self._filter_btn("Tất cả",   True)
        self.btn_filter_exc = self._filter_btn("Đổi hàng", False)
        self.btn_filter_ret = self._filter_btn("Trả hàng", False)

        fr.addWidget(self.txt_search, 1)
        for b in (self.btn_filter_all, self.btn_filter_exc, self.btn_filter_ret):
            fr.addWidget(b)
        hl.addLayout(fr)

        # History table
        self.tbl_history = styled_table([
            "Mã GD", "Mã HĐ", "Sản phẩm cũ", "SL",
            "Đơn giá", "Sản phẩm mới", "Chênh lệch",
            "Hoàn tiền", "Lý do", "Loại", "Thời gian"
        ])
        hh = self.tbl_history.horizontalHeader()
        for col, w in enumerate([60, 60, 155, 50, 100, 150, 100, 100, 0, 85, 130]):
            if w:
                self.tbl_history.setColumnWidth(col, w)
            else:
                hh.setSectionResizeMode(col, QHeaderView.Stretch)
        self.tbl_history.setMinimumHeight(200)
        hl.addWidget(self.tbl_history)

    # ── Helpers ─────────────────────────────────────────────────────────────
    def _filter_btn(self, text, active):
        btn = QPushButton(text)
        btn.setFixedHeight(38)
        btn.setCursor(Qt.PointingHandCursor)
        if active:
            btn.setStyleSheet(f"""
                QPushButton{{background:{PRIMARY};color:white;border:none;
                    border-radius:8px;font-size:13px;font-weight:700;
                    padding:0 16px;font-family:'Nunito',sans-serif;}}
                QPushButton:hover{{background:{PRIMARY_DARK};}}
            """)
        else:
            btn.setStyleSheet(f"""
                QPushButton{{background:#f1f5f9;color:{TEXT_MID};
                    border:1.5px solid {BORDER};border-radius:8px;
                    font-size:13px;font-weight:700;padding:0 16px;
                    font-family:'Nunito',sans-serif;}}
                QPushButton:hover{{background:#e2e8f0;color:{TEXT_DARK};}}
            """)
        return btn

    def _style_combo(self, cb):
        _combo_style(cb)

    # ── Step indicator update (gọi từ controller hoặc tự gọi) ───────────────
    def set_step(self, step: int):
        """Cập nhật màu step badge khi chuyển bước."""
        for num_w, txt_w, active in [
            (self._sl1, self._st1, step == 1),
            (self._sl2, self._st2, step == 2),
        ]:
            if active:
                num_w.setStyleSheet(
                    f"background:{PRIMARY};color:white;border-radius:11px;"
                    "font-size:12px;font-weight:800;padding:2px 8px;"
                    "font-family:'Nunito',sans-serif;"
                )
                txt_w.setStyleSheet(
                    f"color:{TEXT_DARK};font-size:13px;font-weight:800;"
                    "font-family:'Nunito',sans-serif;background:transparent;"
                )
            else:
                num_w.setStyleSheet(
                    "background:#e2e8f0;color:#94a3b8;border-radius:11px;"
                    "font-size:12px;font-weight:800;padding:2px 8px;"
                    "font-family:'Nunito',sans-serif;"
                )
                txt_w.setStyleSheet(
                    f"color:{TEXT_LIGHT};font-size:13px;font-weight:600;"
                    "font-family:'Nunito',sans-serif;background:transparent;"
                )
