import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import dataMgr as d
import server_scan.scanner as scanner
import threading

def getForeground():
	darkMode = d.get_key("SETTINGS_SV_DarkMode", True) and d.get_key("SETTINGS_SunValleyTheme", True)
	if darkMode:
		return "white"
	return "black"

def create(notebook: ttk.Notebook):
	serversFrame = ttk.Frame(notebook, padding=(20,20,20,20))
	notebook.add(serversFrame, text="Servers")

	treeview = ttk.Treeview(serversFrame, columns=("Note"), height=7)
	treeview.pack(padx=10, pady=10, fill="both")

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

	################################################

	entryFrame = ttk.Frame(serversFrame, width=600)
	#entryFrame.pack_propagate(False)
	entryFrame.pack(fill="x", expand=True, pady=2)

	buttonFrame = ttk.Frame(serversFrame, width=600)
	#buttonFrame.pack_propagate(False)
	buttonFrame.pack(fill="x", expand=True, pady=2)

	addEntryPlaceholder = "Server/Channel ID"
	addEntryVar = tk.StringVar(value=addEntryPlaceholder)

	addEntry = ttk.Entry(entryFrame, textvariable=addEntryVar, foreground="grey", width=35)
	addEntry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

	def focus_in(e):
		if addEntryVar.get() == addEntryPlaceholder:
			addEntryVar.set("")
			addEntry.config(foreground=getForeground())

	def focus_out(e):
		if addEntryVar.get() == "":
			addEntryVar.set(addEntryPlaceholder)
			addEntry.config(foreground="grey")

	addEntry.bind("<FocusIn>", focus_in)
	addEntry.bind("<FocusOut>", focus_out)

	################################################

	noteEntryPlaceholder = "Note"
	noteEntryVar = tk.StringVar(value=noteEntryPlaceholder)

	noteEntry = ttk.Entry(entryFrame, textvariable=noteEntryVar, foreground="grey", width=35)
	noteEntry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

	def focus_in(e):
		if noteEntryVar.get() == noteEntryPlaceholder:
			noteEntryVar.set("")
			noteEntry.config(foreground=getForeground())

	def focus_out(e):
		if noteEntryVar.get() == "":
			noteEntryVar.set(noteEntryPlaceholder)
			noteEntry.config(foreground="grey")

	noteEntry.bind("<FocusIn>", focus_in)
	noteEntry.bind("<FocusOut>", focus_out)

	################################################

	selectedServer = ""
	lastSelected = ""

	def add_server():
		nonlocal selectedServer
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

	def add_channel(ignore_duplicates=False):
		nonlocal selectedServer
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
			if not ignore_duplicates:
				messagebox.showwarning("Can't add", f"Server/Channel with ID '{addEntryVar.get()}' already exists")
			return
		treeview.insert(selectedServer, tk.END, text=addEntryVar.get(), value=(noteEntryVar.get(),))
		treeview.item(selectedServer, open=True)
		save_treeview()

	SCAN_IN_PROGRESS = False
	SCAN_TARGET = ""

	startScannerBtn = ttk.Button(buttonFrame, text="Scan Channels")

	def scanner_add_channel(channelId, channelName):
		nonlocal SCAN_IN_PROGRESS, SCAN_TARGET
		if not SCAN_IN_PROGRESS:
			return
		if SCAN_TARGET == "":
			return
		exists = False
		for root in treeview.get_children():
			if treeview.item(root, "text") == str(channelId):
				exists = True
				break

			for child in treeview.get_children(root):
				if treeview.item(child, "text") == str(channelId):
					exists = True
					break
		if exists:
			return
		
		treeview.insert(SCAN_TARGET, tk.END, text=(str(channelId)), value=(channelName,))
		treeview.item(SCAN_TARGET, open=True)

	def scanner_complete():
		nonlocal SCAN_IN_PROGRESS, SCAN_TARGET
		SCAN_IN_PROGRESS = False
		SCAN_TARGET = ""
		startScannerBtn.config(text="Scan Channels")
		save_treeview()

	def update_scan_progress(PROGRESS, TOTAL):
		startScannerBtn.config(text=f"Scanning... ({PROGRESS}/{TOTAL})")

	scanner.setHitCallback(scanner_add_channel)
	scanner.setCompleteCallback(scanner_complete)
	scanner.setProgressCallback(update_scan_progress)

	def start_scanner():
		nonlocal SCAN_IN_PROGRESS, SCAN_TARGET, selectedServer
		if SCAN_IN_PROGRESS:
			return
		SCAN_IN_PROGRESS = True
		SCAN_TARGET = selectedServer
		item = treeview.item(SCAN_TARGET)
		t = threading.Thread(target=scanner.scanServer, daemon=True, args=(item["text"],))
		t.start()
		startScannerBtn.config(text="Scanning...")
	
	def remove_selected():
		if lastSelected == "":
			return
		treeview.delete(lastSelected)
		addChannelBtn.state(["disabled"])
		startScannerBtn.state(["disabled"])
		removeBtn.state(["disabled"])
		save_treeview()

	addServerBtn = ttk.Button(buttonFrame, text="Add Server", command=add_server)
	addServerBtn.pack(padx=3, side=tk.LEFT, expand=True, fill="x")

	addChannelBtn = ttk.Button(buttonFrame, text="Add Channel", command=add_channel)
	addChannelBtn.pack(padx=3, side=tk.LEFT, expand=True, fill="x")
	addChannelBtn.state(["disabled"])

	startScannerBtn.config(command=start_scanner)
	startScannerBtn.pack(padx=3, side=tk.LEFT, expand=True, fill="x")
	startScannerBtn.state(["disabled"])

	removeBtn = ttk.Button(buttonFrame, text="Remove", command=remove_selected)
	removeBtn.pack(padx=3, side=tk.LEFT, expand=True, fill="x")
	removeBtn.state(["disabled"])

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

	def on_click(event):
		nonlocal selectedServer, lastSelected
		item = treeview.identify_row(event.y)
		if item:
			lastSelected = item
			parent = treeview.parent(item)
			parent_text = treeview.item(parent)["text"] if parent else "Root"
			#print("Clicked:", treeview.item(item)["text"], "| Note:", treeview.item(item)["values"], "| Parent:", parent_text)
			addChannelBtn.state(["!disabled"])
			removeBtn.state(["!disabled"])
			if parent_text == "Root":
				addChannelBtn.state(["!disabled"])
				startScannerBtn.state(["!disabled"])
				selectedServer = item
			else:
				addChannelBtn.state(["disabled"])
				startScannerBtn.state(["disabled"])

	treeview.bind("<Button-1>", on_click)  # Left click