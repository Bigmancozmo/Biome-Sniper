from tkinter import *
from tkinter import ttk
import dataMgr as d

def create(notebook: ttk.Notebook):
	def discord_token_changed(*args):
		d.set_key("DiscordToken", discord_token_val.get())

	discordTokenFrame = ttk.Frame(notebook, padding=(10,10,10,10))
	notebook.add(discordTokenFrame, text="Discord Token")
	ttk.Label(discordTokenFrame, text="Do NOT share this!").pack()
	ttk.Label(discordTokenFrame, text="It can be used to bypass 2FA and get in your Discord account.").pack()
	discord_token_val = StringVar(value=d.get_key("DiscordToken", ""))
	token_input = ttk.Entry(discordTokenFrame, textvariable=discord_token_val, show="•")
	token_input.pack(fill="x", padx=30)
	discord_token_val.trace_add("write", discord_token_changed)