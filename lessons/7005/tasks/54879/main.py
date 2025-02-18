import sys
from io import BytesIO
import requests
from PIL import Image
from get_spn import get_spn

search_query = " ".join(sys.argv[1:])

geo_url = "http://geocode-maps.yandex.ru/1.x/"
geo_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": search_query,
    "format": "json"
}

geo_response = requests.get(geo_url, params=geo_params)
geo_data = geo_response.json()
geo_object = geo_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]

coord_str = geo_object["Point"]["pos"]
longitude, latitude = coord_str.split(" ")
span_lon, span_lat = get_spn(geo_object)

map_params = {
    "ll": f"{longitude},{latitude}",
    "spn": f"{span_lon},{span_lat}",
    "l": "map",
    "pt": f"{longitude},{latitude},comma"
}

map_url = "http://static-maps.yandex.ru/1.x/"
map_response = requests.get(map_url, params=map_params)
Image.open(BytesIO(map_response.content)).show()