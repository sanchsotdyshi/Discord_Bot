import discord
import asyncio
import bs4
import requests
from config import *
from bs4 import BeautifulSoup
import os



def download_game(game):
	"""
	Функция получает на вход название игры
	и возвращает путь к уже скачанному файлу
	"""

	"""
	Мы игнорируем основной сайт все запросы и парсинг
	происходят сразу на файловом сервере
	По полученному имени игры формируем ссылку на сервер
	"""
	game_name = game.replace(' ', '%20')
	url = 'https://onlinefixuploads.ru/torrents/' + game_name + '/'
	
	#Создаем сессию и по url запрашиваем страницу
	s = requests.Session()
	headers = {
		'Referer': 'https://online-fix.me/',	
	}
	page = s.get(url, headers=headers)
	soup = BeautifulSoup(page.text, 'lxml')

	#На странице находим все ссылки и среди них ищем ту,
	#Которая будет указывать на файл(название будет оканчиватьсяна .torrent)
	links = soup.find_all('a')
	for link in links:
		if '.torrent' in link.text:
			file_name = link.get('href')

	#Создаем url и заголовки запроса для файла игры
	file_url = 'https://onlinefixuploads.ru/torrents/' + game_name + '/' + file_name
	headers_2 = {
		'Referer': 'https://onlinefixuploads.ru/torrents/Inertial%20Drift/',
	}

	# Получаем файл, записываем его в папку и возвращаем название
	game_data = s.get(file_url, headers=headers_2)
	with open(file_name, 'wb') as game_file:
		game_file.write(game_data.content)

	return file_name


class MyBot(discord.Client):
	async def on_message(self, message):
		if message.content.startswith('!d '):
			"""
			Если сообщение начинается с команды !d, запускаем функцию скачки игры.
			На выходе получаем путь к файлу со скаченной игрой.
			Определяем канал, с которого пришла команда.
			"""
			game_path = download_game(message.content[3:])
			text_channel = message.channel
			#Открываем файл и отпраляем его в сообщении
			with open(game_path, 'rb') as game_file:
				await text_channel.send(file=discord.File(game_file))

			#Печатаем лог и удаляем файл
			print("Dowloading - "game_path)
			os.remove(game_path)


	
	async def on_ready(self):
		#Функция сообщает в консоль о готовности бота
		print('ready')
	

#Запуск бота
client = MyBot()
client.run(TOKEN)

