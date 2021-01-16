import bs4
import requests
from bs4 import BeautifulSoup


class StopGamesBot(object):
	"""
	Класс представляет собой реализация парсера для сайта https://stopgame.ru/
	Парсит главную страницу и передает боту все свежие новости.
	"""
	def __init__(self):
		self.url = 'https://stopgame.ru/news'
		self.news_url = 'https://stopgame.ru'
		self.last_news = 46349


	"""По заданному URL получает код страницы"""
	def get_page(self, url):
		req = requests.get(url)
		page = req.text
		return page

	"""Получает порядковый номер новости на сайте"""
	def get_news_num(self, link):
		data = link.split('/')
		num = int(data[2])
		return num

	"""Собирает последние новости с главной страницы"""
	def get_news(self, soup):
		news = []
		for new in soup.find_all('div', 'item article-summary'):
			item = []
			caption = new.find('div', 'caption caption-bold')
			if self.get_news_num(caption.a['href']) <= self.last_news:
				continue
			else:
				news_object = {
					'type': 'mh',
					'text': caption.a.string
				}
				item.append(news_object)

				news_object = {
					'type': 'ln',
					'text': self.news_url + caption.a['href']
				}
				item.append(news_object)
				item.append(self.get_news_num(caption.a['href']))
				news.append(item)

		return news

	"""Функция для запуска парсера"""
	def check(self):
		page = self.get_page(self.url)
		soup = BeautifulSoup(page, 'lxml')
		news = self.get_news(soup)
		if len(news) == 0:
			pass
		else:
			self.last_news = news[0][2]
		return news