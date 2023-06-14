import requests
from bs4 import BeautifulSoup
import random


async def get_travel_tip():
    url = 'https://apartos.ru/category-touristic-hints/61-best-tourist-tips-ever.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    tips = []
    h3 = soup.find('h3')

    for h3 in soup.find_all('h3'):
        title = h3.text.strip()
        text = ''
        for sibling in h3.next_siblings:
            if sibling.name == 'p':
                text += sibling.text.strip().replace('\r', '').replace('    ', '')
            elif sibling.name == 'h3':
                break
        tips.append([title, text])

    for i in range(1, 5):
        del tips[-1]

    random_tip = random.choice(tips)

    return f'***Совет №{random_tip[0]}***\n{random_tip[1]}'
