from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QLabel, QPushButton, QGridLayout, QWidget, QCheckBox, QLineEdit, QVBoxLayout, QHBoxLayout, QFrame, \
    QGraphicsDropShadowEffect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from databases.db_managements import AccountDBManagement, SystemDBManagement
from gui.core.json_settings import Settings
from gui.core.json_themes import Themes
from gui.widgets import PyDialog, PyLineEdit, PyPushButton, PyComboBox

import configparser
import os

class LoginWindow(PyDialog):
    def __init__(self):
        super().__init__(None, message= "로그인이 필요합니다.")
        self.DBManager= None
        self.setupUi()
        self.setFixedSize(self.sizeHint())
        
        #  SETTING INI FILE PATH
        self.ini_file_path= "D:\Project\gui" 
        self.config= configparser.ConfigParser()
        self.ini_file= 'Login_info.ini'
        self.load_login_info() # LOAD SAVED ID IF EXISTS
    

    def setupUi(self):
        settings = Settings()
        self.settings = settings.items
        themes = Themes()
        self.themes = themes.items
        self.DBManager= AccountDBManagement(self.settings["database_info"]["host"], self.settings["database_info"]["port"],
                                            self.settings["database_info"]["name"],
                                            self.settings["database_info"]["user"], self.settings["database_info"]["pw"])

        self.id = None
        self.password = None

        self.loginLayout= QVBoxLayout(self)
        self.system_Box= QHBoxLayout(self)
        self.id_Box= QHBoxLayout(self)
        self.pw_Box= QHBoxLayout(self)
        self.function_Box= QHBoxLayout(self)
        self.btn_box= QHBoxLayout(self)

        self.sys_label = QLabel("System", self)
        
        self.sys_cbBox= QComboBox()
        self.sys_cbBox.addItem("01_SECURITY")
        self.sys_cbBox.addItem("02_INTERSECTION")
        self.sys_cbBox.addItem("03_SCHOOLZONE")
        self.sys_cbBox.addItem("04_LEFT TURN")

        self.system_Box.addWidget(self.sys_label)
        self.system_Box.addWidget(self.sys_cbBox)

        self.id_label = QLabel()
        self.id_label.setObjectName("id_label")
        self.id_label.setText("ID")

        self.id_edit = QLineEdit()
        self.id_Box.addWidget(self.id_label)
        self.id_Box.addWidget(self.id_edit)

        self.pw_label = QLabel()
        self.pw_label.setObjectName("pw_label")
        self.pw_label.setText("Password")

        self.pw_edit = QLineEdit()
        self.pw_edit.setEchoMode(QLineEdit.Password)

        self.pw_Box.addWidget(self.pw_label)
        self.pw_Box.addWidget(self.pw_edit)

        self.idSave_chkBox = QCheckBox("Save Id")
        self.login_label = QLabel("Please Enter Id and Password", self)
        self.login_cnt= 0
        self.login_failedCnt_label = QLabel(u"Login Failed: " + str(self.login_cnt) + "/5")

        self.function_Box.addWidget(self.idSave_chkBox)
        self.function_Box.addWidget(self.login_failedCnt_label)

        self.login_btn = QPushButton()

        self.close_btn = QPushButton()
        self.btn_box.addWidget(self.login_btn)
        self.btn_box.addWidget(self.close_btn)

        self.loginLayout.addLayout(self.system_Box)
        self.loginLayout.addLayout(self.id_Box)
        self.loginLayout.addLayout(self.pw_Box)
        self.loginLayout.addLayout(self.function_Box)
        self.loginLayout.addWidget(self.login_label)
        self.loginLayout.addLayout(self.btn_box)

        self.alert_main_L.addLayout(self.loginLayout)

        self.alert_main_L.addWidget(self.btnBox)
        self.id_edit.textChanged.connect(self.setId)
        self.pw_edit.textChanged.connect(self.setPassword)
        # self.idSave_chkBox.checkStateChanged.connect(self.chkBox_checked)
        self.login_btn.clicked.connect(self.loginBtn_clicked)
        self.close_btn.clicked.connect(self.closeBtn_clicked)

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.id_label.setText(QCoreApplication.translate("Dialog", u"아이디 ", None))
        self.pw_label.setText(QCoreApplication.translate("Dialog", u"비밀번호 ", None))
        self.login_btn.setText(QCoreApplication.translate("Dialog", u"로그인", None))
        self.close_btn.setText(QCoreApplication.translate("Dialog", u"닫기", None))

    def setId(self, id): self.id = id
    def setPassword(self, password): self.password = password

    def loginBtn_clicked(self):
        try:
            accounts = self.DBManager.readAllData()["account"]
        except Exception as e:
            self.login_label.setText("Error reading data from database.")
            print(f"Error: {e}")
            return
            
        login_successful= False
        for account in accounts:
            if account["id"]== self.id and account["password"]== self.password:
                self.login_label.setText("Login Successful")
                self.save_login_info()
                self.accept()
                login_successful= True
                break
        if not login_successful:
            self.login_label.setText("Login Failed. Try Again")
            self.login_failCnt()  # METHOD CALL
            

    def login_failCnt(self):
        self.login_cnt += 1
        self.login_failedCnt_label.setText(u"Login Failed: " + str(self.login_cnt) + "/5")

        if self.login_cnt>= 5:
            self.login_label.setText("You failed to log in five times. \nQuit the program.")
            self.login_failedCnt_label.setWindowTitle("Login Failed: 5/5")
            self.login_btn.setEnabled(False)

    def load_login_info(self):
        # LOAD THE SAVED ID FROM TEH INI FILE IF THE 'idSave_chkBox' WAS CHECKED
        if os.path.exists(self.ini_file):
            self.config.read(self.ini_file)
            if "Login_info" in self.config and "id" in self.config["Login_info"]:
                saved_id= self.config["Login_info"]["id"]
                self.id_edit.setText(saved_id) # SET THE SAVED ID TO THE QLINEEDIT
    
    def save_login_info(self):
        # SAVE THE CURRENT ID TO THE INI FILE IF THE 'idSave_chkBox' IS CHECKED
        if self.idSave_chkBox.isChecked():
            self.config["Login_info"]= {"id": self.id}
            with open(self.ini_file, 'w') as configfile: self.config.write(configfile)

    def closeBtn_clicked(self): self.reject()