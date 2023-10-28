import time
import json
from replit import db
from slack_sdk import WebClient


with open('backup.json') as f:
	d = json.loads(f.read())

while True:
	for i in d:
		print(i, d[i]['display_name'])
		c = WebClient(token=db[i])
		c.users_profile_set(profile={
			"status_emoji": ":weary_russian: ",
			"status_text": f"really @{d[i]['display_name']} ({d[i]['real_name']})",
			# "status_expiration": 99999999999999999
		})
	time.sleep(60)
	print('\a')