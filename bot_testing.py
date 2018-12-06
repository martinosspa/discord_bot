# Work with Python 3.6
import discord
import json
import atexit
import random
from pprint import pprint

TOKEN = 'MzI2ODI1MjczNzA0MDU0Nzk0.DuhaRA.tsw2k4gWFsF1RfTtoJbQnNFB600'

client = discord.Client()

data = {}
options = ['hit', 'option2', 'option3', 'option4']
general_options = ['walk']
all_options = options + general_options

def generate_info(user):
	data[user] = {}
	data[user]['level'] = 1
	data[user]['encounter'] = {}
	data[user]['in_encounter'] = False

def generate_encounter(user):
	encounter = {}
	encounter['name'] = 'test name'
	encounter['level'] = data[user]['level']
	encounter['health'] = 100
	encounter['armor'] = 100
	data[user]['in_encounter'] = True
	data[user]['encounter'] = encounter

def hit_encounter(user):
	level = data[user]['level']
	hit = level * random.uniform(level*0.1, level*0.2)
	if data[user]['encounter']['health'] - hit > 0:
		data[user]['encounter']['health'] -= hit
	else:
		pass

async def send_options(channel, user):
	await send_encounter_info(channel, user)
	await client.send_message(channel, format_message(options))

async def next_encounter(channel, user):
	if user in data:
		user_info = data[user]
	else:
		generate_info(user)

	if data[user]['in_encounter']:
		# TEMPORARY
		#load_encounter(user)
		generate_encounter(user)
	else:
		generate_encounter(user)

async def pick_general_option(user, message):
	# picks a general option
	if message.content == f'>{general_options[0]}':
		# general option [hit]
		await next_encounter(message.channel, message.author.id)
		
		print(f'{user} new encounter')
	elif message.content == f'>{options[0]}':
		hit_encounter(message.author.id)

	await send_options(message.channel, message.author.id)

async def send_encounter_info(channel, user):
	encounter = data[user]['encounter']
	msg = f"""```fix
			-=- {encounter['name']} -=-
> Armor: {encounter['armor']}		> Health: {encounter['health']}
	```"""
	await client.send_message(channel, msg)

def format_message(options):
	new_message = f"""```fix
>{options[0]}		>{options[1]}
>{options[2]}		>{options[3]}
```"""
	return new_message

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content == '.':
		await client.logout()

	if message.content.startswith('>'):
		#adventure option

		if not message.author.id in data:
			generate_info(message.author.id)

		await pick_general_option(message.author.id, message)

@client.event
async def on_ready():
	print('Logged in')
	global data
	with open('data.json') as f:
		data = json.load(f)


def on_exit():
	with open('data.json', 'w') as file:
		json.dump(data, file)
	client.logout()
atexit.register(on_exit)

client.run(TOKEN)