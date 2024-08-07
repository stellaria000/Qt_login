import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

class MyApp(QWidget):
    def __init__(self):
        super.__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle('QMessageBox')
        self.setGrometry(300, 300, 300, 300)
        self.show()

    def closeEvent(self, event):
        reply= QMessageBox.question(self, 'Message', 'Are you sure to quit?', QMessageBox.Yes| QMessageBox.No, QMessageBox.No)

        if reply== QMessageBox.Yes: event.accept()  
        else: event.ignore()

if __name__== '__main__':
    app= QApplication(sys.argv)
    ex= MyApp()
    
    sys.exit(app.exec())