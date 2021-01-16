import discord
import asyncio
from member_manage import *
from StopGames import *
from config import *
from discord import guild


StopGame = StopGamesBot()

async def check_news(chanel):
	
	received_news = StopGame.check()
	if len(received_news) == 0:
		print('Last: ' + str(StopGame.last_news))
		pass
	else:
		received_news.reverse()
		for news in received_news:
			message = 'Оу, на StopGames новый пост!\n'
			for text in news:
				if type(text) == int:
					continue
				elif text['type'] == 'mh':
					message = message + '**' + text['text'] + '**\n'
				elif text['type'] == 'ln':
					message += 'Ссылка: '
					message = message + text['text'] + '\n'
					print(text['text'])

			message += ('-' * 60)
			await chanel.send(message)
			print('Last: ' + str(StopGame.last_news))


class MyBot(discord.Client):
	async def on_message(self, message):
		if message.content == '>>get role' and message.channel.id == 797063236134371348:
			member = message.author
			role = discord.utils.get(member.guild.roles, id=796790894253703188)
			await member.add_roles(role)

	async def on_ready(self):

		server = discord.utils.get(self.guilds, id=640261638024593419)
		text_chanel = discord.utils.get(server.text_channels, id=695340257305952397)
		await text_chanel.send('Ready')

		text_chanel = discord.utils.get(server.text_channels, id=797853741277511690)
		i = 0
		while 1:
			i += 1
			print('Chek ' + str(i))
			await check_news(text_chanel)
			await asyncio.sleep(60)



client = MyBot()
client.run(TOKEN)

"""	
Примечание, пока что не нужно.

		print('-'*20)
		async for member in server.fetch_members(limit=150):
			print(member.name)
		print('-'*20)
"""

"""		
Примечание: не работает, т.к. не включены итераторы.

	async def on_member_join(self, member):
		print('work')
		server = discord.utils.get(self.guilds, id=640261638024593419)
		text_chanel = discord.utils.get(server.text_channels, id=797063236134371348)
		await text_chanel.send('Привет, введи \">>get role\", чтобы получить первую роль!')
"""
