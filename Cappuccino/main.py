import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QDialog
from PyQt6 import uic


class AddEditCoffeeForm(QDialog):
    def __init__(self, coffee_id=None, parent=None):
        super().__init__(parent)
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.coffee_id = coffee_id
        self.connection = sqlite3.connect("coffee.sqlite")
        self.saveButton.clicked.connect(self.save_data)

        if self.coffee_id:
            self.load_data()

    def load_data(self):
        cursor = self.connection.cursor()
        query = "SELECT * FROM coffee WHERE id = ?"
        result = cursor.execute(query, (self.coffee_id,)).fetchone()
        if result:
            self.nameLineEdit.setText(result[1])
            self.roastDegreeLineEdit.setText(result[2])
            self.groundOrBeansLineEdit.setText(result[3])
            self.tasteDescriptionLineEdit.setText(result[4])
            self.priceSpinBox.setValue(result[5])
            self.packageVolumeSpinBox.setValue(result[6])

    def save_data(self):
        cursor = self.connection.cursor()
        name = self.nameLineEdit.text()
        roast_degree = self.roastDegreeLineEdit.text()
        ground_or_beans = self.groundOrBeansLineEdit.text()
        taste_description = self.tasteDescriptionLineEdit.text()
        price = self.priceSpinBox.value()
        package_volume = self.packageVolumeSpinBox.value()

        if self.coffee_id:
            query = """
                UPDATE coffee
                SET name = ?, roast_degree = ?, ground_or_beans = ?, taste_description = ?, price = ?, package_volume = ?
                WHERE id = ?
            """
            cursor.execute(query, (
                name, roast_degree, ground_or_beans, taste_description, price, package_volume, self.coffee_id))
        else:
            query = """
                INSERT INTO coffee (name, roast_degree, ground_or_beans, taste_description, price, package_volume)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (name, roast_degree, ground_or_beans, taste_description, price, package_volume))

        self.connection.commit()
        self.connection.close()
        self.accept()


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.load_data()
        self.addButton.clicked.connect(self.add_record)
        self.editButton.clicked.connect(self.edit_record)

    def load_data(self):
        cursor = self.connection.cursor()
        query = "SELECT * FROM coffee"
        result = cursor.execute(query).fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Name", "Roast Degree", "Ground/Beans", "Taste", "Price", "Volume"]
        )
        for i, row in enumerate(result):
            for j, value in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(value)))

    def add_record(self):
        dialog = AddEditCoffeeForm(parent=self)
        if dialog.exec():
            self.load_data()

    def edit_record(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1:
            coffee_id = int(self.tableWidget.item(selected_row, 0).text())
            dialog = AddEditCoffeeForm(coffee_id=coffee_id, parent=self)
            if dialog.exec():
                self.load_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
