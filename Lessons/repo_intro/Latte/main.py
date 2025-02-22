import sys
import os
import sqlite3
from PyQt6 import QtWidgets
from UI import mainUI, addEditCoffeeForm

class MainWindow(QtWidgets.QMainWindow, mainUI.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_data()
        self.pushButton_add.clicked.connect(self.open_add_edit_form)
        self.pushButton_edit.clicked.connect(self.open_edit_form)

    def load_data(self):
        db_path = os.path.join('data', 'coffee.sqlite')
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("SELECT * FROM coffee")
        rows = cur.fetchall()
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(7)
        for row_index, row_data in enumerate(rows):
            for col_index, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.tableWidget.setItem(row_index, col_index, item)
        con.close()

    def open_add_edit_form(self):
        self.add_edit_form = addEditCoffeeForm.AddEditCoffeeForm()
        self.add_edit_form.show()

    def open_edit_form(self):
        selected_items = self.tableWidget.selectedItems()
        if selected_items:
            coffee_id = selected_items[0].text()
            self.add_edit_form = addEditCoffeeForm.AddEditCoffeeForm(coffee_id=coffee_id)
            self.add_edit_form.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
