import requests
import csv
from bs4 import BeautifulSoup
HOST = 'https://www.banki.ru/'
URL = 'https://www.banki.ru/services/responses/bank/otpbank/?page=2'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
}

def get_html(url,params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('div', class_='responses-list mobile-full-width')
    cards = []
    icon = items.find_all('article', class_='responses__item')

    for i in icon:
        if len(i.find('div', class_='flexbox flexbox--inline flexbox--row flexbox--gap_xsmall flexbox--align-items_baseline').find_all('span')) == 3:
            cards.append(
            {
                'article': i.find('div', class_='flexbox flexbox--row flexbox--gap_xxsmall flexbox--align-items_flex-start').find('a', class_='header-h3').get_text(strip=True),
                'fit_back': i.find('div', class_='responses__item__message markup-inside-small markup-inside-small--bullet').get_text(strip=True),
                'stars': i.find('div', class_='flexbox flexbox--inline flexbox--row flexbox--gap_xsmall flexbox--align-items_baseline').find_all('span')[1].get_text(strip=True)

            }
        )

    return cards
def save_data(items,path):
    with open(path, 'w', encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['article', 'fit_back', 'stars'])
        for item in items:
            writer.writerow([item['article'], item['fit_back'], item['stars']])


# html=get_html(f'https://www.banki.ru/services/responses/bank/otpbank/?page={2}')
# print(get_content(html.text))
def parser():
    PAGENATION = input('укажите кол-во страниц для парсинга')
    PAGENATION=int(PAGENATION.strip())
    html=get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGENATION):
            print(f'Парсим страницу {page}')
            html = get_html(f'https://www.banki.ru/services/responses/bank/otpbank/?page={page}')
            cards.extend(get_content(html.text))
            save_data(cards, 'cards.csv')
    else:
        print('Error')
parser()


