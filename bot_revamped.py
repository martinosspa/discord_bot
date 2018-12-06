import discord
import json
import atexit
import random
from pprint import pprint

token = 'MzI2ODI1MjczNzA0MDU0Nzk0.DuhaRA.tsw2k4gWFsF1RfTtoJbQnNFB600'
client = discord.Client()
attack_types = ['phys', 'magic']
data = {}
last_message = None

def generate_encounter():
	encounter = {}
	data['encounter'] = {}
	encounter['health'] = 100
	encounter['armor'] = 100
	encounter['name'] = 'test name'
	encounter['magic_shield'] = 100
	encounter['max_health'] = encounter['health']
	data['encounter'] = encounter


async def send_encounter_info(channel, replace=False):
	encounter = data['encounter']
	msg = f"""```fix
> Armor: {encounter['armor']}		> Health: {encounter['health']}
> Magic Armor: {encounter['magic_shield']}
```"""
	global last_message
	if replace:
		await client.edit_message(last_message, msg)
	else:
		last_message = await client.send_message(channel, msg)


def generate_info(user):
	data[user] = {}
	data[user]['level'] = 1
	data[user]['magic_damage'] = 10
	data[user]['attack_damage'] = 10


def user_attack(user, attack_type):
	if attack_type == attack_types[0]:
		#physical
		hit = data[user]['attack_damage']*((data['encounter']['armor']-50)/(500 - 50) + 0.5)
	else:
		hit = data[user]['magic_damage']*((data['encounter']['magic_shield']-50)/(500 - 50) + 0.5)

	if data['encounter']['health'] - hit > 0:
		data['encounter']['health'] = round(data['encounter']['health'] - hit)
	elif data['encounter']['health'] - hit < 0:
		data['encounter']['health'] = 0
		# boss defeated



@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if message.content == '.start':
		await send_encounter_info(message.channel)

	if message.content == '.':
		await client.logout()
	if message.content.startswith('>'):
		if not message.author.id in data:
			generate_info(message.author.id)

		if message.content.startswith(f'>{attack_types[0]}'): # physical damage
			print(f'boss physical damage taken from {message.author.name}')
			user_attack(message.author.id, attack_types[0])
			await send_encounter_info(message.channel, replace=True)
			await client.delete_message(message)

		elif message.content.startswith(f'>{attack_types[1]}'):
			print(f'boss magic damage taken from {message.author.name}')
			user_attack(message.author.id, message.content)
			await send_encounter_info(message.channel, replace=True)
			await client.delete_message(message)


@client.event
async def on_ready():
	print('Logged in')
	with open('data.json') as f:
		global data
		data = json.load(f)
	if not 'encounter' in data:
		generate_encounter()

	



def on_exit():
	with open('data.json', 'w') as file:
		json.dump(data, file)
	client.logout()

atexit.register(on_exit)
client.run(token)