import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import dataMgr as d
import updater

def start():
	root = Tk()
	root.geometry("500x690")
	root.title("Sol's RNG PS Sniper")

	mainframe = ttk.Frame(root, padding=(10,10,10,10))

	ttk.Label(mainframe, text="-------------------- Message Keywords --------------------").pack()

	def add_keyword_toggle(dataKey, dText, default=False):
		snipe_void_coin = BooleanVar(value=d.get_key(dataKey, default))
		checkbox = ttk.Checkbutton(mainframe, text=dText, variable=snipe_void_coin)
		checkbox.pack()

		def void_coin_changed(*args):
			d.set_key(dataKey, snipe_void_coin.get())

		snipe_void_coin.trace_add("write", void_coin_changed)

	add_keyword_toggle("KEYWORD_VoidCoin", "Void Coin", True)
	add_keyword_toggle("KEYWORD_Mari", "Mari")
	add_keyword_toggle("KEYWORD_Jest", "Jester", True)
	add_keyword_toggle("KEYWORD_Obliv", "Oblivion Potion")
	add_keyword_toggle("KEYWORD_SandStorm", "Sand Storm")
	add_keyword_toggle("KEYWORD_Heaven", "Heaven")
	add_keyword_toggle("KEYWORD_Starfall", "Starfall")
	add_keyword_toggle("KEYWORD_Aurora", "Aurora")
	add_keyword_toggle("KEYWORD_Corruption", "Corruption")
	add_keyword_toggle("KEYWORD_Null", "Null")
	add_keyword_toggle("KEYWORD_GLIT", "GLITCHED", True)
	add_keyword_toggle("KEYWORD_DREAM", "DREAMSPACE", True)
	add_keyword_toggle("KEYWORD_CYBER", "CYBERSPACE", True)

	ttk.Label(mainframe, text="-------------------- Discord Token --------------------").pack()
	ttk.Label(mainframe, text="Do NOT share this!").pack()
	ttk.Label(mainframe, text="It can be used to bypass 2FA and get in your Discord account.").pack()
	discord_token_val = StringVar(value=d.get_key("DiscordToken", ""))
	token_input = ttk.Entry(mainframe, textvariable=discord_token_val, show="•")
	token_input.pack()

	treeview = ttk.Treeview(mainframe, columns=("Note"))
	treeview.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

	treeview.heading("#0", text="Server/Channel ID")
	treeview.heading("Note", text="Note")

	treeviewData = d.get_key("treeview", {
		"1186570213077041233": {
			"note": "Sol's RNG Discord",
			"children": {
				"1282542323590496277": "#biomes",
				"1282543762425516083": "#merchants"
			}
		}
	})

	def load_treeview():
		for rootName in treeviewData:
			rootData = treeviewData[rootName]
			root = treeview.insert("", tk.END, text=rootName, value=(rootData["note"],))
			for childName in rootData["children"]:
				childNote = rootData["children"][childName]
				treeview.insert(root, tk.END, text=childName, value=(childNote,))

	load_treeview()

	frame = ttk.Frame(mainframe)
	frame.pack(fill=tk.X)

	################################################

	addEntryPlaceholder = "Server/Channel ID"
	addEntryVar = tk.StringVar(value=addEntryPlaceholder)

	addEntry = ttk.Entry(frame, textvariable=addEntryVar, foreground="grey")
	addEntry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

	def focus_in(e):
		if addEntryVar.get() == addEntryPlaceholder:
			addEntryVar.set("")
			addEntry.config(foreground="black")

	def focus_out(e):
		if addEntryVar.get() == "":
			addEntryVar.set(addEntryPlaceholder)
			addEntry.config(foreground="grey")

	addEntry.bind("<FocusIn>", focus_in)
	addEntry.bind("<FocusOut>", focus_out)

	################################################

	noteEntryPlaceholder = "Note"
	noteEntryVar = tk.StringVar(value=noteEntryPlaceholder)

	noteEntry = ttk.Entry(frame, textvariable=noteEntryVar, foreground="grey")
	noteEntry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

	def focus_in(e):
		if noteEntryVar.get() == noteEntryPlaceholder:
			noteEntryVar.set("")
			noteEntry.config(foreground="black")

	def focus_out(e):
		if noteEntryVar.get() == "":
			noteEntryVar.set(noteEntryPlaceholder)
			noteEntry.config(foreground="grey")

	noteEntry.bind("<FocusIn>", focus_in)
	noteEntry.bind("<FocusOut>", focus_out)

	################################################

	selectedServer = ""

	def add_server():
		if not addEntryVar.get().isdigit():
			return
		name = addEntryVar.get()
		exists = False

		for root in treeview.get_children():
			if treeview.item(root, "text") == name:
				exists = True
				break

			for child in treeview.get_children(root):
				if treeview.item(child, "text") == name:
					exists = True
					break
		if exists:
			messagebox.showwarning("Can't add", f"Server/Channel with ID '{addEntryVar.get()}' already exists")
			return
		treeview.insert("", tk.END, text=addEntryVar.get(), value=(noteEntryVar.get(),))
		save_treeview()

	def add_channel():
		if not addEntryVar.get().isdigit():
			return
		name = addEntryVar.get()
		exists = False

		for root in treeview.get_children():
			if treeview.item(root, "text") == name:
				exists = True
				break

			for child in treeview.get_children(root):
				if treeview.item(child, "text") == name:
					exists = True
					break
		if exists:
			messagebox.showwarning("Can't add", f"Server/Channel with ID '{addEntryVar.get()}' already exists")
			return
		treeview.insert(selectedServer, tk.END, text=addEntryVar.get(), value=(noteEntryVar.get(),))
		treeview.item(selectedServer, open=True)
		save_treeview()

	addServerBtn = ttk.Button(frame, text="Add Server", command=add_server)
	addServerBtn.pack(side=tk.LEFT)

	addChannelBtn = ttk.Button(frame, text="Add Channel", command=add_channel)
	addChannelBtn.pack(side=tk.LEFT)
	addChannelBtn.state(["disabled"])

	def discord_token_changed(*args):
		d.set_key("DiscordToken", discord_token_val.get())
	discord_token_val.trace_add("write", discord_token_changed)

	def start_macro():
		root.destroy()
		os.system("python internals.py")

	def save_treeview():
		data = {}
		for root in treeview.get_children():
			item = treeview.item(root)
			itemData = {}
			childrenData = {}
			for child in treeview.get_children(root):
				childItem = treeview.item(child)
				childrenData[childItem["text"]] = childItem["values"][0]
			itemData["note"] = item["values"][0]
			itemData["children"] = childrenData
			data[item["text"]] = itemData
		d.set_key("treeview", data)

	menu = tk.Menu(root, tearoff=0)

	def show_menu(event):
		item = treeview.identify_row(event.y)
		if item:
			treeview.selection_set(item)
			menu.post(event.x_root, event.y_root)

	def remove_selected():
		for item in treeview.selection():
			treeview.delete(item)
		save_treeview()

	menu.add_command(label="Remove", command=remove_selected)
	treeview.bind("<Button-3>", show_menu)

	def on_click(event):
		global selectedServer
		item = treeview.identify_row(event.y)
		if item:
			parent = treeview.parent(item)
			parent_text = treeview.item(parent)["text"] if parent else "Root"
			#print("Clicked:", treeview.item(item)["text"], "| Note:", treeview.item(item)["values"], "| Parent:", parent_text)
			if parent_text == "Root":
				addChannelBtn.state(["!disabled"])
				selectedServer = item
			else:
				addChannelBtn.state(["disabled"])

	treeview.bind("<Button-1>", on_click)  # Left click


	btn = ttk.Button(mainframe, text="Start Macro", command=start_macro)
	btn.pack()

	mainframe.pack()
	root.mainloop()

if updater.update_available():
	if os.path.exists('apply-update.py'):
		os.remove('apply-update.py')
	print("An update is available")
	os.system('python -c "import updater; updater.update()"')
else:
	if os.path.exists('apply-update.py'):
		os.remove('apply-update.py')
	start()