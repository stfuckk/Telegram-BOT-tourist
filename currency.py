import requests

API_KEY_OW = open("TOKEN.txt").read().split()[1]
API_KEY = open("TOKEN.txt").read().split()[4]


def exchange_currency(amount, city) -> str:
    url = f"https://openexchangerates.org/api/latest.json?app_id={API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Определение кода валюты по городу
    currency_code = None
    for cur_code, cur_info in data['rates'].items():
        if not isinstance(cur_info, dict):
            continue
        if cur_info['name'].lower() == city.lower():
            currency_code = cur_code
            break

    if currency_code is None:
        return f"К сожалению, мы не можем обменять валюту в городе {city}"

    # Расчет суммы обмена
    exchange_rate = data['rates'][currency_code]['rate']
    result = round(amount / exchange_rate, 2)

    return f"Вы меняете {amount} RUB ===> {result} {currency_code} in {city}"


print(exchange_currency(1000, 'London'))
