import requests
from bs4 import BeautifulSoup
import pandas
import json

url = 'https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&infinite=1'

page = requests.get(url)
data = page.json()
soup = BeautifulSoup(data['results_html'], "html.parser")
all_games = soup.find_all('a')

for game in all_games:
    print('******************************')
    print(game.find('span', {'class': 'title'}).text.strip())
    print(game.find('div', {'class': 'col search_price_discount_combined responsive_secondrow'}).text.strip())