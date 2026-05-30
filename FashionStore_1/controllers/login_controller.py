import traceback

from PyQt5.QtWidgets import QMessageBox

from ui.main_window import MainWindow
from utils.settings import save_login, clear_login


class LoginController:

    def __init__(self, ui):

        self.ui = ui

        self.ui.btn_login.clicked.connect(
            self.login
        )

    # =========================================
    # LOGIN
    # =========================================

    def login(self):

        username = self.ui.txt_username.text().strip()

        password = self.ui.txt_password.text().strip()

        # =====================================
        # DEMO ACCOUNT
        # =====================================

        if username == "admin" and password == "123456":

            # =================================
            # REMEMBER LOGIN
            # =================================

            if self.ui.chk_remember.isChecked():

                save_login(username, password)

            else:

                clear_login()

            # =================================
            # OPEN MAIN WINDOW
            # =================================

            try:

                self.main_window = MainWindow()

                self.main_window.show()

                self.ui.hide()

            except Exception as e:

                traceback.print_exc()

                from utils.message_utils import show_error
                show_error(
                    self.ui,
                    "Lỗi mở cửa sổ chính",
                    f"Không thể mở trang chủ:\n{str(e)}\n\nXem console để biết chi tiết."
                )

        else:

            self.ui.lbl_status.setText(
                "Sai tài khoản hoặc mật khẩu"
            )
