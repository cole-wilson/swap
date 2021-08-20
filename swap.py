[input('ARE YOU SURE!!!!!?!????') for i in range(10)]
import os
import time
import json
import random
from replit import db
import urllib.request as ur

if open('um').read() == 'swap':
	print('unswap first')
	exit(1)
with open('um', 'w+') as f:
	f.write('swap')

blacklist = [
	"U02BVDP7G5Q",
	"U02BSCXFXA9",
	"U01651Q77EV",
	"backup"
] # remember to update main.py too

user_ids = list(db.keys())
user_ids = list(filter(lambda i: i not in blacklist, user_ids))

try:
	from slack_sdk import WebClient
except ModuleNotFoundError:
	os.system('pip3 install slack_sdk')
	from slack_sdk import WebClient

bot_client = WebClient(token=os.getenv('BOT_TOKEN'))

# ================== get ==========================
backup = {}
for user_id in user_ids:
	user_token = db[user_id]
	client = WebClient(token=user_token)
	profile = client.users_profile_get()['profile']

	fields = [
		"real_name",
		"real_name_normalized",
		"display_name",
		"display_name_normalized",
		"status_text",
		"status_emoji",
		"status_expiration",
		"image_original",
	]

	user_backup = {"id": user_id}
	for i in fields:
		user_backup[i] = profile[i]
	backup[user_id] = user_backup

with open('backup.json', 'w+') as backup_file:
	serialized = json.dumps(backup, indent=2)
	backup_file.write(serialized)
	db['backup'] = serialized

data = backup
# =================== set =======================
possible_ids = [*user_ids]
random.shuffle(possible_ids)
for user_id in user_ids:
	user_token = db[user_id]
	client = WebClient(token=user_token)
	
	index = 1 if possible_ids[0] == user_id else 0
	newdata = data[possible_ids[index]]
	newid = possible_ids[index]
	possible_ids.pop(index)
	
	newphoto = newdata['image_original']
	ur.urlretrieve(newphoto, 'image.png')
	client.users_setPhoto(image='image.png')
	del newdata['image_original']
	del newdata['id']
	newdata['status_text'] = f"#swap: I'm actually {data[user_id]['display_name']} (@{data[user_id]['real_name']})"
	newdata['status_emoji'] = ':sussy:'
	newdata['status_expiration'] = round(time.time())+(86400*2)
	client.users_profile_set(profile=newdata)
	print('done:', user_id, '->', newid)
#########################
text = ''
for i in user_ids:
	text += f"<@{i}>"
text = []
for i in backup.keys():
	text.append(f"<@{i}>")
bot_client.chat_postMessage(
	channel="swap",
	text=f"{', '.join(text)} you have all been swapped!"
)