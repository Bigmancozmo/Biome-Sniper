import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import dataMgr as d

try:
	import selfcord
except:
	os.system("py -3 -m pip install git+https://github.com/dolfies/discord.py-self@renamed#egg=selfcord.py[voice]")

try:
	import win10toast
except:
	os.system("python -m pip install win10toast")

try:
	import requests
except:
	os.system("python -m pip install requests")

try:
	import urllib
except:
	os.system("python -m pip install urllib")

from urllib.parse import urlparse, parse_qs, unquote
import selfcord, asyncio, requests, webbrowser
from win10toast import ToastNotifier

toast = ToastNotifier()

target_guilds = []
target_channels = []
if d.get_key("Server_SpyOnBMC", True):
	target_guilds.append(1000444267308777543)
	target_channels.append(1414096735013441680)
	target_channels.append(1154374652664233994)
	target_channels.append(1416223439613857942)
if d.get_key("Server_SolsRNG", False):
	target_guilds.append(1186570213077041233)
	target_channels.append(1282542323590496277)
	target_channels.append(1282543762425516083)

PRIVATE_SERVER_BASE = "https://www.roblox.com/games/15532962292/Sols-RNG-Eon-1-8?privateServerLinkCode="

# your discord token
TOKEN = "ImNotGivingYouMyTokenBuddy"

KEYWORDS = ["GLITCHED", "DREAMSPACE"]

keywords = []
if(d.get_key("KEYWORD_VoidCoin", False)):
    keywords.append("VOID")
if(d.get_key("KEYWORD_Mari", False)):
    keywords.append("MARI")
if(d.get_key("KEYWORD_Jest", False)):
    keywords.append("JEST")
if(d.get_key("KEYWORD_Obliv", False)):
    keywords.append("OBLIV")
if(d.get_key("KEYWORD_SandStorm", False)):
    keywords.append("SANDSTORM")
if(d.get_key("KEYWORD_Heaven", False)):
    keywords.append("HEAV")
if(d.get_key("KEYWORD_Starfall", False)):
    keywords.append("STARF")
if(d.get_key("KEYWORD_Corruption", False)):
    keywords.append("CORRUP")
if(d.get_key("KEYWORD_Null", False)):
    keywords.append("NULL")
if(d.get_key("KEYWORD_GLIT", False)):
    keywords.append("GLIT")
if(d.get_key("KEYWORD_DREAM", False)):
    keywords.append("DREAM")
TOKEN = d.get_key("DiscordToken", "")
KEYWORDS = keywords

BLACKLIST = ["ENDED"]

def resolve_share_link(share_url):
	try:
		headers = {
			'User-Agent': 'Roblox/WinInet'
		}

		response = requests.get(share_url, headers=headers, allow_redirects=True)
		location = response.url
		print(f"📍 Final URL after redirects: {location}")

		parsed_url = urlparse(location)
		query_params = parse_qs(parsed_url.query)

		deep_link_encoded = query_params.get('af_dp', query_params.get('deep_link_value'))
		if not deep_link_encoded:
			print('❌ Deep link not found in redirect.')
			return None

		roblox_uri = unquote(deep_link_encoded[0])
		print(f"🔗 Resolved Roblox URI: {roblox_uri}")
		return roblox_uri

	except Exception as e:
		print(f"🚫 Error resolving share link: {e}")
		return None

async def handle_message(message):
	allText = ""
	if message.content:
		allText = allText+message.content
	if(message.embeds):
		title = message.embeds[0].title or ""
		title_upper = title.upper()  # make case-insensitive
		allText = allText+title_upper
		allText = allText+message.embeds[0].description

	allText = allText.replace(" ", "")
	allText = allText.replace("-", "")
	allText = allText.replace("!", "")
	allText = allText.replace("@", "")
	allText = allText.replace("^", "")
	allText = allText.replace("`", "")
	
	matched_keywords = [word for word in KEYWORDS if word in allText.upper()]
	matched_blacklist = [word for word in BLACKLIST if word in allText.upper()]

	if matched_keywords and not matched_blacklist:
		toast.show_toast("Biome Sniper", "Joining "+str(matched_keywords), duration=5, threaded=True)
		shareUrl = allText.split("www.roblox.com/share")[1].split("=Server")[0]
		deeplink = resolve_share_link("https://www.roblox.com/share"+shareUrl+"=Server")
		#deeplink = deeplink.replace("roblox://", "ms-xbl-681f8096://")
		print("Joining: "+deeplink)
		webbrowser.open(deeplink)

class CustomClient(selfcord.Client):
	async def on_ready(self):
		toast.show_toast("Biome Sniper", "Logged in as "+str(self.user), duration=5, threaded=True)
		print("Logged in as", self.user)
	async def on_message(self, message):
		if not message.guild:
			return
		if not message.channel:
			return
		if not message.guild.id in target_guilds:
			return
		if not message.channel.id in target_channels:
			return
		await handle_message(message)

def start():
	client = CustomClient()
	client.run(TOKEN)

start()