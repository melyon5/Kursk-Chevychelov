import sys
from io import BytesIO
import requests
from PIL import Image
from scale import get_map_params


def haversine(lon1, lat1, lon2, lat2):
    import math
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
        "type": "biz",
        "results": "10"
    }
    response = requests.get(search_url, params=search_params)
    if not response:
        sys.exit(1)
    search_json = response.json()
    features = search_json.get("features", [])
    if not features:
        sys.exit(1)
    pharmacy_coords = []
    pt_list = []
    for feature in features:
        ph_data = feature["properties"]["CompanyMetaData"]
        hours_info = ph_data.get("Hours")
        color = "pm2grl"
        if hours_info:
            text = hours_info.get("text", "").lower()
            if "круглосуточ" in text:
                color = "pm2gnl"
            else:
                color = "pm2blm"
        ph_coord = feature["geometry"]["coordinates"]
        ph_coord_str = f"{ph_coord[0]},{ph_coord[1]}"
        pharmacy_coords.append(ph_coord_str)
        pt_list.append(f"{ph_coord_str},{color}")

    pt_address = f"{addr_coord},pm2rdm"
    pt_list.append(pt_address)
    all_coords = pharmacy_coords + [addr_coord]
    center, spn = get_map_params(all_coords)
    pt = "~".join(pt_list)

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


if __name__ == "__main__":
    main()
