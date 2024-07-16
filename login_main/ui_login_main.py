import sys

from PySide6.QtWidgets import QApplication
from login_main.ui_main_login import LoginDialog, LoginWindow

if __name__== "__main__":
    app= QApplication(sys.argv)
    window= LoginWindow()
    window.show()

    app.exec_()