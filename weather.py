import requests

# Задаем URL и API-KEY OpenWeatherMap
URL = 'http://api.openweathermap.org/data/2.5/weather'
API_KEY = open("TOKEN.txt").read().split()[1]
print(API_KEY)


# Получаем погоду в виде текста
# "->" указывает на тип возвращаемого значения
async def get_weather(city: str) -> str:
    # параметры запроса
    params = {'q': city, 'appid': API_KEY, 'units': 'metric', 'lang': 'ru'}
    response = requests.get(URL, params=params)

    # обрабатываем ответ
    if response.status_code == 200:
        data = response.json()
        # температура
        temp = data['main']['temp']
        # температура по ощущениям
        temp_fell = data['main']['feels_like']
        # влажность
        humidity = data['main']['humidity']
        # скорость ветра
        wind = data['wind']['speed']
        # прогноз на ближайшие дни
        forecast = data['weather'][0]['description']
        return (f'**ПОГОДА В {city.upper()}**\n'
                f'Температура: **{temp}°C**\n'
                f'Ощущается как: **{temp_fell}°C**\n'
                f'Влажность: **{humidity}%**\n'
                f'Скорость ветра: **{wind}м/c**\n'
                f'Прогноз на ближайшие дни: **{forecast}**')
    else:
        return 'Не удалось получить данные о погоде. Попробуйте ещё раз.'