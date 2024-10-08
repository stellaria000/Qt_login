from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QLabel, QPushButton, QGridLayout, QWidget, QCheckBox, QLineEdit, QVBoxLayout, QHBoxLayout, QFrame, \
    QGraphicsDropShadowEffect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from databases.db_managements import AccountDBManagement, SystemDBManagement
from gui.core.json_settings import Settings
from gui.core.json_themes import Themes
from gui.widgets import PyDialog, PyLineEdit, PyPushButton, PyComboBox

import configparser
import hashlib
import base64
import os

class LoginWindow(PyDialog):
    def __init__(self):
        self.login_cnt= 0 # INCREASE BY 1 IF FAILED TO LOG IN

        # FILE MANAGER- SETTING INI FILE PATH
        self.ini_file_path= "D:/Project/gui" 
        self.config= configparser.ConfigParser()
        self.ini_file= os.path.join(self.ini_file_path, 'Login_info.ini')

        super().__init__(None, message= "로그인이 필요합니다.")
        self.setupUi()
        self.setFixedSize(self.sizeHint())

        # CONNECTING TO THE DATABASE
        self.accDBManager = AccountDBManagement(self.settings["database_info"]["host"], self.settings["database_info"]["port"],
                                             self.settings["database_info"]["name"],
                                             self.settings["database_info"]["user"], 
                                             self.settings["database_info"]["pw"])
        self.systemDBManager = SystemDBManagement(self.settings["database_info"]["host"], self.settings["database_info"]["port"],
                                                  self.settings["database_info"]["name"],
                                                  self.settings["database_info"]["user"], 
                                                  self.settings["database_info"]["pw"])
        self.load_login_info() # LOAD SAVED ID IF EXISTS
        self.load_systems() # LOAD SAVED SYSTEMS IF EXISTS& SAVES FOR COMBOBOX

    def setupUi(self):
        settings = Settings()
        self.settings = settings.items
        themes = Themes()
        self.themes = themes.items

        self.id = None
        self.password = None

        self.alert_label.hide()
        self.alert_title_frame.hide()
        self.dialog_bar.hide()
        self.btnBox.hide()

        self.loginLayout= QVBoxLayout(self)
        self.system_Box= QHBoxLayout(self)
        self.id_Box= QHBoxLayout(self)
        self.pw_Box= QHBoxLayout(self)
        self.function_Box= QHBoxLayout(self)
        self.btn_box= QHBoxLayout(self)

        self.sys_label = QLabel("System", self)
        self.sys_label.setFixedSize(50, 30)
        self.sys_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sys_label.setStyleSheet("color: white")
        
        self.sys_cbBox= PyComboBox(
            name= "system", default_text= "system", radius= 4,  
            bg_color= self.themes["app_color"]["dark_two"]
        )
        self.sys_cbBox.setMaximumHeight(30)
        self.sys_cbBox.setMaximumWidth(250)
        self.sys_cbBox.setStyleSheet(f"color: {self.themes["app_color"]["text_foreground"]};background-color: {self.themes["app_color"]["dark_two"]};"
                                     f"border-radius: 4px;")

        self.system_Box.addWidget(self.sys_label)
        self.system_Box.addWidget(self.sys_cbBox)
        self.system_Box.setContentsMargins(10, 10, 10, 10)

        self.id_label = QLabel()
        self.id_label.setObjectName("id_label")
        self.id_label.setText("ID")
        self.id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.id_label.setFixedSize(50, 30)
        self.id_label.setStyleSheet('color: white')

        self.id_edit = PyLineEdit(
            text="", place_holder_text="",
            radius=4, border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_two"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["P_blue_1"],
            name="idEdit"
        )
        self.id_edit.setMinimumHeight(30)
        self.id_edit.setMaximumWidth(250)
        self.id_Box.addWidget(self.id_label)
        self.id_Box.addWidget(self.id_edit)
        # self.id_Box.setSpacing(5)
        self.id_Box.setContentsMargins(10, 10, 10, 10)

        self.pw_label = QLabel()
        self.pw_label.setObjectName("pw_label")
        self.pw_label.setText("Password")
        self.pw_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pw_label.setStyleSheet('color: white')
        self.pw_label.setFixedSize(50, 30)
        self.pw_label.setMaximumHeight(30)

        self.pw_edit = PyLineEdit(
            text="", place_holder_text="",
            radius=4, border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_two"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["P_blue_1"],
            name="pwEdit"
        )
        self.pw_edit.setMinimumHeight(30)
        self.pw_edit.setEchoMode(QLineEdit.Password)
        self.pw_edit.setMaximumWidth(250)
        self.pw_Box.addWidget(self.pw_label)
        self.pw_Box.addWidget(self.pw_edit)
        self.pw_Box.setContentsMargins(10, 10, 10, 10)

        self.idSave_chkBox = QCheckBox("Save Id")
        self.idSave_chkBox.setStyleSheet("color: white; font: 8pt")
        if os.path.exists(self.ini_file):
            self.config.read(self.ini_file)
            if "Login_info" in self.config and "id" in self.config["Login_info"]:
                saved_id= self.config["Login_info"]["id"]
                if saved_id.strip():
                    self.id_edit.setText(saved_id)
                    self.idSave_chkBox.setChecked(True)

        #     else: self.idSave_chkBox.setChecked(False)
        # else: self.idSave_chkBox.setChecked(False)

        self.login_label = QLabel("Please Enter Id and Password", self)
        self.login_label.setStyleSheet("color: white; font: 10pt")
        self.login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
  
        self.login_failedCnt_label = QLabel(u"Login Failed: " + str(self.login_cnt) + "/5")
        self.login_failedCnt_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.login_failedCnt_label.setStyleSheet("color: white; font: 8pt")

        self.function_Box.addWidget(self.idSave_chkBox)
        self.function_Box.addWidget(self.login_failedCnt_label)
        self.function_Box.setContentsMargins(10, 10, 10, 10)

        self.login_btn = PyPushButton(
            text="로그인", radius=4,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.login_btn.setMaximumHeight(40)

        self.close_btn = PyPushButton(
            text="닫기", radius=4,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.close_btn.setMaximumHeight(40)
        self.btn_box.addWidget(self.login_btn)
        self.btn_box.addWidget(self.close_btn)
        self.btn_box.setContentsMargins(10, 10, 10, 10)

        self.loginLayout.addLayout(self.system_Box)
        self.loginLayout.addLayout(self.id_Box)
        self.loginLayout.addLayout(self.pw_Box)
        self.loginLayout.addLayout(self.function_Box)
        self.loginLayout.addWidget(self.login_label)
        self.loginLayout.addLayout(self.btn_box)
        self.loginLayout.setSpacing(5)

        self.alert_main_L.addLayout(self.loginLayout)

        self.alert_main_F.setObjectName("alert_main_F")
        self.alert_main_F.setStyleSheet(
            "QFrame#alert_main_F { border: 1px solid #343b48; border-radius: 2px; background-color: " +
            self.themes["app_color"]["dark_one"] + "; }"
        )

        self.ok_button.hide()
        self.cancel_button.hide()
        self.alert_main_L.addWidget(self.btnBox)
        self.id_edit.textChanged.connect(self.setId)
        # self.id_edit.textChanged.connect(self.updateInFile)
        self.pw_edit.textChanged.connect(self.setPassword)
        self.idSave_chkBox.checkStateChanged.connect(self.chkBox_stateChange)
        self.login_btn.clicked.connect(self.loginBtn_clicked)
        self.close_btn.clicked.connect(self.closeBtn_clicked)

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.id_label.setText(QCoreApplication.translate("Dialog", u"아이디 ", None))
        self.pw_label.setText(QCoreApplication.translate("Dialog", u"비밀번호 ", None))
        self.login_btn.setText(QCoreApplication.translate("Dialog", u"로그인", None))
        self.close_btn.setText(QCoreApplication.translate("Dialog", u"닫기", None))

    # METHODSSSSSSS

    def setId(self, id): 
        self.id = self.id_edit.text().strip()
        if self.idSave_chkBox.isChecked(): self.updateIniFile()


    def setPassword(self, password): self.password = password


    def load_systems(self): # LOAD THE SAVED SYSTEM INFORMATION FROM DATABASE
        try: # ADD SYSTEM ITEM INTO COMBOBOX
            systems= self.systemDBManager.readAllData()
            system_list= systems.get("system", [])
            for system in system_list:
                sys_id= system.get("sys_id", "")
                sys_name= system.get("sys_name", "")
                self.sys_cbBox.addItem(f"{sys_id}_{sys_name}")
        except Exception as e: print(f"Error loading systems: {e}")


    def load_login_info(self):
        # LOAD THE SAVED ID FROM THE INI FILE IF THE 'idSave_chkBox' WAS CHECKED
        if os.path.exists(self.ini_file):
            self.config.read(self.ini_file)
            if "Login_info" in self.config and "id" in self.config["Login_info"]:
                saved_id= self.config["Login_info"]["id"]
                self.id_edit.setText(saved_id) # SET THE SAVED ID TO THE QLINEEDIT
                self.idSave_chkBox.setChecked(True)
                self.id= saved_id


    def chkBox_stateChange(self, state):
        '''READS INI FILE TO CHECK IF THERE'S WRITTEN ID, 
        IF IT HAS AN ID, CHECKBOX AUTOMATICALLY CHECKED WHEN LOGIN WINDOW LOADS 
        AND ID SETTED BY THE ID FROM INI FILE'''
        current_id= self.id_edit.text().strip()

        if state== Qt.Checked: 
            if current_id:
                self.config["Login_info"]= {"id": current_id}
                with open(self.ini_file, 'w') as configfile: self.config.write(configfile)
        else: # UNCHECKED- DELETES ID FROM INI FILE(PASS IF INI IS EMPTY)
            if os.path.exists(self.ini_file): 
                self.config.read(self.ini_file)
                if "Login_info" in self.config:
                    self.config.remove_section("Login_info")
                    with open(self.ini_file, 'w') as configfile: self.config.write(configfile)


    def updateIniFile(self):
        if self.idSave_chkBox.isChecked():
            current_id = self.id_edit.text().strip()
            self.config["Login_info"] = {"id": current_id}
            with open(self.ini_file, 'w') as configfile:
                self.config.write(configfile)


    def loginBtn_clicked(self): 
        selected_system= self.sys_cbBox.currentText()
        sys_id= selected_system.split("_")[0]  

        if not sys_id: # NO SYSTEM SELECTED
            self.login_label.setText("System id could not be determined")
            return
        
        if not self.id or not self.password:  # NO ID OR PW INPUT
            self.login_label.setText("Enter Id and Password Correctly")
            return
        
        try: # READS DATA FROM ACCOUNTS TABLE
            accounts= self.accDBManager.readAllData()["account"]
        except Exception as e: 
            self.login_label.setText("Error reading data from database.")
            print(f"Error: {e}")
            return
        
        account_found= None
        for account in accounts:    # CHECKS IF ACCOUNTS EXISTS IN DATABASE
            package_list_split= [pkg.strip() for pkg in account["account_package_list"].split(',')]
            if account["id"]== self.id and sys_id in package_list_split:
                account_found= account
                break

        if account_found: self.validate_login(account_found)
        else: self.login_label.setText("Account not found\nor System mismatch")


    def validate_login(self, account): # CHECKS LOGIN INFO WITH DB 
        login_successful= False
        # self.login_cnt= accountsDB.get("login_attempt_count", 0)

        if account["use_or_not"]== 'n': # CHECKS ACCOUNTS IF LOCKED
            self.login_label.setText("This account is locked.\nCan't log in")
            return
        
        encrypted_password= self.accDBManager.encrypt_password(self.password, account["id"])

        if account["password"]== encrypted_password: # LOGIN SUCCESSFUL
            self.login_label.setText("Login Successful")
            self.accDBManager.updateLoginAttempts(self.id, 0)
            login_successful= True
            self.accept()
        else:
            self.login_label.setText("Incorrect Password")
            self.login_failCnt(account)
            return
        
        if not login_successful:
                self.login_label.setText("Account not found\nor Incorrect password")
                self.login_failCnt(account)
        

    def login_failCnt(self, account):   
        try:
            self.login_cnt= account.get("login_attempt_count", 0)
            self.login_cnt+= 1 
            self.accDBManager.updateLoginAttempts(self.id, self.login_cnt)
            self.login_failedCnt_label.setText(u"Login Failed: " + str(self.login_cnt) + "/5")

            if self.login_cnt>= 5:  # DISABLE LOGIN AFTER FAILED TO LOG IN FIVE TIMES
                self.login_label.setText("Account is locked due to \ntoo many failed login attempts")
                self.accDBManager.updateUseorNot(self.id, 'n')  
                # self.login_cnt= 0
            
        except Exception as e:
            self.login_label.setText("Error updating\nlogin attempts in database.")
            print(f"Error:{e}")
                
    
    def closeBtn_clicked(self): self.reject()
        