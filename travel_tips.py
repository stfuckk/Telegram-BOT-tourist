import requests
from bs4 import BeautifulSoup
import random


def get_travel_tip():
    url = 'https://apartos.ru/category-touristic-hints/61-best-tourist-tips-ever.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    tips = []
    h3 = soup.find('h3')
    found_h3 = False
    while h3:
        content = []
        if found_h3 == True:
            break
        for sibling in h3.find_next_siblings():
            if sibling.name == 'h3':
                found_h3 = True
                break
            content.append(sibling)
        tips.append([h3.text.strip(), ''.join([str(x) for x in content]).strip()])
        h3 = sibling

    random_tip = random.choice(tips)

    return f'***Совет №{random_tip[0]}***\n{random_tip[1]}'


get_travel_tip()
