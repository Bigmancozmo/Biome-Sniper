import discord, json

def getKeywordInfo(kwd):
	with open("snipe_map.json", "r") as f:
		KEYWORD_MAP = json.load(f)
	if kwd in KEYWORD_MAP:
		dta = KEYWORD_MAP[kwd]
		return {
			"name": kwd,
			"key": dta["key"],
			"words": dta["words"],
			"image": dta["image"]
		}
	else:
		return {
			"name": "ULTRA RARE ERROR BIOME",
			"key": "SomethingWentWrongLilBro",
			"words": [],
			"image": "/biomes/UnknownBiome.png"
		}

def getKeywordDataFromKeyword(match):
	with open("snipe_map.json", "r") as f:
		KEYWORD_MAP = json.load(f)
	found = "FailedToFind"
	for name in KEYWORD_MAP:
		if match in KEYWORD_MAP[name]["words"]:
			found = name
			break
	return getKeywordInfo(found)

# It scares me but it works so who gaf
def convertMessageToDict(msgIn):
	if isinstance(msgIn, dict):
		return msgIn
	else:
		message = {}
		
		if msgIn.content:
			message["content"] = msgIn.content

		if msgIn.embeds:
			message["embeds"] = []
			for embed in msgIn.embeds:
				dta = {
					"title": "",
					"description": "",
					"footer": ""
				}
				if embed.title:
					dta["title"] = embed.title
				if embed.description:
					dta["description"] = embed.description
				if embed.footer:
					dta["footer"] = embed.footer.text
				if embed.fields:
					# I'm too lazy to add extra code for this
					# so i just append it to description
					for field in embed.fields:
						if field.name:
							dta["title"] = dta["title"] + field.name
						if field.value:
							dta["title"] = dta["title"] + field.value

				message["embeds"].append(dta)
		
		if msgIn.components:
			message["components"] = []
			for component in msgIn.components:
				newComp = {}
				newComp["type"] = component.type
				if component.type == discord.ComponentType.button:
					newComp["url"] = component.url
				else:
					if component.type == discord.ComponentType.action_row:
						newChildren = []
						for action in component.children:
							newChild = {}
							newChild["type"] = action.type
							if action.type == discord.ComponentType.button:
								newChild["url"] = action.url
							newChildren.append(newChild)
						newComp["children"] = newChildren
				message["components"].append(newComp)

		return message

def extractText(messageInput, filter=False):
	message = convertMessageToDict(messageInput)
	allText = ""
	if "content" in message:
		allText = allText + message["content"]
	if "embeds" in message:
		for embed in message["embeds"]:
			if "title" in embed:
				allText = allText + str(embed["title"])
			if "description" in embed:
				allText = allText + str(embed["description"])
			if "footer" in embed:
				allText = allText + str(embed["footer"])
	if "components" in message:
		# For MultiScope 2.0.0
		# embeds have a "Join Server" button rather than a link.
		# I dont know if MS2 uses ActionRow or Button so I just check both
		for component in message["components"]:
			if component["type"] == discord.ComponentType.button:
				allText = allText + component["url"]
			else:
				if component["type"] == discord.ComponentType.action_row:
					for action in component["children"]:
						if action["type"] == discord.ComponentType.button:
							allText = allText + action["url"]
	
	if filter:
		allText = allText.replace(" ", "")
		allText = allText.replace("-", "")
		allText = allText.replace("!", "")
		allText = allText.replace("@", "")
		allText = allText.replace("^", "")
		allText = allText.replace("`", "")

	return allText

def hasLink(message):
	text = extractText(message)
	if ("roblox.com/games/15532962292" in text) or ("roblox.com/share" in text):
		return True
	return False