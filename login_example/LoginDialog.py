from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QGridLayout, QWidget, QVBoxLayout


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

        self.id= None
        self.passowrd= None

    def setupUI(self):
        self.setGeometry(1100, 200, 500, 300)
        self.setWindowTitle("LogIn")
        self.setWindowIcon(QIcon('login_icon.png'))

        label_1= QLabel("ID: ")
        label_1.setObjectName("id_txtLb")
        label_2= QLabel("Password: ")
        label_2.setObjectName("pw_txtLb")

        self.lineEdit_1= QLineEdit()
        self.lineEdit_2= QLineEdit()
        self.pushButton_1= QPushButton("Log in")
        self.pushButton_1.clicked.connect(self.pushButtonClicked)

        layout= QGridLayout()
        layout.addWidget(label_1, 0, 0)
        layout.addWidget(self.lineEdit_1, 0, 1)
        layout.addWidget(self.pushButton_1, 0, 2)
        layout.addWidget(label_2, 1, 0)
        layout.addWidget(self.lineEdit_2, 1, 1)

        self.setLayout(layout)

    '''
    In dialog window- after user put Id/Password, and clicks the log in button-
    pushButtonClicked method gets called:
    read the text from self.lineEdit_1& lineEdit_2 and save it in the instance variable(self.id, password)
    the value input from the widget is saved in the instance varioables, so that the main window can read
    '''
    def pushButtonClicked(self):
        self.id= self.lineEdit_1.text()
        self.password= self.lineEdit_2.text()
        self.close()
        # close 메소드를 호출해 다이얼로그 창을 닫는다
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setGeometry(800, 200, 300, 300)
        self.setWindowTitle("Login Example")
        self.setWindowIcon(QIcon('login_icon.png'))

        self.pushButton= QPushButton("Log In")
        self.pushButton.clicked.connect(self.pushButtonClicked)
        self.label= QLabel()

        layout= QVBoxLayout()
        layout.addWidget(self.pushButton)
        layout.addWidget(self.label)

        self.setLayout(layout)

    '''
        앞에서 정의한 LoginDialog 클래스의 인스턴스 생성, 인스턴스의 메소드인 exec_를 호출한다.
        # exec_ 메소듸 다이얼로그 창을 Modal 형태로 출력한다(Modal 다이얼로그는 해당 다이얼로그 창을 닫을 때까지 부모 윈도우로 이동할 수 없다)
        사용자가 로그인 다이얼로그 창을 닫으면 dlf.exec_() 이후의 구문이 실행됩니다. 앞서 다이얼로그 창에서 인스턴스 변수인 dlg.id와 dlg.password에 
        위젯을 통해 입력받은 값을 저장해뒀으므로 해당 변수를 통해 아이디와 비밀번호를 메인 윈도우로 얻어올 수 있다. 메인 윈도우로 얻어온 아이디와 비밀번호를
        메인 윈도우의 self.label 객체를 통해 화면에 출력한다.
    '''
    def pushButtonClicked(self):
        dlg= LoginDialog()
        dlg.exec_()
        id= dlg.id
        password= dlg.password
        self.label.setText("id: %s password: %s" % (id, password))

