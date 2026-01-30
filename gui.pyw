import os, sys
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import dataMgr as d
import updater

from PIL import Image, ImageTk

import tabs.targets
import tabs.discordToken
import tabs.servers
import tabs.settings
import tabs.webhook

def start():
	root = Tk()
	root.title("BMC's Biome Sniper - " + updater.CURRENT)
	root.resizable(False, False)
	
	if sys.platform == "win32":
		try:
			import sv_ttk
		except:
			os.system("pip install sv-ttk")
		import sv_ttk
		sv_ttk.set_theme("dark")

	icon = Image.open("icon.png")
	photo = ImageTk.PhotoImage(icon)
	root.wm_iconphoto(False, photo)

	notebook = ttk.Notebook(root)
	notebook.pack(fill="both", expand=True)

	tabs.targets.create(notebook)
	tabs.discordToken.create(notebook)
	tabs.servers.create(notebook, root)
	#tabs.settings.create(notebook)
	tabs.webhook.create(notebook)

	def start_macro():
		root.destroy()
		os.system("py internals.py")

	btn = ttk.Button(root, text="Start Sniping", command=start_macro)
	btn.pack(pady=10)

	#mainframe.pack()
	root.update_idletasks() # calculate sizes
	root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}") # auto-fit
	root.mainloop()

if updater.update_available():
	if os.path.exists('apply-update.py'):
		os.remove('apply-update.py')
	print("An update is available")
	os.system('py -c "import updater; updater.update()"')
else:
	if os.path.exists('apply-update.py'):
		os.remove('apply-update.py')
	start()