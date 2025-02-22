import sys
from io import BytesIO
import requests
from PIL import Image
from scale import get_spn

def main():
    if len(sys.argv) < 2:
        sys.exit(1)
    toponym_to_find = " ".join(sys.argv[1:])
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": toponym_to_find,
        "format": "json"
    }
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        sys.exit(1)
    json_response = response.json()
    try:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    except (IndexError, KeyError):
        sys.exit(1)
    toponym_coordinates = toponym["Point"]["pos"]
    longitude, latitude = toponym_coordinates.split()
    spn = get_spn(toponym)
    map_api_server = "https://static-maps.yandex.ru/1.x/"
    map_params = {
        "ll": f"{longitude},{latitude}",
        "spn": spn,
        "l": "map",
        "pt": f"{longitude},{latitude},pm2rdm"
    }
    response = requests.get(map_api_server, params=map_params)
    if not response:
        sys.exit(1)
    image = Image.open(BytesIO(response.content))
    image.show()

if __name__ == "__main__":
    main()
