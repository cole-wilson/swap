[input('ARE YOU SURE!!!!!?!????') for i in range(10)]
import os
import json
import urllib.request as ur
from replit import db

with open('um', 'w+') as f:
	f.write('unswap')

try:
	from slack_sdk import WebClient
except ModuleNotFoundError:
	os.system('pip3 install slack_sdk')
	from slack_sdk import WebClient
bot_client = WebClient(token=os.getenv('BOT_TOKEN'))
backup = json.loads(open('backup.json').read())

for user_id in backup:
	client = WebClient(token=db[user_id])
	profile = backup[user_id]
	del profile['id']

	ur.urlretrieve(profile['image_original'], 'image.png')
	client.users_setPhoto(image='image.png')
	
	del profile['image_original']
	client.users_profile_set(profile=profile)
	print('done:', user_id)

#########################
text = []
for i in backup.keys():
	text.append(f"<@{i}>")
bot_client.chat_postMessage(
	channel="swap",
	text=f"{', '.join(text)} you have all been *UN*swapped!"
)