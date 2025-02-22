from PyQt6 import QtCore, QtGui, QtWidgets
import sqlite3
import os


class AddEditCoffeeForm(QtWidgets.QWidget):
    def __init__(self, coffee_id=None):
        super().__init__()
        self.coffee_id = coffee_id
        self.setupUi()
        if self.coffee_id:
            self.load_coffee_data()

    def setupUi(self):
        self.setWindowTitle("Добавить/Редактировать кофе")
        self.resize(400, 320)

        self.label_name = QtWidgets.QLabel("Название сорта:", self)
        self.label_name.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.lineEdit_name = QtWidgets.QLineEdit(self)
        self.lineEdit_name.setGeometry(QtCore.QRect(120, 10, 250, 30))

        self.label_roast = QtWidgets.QLabel("Степень обжарки:", self)
        self.label_roast.setGeometry(QtCore.QRect(10, 50, 100, 30))
        self.lineEdit_roast = QtWidgets.QLineEdit(self)
        self.lineEdit_roast.setGeometry(QtCore.QRect(120, 50, 250, 30))

        self.label_type = QtWidgets.QLabel("Молотый/в зернах:", self)
        self.label_type.setGeometry(QtCore.QRect(10, 90, 100, 30))
        self.lineEdit_type = QtWidgets.QLineEdit(self)
        self.lineEdit_type.setGeometry(QtCore.QRect(120, 90, 250, 30))

        self.label_description = QtWidgets.QLabel("Описание вкуса:", self)
        self.label_description.setGeometry(QtCore.QRect(10, 130, 100, 30))
        self.textEdit_description = QtWidgets.QTextEdit(self)
        self.textEdit_description.setGeometry(QtCore.QRect(120, 130, 250, 60))

        self.label_price = QtWidgets.QLabel("Цена:", self)
        self.label_price.setGeometry(QtCore.QRect(10, 200, 100, 30))
        self.lineEdit_price = QtWidgets.QLineEdit(self)
        self.lineEdit_price.setGeometry(QtCore.QRect(120, 200, 250, 30))

        self.label_volume = QtWidgets.QLabel("Объем упаковки:", self)
        self.label_volume.setGeometry(QtCore.QRect(10, 240, 100, 30))
        self.lineEdit_volume = QtWidgets.QLineEdit(self)
        self.lineEdit_volume.setGeometry(QtCore.QRect(120, 240, 250, 30))

        self.pushButton_save = QtWidgets.QPushButton("Сохранить", self)
        self.pushButton_save.setGeometry(QtCore.QRect(150, 280, 100, 30))
        self.pushButton_save.clicked.connect(self.save_data)

    def load_coffee_data(self):
        db_path = os.path.join('data', 'coffee.sqlite')
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("SELECT * FROM coffee WHERE id=?", (self.coffee_id,))
        row = cur.fetchone()
        con.close()
        if row:
            self.lineEdit_name.setText(row[1])
            self.lineEdit_roast.setText(row[2])
            self.lineEdit_type.setText(row[3])
            self.textEdit_description.setText(row[4])
            self.lineEdit_price.setText(str(row[5]))
            self.lineEdit_volume.setText(str(row[6]))

    def save_data(self):
        name = self.lineEdit_name.text()
        roast = self.lineEdit_roast.text()
        coffee_type = self.lineEdit_type.text()
        description = self.textEdit_description.toPlainText()
        price = self.lineEdit_price.text()
        volume = self.lineEdit_volume.text()
        db_path = os.path.join('data', 'coffee.sqlite')
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        if self.coffee_id:
            cur.execute(
                "UPDATE coffee SET name=?, roast=?, type=?, description=?, price=?, volume=? WHERE id=?",
                (name, roast, coffee_type, description, price, volume, self.coffee_id)
            )
        else:
            cur.execute(
                "INSERT INTO coffee (name, roast, type, description, price, volume) VALUES (?, ?, ?, ?, ?, ?)",
                (name, roast, coffee_type, description, price, volume)
            )
        con.commit()
        con.close()
        self.close()
