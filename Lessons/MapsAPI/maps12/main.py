import sys
import re, math
from PyQt6 import uic
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

API_KEY_STATIC = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'

def haversine(lon1, lat1, lon2, lat2):
    R = 6371000
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

class MainWindow(QMainWindow):
    g_map: QLabel
    press_delta = 0.1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('main_window.ui', self)
        self.map_zoom = 10
        self.map_ll = [37.977751, 55.757718]
        self.marker = None
        self.original_full_address = ""
        self.postal_code = ""
        self.theme_checkbox.stateChanged.connect(self.refresh_map)
        self.search_button.clicked.connect(self.search_object)
        self.search_line.returnPressed.connect(self.search_object)
        self.reset_button.clicked.connect(self.reset_search)
        self.postal_checkbox.stateChanged.connect(self.update_address_field)
        self.g_map.installEventFilter(self)
        self.refresh_map()

    def eventFilter(self, source, event):
        if source == self.g_map and event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.RightButton:
                self.search_org_at_click(event)
            return True
        return super().eventFilter(source, event)

    def search_org_at_click(self, event):
        x = event.position().x()
        y = event.position().y()
        w = self.g_map.width()
        h = self.g_map.height()
        dx = x - w/2
        dy = y - h/2
        dlon = 360 / (256 * (2 ** self.map_zoom))
        new_lon = self.map_ll[0] + dx * dlon
        center_merc = math.log(math.tan(math.pi/4 + math.radians(self.map_ll[1])/2))
        dmy = (2 * math.pi) / (256 * (2 ** self.map_zoom))
        new_merc = center_merc - dy * dmy
        new_lat = math.degrees(2 * math.atan(math.exp(new_merc)) - math.pi/2)
        self.reset_search()
        self.search_org(new_lon, new_lat)

    def search_org(self, lon, lat):
        geocoder_apikey = "6bf2895d-8652-402b-a66b-98ce0ace342c"
        url = "https://search-maps.yandex.ru/v1/"
        params = {
            "apikey": geocoder_apikey,
            "text": "организация",
            "ll": f"{lon},{lat}",
            "spn": "0.001,0.001",
            "lang": "ru_RU"
        }
        session = requests.Session()
        retry = Retry(total=10, connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        response = session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "features" not in data or len(data["features"]) == 0:
            return
        feature = data["features"][0]
        org_coords = feature["geometry"]["coordinates"]
        distance = haversine(lon, lat, org_coords[0], org_coords[1])
        if distance > 50:
            return
        self.marker = [org_coords[0], org_coords[1]]
        org_meta = feature["properties"].get("CompanyMetaData", {})
        name = org_meta.get("name", "")
        address = org_meta.get("address", "")
        self.original_full_address = f"{name}, {address}" if name and address else feature["properties"].get("text", "")
        try:
            self.postal_code = org_meta.get("postal_code", "")
        except Exception:
            self.postal_code = ""
        self.update_address_field()
        self.refresh_map()

    def search_object(self):
        query = self.search_line.text().strip()
        if not query:
            return
        geocoder_apikey = "6bf2895d-8652-402b-a66b-98ce0ace342c"
        url = "https://geocode-maps.yandex.ru/1.x"
        params = {"apikey": geocoder_apikey, "geocode": query, "format": "json"}
        session = requests.Session()
        retry = Retry(total=10, connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        response = session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        geo_object = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        pos_str = geo_object["Point"]["pos"]
        lon, lat = map(float, pos_str.split())
        self.map_ll = [lon, lat]
        self.marker = [lon, lat]
        self.original_full_address = geo_object["metaDataProperty"]["GeocoderMetaData"]["text"]
        try:
            self.postal_code = geo_object["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
        except KeyError:
            try:
                self.postal_code = geo_object["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]\
                    ["Country"]["AdministrativeArea"]["SubAdministrativeArea"]["Locality"]\
                    ["Thoroughfare"]["Premise"]["PostalCode"]["PostalCodeNumber"]
            except Exception:
                self.postal_code = ""
        self.update_address_field()
        self.refresh_map()

    def update_address_field(self):
        addr = self.original_full_address
        if self.postal_checkbox.isChecked():
            if self.postal_code and self.postal_code not in addr:
                addr = addr + ", " + self.postal_code
        else:
            addr = re.sub(r'\b\d{6}\b,?\s*', '', addr)
        self.address_field.setText(addr)

    def reset_search(self):
        self.marker = None
        self.original_full_address = ""
        self.postal_code = ""
        self.address_field.setText("")
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
