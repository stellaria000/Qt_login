from msilib import Dialog
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtSql import QSqlQuery, QSqlDatabase
from PySide6.QtWidgets import QDialogButtonBox, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QDialog, \
    QVBoxLayout, QMainWindow, QHBoxLayout, QMessageBox
from login_db import init_db

# MAIN DIALOGUE UI
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.setWindowTitle("Log In")

        # Initialize database connection (example; replace with your actual initialization)
        self.db = init_db()
        self.id = None
        self.password = None
        self.right_id = 'test'
        self.right_password = 'test'

        self.id_edit.textChanged.connect(self.setId)
        self.pw_edit.textChanged.connect(self.setPassword)
        self.login_btn.clicked.connect(self.loginBtn_clicked)
        self.close_btn.clicked.connect(self.closeBtn_clicked)

    def setupUi(self):
        self.setFixedSize(300, 150)
        self.setStyleSheet("background-color: #1b1e23")

        # Create main layout
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(10, 10, 10, 10)

        # ID Box
        id_box = QHBoxLayout()
        id_box.setSpacing(10)

        self.id_label = QLabel("ID", self)
        self.id_label.setStyleSheet("color: white")
        self.id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.id_label.setMinimumWidth(50)
        self.id_edit = QLineEdit(self)
        self.id_edit.setStyleSheet("border-radius: 2px; background-color: #272c36; color: #8a95aa")

        id_box.addWidget(self.id_label)
        id_box.addWidget(self.id_edit)

        # Password Box
        pw_box = QHBoxLayout()
        pw_box.setSpacing(10)

        self.pw_label = QLabel("Password", self)
        self.pw_label.setStyleSheet("color: white")
        self.pw_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pw_label.setMinimumWidth(50)
        self.pw_edit = QLineEdit(self)
        self.pw_edit.setEchoMode(QLineEdit.Password)
        self.pw_edit.setStyleSheet("border-radius: 2px; background-color: #272c36; color: #8a95aa")

        pw_box.addWidget(self.pw_label)
        pw_box.addWidget(self.pw_edit)

        # Button Box
        button_box = QHBoxLayout()
        button_box.setSpacing(10)

        self.login_btn = QPushButton("Log In", self)
        self.login_btn.setStyleSheet("border-radius: 2px; background-color: #2c313c; color: #8a95aa")

        self.close_btn = QPushButton("Close", self)
        self.close_btn.setStyleSheet("border-radius: 2px; background-color: #2c313c; color: #8a95aa")

        button_box.addWidget(self.login_btn)
        button_box.addWidget(self.close_btn)

        # Add boxes to main layout
        mainLayout.addLayout(id_box)
        mainLayout.addLayout(pw_box)
        mainLayout.addLayout(button_box)

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("Dialog", u"Log In", None))
        self.id_label.setText(QCoreApplication.translate("Dialog", u"ID", None))
        self.pw_label.setText(QCoreApplication.translate("Dialog", u"Password", None))
        self.close_btn.setText(QCoreApplication.translate("Dialog", u"Close", None))

    def setId(self, id):
        self.id = id

    def setPassword(self, password):
        self.password = password

    def loginBtn_clicked(self):
        id_exists= False
        password_correct= False
        query = QSqlQuery(self.db)
        # query.prepare("SELECT * FROM ACCOUNTS WHERE ID = ? AND PASSWORD = ?")
        query.prepare("SELECT * FROM ACCOUNTS WHERE ID = ?")
        query.addBindValue(self.id)
        # query.addBindValue(self.password)

        # if not query.exec():
        #     print(query.lastError().text())
        #     return
        if query.exec() and query.next(): id_exists= True

        query.prepare("SELECT * FROM ACCOUNTS WHERE ID = ? AND PASSWORD = ?")
        query.addBindValue(self.id)
        query.addBindValue(self.password)

        if query.exec() and query.next():
            password_correct= True

        if id_exists and password_correct:
            msg_dialog= LoginMessageDialog("Login Successful")
            msg_dialog.exec()
            self.close()
        else:
            msg_dialog = LoginMessageDialog("Login Failed. Try again")
            msg_dialog.exec()

            if not id_exists and not password_correct:
                self.id_edit.clear()
                self.pw_edit.clear()
            elif not id_exists: self.id_edit.clear()
            elif not password_correct: self.pw_edit.clear()


    def closeBtn_clicked(self):
        self.close()

    def showMessage(self, title, message):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.exec_()

# Pop-up window after Log In button pushed: Login result message dialog
class LoginMessageDialog(QDialog):
    def __init__(self, message):
        super().__init__()
        self.message= message
        self.setupUi()

    def setupUi(self):
        self.resize(200, 100)
        self.setWindowTitle("Login Message")
        self.setStyleSheet("background-color: #1b1e23")

        self.message_label= QLabel(self.message)
        self.message_label.setObjectName("msg_label")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setStyleSheet("color: #8a95aa")
        self.msg_close_btn= QPushButton("Close")
        self.msg_close_btn.setObjectName("msg_close_btn")
        self.msg_close_btn.setStyleSheet("border-radius: 2px; background-color: #2c313c; color: #8a95aa")

        msg_layout= QGridLayout()
        msg_layout.addWidget(self.message_label, 0, 0)
        msg_layout.addWidget(self.msg_close_btn, 1, 1)
        self.setLayout(msg_layout)

        self.msg_close_btn.clicked.connect(self.closeButtonClicked)

    def closeButtonClicked(self): self.close()