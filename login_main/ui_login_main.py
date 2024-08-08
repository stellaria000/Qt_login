import sys

from PySide6.QtWidgets import QApplication
from ui_main_login import LoginWindow


if __name__== "__main__":
    app= QApplication(sys.argv)
    window= LoginWindow()
    window.show()

    app.exec_()