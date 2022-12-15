import psycopg2
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QPushButton, \
    QLineEdit, QComboBox, QLabel, QTableWidget, QTableWidgetItem, QDateTimeEdit
from PyQt5 import uic
from PyQt5.QtCore import *
from psycopg2 import OperationalError
import helper

db = dict()


# Подкласс QMainWindow для настройки основного окна приложения
class UIForm(QMainWindow):
    def __init__(self, login, password):
        super(UIForm, self).__init__()

        # Загрузка ui файла
        uic.loadUi("main.ui", self)

        # подключаемся к базе данных
        self.connection = create_connection(self, "postgres", login, password, "127.0.0.1", "5432")

        # Инициализация объектов Категории сведений
        self.info = self.findChild(QComboBox, "comboBox")
        self.info.addItems(["Репертуар кинотеатра",
                            "Адрес и район кинотеатра",
                            "Число свободных мест на сеанс",
                            "Цена билетов на сеанс",
                            "Жанр, производство и режиссер фильма",
                            "Вместимость кинотеатра",
                            "Справка о сеансах фильма",
                            "Отчёт о прокате фильма"])
        self.info.setEditable(False)
        self.info.activated.connect(self.onActivated)

        # Инициализация метки
        self.label = self.findChild(QLabel, "label")
        self.label2 = self.findChild(QLabel, "label_2")
        self.label2.hide()

        self.access = self.findChild(QLabel, "label_access")
        self.access.setText("Уровень доступа: " + login)

        # Ввод данных
        self.input = self.findChild(QLineEdit, "lineEdit")

        self.date = self.findChild(QDateTimeEdit, 'dateTimeEdit')
        self.date.setDateTime(QDateTime.currentDateTime())
        self.date.hide()

        self.film = self.findChild(QLineEdit, "lineEdit_film")
        self.film.hide()

        self.query = ''

        # Кнопка поиск
        self.button = self.findChild(QPushButton, 'pushButton')
        self.button.clicked.connect(self.onClicked)

        # Кнопка удаление
        self.button_del = self.findChild(QPushButton, 'pushButton_delete')
        self.button_del.clicked.connect(self.onClicked_del)

        # Кнопка вставка
        self.button_ins = self.findChild(QPushButton, 'pushButton_insert')
        self.button_ins.clicked.connect(self.onClicked_ins)

        # Кнопка обновления
        self.button_up = self.findChild(QPushButton, 'pushButton_update')
        self.button_up.clicked.connect(self.onClicked_up)

        if login == 'employee':
            self.button_del.hide()
            self.button_ins.hide()
            self.button_up.hide()

        # Вывод данных
        self.output = self.findChild(QTableWidget, 'tableWidget')

    def onClicked_del(self):
        db[0] = helper.UIHelper('delete', self.connection)
        db[0].show()

    def onClicked_ins(self):
        db[0] = helper.UIHelper('insert', self.connection)
        db[0].show()

    def onClicked_up(self):
        db[0] = helper.UIHelper('update', self.connection)
        db[0].show()

    def onActivated(self, ind):
        s = 'Введите название'
        if ind in [0, 1, 5, 6]:
            self.label.setText(s + ' кинотеатра')
            self.date.hide()
            self.film.hide()
            self.label2.hide()
        elif ind == 4:
            self.date.hide()
            self.film.hide()
            self.label2.hide()
            self.label.setText(s + ' фильма')
        else:
            self.label.setText(s + ' кинотеатра')
            self.date.show()
            self.film.show()
            self.label2.show()
        if ind == 7:
            self.label.setText(s + ' города')
            self.date.hide()
            self.film.hide()
            self.label2.hide()

    def onClicked(self):
        cinema = self.input.text()
        film = self.film.text()
        year = self.date.date().year()
        month = self.date.date().month()
        day = self.date.date().day()

        hour = self.date.time().hour()
        minute = self.date.time().minute()

        if self.info.currentIndex() == 0:
            self.query = f"select cinema_category from cinemas where cinema_name = '{cinema}'"
        elif self.info.currentIndex() == 1:
            self.query = f"select cinema_district, cinema_location from cinemas where cinema_name = '{cinema}'"
        elif self.info.currentIndex() == 2:
            self.query = f"select session_free_seats from sessions\
            where(cinema_name='{cinema}' and session_time = '{hour}:{minute}'\
            and session_date = '{year}.{month}.{day}' and film_name = '{film}')"
        elif self.info.currentIndex() == 3:
            self.query = f"select session_cost from sessions\
            where(cinema_name='{cinema}' and session_time = '{hour}:{minute}' \
            and session_date = '{year}.{month}.{day}' and film_name = '{film}')"
        elif self.info.currentIndex() == 4:
            self.query = f"select film_genre, film_producer from films where film_name = '{cinema}'"
        elif self.info.currentIndex() == 5:
            self.query = f"select cinema_capacity from cinemas where cinema_name = '{cinema}'"
        elif self.info.currentIndex() == 6:
            self.query = f"select film_name, session_time, session_date, session_cost from sessions where cinema_name = '{cinema}'"
        elif self.info.currentIndex() == 7:
            self.query = f"select film_name, s.cinema_name, session_cost from sessions\
             as s inner join cinemas as c on c.cinema_name = s.cinema_name where cinema_district = '{cinema}'"

        self.executeTable()

    def executeTable(self):
        users = execute_read_query(self.connection, self.query)
        words = self.query.split()
        names = list()
        for i in range(1, len(words)):
            if words[i] == 'from':
                break
            else:
                if ',' in words[i]:
                    words[i] = words[i][0:-1]
                names.append(words[i])

        self.output.setRowCount(len(users))
        self.output.setColumnCount(len(names))
        self.output.setHorizontalHeaderLabels(names)

        for i in range(len(users)):
            for j in range(len(names)):
                self.output.setItem(i, j, QTableWidgetItem(str(users[i][j])))


# подключение к базе данных
def create_connection(self, db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Подключение к базе данных PostgreSQL прошло успешно")
    except OperationalError as e:
        print(f"Произошла ошибка '{e}'")
        QMessageBox.information(self, 'Ошибка', "Неверный пользователь")
        return -1
    return connection


# создавать таблицы, а также добавлять, изменять и удалять записи.
def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Запрос выполнен успешно")
    except OperationalError as e:
        print(f"Произошла ошибка '{e}'")


# выборка
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"Произошла ошибка '{e}'")
