import sys
import requests


def main():
    address_query = " ".join(sys.argv[1:])
    geocoder_api = "http://geocode-maps.yandex.ru/1.x/"

    params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": address_query,
        "format": "json"
    }
    response = requests.get(geocoder_api, params=params)
    if not response:
        sys.exit(1)
    json_response = response.json()
    try:
        geo_object = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    except (IndexError, KeyError):
        print("Адрес не найден")
        sys.exit(1)

    coordinates = geo_object["Point"]["pos"]

    params_district = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": coordinates,
        "kind": "district",
        "format": "json"
    }
    response_district = requests.get(geocoder_api, params=params_district)
    if not response_district:
        sys.exit(1)
    json_district = response_district.json()
    try:
        district_object = json_district["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        district_name = district_object["name"]
    except (IndexError, KeyError):
        print("Район не найден")
        sys.exit(1)

    print("Заданный адрес находится в районе:", district_name)


if __name__ == "__main__":
    main()
