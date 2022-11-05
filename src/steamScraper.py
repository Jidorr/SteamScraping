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

    price = game.find('div', {'class': 'col search_price_discount_combined responsive_secondrow'})
    try:
        price1 = price.find('div', {'class': 'col search_price discounted responsive_secondrow'}).text.strip()
    except:
        continue

    d.append(
        {
            'Name': game.find('span', {'class': 'title'}).text.strip(),
            'Tags': tags_list[0:3],
            'Original price': price1.split('€')[0],
            'Discount': price.find('div', {'class': 'col search_discount responsive_secondrow'}).text.strip(),
            'Offer price': price1.split('€')[1]
        }
    )
df = pd.DataFrame(d)

end_time = time.time()
elapsed_time = end_time-start_time
print(df)
print(f"Scraping time: {elapsed_time} seconds")