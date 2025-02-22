import random
import requests
from io import BytesIO
from PIL import Image

API_KEY = "8013b162-6b42-4997-9691-77b7074026e0"

CITIES = [
    "Москва",
    "Санкт-Петербург",
    "Новосибирск",
    "Екатеринбург",
    "Казань",
    "Нижний Новгород",
    "Челябинск",
    "Самара",
    "Омск",
    "Ростов-на-Дону"
]


def get_city_params(city):
    geocoder_api = "http://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": API_KEY,
        "geocode": city,
        "format": "json",
        "kind": "locality"
    }
    response = requests.get(geocoder_api, params=params)
    response.raise_for_status()
    json_response = response.json()
    try:
        geo_object = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    except (IndexError, KeyError):
        raise Exception("Город не найден")
    center = geo_object["Point"]["pos"].replace(" ", ",")
    try:
        envelope = geo_object["boundedBy"]["Envelope"]
        lower = list(map(float, envelope["lowerCorner"].split()))
        upper = list(map(float, envelope["upperCorner"].split()))
        spn_lon = abs(upper[0] - lower[0])
        spn_lat = abs(upper[1] - lower[1])
        if spn_lon < 0.005:
            spn_lon = 0.005
        if spn_lat < 0.005:
            spn_lat = 0.005
        spn = f"{spn_lon},{spn_lat}"
    except Exception:
        spn = "0.005,0.005"
    return center, spn


def get_city_map(city):
    center, spn = get_city_params(city)
    static_api = "https://static-maps.yandex.ru/1.x/"
    params = {
        "ll": center,
        "spn": spn,
        "l": "map"
    }
    response = requests.get(static_api, params=params)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))


def main():
    cities = CITIES.copy()
    random.shuffle(cities)
    for city in cities:
        print("Показывается карта для города (загадать нельзя!):", city)
        img = get_city_map(city)
        img.show()
        input("Нажмите Enter для перехода к следующему городу...")


if __name__ == "__main__":
    main()
