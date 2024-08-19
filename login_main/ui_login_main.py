if __name__ == "__main__":
    # APPLICATION
    # ///////////////////////////////////////////////////////////////
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("PREVAX2.ico"))
 
    window= MainWindow()
    window.setEnabled(False)
    window.show()
    login_window= LoginWindow()
    # login_window.exec()

    if login_window.exec() == QDialog.Rejected:
        window.setEnabled(True)
    else:
        sys.exit(0)

    sys.exit(app.exec())