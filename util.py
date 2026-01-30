import discord

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
				message["embeds"].append({
					"title": embed.title,
					"description": embed.description
				})
		
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
						newComp["children"] = newChild
				message["components"].append(newComp)

		return message

def extractText(messageInput, filter=False):
	message = convertMessageToDict(messageInput)
	allText = ""
	if "content" in message:
		allText = allText + message["content"]
	if "embeds" in message:
		for embed in message["embeds"]:
			allText = allText + str(embed["title"])
			allText = allText + str(embed["description"])
	if "components" in message:
		# For MultiScope 2.0.0
		# embeds have a "Join Server" button rather than a link.
		# I dont know if MS2 uses ActionRow or Button so I just check both
		for component in message["components"]:
			if component.type == discord.ComponentType.button:
				allText = allText + component["url"]
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