from tkinter import *
from tkinter import ttk
import dataMgr as d


def create(notebook: ttk.Notebook):
	settingsFrame = ttk.Frame(notebook, padding=(10,10,10,10))
	notebook.add(settingsFrame, text="Settings")
	ttk.Label(settingsFrame, text="Customize some of the sniper's behavior")

	def settingFrame():
		frame = ttk.Frame(settingsFrame)
		frame.pack(pady=3, fill="x")
		#frame.pack_propagate(False)
		return frame

	def boolSetting(name, info, key, default):
		sKey = f"SETTINGS_{key}"
		val = d.get_key(sKey, default)
		frame = settingFrame()
		
		toggleValue = BooleanVar(value=val)
		frame.toggleValue = toggleValue
		toggle = ttk.Checkbutton(frame, variable=toggleValue, text=name)
		toggle.pack()

		def on_change(*args):
			d.set_key(sKey, toggleValue.get())
		
		toggleValue.trace_add("write", on_change)
	
	boolSetting(
		"Alternate Link Resolver",
		"!! Disable if you dare !!\nSends share links through my custom\nAPI, because Roblox doesn't like to\njoin them sometimes.",
		"AltLinkResolver",
		True
	)

	boolSetting(
		"Custom Theme",
		"Makes the UI look pretty.\nAlso makes it more laggy",
		"SunValleyTheme",
		True
	)

	boolSetting(
		"Dark Theme",
		"Only works if Custom Theme is enabled.",
		"SV_DarkMode",
		True
	)
