# A lot of this code was from another project and just shoved into here
# So ignore a lot of the stuff
# such as:
#
# KEYWORDS = [...]
# keywords = []
# .....
# KEYWORDS = keywords

print("Importing packages, this may take a moment if it's your first time running the script.")

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import dataMgr as d

try:
	import discord
except:
	print("Installing Selfcord...")
	os.system("pip install -U discord.py-self")

try:
	import ducknotify
except:
	print("Installing Ducknotify...")
	os.system("python -m pip install ducknotify")

try:
	import requests
except:
	print("Installing Requests...")
	os.system("python -m pip install requests")

try:
	import urllib
except:
	print("Installing Urllib...")
	os.system("python -m pip install urllib")

from urllib.parse import urlparse, parse_qs, unquote
import discord, asyncio, requests, webbrowser
import ducknotify

print("Done")

target_guilds = []
target_channels = []

treeview_data = d.get_key("treeview", {})
for rootName in treeview_data:
	target_guilds.append(rootName)
	for childName in treeview_data[rootName]["children"]:
		target_channels.append(childName)

PRIVATE_SERVER_BASE = "https://www.roblox.com/games/15532962292/Sols-RNG-Eon-1-8?privateServerLinkCode="

# your discord token
TOKEN = "ImNotGivingYouMyTokenBuddy"

keywords = []

'''with sync_playwright() as p:
    url = p.chromium.launch(headless=True).new_page().goto("https://www.roblox.com/share?code=1c18d2fc5d6e304c868704571a5804c2&type=Server")
    page = p.chromium.launch(headless=True).new_page()
    page.goto("YOUR_SHARE_URL")
    page.wait_for_url("**LinkCode=**")
    print(page.url)'''

if(d.get_key("KEYWORD_VoidCoin", False)):
    keywords.append("VOID")
if(d.get_key("KEYWORD_Mari", False)):
    keywords.append("MARI")
if(d.get_key("KEYWORD_Jest", False)):
    keywords.append("JEST")
if(d.get_key("KEYWORD_Obliv", False)):
    keywords.append("OBLIV")
if(d.get_key("KEYWORD_SandStorm", False)):
    keywords.append("SAND")
    keywords.append("SANDSTORM")
    keywords.append("SAND STORM")
if(d.get_key("KEYWORD_Aurora", False)):
    keywords.append("AURORA")
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
if(d.get_key("KEYWORD_CYBER", False)):
    keywords.append("CYBER")

TOKEN = d.get_key("DiscordToken", "")

blacklist = ["ENDED", "FAKE", "BAIT", "OVER", "HEAVENLY"]

print(keywords)

def resolve_share_link(share_url):
	if "privateServerLinkCode" in share_url:
		split1 = share_url.split("LinkCode=")[1]
		return f"roblox://placeId=15532962292&linkCode={split1}"
	else:
		split1 = share_url.split("?code=")[1]
		split2 = split1.split("&type")[0]
		return f'roblox://navigation/share_links?code={split2}&type=Server'

def getLink(allText):
	split1 = allText.split("https://www.roblox.com")
	split1 = split1[len(split1)-1]
	final = split1
	
	if "privateServerLinkCode" in final:
		final = final.split("ServerLinkCode=")[1]
		final2 = ""
		for char in final:
			if char.isdigit():
				final2 = final2 + char
			else:
				break
		final = f"https://www.roblox.com/games/15532962292/join?privateServerLinkCode={final2}"
	else:
		final = final.split("?code=")[1].split("&type")[0]
		final = f'https://www.roblox.com/share?code={final}&type=Server'
	return final

async def handle_message(message):
	allText = ""
	
	if message.content:
		allText = allText + message.content
	if message.embeds:
		for embed in message.embeds:
			allText = allText + str(embed.title)
			allText = allText + str(embed.description)
	if message.components:
		# For MultiScope 2.0.0
		# embeds have a "Join Server" button rather than a link.
		# I dont know if MS2 uses ActionRow or Button so I just check both
		for component in message.components:
			if component.type == discord.ComponentType.button:
				allText = allText + action.url
			else:
				if component.type == discord.ComponentType.action_row:
					for action in component.children:
						if action.type == discord.ComponentType.button:
							allText = allText + action.url

	allText = allText.replace(" ", "")
	allText = allText.replace("-", "")
	allText = allText.replace("!", "")
	allText = allText.replace("@", "")
	allText = allText.replace("^", "")
	allText = allText.replace("`", "")
	
	print(allText)
	
	matched_keywords = [word for word in keywords if word in allText.upper()]
	matched_blacklist = [word for word in blacklist if word in allText.upper()]

	if matched_keywords and not matched_blacklist:
		sendNotif = False
		try:
			deeplink = resolve_share_link(getLink(allText))
			#deeplink = deeplink.replace("roblox://", "roblox-player://")
			if sys.platform == "win32":
				os.startfile(deeplink)
			else:
				webbrowser.open(deeplink)
			sendNotif = True
		except Exception as e:
			print("No PS link found, but saw " + str(matched_keywords), f'({message.guild.id}/{message.channel.id})')
			print(allText)
			print("Proper error:", e)
		if sendNotif:
			print("Sniped " + str(matched_keywords))
			ducknotify.notify("Biome Sniper", "Joining "+str(matched_keywords))

class CustomClient(discord.Client):
	async def on_ready(self):
		print("PRE log in")
		ducknotify.notify("Biome Sniper", "Logged in as "+str(self.user))
		print("Logged in as", self.user)
		print(self.get_channel(1423091592775864351))
	async def on_message(self, message):
		global target_channels
		global target_guilds
		if not message.guild:
			return
		if not message.channel:
			return
		if not str(message.guild.id) in target_guilds:
			return
		if not str(message.channel.id) in target_channels:
			return
		await handle_message(message)

def start():
	print("Target Servers:", target_guilds)
	print("Target Channels:", target_channels)
	client = CustomClient()
	client.run(TOKEN)

start()