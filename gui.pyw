import os, sys, webbrowser
from tkinter import *
from tkinter import ttk
import updater

from PIL import Image, ImageTk

import tabs.targets
import tabs.discordToken
import tabs.servers
import tabs.settings
import tabs.webhook

DISCORD = "https://discord.gg/tVVghYhTX8"

def start():
	root = Tk()
	root.title("BMC's Biome Sniper - " + updater.CURRENT)
	root.resizable(False, False)
	
	container = ttk.Frame(root)
	container.pack()

	tabs.settings.apply(root)

	icon = Image.open("icon.png")
	photo = ImageTk.PhotoImage(icon)
	root.wm_iconphoto(False, photo)

	notebook = ttk.Notebook(container)
	notebook.pack(fill="both", expand=True)

	tabs.targets.create(notebook)
	tabs.discordToken.create(notebook)
	tabs.servers.create(notebook)
	tabs.webhook.create(notebook)
	tabs.settings.create(notebook, root)

	def start_macro():
		root.destroy()
		os.system(f"{sys.executable} internals.py")

	discordLink = ttk.Label(container, text="Join Discord", cursor="hand2")
	discordLink.pack(padx=10, pady=10, side=LEFT)
	discordLink.bind("<Button-1>", lambda e: webbrowser.open(DISCORD))

	btn = ttk.Button(container, text="Start Sniper", command=start_macro)
	btn.pack(pady=10, padx=10, side=RIGHT)

	#mainframe.pack()
	root.update_idletasks() # calculate sizes
	root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}") # auto-fit
	root.mainloop()

if updater.update_available():
	if os.path.exists('apply-update.py'):
		os.remove('apply-update.py')
	print("An update is available")
	os.system(f'{sys.executable} -c "import updater; updater.update()"')
else:
	if os.path.exists('apply-update.py'):
		os.remove('apply-update.py')
	start()