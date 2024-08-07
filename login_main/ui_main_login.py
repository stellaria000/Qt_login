from msilib import Dialog
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtSql import QSqlQuery, QSqlDatabase
from PySide6.QtWidgets import QDialogButtonBox, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QDialog, \
    QVBoxLayout, QMainWindow, QHBoxLayout, QMessageBox, QComboBox, QCheckBox
from login_db import init_db


# MAIN DIALOGUE UI
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.login_cnt = 0
        self.setupUi()
        self.setWindowTitle("Log In")

        # INITIALIZE DATABASE CONNEXTION(EXAMPLE: REPLACE W/ YOUR ACTUAL INITIALIZATION)
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
        self.setFixedSize(300, 200)  # #343b48
        self.setStyleSheet("background-color: #1b1e23")

        # MAIN LAYOUT CONTAINS OTHER BOXES
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(20, 20, 20, 20)
        mainLayout.setSpacing(10)

        # SYSTEM BOX
        system_box = QHBoxLayout()
        system_box.setSpacing(10)

        self.sys_label = QLabel("System", self)
        self.sys_label.setMinimumWidth(50)
        self.sys_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sys_label.setStyleSheet("color: white")

        self.sys_cbBox = QComboBox()
        self.sys_cbBox.addItem("01_SECURITY")
        self.sys_cbBox.addItem("02_INTERSECTION")
        self.sys_cbBox.addItem("03_SCHOOLZONE")
        self.sys_cbBox.addItem("04_LEFT TURN")
        self.sys_cbBox.setMinimumWidth(200)
        self.sys_cbBox.setStyleSheet("border-radius: 2px; background-color: #272c36; color: #8a95aa")

        system_box.addWidget(self.sys_label)
        system_box.addWidget(self.sys_cbBox)

        # ID BOX
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

        # PASSWORD BOX
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

        # LOGIN FUNCTION(ID SAVE, LOGIN COUNT)
        function_box = QHBoxLayout()
        function_box.setSpacing(10)

        self.idSave_chkBox = QCheckBox("Save Id")
        self.idSave_chkBox.setStyleSheet("color: white; font: 8pt")

        # LOGIN LABEL- REPLACING LOGIN MESSAGE DIALOG
        self.login_label = QLabel("Please Enter Id and Password", self)
        self.login_label.setStyleSheet("color: white; font: 12pt")
        self.login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.login_failedCnt_label = QLabel(u"Login Failed: " + str(self.login_cnt) + "/5")
        self.login_failedCnt_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.login_failedCnt_label.setStyleSheet("color: white; font: 8pt")

        function_box.addWidget(self.idSave_chkBox)
        function_box.addWidget(self.login_failedCnt_label)

        # Button Box
        button_box = QHBoxLayout()
        button_box.setSpacing(10)

        self.login_btn = QPushButton("Log In", self)
        self.login_btn.setStyleSheet("border-radius: 2px; background-color: #2c313c; color: #8a95aa")

        self.close_btn = QPushButton("Close", self)
        self.close_btn.setStyleSheet("border-radius: 2px; background-color: #2c313c; color: #8a95aa")

        button_box.addWidget(self.login_btn)
        button_box.addWidget(self.close_btn)

        # ADD BOXES TO MAIN LAYOUT
        mainLayout.addLayout(system_box)
        mainLayout.addLayout(id_box)
        mainLayout.addLayout(pw_box)
        mainLayout.addLayout(function_box)
        mainLayout.addWidget(self.login_label)
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
        '''log in with the accounts uploaded in the database
        id_exists = False
        password_correct = False

        # Check if the ID exists
        query = QSqlQuery(self.db)
        query.prepare("SELECT * FROM ACCOUNTS WHERE ID = ?")
        query.addBindValue(self.id)

        if query.exec() and query.next():
            id_exists = True

        # Check if the ID and Password match
        query.prepare("SELECT * FROM ACCOUNTS WHERE ID = ? AND PASSWORD = ?")
        query.addBindValue(self.id)
        query.addBindValue(self.password)

        if query.exec() and query.next():
            password_correct = True

        if id_exists and password_correct:
            login_success = LoginMessageDialog("Login Successful.")
            login_success.setWindowTitle("Login Successful")
            login_success.exec_()
            self.accept()
        else:
            login_failed = LoginMessageDialog("Login Failed. Try again.")
            login_failed.setWindowTitle("Login Failed")
            login_failed.exec_()
            if not id_exists:
                self.id_edit.clear()
            if not password_correct:
                self.pw_edit.clear()
        '''
        if not self.id or not self.password:  # NO ID OR PW INPUT
            self.login_label.setText("Enter Id and Password Correctly")

        elif self.id != self.right_id or self.password != self.right_password:
            if self.id != self.right_id: self.id_edit.clear()
            if self.password != self.right_password: self.pw_edit.clear()
            self.login_label.setText("Login Failed. Try Again")
            self.login_failCnt()  # METHOD CALL

        else:
            self.login_label.setText("Login Successful")
            self.accept()

    def login_failCnt(self):
        self.login_cnt += 1
        self.login_failedCnt_label.setText(u"Login Failed: " + str(self.login_cnt) + "/5")

        # if self.login_cnt>= 5:

    def closeBtn_clicked(self):
        self.close()

    def showMessage(self, title, message):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.exec_()

# POP-UP WINDOW AFTER LOGIN BUTTON PUSHED: LOGIN RESULT MESSAGE DIALOG
class LoginMessageDialog(QDialog):
    def __init__(self, message):
        super().__init__()
        self.message = message
        self.setupUi()

    def setupUi(self):
        self.resize(200, 100)
        self.setWindowTitle("Login Message")
        self.setStyleSheet("background-color: #1b1e23")

        self.message_label = QLabel(self.message)
        self.message_label.setObjectName("msg_label")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setStyleSheet("color: #8a95aa")
        self.msg_close_btn = QPushButton("Close")
        self.msg_close_btn.setObjectName("msg_close_btn")
        self.msg_close_btn.setStyleSheet("border-radius: 2px; background-color: #2c313c; color: #8a95aa")

        msg_layout = QGridLayout()
        msg_layout.addWidget(self.message_label, 0, 0)
        msg_layout.addWidget(self.msg_close_btn, 1, 1)
        self.setLayout(msg_layout)

        self.msg_close_btn.clicked.connect(self.closeButtonClicked)

    def closeButtonClicked(self): self.close()