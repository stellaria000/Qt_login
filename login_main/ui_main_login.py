from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QDialogButtonBox, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QDialog, \
    QVBoxLayout, QMainWindow


# MAIN DIALOGUE UI
class LoginDialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName(): Dialog.setObjectName(u"login_Dialog")
        Dialog.resize(300, 150)
        Dialog.setWindowTitle("Log In")

        self.mainBox= QDialogButtonBox(Dialog)
        self.mainBox.setObjectName(u"buttonBox")
        self.mainBox.setWindowTitle(u"Log In")
        self.mainBox.setContentsMargins(10, 10, 10, 10)

        self.gridLayoutWidget= QWidget(Dialog)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setContentsMargins(10, 10, 10, 10)
        self.gridLayout= QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(10, 10, 10, 10)

        self.id_label= QLabel(self.gridLayoutWidget)
        self.id_label.setObjectName("id_label")
        self.id_label.setText("ID: ")
        self.id_edit= QLineEdit(self.gridLayoutWidget)
        self.id_edit.setObjectName("id_edit")
        self.pw_label= QLabel(self.gridLayoutWidget)
        self.pw_label.setObjectName("pw_label")
        self.pw_label.setText("Password: ")
        self.pw_edit= QLineEdit(self.gridLayoutWidget)
        # HIDING PASSWORD INPUT
        self.pw_edit.setEchoMode(QLineEdit.Password)
        self.pw_edit.setObjectName("pw_edit")

        self.login_btn= QPushButton(self.gridLayoutWidget)
        self.login_btn.setObjectName(u"login_btn")
        self.login_btn.setText(u"Log In")
        self.close_btn= QPushButton(self.gridLayoutWidget)
        self.close_btn.setObjectName("close_btn")
        self.close_btn.setText("Close")

        self.gridLayout.addWidget(self.id_label, 0, 0)
        self.gridLayout.addWidget(self.id_edit, 0, 1)
        self.gridLayout.addWidget(self.pw_label, 1, 0)
        self.gridLayout.addWidget(self.pw_edit, 1, 1)
        self.gridLayout.addWidget(self.login_btn, 1, 2)
        self.gridLayout.addWidget(self.close_btn, 2, 2)

        self.retranslateUi(Dialog)
        self.mainBox.accepted.connect(Dialog.accept)
        self.mainBox.rejected.connect(Dialog.reject)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.id_label.setText(QCoreApplication.translate("Dialog", u"ID: ", None))
        self.pw_label.setText(QCoreApplication.translate("Dialog", u"Password: ", None))
        self.close_btn.setText(QCoreApplication.translate("Dialog", u"Close", None))

# Functions for button action events, etc.
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui= LoginDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Log In")

        self.id= None
        self.password= None
        self.right_id= 'test'
        self.right_password= 'test'

        self.ui.id_edit.textChanged.connect(self.setId)
        self.ui.pw_edit.textChanged.connect(self.setPassword)
        self.ui.login_btn.clicked.connect(self.loginBtn_clicked)
        self.ui.close_btn.clicked.connect(self.closeBtn_clicked)

    def setId(self, id): self.id= id

    def setPassword(self, password): self.password= password

    def loginBtn_clicked(self):
        if self.id!= self.right_id or self.password!= self.right_password:
            login_failed= LoginMessageDialog("Login Failed. Try again.")
            login_failed.setWindowTitle("Login Failed")
            login_failed.exec_()
            if self.id != self.right_id and self.password!= self.right_password:
                self.ui.id_edit.clear()
                self.ui.pw_edit.clear()
            elif self.password != self.right_password: self.ui.pw_edit.clear()
            else: self.ui.id_edit.clear()

        else: # close both dialogues when the id and password both is right
            login_success= LoginMessageDialog("Login Successful.")
            login_success.setWindowTitle("Login Successful")
            login_success.exec_()
            self.close()

    def closeBtn_clicked(self): self.close()

# Pop-up window after Log In button pushed: Login result message dialog
class LoginMessageDialog(QDialog):
    def __init__(self, message):
        super().__init__()
        self.message= message
        self.setupUi()

    def setupUi(self):
        self.resize(200, 100)
        self.setWindowTitle("Login Message")

        self.message_label= QLabel(self.message)
        self.message_label.setObjectName("msg_label")
        self.msg_close_btn= QPushButton("Close")
        self.msg_close_btn.setObjectName("msg_close_btn")

        msg_layout= QGridLayout()
        msg_layout.addWidget(self.message_label, 0, 0)
        msg_layout.addWidget(self.msg_close_btn, 1, 1)
        self.setLayout(msg_layout)

        self.msg_close_btn.clicked.connect(self.closeButtonClicked)

    def closeButtonClicked(self): self.close()