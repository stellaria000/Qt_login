import sys

from PySide6.QtWidgets import QApplication

from LoginDialog import MyWindow

if __name__== "__main__":
    app= QApplication(sys.argv)
    window= MyWindow()
    window.show()
    app.exec_()
