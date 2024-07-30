'''
    SQL Books Example
    This example shows how to use Qt SQL classes with a model/view framework.
    The books example shows how Qt's SQL classes can be used with the model/view framework to
    create rich user interfaces for information stored in a database.
'''
import sys

from PySide6.QtWidgets import QApplication

from SQL_Books_Example.bookwindow import BookWindow

if __name__== "__main__":
    app= QApplication([])

    window= BookWindow()
    window.resize(1000, 800)
    window.show()

    sys.exit(app.exec())