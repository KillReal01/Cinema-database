from PyQt5.QtWidgets import QDialogButtonBox, QLineEdit, QLabel, QDialog
from PyQt5 import uic
import database


# Подкласс QMainWindow для настройки основного окна приложения
class UIHelper(QDialog):
    def __init__(self, type_=None, connection_=None):
        super(UIHelper, self).__init__()

        # Загрузка ui файла
        uic.loadUi("helper.ui", self)
        self.connection = connection_
        self.type = type_
        self.query = ''

        self.line1 = self.findChild(QLineEdit, "lineEdit_1")
        self.line2 = self.findChild(QLineEdit, "lineEdit_2")
        self.line3 = self.findChild(QLineEdit, "lineEdit_3")
        self.line4 = self.findChild(QLineEdit, "lineEdit_4")

        self.label1 = self.findChild(QLabel, "label_1")
        self.label2 = self.findChild(QLabel, "label_2")
        self.label3 = self.findChild(QLabel, "label_3")
        self.label4 = self.findChild(QLabel, "label_4")

        self.buttonBox = self.findChild(QDialogButtonBox, 'buttonBox')
        self.buttonBox.accepted.connect(self.onClicked)

        if self.type == 'insert':
            self.label1.setText('Название кинотеатра')
            self.label2.setText('Район')

            self.line2.show()
            self.line3.show()
            self.line4.show()

            self.label2.show()
            self.label3.show()
            self.label4.show()

        if self.type == 'update':
            self.label1.setText('Название кинотеатра')
            self.label2.setText('Новая категория')

            self.line2.show()
            self.label2.show()

            self.line3.hide()
            self.line4.hide()
            self.label3.hide()
            self.label4.hide()

        if self.type == 'delete':
            self.label1.setText('Название фильма')

            self.line2.hide()
            self.line3.hide()
            self.line4.hide()

            self.label2.hide()
            self.label3.hide()
            self.label4.hide()


    def onClicked(self):
        if self.type == 'insert':
            self.query = f"insert into cinemas(values('{self.line1.text()}', '{self.line2.text()}', '{self.line3.text()}', '{self.line4.text()}', f_capacity('{self.line4.text()}')));"

        if self.type == 'update':
            self.query = f"update cinemas set cinema_category = '{self.line2.text()}', cinema_capacity = f_capacity('{self.line2.text()}') where cinema_name = '{self.line1.text()}'"

        if self.type == 'delete':
            self.query = f"delete from films where film_name = '{self.line1.text()}'"

        database.execute_query(self.connection, self.query)
        self.close()
