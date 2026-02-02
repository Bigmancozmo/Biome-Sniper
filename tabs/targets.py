from tkinter import *
from tkinter import ttk
import dataMgr as d
from enum import Enum

class Column(Enum):
	MERCHANT = 0
	WEATHER = 1
	BIOME = 2
	RARE_BIOME = 3

def create(notebook: ttk.Notebook):
	keywordsFrame = ttk.Frame(notebook, padding=(10,10,10,10))
	notebook.add(keywordsFrame, text="Targets")

	keywordToggleFrame = ttk.Frame(keywordsFrame)
	keywordToggleFrame.pack(fill="x")

	TOGGLES_PER_ROW = 4
	keywordIdx = 0

	for c in range(TOGGLES_PER_ROW):
		keywordToggleFrame.columnconfigure(c, weight=1)

	def add_keyword_toggle(dataKey, dText, default, col, row):
		nonlocal keywordIdx
		booleanVar = BooleanVar(value=d.get_key(dataKey, default))
		checkbox = ttk.Checkbutton(keywordToggleFrame, text=dText, variable=booleanVar)
		checkbox.grid(
			row=row,
			column=col,
			sticky="w"
		)
		keywordIdx += 1

		def void_coin_changed(*args):
			d.set_key(dataKey, booleanVar.get())

		booleanVar.trace_add("write", void_coin_changed)

	add_keyword_toggle("KEYWORD_Mari", "Mari", False, Column.MERCHANT.value, 0)
	add_keyword_toggle("KEYWORD_VoidCoin", "Void Coin", True, Column.MERCHANT.value, 1)
	add_keyword_toggle("KEYWORD_GearA", "Gear A", True, Column.MERCHANT.value, 2)
	add_keyword_toggle("KEYWORD_GearB", "Gear B", True, Column.MERCHANT.value, 3)
	add_keyword_toggle("KEYWORD_LuckyPenny", "Lucky Penny", True, Column.MERCHANT.value, 4)
	add_keyword_toggle("KEYWORD_VoidCoin", "Void Coin", True, Column.MERCHANT.value, 5)
	add_keyword_toggle("KEYWORD_Jest", "Jester", True, Column.MERCHANT.value, 6)
	add_keyword_toggle("KEYWORD_Obliv", "Oblivion Potion", False, Column.MERCHANT.value, 7)

	add_keyword_toggle("KEYWORD_Windy", "Windy", False, Column.WEATHER.value, 0)
	add_keyword_toggle("KEYWORD_Snowy", "Snowy", False, Column.WEATHER.value, 1)
	add_keyword_toggle("KEYWORD_Rainy", "Rainy", False, Column.WEATHER.value, 2)

	add_keyword_toggle("KEYWORD_SandStorm", "Sand Storm", False, Column.BIOME.value, 0)
	add_keyword_toggle("KEYWORD_Heaven", "Heaven", False, Column.BIOME.value, 1)
	add_keyword_toggle("KEYWORD_Starfall", "Starfall", False, Column.BIOME.value, 2)
	add_keyword_toggle("KEYWORD_Corruption", "Corruption", False, Column.BIOME.value, 3)
	add_keyword_toggle("KEYWORD_Hell", "Hell", False, Column.BIOME.value, 4)
	add_keyword_toggle("KEYWORD_Null", "Null", False, Column.BIOME.value, 5)

	add_keyword_toggle("KEYWORD_GLIT", "GLITCHED", True, Column.RARE_BIOME.value, 0)
	add_keyword_toggle("KEYWORD_DREAM", "DREAMSPACE", True, Column.RARE_BIOME.value, 1)
	add_keyword_toggle("KEYWORD_CYBER", "CYBERSPACE", True, Column.RARE_BIOME.value, 2)