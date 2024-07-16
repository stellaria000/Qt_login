    def setupUi(self, Dialog):
        self.gridLayoutWidget= QWidget(Dialog)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayout= QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")




        self.retranslateUi(Dialog)

        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))

