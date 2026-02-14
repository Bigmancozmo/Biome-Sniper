try:
	print("Importing packages, this may take a moment if it's your first time running the script.")

	import os
	import sys
	import dataMgr as d
	import time, threading
	import requests
	import datetime
	import util
	import json

	sys.stdout.reconfigure(encoding='utf-8')

	with open("snipe_map.json", "r") as f:
		KEYWORD_MAP = json.load(f)

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
		os.system(f"{sys.executable} -m pip install -U discord.py-self")

	try:
		import ducknotify
	except:
		print("Installing Ducknotify...")
		os.system(f"{sys.executable} -m pip install ducknotify")

	try:
		import requests
	except:
		print("Installing Requests...")
		os.system(f"{sys.executable} -m pip install requests")

	import discord, requests, webbrowser
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

	for keyword in KEYWORD_MAP:
		data = util.getKeywordInfo(keyword)
		if d.get_key(data["key"], False):
			for kwd in data["words"]:
				keywords.append(kwd)

	TOKEN = d.get_key("DiscordToken", "")
	blacklist = ["ENDED", "FAKE", "BAIT", "OVER", "HEAVENLY"]

	print(keywords)

	ALTERNATE_SHARE_RESOLVER = d.get_key("SETTINGS_AltLinkResolver", True)

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
		try:
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
		except:
			return "Link Not Found"

	async def handle_message(message):
		allText = util.extractText(message, True)
		noUrl = allText.replace(getLink(allText), "")

		if "Guild:" in allText and "Channel:" in allText and "BMC's Sniper" in allText and "Sniped link" in allText:
			return

		matched_keywords = [word for word in keywords if word in noUrl.upper()]
		matched_blacklist = [word for word in blacklist if word in noUrl.upper()]

		if matched_keywords and not matched_blacklist:
			if PAUSED:
				print("Saw", matched_keywords, "but the macro is paused")
				if "GLIT" in matched_keywords or "CYBER" in matched_keywords or "DREAM" in matched_keywords:
					print("Rare biome detected, bypassing pause")
				else:
					return
			print("Matched keywords")
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
				print("An error occurred:", e)
			if sendNotif:
				print("Sniped " + str(matched_keywords))
				ducknotify.notify("Biome Sniper", "Joining "+str(matched_keywords) +", will pause for 120 seconds")
				t = threading.Thread(target=pause_for, args=(120,))
				t.start()
			try:
				url = d.get_key('WebhookURL', None)
				kwdData = util.getKeywordDataFromKeyword(matched_keywords[0])

				payload = {
					"embeds": [
						{
							"title": "Sniped link",
							"description": f"# {kwdData["name"]}\n"+
							f"- **Guild:** {message.guild.name}\n"+
							f"- **Channel:** #{message.channel.name}\n"+
							f"{getLink(allText)}\n",
							"timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
							"footer": {"text": "BMC's Sniper"},
						}
					]
				}

				payload["embeds"][0]["thumbnail"] = {"url": "https://keylens-website.web.app"+kwdData["image"]}

				if url is not None and url != "" and url.startswith("http"):
					requests.request("POST", url, json=payload, headers={
						"Content-Type": "application/json",
						"User-Agent": "insomnia/11.2.0"
					})

			except Exception as e:
				print("Error sending webhook message:", e)

	class CustomClient(discord.Client):
		async def on_ready(self):
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
except Exception as e:
	import shutil, os
	def experimentalPatch(folder):
		print("Cleaning", folder)
		for f in os.listdir(folder):
			if "discord" in f.lower():
				p = os.path.join(folder, f)
				shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
	import site
	print(e)
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