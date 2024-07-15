from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QDialogButtonBox, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QDialog, \
    QVBoxLayout


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName(): Dialog.setObjectName(u"Dialog")
        Dialog.resize(500, 300)

        self.mainBox= QDialogButtonBox(Dialog)
        self.mainBox.setObjectName(u"buttonBox")
        self.mainBox.setWindowTitle(u"Log In")

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
        self.gridLayout.addWidget(self.close_btn, 2, 2)

        self.retranslateUi(Dialog)
        self.mainBox.accepted.connect(Dialog.accept)
        self.mainBox.rejected.connect(Dialog.reject)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.id_label.setText(QCoreApplication.translate("Dialog", u"ID: ", None))
        self.pw_label.setText(QCoreApplication.translate("Dialog", u"Password: ", None))
        self.close_btn.setText(QCoreApplication.translate("Dialog", u"Close", None))

# New window pop-up when login successful
class LoginSuccessful(QDialog):
    def setupUi(self):
        self.resize(200, 100)
        self.setWindowTitle("Login Failed")

        self.fail_label= QLabel("Login failed. Try again.")
        self.fail_label.setObjectName(u"fail_label")
        self.fail_close_btn= QPushButton("Close")
        self.fail_close_btn.setObjectName(u"fail_close_btn")

        fail_layout= QGridLayout()
        fail_layout.addWidget(self.fail_label, 0, 0)
        fail_layout.addWidget(self.fail_close_btn, 1, 1)

        self.fail_close_btn.clicked.connect(self.closeButtonClicked)

    def closeButtonClicked(self): self.close()

# New window pop-up when login failed
class LoginFailed(QDialog):
    def setupUi(self):
        self.resize(200, 100)
        self.setWindowTitle("Login Failed")

        self.fail_label = QLabel("Login failed. Try again.")
        self.fail_label.setObjectName(u"fail_label")
        self.fail_close_btn = QPushButton("Close")
        self.fail_close_btn.setObjectName(u"fail_close_btn")

        fail_layout = QGridLayout()
        fail_layout.addWidget(self.fail_label, 0, 0)
        fail_layout.addWidget(self.fail_close_btn, 1, 1)

        self.fail_close_btn.clicked.connect(self.closeButtonClicked)

    def closeButtonClicked(self): self.close()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui= Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.login_btn.clicked.connect(self.loginBtn_clicked)
        self.ui.close_btn.clicked.connect(self.closeBtn_clicked)

        self.id= None
        self.password= None

        self.right_id= 'test'
        self.right_password= 'test'

    def setId(self, id): self.id= id

    def setPassword(self, password): self.password= password

    def loginBtn_clicked(self):
        if self.id== self.right_id and self.password== self.right_password:
            login_Successful= LoginSuccessful()
        else:
            if self.id!= self.right_id:
                login_failed= LoginFailed()
            elif self.password!= self.right_password
    def closeBtn_clicked(self): self.close()
