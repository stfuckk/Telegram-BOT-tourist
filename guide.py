import requests
from bs4 import BeautifulSoup


# парсинг TripAdvisor
async def get_guide_list(place: str) -> str:
    url = f"https://www.tripadvisor.com/Attractions-g{place}-Activities-c47-t52-oa30"

    # получаем html
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # извлекаем информацию о местах
    places = soup.find_all("div", {"class": "attraction_clarity_cell"})
    top_places = []
    for place in places:
        # исключаем отели и гостиницы
        if "Hotel" not in place.find("div", {"class": "listing_title"}).text:
            name = place.find("div", {"class": "listing_title"}).text.strip()
            rating = place.find("span", {"class": "more"}).text.strip()
            address = place.find("div", {"class": "listing_address"}).text.strip()
            photo = place.find("img", {"class": "photo_image"})["src"]
            description = place.find("div", {"class": "listing_details"}).text.strip()

            top_places.append(f'')

