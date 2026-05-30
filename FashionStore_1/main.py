import sys
import traceback

from PyQt5.QtWidgets import QApplication
from ui.main_window import GLOBAL_STYLE

from database.init_db import init_database
from ui.login_window import LoginWindow
from controllers.login_controller import LoginController
def main():

    try:
        
        # =========================================
        # KHỞI TẠO DATABASE
        # =========================================
        init_database()

        app = QApplication(sys.argv)
        app.setStyleSheet(GLOBAL_STYLE)

        window = LoginWindow()

        controller = LoginController(window)

        window.show()

        sys.exit(app.exec_())

    except Exception as e:

        print("===== ERROR =====")

        traceback.print_exc()

        input()


if __name__ == "__main__":

    main()
