import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.QtGui import QPainter, QColor
from PyQt6 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI.ui', self)
        self.button = self.findChild(QPushButton, "pushButton")
        self.button.clicked.connect(self.add_circle)
        self.circles = []

    def add_circle(self):
        x = random.randint(10, self.width() - 50)
        y = random.randint(10, self.height() - 50)
        radius = random.randint(10, 100)
        self.circles.append((x, y, radius))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor("yellow"))
        for x, y, radius in self.circles:
            painter.drawEllipse(x, y, radius, radius)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
