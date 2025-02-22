import sys
import math
from io import BytesIO
import requests
from PIL import Image
from scale import get_spn_points


def haversine(lon1, lat1, lon2, lat2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def main():
    if len(sys.argv) < 2:
        sys.exit(1)
    address_query = " ".join(sys.argv[1:])

    geocoder_url = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": address_query,
        "format": "json"
    }
    response = requests.get(geocoder_url, params=geocoder_params)
    if not response:
        sys.exit(1)
    geo_json = response.json()
    try:
        address_obj = geo_json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    except (IndexError, KeyError):
        sys.exit(1)
    addr_coord = address_obj["Point"]["pos"]
    lon_addr, lat_addr = addr_coord.split()
    addr_coord = f"{lon_addr},{lat_addr}"

    search_url = "https://search-maps.yandex.ru/v1/"
    search_params = {
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
        "text": "аптека",
        "lang": "ru_RU",
        "ll": addr_coord,
        "type": "biz"
    }
    response = requests.get(search_url, params=search_params)
    if not response:
        sys.exit(1)
    search_json = response.json()
    try:
        pharmacy = search_json["features"][0]
    except (IndexError, KeyError):
        sys.exit(1)
    ph_data = pharmacy["properties"]["CompanyMetaData"]
    ph_name = ph_data.get("name", "Неизвестно")
    ph_address = ph_data.get("address", "Неизвестно")
    ph_hours = ph_data.get("Hours", "Не указано")
    ph_coord = pharmacy["geometry"]["coordinates"]
    ph_coord_str = f"{ph_coord[0]},{ph_coord[1]}"

    distance = haversine(float(lon_addr), float(lat_addr), ph_coord[0], ph_coord[1])

    center_lon = (float(lon_addr) + ph_coord[0]) / 2
    center_lat = (float(lat_addr) + ph_coord[1]) / 2
    center = f"{center_lon},{center_lat}"
    spn = get_spn_points(addr_coord, ph_coord_str)

    pt = f"{addr_coord},pm2blm~{ph_coord_str},pm2rdm"

    map_url = "https://static-maps.yandex.ru/1.x/"
    map_params = {
        "ll": center,
        "spn": spn,
        "l": "map",
        "pt": pt
    }
    response = requests.get(map_url, params=map_params)
    if not response:
        sys.exit(1)
    image = Image.open(BytesIO(response.content))
    image.show()

    snippet = f"Аптека: {ph_name}\nАдрес: {ph_address}\nВремя работы: {ph_hours}\nРасстояние: {distance:.0f} м"
    print(snippet)


if __name__ == "__main__":
    main()
