import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import time
import sys
from datetime import date

# Logging start time
start_time = time.time()

# Take first console argument as number of "infinite pages to scroll", max 10 pages and defaults to 2
try:
    numPagines = int(sys.argv[1])
    if numPagines > 10:
        numPagines = 2
except:
    numPagines = 2

# Empty list that will be appended
d = []

# Looping over every page (could be infinite)
for i in range(0, numPagines):
    url = f'https://store.steampowered.com/search/results/?query&start={i*50}&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&infinite=1'
    # Getting page content and parsing the html
    page = requests.get(url)
    data = page.json()
    soup = BeautifulSoup(data['results_html'], "html.parser")
    # Finding html code for all games, which is inside an 'a' tag
    all_games = soup.find_all('a')

    # Looping over every found game
    for game in all_games:
        # Getting the game page url and parsing the html
        game_url = game['href']
        game_page = requests.get(game_url)
        soup = BeautifulSoup(game_page.text, "html.parser")
        # Finding all the game tags
        tags = soup.find('div', {'class': 'glance_tags popular_tags'})
        
        # Handling possible missing values
        try:
            tags_list = [tag.text.strip() for tag in tags]
            while("" in tags_list):
                tags_list.remove("")
        except:
            tags_list = ['untagged']

        # Getting the discount and the original and final price
        price = game.find('div', {'class': 'col search_price_discount_combined responsive_secondrow'})
        try:
            price1 = price.find('div', {'class': 'col search_price discounted responsive_secondrow'}).text.strip()
        except:
            continue

        # Creating a dictionary with the obtained information
        d.append(
            {
                'Name': game.find('span', {'class': 'title'}).text.strip(),
                'Tags': tags_list[0:3],
                'Original price': price1.split('€')[0],
                'Discount': price.find('div', {'class': 'col search_discount responsive_secondrow'}).text.strip(),
                'Offer price': price1.split('€')[1]
            }
        )
    # Pausing requests for 5 seconds to avoid overloading the server
    time.sleep(5)

# Creating a result pandas DataFrame and exporting a csv file with the current date as the file name
df = pd.DataFrame(d)
today = date.today().strftime("%b-%d-%Y")
df.to_csv(f"../outputs/{str(today)}_offers.csv", index=False)

# Fetching final execution time
end_time = time.time()
elapsed_time = end_time-start_time
print(f"Scraping time: {elapsed_time} seconds")