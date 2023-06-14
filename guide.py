import requests


async def get_guide_list(city: str):
    # получаем координаты города через Геокодер API
    geo_params = {
        'format': 'json',
        'geocode': city,
        'apikey': open("TOKEN.txt").read().split()[2],
    }
    try:
        geo_response = requests.get('https://geocode-maps.yandex.ru/1.x/', params=geo_params)
        geo_json = geo_response.json()
        coords = geo_json['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()
        lat, lon = coords[1], coords[0]
    except (KeyError, IndexError):
        return 'К сожалению, я не смог найти достопримечательности в указанном месте.'

    # ищем достопримечательности
    search_params = {
        'apikey': open("TOKEN.txt").read().split()[3],
        'text': 'достопримечательности',
        'lang': 'ru_RU',
        'll': f'{lon},{lat}',
        'type': 'biz',
        'results': 50,
        'format': 'json'
    }
    search_response = requests.get('https://search-maps.yandex.ru/v1/', params=search_params)
    search_json = search_response.json()

    # если достопримечательности не найдены, возвращаем сообщение об ошибке
    if 'features' not in search_json:
        return 'К сожалению, я не смог найти достопримечательности в указанном месте.'

    # Выводим результаты
    attractions = []
    for feature in search_json['features']:
        name = feature['properties']['name']
        address = feature['properties']['CompanyMetaData']['address']
        f_url = feature['properties']['CompanyMetaData'].get('url', 'нет')
        f_lat = feature['geometry']['coordinates'][1]
        f_lon = feature['geometry']['coordinates'][0]
        attractions.append(f'Название: ***{name}***\n'
                           f'Адрес: ***{address}***\n'
                           f'Координаты: ***{f_lat} , {f_lon}***\n'
                           f'Ссылка: ***{f_url}***')

    return attractions
