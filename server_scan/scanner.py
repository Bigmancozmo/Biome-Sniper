from concurrent.futures import ThreadPoolExecutor
import requests
import dataMgr as d
from logging import warning as warn
import sys, util
from server_scan.blacklist import BLACKLIST_CHANNELS, BLACKLIST_CATEGORIES

sys.stdout.reconfigure(encoding="utf-8")

def getHeaders():
	token = d.get_key("DiscordToken", "")
	return {"Authorization": token}

TOTAL = 999
PROGRESS = 0
CALLBACK = None
COMPLETE_CALLBACK = None
PROGRESS_CALLBACK = None

def setHitCallback(cb):
	global CALLBACK
	CALLBACK = cb

def setProgressCallback(cb):
	global PROGRESS_CALLBACK
	PROGRESS_CALLBACK = cb

def setCompleteCallback(cb):
	global COMPLETE_CALLBACK
	COMPLETE_CALLBACK = cb

def processChannel(channel):
	global TOTAL, PROGRESS, CALLBACK, PROGRESS_CALLBACK
	PROGRESS += 1
	print(f"Channel {PROGRESS}/{TOTAL} ({channel["name"]})")

	if PROGRESS_CALLBACK:
		PROGRESS_CALLBACK(PROGRESS, TOTAL)

	if channel["type"] != 0:
		return
	if channel["parent_id"] != None:
		if channel["parent_id"] in BLACKLIST_CATEGORIES:
			warn(f"Category {channel["parent_id"]} is blacklisted!")
			return
	if channel["id"] in BLACKLIST_CHANNELS or channel["id"] in BLACKLIST_CATEGORIES:
		warn(f"Channel {channel["id"]} is blacklisted!")
		return
	
	channelId = channel["id"]
	channelName = channel["name"]
	endpoint = f"https://discord.com/api/v9/channels/{channelId}/messages?limit=5"
	r = requests.get(endpoint, headers=getHeaders())
	linkMessages = 0
	if r.status_code != 200:
		warn(f"No permission: {channelId} ({r.status_code}) Category={channel["parent_id"]} Name={channel["name"]}")
		return
	for msg in r.json():
		if util.hasLink(msg):
			linkMessages += 1
		if linkMessages >= 2:
			break
	if linkMessages >= 2:
		if CALLBACK:
			CALLBACK(channelId, channelName)

def scanServer(serverId):
	global TOTAL, PROGRESS
	TOTAL = 1
	PROGRESS = 0
	endpoint = f"https://discord.com/api/v10/guilds/{serverId}/channels"
	r = requests.get(endpoint, headers=getHeaders())
	if r.status_code != 200:
		warn(f"Failed to find channels for server {serverId}")
		return
	channels = r.json()
	TOTAL = len(channels)
	with ThreadPoolExecutor(max_workers=10) as pool:
		pool.map(processChannel, channels)
	if COMPLETE_CALLBACK:
		COMPLETE_CALLBACK()
