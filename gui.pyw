import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import dataMgr as d
import updater
import sv_ttk

import tabs.targets
import tabs.discordToken
import tabs.servers

def start():
	root = Tk()
	root.title("BMC's Biome Sniper - " + updater.CURRENT)
	root.resizable(False, False)
	sv_ttk.set_theme("dark")

	notebook = ttk.Notebook(root)
	notebook.pack(fill="both", expand=True)

	tabs.targets.create(notebook)
	tabs.discordToken.create(notebook)
	tabs.servers.create(notebook, root)

	def start_macro():
		root.destroy()
		os.system("python3 internals.py")

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
	os.system('python3 -c "import updater; updater.update()"')
else:
	if os.path.exists('apply-update.py'):
		os.remove('apply-update.py')
	start()