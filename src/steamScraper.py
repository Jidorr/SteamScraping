import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time

url = 'https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&infinite=1'

start_time = time.time()

page = requests.get(url)
data = page.json()
soup = BeautifulSoup(data['results_html'], "html.parser")
all_games = soup.find_all('a')

d = []

for game in all_games:
    game_url = game['href']
    game_page = requests.get(game_url)
    soup = BeautifulSoup(game_page.text, "html.parser")
    tags = soup.find('div', {'class': 'glance_tags popular_tags'})
    try:
        tags_list = [tag.text.strip() for tag in tags]
        while("" in tags_list):
            tags_list.remove("")
    except:
        tags_list = ['untagged']
    d.append(
        {
            'name': game.find('span', {'class': 'title'}).text.strip(),
            'tags': tags_list[0:3],
            'price': game.find('div', {'class': 'col search_price_discount_combined responsive_secondrow'}).text.strip()
        }
    )
df = pd.DataFrame(d)

end_time = time.time()
elapsed_time = end_time-start_time
print(df)
print(f"Scraping time: {elapsed_time} seconds")