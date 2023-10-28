assert input('yes?') == "yes!"
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
	"U02BVDP7G5Q", # also me
	"U02BSCXFXA9", # also me
	"U01651Q77EV", # me
	"U02BT9MHX1B", # also me
	"U01DV5F30CF", # zfogg
	"U01FHRTCN78", # charlampos
	"backup",
] # remember to update main.py too

user_ids = list(db.keys())
user_ids = list(filter(lambda i: i not in blacklist, user_ids))

# print('the following people will be swapped in an hours time:')
# for i in user_ids:
# 	print(f'- <@{i}>')
# print('this means someone will have your profile, and you will have someone elses.')
# print("if you don't want this, please let me know in the next hour! (either in this thread or DM me)")
# print("there is no pressure if you accidently signed up or anything")
# exit(1)
# input()
# testing==============
# user_ids = [
# 	"U02BVDP7G5Q",
# 	"U02BSCXFXA9",
# 	"U01651Q77EV",
# 	"U02BT9MHX1B",
# ]

try:
	from slack_sdk import WebClient
except ModuleNotFoundError:
	os.system('pip3 install slack_sdk')
	from slack_sdk import WebClient

bot_client = WebClient(token=os.getenv('BOT_TOKEN'))

bot_client.chat_postMessage(
	channel="U01651Q77EV",
	text="-"*80
)

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
		"phone",
		"title",
		# "email",
		"pronouns",
		"first_name",
		"last_name",
		"fields"
	]

	user_backup = {"id": user_id}
	for i in fields:
		try:
			user_backup[i] = profile[i]
			if user_backup[i] == '':
				user_backup[i] = ' '
		except KeyError: print('error', i)
	backup[user_id] = user_backup

with open('backup.json', 'w+') as backup_file:
	serialized = json.dumps(backup, indent=2)
	backup_file.write(serialized)
	db['backup'] = serialized

data = backup
# =================== set =======================
offset = 3
assert offset < len(user_ids), "offset >= len(user_ids)"
pia = [*user_ids]
pib = [*user_ids][-offset:] + [*user_ids][:-offset]

c = 0
for user_id, newid in zip(pia, pib):
	c += 1
	print(c)
	user_token = db[user_id]
	client = WebClient(token=user_token)
	newdata = data[newid]

	newphoto = newdata['image_original']
	ur.urlretrieve(newphoto, 'image.png')
	client.users_setPhoto(image='image.png')
	del newdata['image_original']
	del newdata['id']
	# newdata['status_text'] = f"#swap: I'm actually {data[user_id]['real_name']} (@{data[user_id]['display_name']})"
	newdata['status_emoji'] = ':sussy:'
	newdata['status_expiration'] = round(time.time())+(86400*2)
	client.users_profile_set(profile=newdata)
	print('done:', user_id, '->', newid)
	bot_client.chat_postMessage(
		channel="U01651Q77EV",
		text=f"<@{user_id}> is really @{data[user_id]['display_name']}"
	)
	bot_client.chat_postMessage(
		channel=user_id,
		text=f"you have taken @{newdata['display_name']}'s profile."
	)
	bot_client.chat_postMessage(
		channel=newid,
		text=f"@{data[user_id]['display_name']} has your profile."
	)
	

	
	
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