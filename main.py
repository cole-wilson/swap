import os
from replit import db

try:
	from slack_bolt import App
except ModuleNotFoundError:
	os.system('pip3 install slack_bolt')
	from slack_bolt import App
ammount = 7
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_bolt.oauth.callback_options import CallbackOptions
from slack_bolt.response import BoltResponse
from slack_sdk import WebClient

from flask import Flask
app=Flask(__name__)
app.route('/')(lambda: 'the swap signup window has passed! may be back later')
app.run(host="0.0.0.0",port=8080)
exit()
def success(args):
	user_id = args.installation.user_id
	user_token = args.installation.user_token
	# nnn = user_id not in db.keys()
	nnn = True
	db[user_id] = user_token
	response = f"""yay!

	you have successfully signed up for the Great Hackclub Profile Swap of 2021!
	so far [{len(db.keys())-ammount}] people have signed up. I'm waiting for a bit more people!
	head over to #swap on slack for updates

	i will ping you when your profile has been updated!

	if you don't want to be a part of this for some reason, that's fine!
	just contact me and I will remove your profile

	after a day (or less), everything will return back to normal automatically!
	"""
	if nnn:
		try:
			bot_client = WebClient(token=os.getenv('BOT_TOKEN'))
			bot_client.chat_postMessage(
				channel="swap",
				text=f"<@{user_id}> just joined/rejoined! We now have {len(db.keys())-ammount} people!"
			)
		except:
			pass
	return BoltResponse(status=200,body=response)

def failure(args):
	return BoltResponse(status=args.suggested_status_code,body="failure :(\ntry again and if it doesn't work let me know on slack in #swap!")

app = App(
	signing_secret=os.environ.get("SIGNING_SECRET"),
	oauth_settings=OAuthSettings(
		client_id=os.environ.get("CLIENT_ID"),
		client_secret=os.environ.get("CLIENT_SECRET"),
		scopes=[],
		user_scopes=["users.profile:read", "users.profile:write"],
		redirect_uri=None,
		install_path="/",
		redirect_uri_path="/slack/oauth_redirect",
		callback_options=CallbackOptions(success=success, failure=failure),
	),
)

if __name__ == "__main__":
	app.start(port=int(os.environ.get("PORT", 3000)))
