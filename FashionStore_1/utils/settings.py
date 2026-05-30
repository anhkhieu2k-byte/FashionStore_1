import json
import os

# Lấy thư mục AppData của hệ thống Windows (hoặc thư mục home trên OS khác)
APPDATA_DIR = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'FashionStore')
# Đảm bảo thư mục lưu trữ luôn tồn tại
os.makedirs(APPDATA_DIR, exist_ok=True)

SETTINGS_FILE = os.path.join(APPDATA_DIR, "settings.json")


def save_login(username, password):

    data = {
        "remember": True,
        "username": username,
        "password": password
    }

    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)



def clear_login():

    if os.path.exists(SETTINGS_FILE):
        os.remove(SETTINGS_FILE)



def load_login():

    if not os.path.exists(SETTINGS_FILE):
        return None

    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)