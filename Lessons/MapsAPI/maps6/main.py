import sys
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

API_KEY_STATIC = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'

class MainWindow(QMainWindow):
    g_map: QLabel
    press_delta = 0.1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('main_window.ui', self)
        self.map_zoom = 10
        self.map_ll = [37.977751, 55.757718]
        self.marker = None
        self.theme_checkbox.stateChanged.connect(self.refresh_map)
        self.search_button.clicked.connect(self.search_object)
        self.search_line.returnPressed.connect(self.search_object)
        self.refresh_map()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_PageUp and self.map_zoom < 21:
            self.map_zoom += 1
        elif key == Qt.Key.Key_PageDown and self.map_zoom > 0:
            self.map_zoom -= 1
        elif key == Qt.Key.Key_Right:
            self.map_ll[0] += self.press_delta
            if self.map_ll[0] > 180:
                self.map_ll[0] -= 360
        elif key == Qt.Key.Key_Left:
            self.map_ll[0] -= self.press_delta
            if self.map_ll[0] < -180:
                self.map_ll[0] += 360
        elif key == Qt.Key.Key_Up and self.map_ll[1] + self.press_delta < 90:
            self.map_ll[1] += self.press_delta
        elif key == Qt.Key.Key_Down and self.map_ll[1] - self.press_delta > -90:
            self.map_ll[1] -= self.press_delta
        else:
            return
        self.refresh_map()

    def search_object(self):
        query = self.search_line.text().strip()
        if not query:
            return
        geocoder_apikey = "6bf2895d-8652-402b-a66b-98ce0ace342c"
        url = "https://geocode-maps.yandex.ru/1.x"
        params = {
            "apikey": geocoder_apikey,
            "geocode": query,
            "format": "json"
        }
        session = requests.Session()
        retry = Retry(total=10, connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        response = session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        pos_str = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
        lon, lat = map(float, pos_str.split())
        self.map_ll = [lon, lat]
        self.marker = [lon, lat]
        self.refresh_map()

    def refresh_map(self):
        theme = "dark" if self.theme_checkbox.isChecked() else "light"
        map_params = {
            "apikey": API_KEY_STATIC,
            "ll": ','.join(map(str, self.map_ll)),
            "z": self.map_zoom,
            "theme": theme,
        }
        if self.marker:
            map_params["pt"] = f"{self.marker[0]},{self.marker[1]},pm2rdm"
        session = requests.Session()
        retry = Retry(total=10, connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        response = session.get("https://static-maps.yandex.ru/v1", params=map_params)
        img = QImage.fromData(response.content)
        pixmap = QPixmap.fromImage(img)
        self.g_map.setPixmap(pixmap)

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
