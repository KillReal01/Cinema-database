import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QDateEdit, QPushButton, QLineEdit, QLabel
from PyQt5 import uic
import database

s = dict()


# Подкласс QMainWindow для настройки основного окна приложения
class UIStart(QMainWindow):
    def __init__(self):
        super(UIStart, self).__init__()

        # Загрузка ui файла
        uic.loadUi("start.ui", self)
        self.show()

        self.login = self.findChild(QLineEdit, "lineEdit_login")
        self.password = self.findChild(QLineEdit, "lineEdit_password")
        self.password.setEchoMode(QLineEdit.Password)

        self.button = self.findChild(QPushButton, "pushButton")
        self.button.clicked.connect(self.onClicked)

    def onClicked(self):
        UIForm = database.UIForm(self.login.text(), self.password.text())
        if UIForm.connection != -1:
            UIForm.show()
            s[0] = UIForm
            self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = UIStart()
    app.exec()
