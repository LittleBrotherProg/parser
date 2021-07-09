import requests
from bs4 import BeautifulSoup as BS

r = requests.get('https://stopgame.ru/articles/new')
html = BS(r.content, 'html.parser')

for el in html.select('.lent-block'):
	title = el.select('.lent-title > a')
	print( title[0].text )