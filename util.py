import discord

def extractText(message, filter=False):
	allText = ""
	if message["content"]:
		allText = allText + message["content"]
		if message["embeds"]:
			for embed in message["embeds"]:
				allText = allText + str(embed["title"])
				allText = allText + str(embed["description"])
		if message["components"]:
			# For MultiScope 2.0.0
			# embeds have a "Join Server" button rather than a link.
			# I dont know if MS2 uses ActionRow or Button so I just check both
			for component in message["components"]:
				if component.type == discord.ComponentType.button:
					allText = allText + action["url"]
				else:
					if component.type == discord.ComponentType.action_row:
						for action in component["children"]:
							if action.type == discord.ComponentType.button:
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