from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import dataMgr as d
import sys, os

def apply(root):
	s = ttk.Style()
	print(f"Available themes: {s.theme_names()}")

	SunValleyTheme = d.get_key("SETTINGS_SunValleyTheme", True)
	SunValleyDark = d.get_key("SETTINGS_SV_DarkMode", True)
	
	if sys.platform == "win32":
		if SunValleyTheme:
			try:
				import sv_ttk
			except:
				os.system("pip install sv-ttk")
			import sv_ttk
			sv_ttk.set_theme("dark" if SunValleyDark else "light")
		else:
			s.theme_use("alt")
	
	root.update_idletasks() # calculate sizes
	root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}") # auto-fit

def create(notebook: ttk.Notebook, root):
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

		inner = ttk.Frame(frame)  # container for toggle + button
		inner.pack(fill="x")

		toggle = ttk.Checkbutton(inner, variable=toggleValue, text=name)
		toggle.pack(side="left")

		def view_info():
			messagebox.showinfo(f"{name} Info", info)

		btn = ttk.Button(inner, text="View Info", command=view_info)
		btn.pack(side="right")

		def on_change(*args):
			d.set_key(sKey, toggleValue.get())
			apply(root)
			if (not toggleValue.get()) and key == "SunValleyTheme":
				messagebox.showinfo("Restart", "You may need to restart the program\nto fully apply the new theme.")

		toggleValue.trace_add("write", on_change)
	
	boolSetting(
		"Alternate Link Resolver",
		"!! Disable if you dare !!\nSends share links through my custom\nAPI, because Roblox doesn't like to\njoin them sometimes.\nIf the sniper ISN'T joining links, try enabling it.",
		"AltLinkResolver",
		True
	)

	boolSetting(
		"Custom Theme",
		"(WINDOWS ONLY)\nMakes the UI look pretty.\nAlso makes it more laggy\nDisable if you need the script's GUI\nto run faster.",
		"SunValleyTheme",
		True
	)

	boolSetting(
		"Dark Theme (requires Custom Theme)",
		"(WINDOWS ONLY)\nOnly works if Custom Theme is enabled.",
		"SV_DarkMode",
		True
	)

	apply(root)
