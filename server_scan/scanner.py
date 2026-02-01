from concurrent.futures import ThreadPoolExecutor
import requests
import dataMgr as d
from logging import warning as warn
import sys, util, os
import urllib.request

# Set this environment variable to disable the auto updater in that directory
value = os.environ.get("BIOME_SNIPER_DEV_FOLDER")
if value:
	value = value.upper()
else:
	value = "NoFolder"
folder = os.path.dirname(os.path.abspath(__file__)).upper()

if value in folder:
	print("Skipping blacklist update")
else:
	print("Updating blacklist...")
	urllib.request.urlretrieve(
		"https://raw.githubusercontent.com/Bigmancozmo/Biome-Sniper/main/server_scan/blacklist.py",
		"server_scan/blacklist.py"
	)
	print("Blacklist download complete")

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

	if PROGRESS_CALLBACK:
		PROGRESS_CALLBACK(PROGRESS, TOTAL)

	if channel["type"] != 0:
		return
	if channel["parent_id"] != None:
		if channel["parent_id"] in BLACKLIST_CATEGORIES:
			return
	if channel["id"] in BLACKLIST_CHANNELS or channel["id"] in BLACKLIST_CATEGORIES:
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
		print(f"{channelName} passed: {linkMessages}/5")
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
	DEBUG_MODE = False
	if DEBUG_MODE:
		# Slow, but logs errors
		for channel in channels:
			processChannel(channel)
	else:
		# Fast, but doesn't log errors
		print("Go my minions")
		with ThreadPoolExecutor(max_workers=50) as pool:
			pool.map(processChannel, channels)
	if COMPLETE_CALLBACK:
		COMPLETE_CALLBACK()
