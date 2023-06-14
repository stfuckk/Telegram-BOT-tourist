import requests

API_KEY_OW = open("TOKEN.txt").read().split()[1]
API_KEY = open("TOKEN.txt").read().split()[4]


async def exchange_currency(amount, country):
    country = country.upper()
    # Получаем код валюты по стране
    try:
        response = requests.get(f"https://restcountries.com/v3/name/{country}")
        currency_code = response.json()[0]["currencies"]
        currency_code = list(currency_code.keys())[0]
    except:
        return f'Не могу найти такую страну в списке, проверьте правильность написания!'

    # Получаем курс валюты
    response = requests.get("https://openexchangerates.org/api/latest.json", params={
        "app_id": API_KEY,
        "symbols": "RUB," + currency_code
    })
    exchange_rate = response.json()["rates"]["RUB"]
    # Обмениваем валюту

    # здесь мы переводим рубли в доллары
    result = amount / exchange_rate

    exchange_rate = response.json()["rates"][currency_code]

    # здесь мы переводим доллары в нужную валюту
    result = round(result * exchange_rate, 2)

    return f'Вы меняете {amount} RUB ===> {result} {currency_code} in {country}'

