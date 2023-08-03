import requests
from bs4 import BeautifulSoup 
import csv
import os

URL = 'https://www.vlsu.ru/index.php?id=3'
HEADERS = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36', 'accept': '*/*'}
HOST = 'http://www.vlsu.ru/'
FILE = 'cars.csv'


def  get_html(url, params=None):
 	r = requests.get(url, headers=HEADERS, params=params)
 	return r


def get_pages_count(html):
	soup = BeautifulSoup(html, 'html.parser')
	pagination = soup.find_all('li', class_='page-item')
	if pagination:
		return int(pagination[-1].get_text())
	else:
		return 1
	

def get_content(html):
 soup = BeautifulSoup(html, 'html.parser') 
 items = soup.find_all('div', class_='pro-item')

 
 cars = []
 for item in items:
    cars.append({
  	'title': item.find('div', class_='title').get_text(strip=True),
  	'sil': HOST + item.find('a').get('href'),
  	'cena': item.find('div',  class_='price').get_text(strip=True),
  	'time': item.find('div',  class_='status').get_text(strip=True),
  	'mass': item.find('div',  class_='features').get_text(strip=True)
  	
  	
   })
 return cars

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название товаров', 'Ссылка на товар', 'Цена в руб', 'Наличие', 'Характеристики'])
        for item in items:
            writer.writerow([item['title'], item['sil'], item['cena'], item['time'], item['mass']])

def parse():
    FILE = input('Введите название файла с расширением: ')
    URL = input('Введите URL: ')
    URL = URL.strip()
    FILE = FILE.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Изъято страниц {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        save_file(cars, FILE)
        print(f'Получено {len(cars)} товаров')
        os.startfile(FILE)
    else:
        print('Error')
