import sys
from PySide6.QtWidgets import QApplication, QWidget, QCheckBox
from PySide6.QtCore import Qt

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
    
    def setupUi(self):
        chk= QCheckBox('Show title', self)
        chk.move(20, 20)
        chk.toggle()
        chk.stateChanged.connect(self.changeTitle)

        self.setWindowTitle('QCheckBox')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def changeTitle(self, state):
        if state== Qt.Checked: self.setWindowTitle('QCheckBox')
        else: self.setWindowTitle('')

if __name__== '__main__':
    app= QApplication(sys.argv)
    ex= MyApp()
    sys.exit(app.exec())

'''
    isChecked(): return the state of current Checkbox, True or False
    checkState(): return the state of checkBox
    toggle(): change the state of the checkBox
'''

''' # signals
    pressed, released, clicked, stateChanged()
'''