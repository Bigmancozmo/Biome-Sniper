from tkinter import *
from tkinter import ttk
import dataMgr as d

def create(notebook: ttk.Notebook):
	keywordsFrame = ttk.Frame(notebook, padding=(10,10,10,10))
	notebook.add(keywordsFrame, text="Targets")

	keywordToggleFrame = ttk.Frame(keywordsFrame)
	keywordToggleFrame.pack(fill="x")

	TOGGLES_PER_ROW = 4
	keywordIdx = 0

	for c in range(TOGGLES_PER_ROW):
		keywordToggleFrame.columnconfigure(c, weight=1)

	def add_keyword_toggle(dataKey, dText, default=False):
		nonlocal keywordIdx
		snipe_void_coin = BooleanVar(value=d.get_key(dataKey, default))
		checkbox = ttk.Checkbutton(keywordToggleFrame, text=dText, variable=snipe_void_coin)
		checkbox.grid(
			row=(keywordIdx % TOGGLES_PER_ROW),
			column=(keywordIdx // TOGGLES_PER_ROW),
			sticky="w"
		)
		keywordIdx += 1

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