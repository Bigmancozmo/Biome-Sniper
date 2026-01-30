# A lot of this code was from another project and just shoved into here
# So ignore a lot of the stuff
# such as:
#
# KEYWORDS = [...]
# keywords = []
# .....
# KEYWORDS = keywords


try:
	print("Importing packages, this may take a moment if it's your first time running the script.")

	import os
	import sys
	sys.stdout.reconfigure(encoding='utf-8')
	import dataMgr as d
	import time, threading
	import requests
	import datetime

	PAUSED = False

	def pause_for(dur):
		global PAUSED
		PAUSED = True
		time.sleep(dur)
		PAUSED = False

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
	if(d.get_key("KEYWORD_Hell", False)):
		keywords.append("HELL")
	if(d.get_key("KEYWORD_Windy", False)):
		keywords.append("WIND")
	if(d.get_key("KEYWORD_Rainy", False)):
		keywords.append("RAIN")
	#if(d.get_key("KEYWORD_Snowy", False)): # TODO: Enable after winter event
	#	keywords.append("SNOW")
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

	DONTSNIPE_MARKER = "HIMACROPLSDONTSNIPETHIS"
	blacklist = ["ENDED", "FAKE", "BAIT", "OVER", "HEAVENLY", DONTSNIPE_MARKER]

	print(keywords)

	ALTERNATE_SHARE_RESOLVER = True

	def resolve_share_link(share_url):
		if "privateServerLinkCode" in share_url:
			split1 = share_url.split("LinkCode=")[1]
			return f"roblox://placeId=15532962292&linkCode={split1}"
		else:
			split1 = share_url.split("?code=")[1]
			split2 = split1.split("&type")[0]
			if ALTERNATE_SHARE_RESOLVER:
				req = requests.get(f"https://bmc-sniper-aa5f1gef.vercel.app/resolve/{split2}")
				return f"roblox://placeId=15532962292&linkCode={req.text}"
			else:
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

		matched_keywords = [word for word in keywords if word in allText.upper()]
		matched_blacklist = [word for word in blacklist if word in allText.upper()]

		if matched_keywords and not matched_blacklist:
			if PAUSED:
				print("It's paused buddy")
				if "GLIT" in matched_keywords or "CYBER" in matched_keywords or "DREAM" in matched_keywords:
					print("BUT I WILL BYPASS ITTTTT")
				else:
					return
			print("Matched keywords")
			sendNotif = False
			try:
				deeplink = resolve_share_link(getLink(allText))
				#deeplink = deeplink.replace("roblox://", "roblox-player://")
				if sys.platform == "win32":
					print("OPENING WITH WIN32")
					os.startfile(deeplink)
				else:
					print("OPENING WITH WEB BROWSER")
					webbrowser.open(deeplink)
				sendNotif = True
			except Exception as e:
				print("No PS link found, but saw " + str(matched_keywords), f'({message.guild.id}/{message.channel.id})')
				print(allText)
				print("Proper error:", e)
			if sendNotif:
				print("Sniped " + str(matched_keywords))
				ducknotify.notify("Biome Sniper", "Joining "+str(matched_keywords) +", will pause for 120 seconds")
				t = threading.Thread(target=pause_for, args=(120,))
				t.start()
			try:
				url = d.get_key('WebhookURL', None)

				images = {
					"MARI": "/merchants/Mari.png",
					"JEST": "/merchants/Jester.png",
					"SAND": "/biomes/SAND STORM.png",
					"SANDSTORM": "/biomes/SAND STORM.png",
					"SAND STORM": "/biomes/SAND STORM.png",
					"AURORA": "/biomes/AURORA.png",
					"HEAV": "/biomes/HEAVEN.png",
					"HELL": "/biomes/HELL.png",
					"WIND": "/biomes/WINDY.png",
					"RAIN": "/biomes/RAINY.png",
					"STARF": "/biomes/STARFALL.png",
					"CORRUP": "/biomes/CORRUPTION.png",
					"NULL": "/biomes/NULL.png",
					"GLIT": "/biomes/GLITCHED.png",
					"DREAM": "/biomes/DREAMSPACE.png",
					"CYBER": "/biomes/CYBERSPACE.png",
					"VOID": "/merchants/Mari.png",
					"OBLIV": "/merchants/Jester.png",
				}

				# only displayed in webhook embed
				fullNames = {
					"MARI": "MARI",
					"JEST": "JESTER",
					"SAND": "SAND STORM",
					"SANDSTORM": "SAND STORM",
					"SAND STORM": "SAND STORM",
					"AURORA": "AURORA",
					"HEAV": "HEAVEN",
					"HELL": "HELL",
					"WIND": "WINDY",
					"RAIN": "RAINY",
					"STARF": "STARFALL",
					"CORRUP": "CORRUPTION",
					"NULL": "NULL",
					"GLIT": "GLITCHED",
					"DREAM": "DREAMSPACE",
					"CYBER": "CYBERSPACE",
					"VOID": "VOID COIN",
					"OBLIV": "OBLIVION POTION",
				}

				payload = {"embeds": [
        		{
            		"title": "Sniped link",
            		"description": f"# {fullNames.get(matched_keywords[0], 'idk')}\n"+
					f"- **Guild:** {message.guild.name}\n"+
					f"- **Channel:** #{message.channel.name}\n"+
					f"{getLink(allText)}\n"+
					f"-# ||{DONTSNIPE_MARKER}||\n",
            		"timestamp": datetime.datetime.now().isoformat(),
            		"footer": {"text": "BMC's Biome Sniper"},
        		}]}

				if images.get(matched_keywords[0]):
					payload["embeds"][0]["thumbnail"] = {"url": "https://keylens-website.web.app"+images[matched_keywords[0]]}

				if url is not None and url != "" and url.startswith("http"):
					requests.request("POST", url, json=payload, headers={
						"Content-Type": "application/json",
						"User-Agent": "insomnia/11.2.0"
					})

			except Exception as e:
				print("Error sending webhook message:", e)

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
except:
	import shutil, os
	def experimentalPatch(folder):
		print("Cleaning", folder)
		for f in os.listdir(folder):
			if "discord" in f.lower():
				p = os.path.join(folder, f)
				shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
	import site
	selection = input("Something went wrong. Apply experimental fix? (y/n): ")
	if selection == "y":
		print("Applying... this may take a moment")
		time.sleep(1)
		sitePackages = site.getsitepackages()
		for dir in sitePackages:
			experimentalPatch(dir)
		print("Reinstalling...")
		os.system("pip install -U discord.py-self")
		time.sleep(1)
		input("Fix applied!\nYou'll need to restart the script.\nPress enter to continue")