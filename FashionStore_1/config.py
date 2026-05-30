APP_NAME = "Fashion Store Management"

WINDOW_WIDTH  = 1280
WINDOW_HEIGHT = 800

# ============================================================
# THEME — Dựa trên ảnh thiết kế (Blue & Clean UI)
# ============================================================
PRIMARY        = "#2563eb"      # Xanh dương đậm (Nút chính)
PRIMARY_DARK   = "#1d4ed8"      
PRIMARY_LIGHT  = "#eff6ff"      # Xanh rất nhạt cho hover/active

BG_MAIN        = "#f4f7f9"      # Nền chính xám/xanh nhạt
BG_SIDEBAR     = "#113c5e"      # Nền sidebar xanh đen
BG_SIDEBAR_ACT = "#1a5276"      # Nền sidebar khi active (lighter)
BG_CARD        = "#ffffff"      # Nền card trắng
BG_INPUT       = "#ffffff"      

BORDER         = "#e2e8f0"      # Viền xám nhạt
BORDER_MED     = "#cbd5e1"

TEXT_DARK      = "#1e293b"      # Chữ đen
TEXT_MID       = "#475569"      # Chữ xám
TEXT_LIGHT     = "#94a3b8"      # Chữ nhạt
TEXT_WHITE     = "#ffffff"

SUCCESS        = "#10b981"      # Xanh ngọc
WARNING        = "#f59e0b"      # Vàng/Cam
DANGER         = "#ef4444"      # Đỏ
INFO           = "#0ea5e9"      # Xanh dương sáng
PURPLE         = "#8b5cf6"      # Tím

TABLE_ALT      = "#fafafa"      # Hàng chẵn của bảng

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME  = os.path.join(BASE_DIR, "database", "fashion_store.db")
