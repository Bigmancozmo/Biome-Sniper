import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
import dataMgr as d
import tkinter.simpledialog as sd

root = Tk()
root.geometry("500x720")
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
add_keyword_toggle("KEYWORD_Corruption", "Corruption")
add_keyword_toggle("KEYWORD_Null", "Null")
add_keyword_toggle("KEYWORD_GLIT", "GLITCHED", True)
add_keyword_toggle("KEYWORD_DREAM", "DREAMSPACE", True)

ttk.Label(mainframe, text="-------------------- Target Servers --------------------").pack()
ttk.Label(mainframe, text="Note: These will only work if you have access to them.").pack()
add_keyword_toggle("Server_SpyOnBMC", "spy on bmc", True)
add_keyword_toggle("Server_SolsRNG", "Sol's RNG", False)

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

serverId = treeview.insert("", tk.END, text="123", value=("Sol's RNG Discord",))
channelId = treeview.insert(serverId, tk.END, text="456", value=("#biomes",))
channelId = treeview.insert(serverId, tk.END, text="789", value=("#merchants",))

def discord_token_changed(*args):
    d.set_key("DiscordToken", discord_token_val.get())
discord_token_val.trace_add("write", discord_token_changed)

def start_macro():
    root.destroy()
    os.system("python internals.py")

d.set_key("channels", {
    "Sol's RNG Discord": {}
})

menu = tk.Menu(root, tearoff=0)

def show_menu(event):
    item = treeview.identify_row(event.y)
    if item:
        treeview.selection_set(item)
        menu.post(event.x_root, event.y_root)

def remove_selected():
    for item in treeview.selection():
        treeview.delete(item)

menu.add_command(label="Remove", command=remove_selected)
treeview.bind("<Button-3>", show_menu)

def on_click(event):
    item = treeview.identify_row(event.y)
    if item:
        print("Clicked:", treeview.item(item)["text"], "| Note:", treeview.item(item)["values"])

treeview.bind("<Button-1>", on_click)  # Left click


btn = ttk.Button(mainframe, text="Start Macro", command=start_macro)
btn.pack()

mainframe.pack()
root.mainloop()