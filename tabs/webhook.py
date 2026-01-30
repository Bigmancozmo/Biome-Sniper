import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import dataMgr as d
import updater

def create(notebook: ttk.Notebook):
	def webhook_url_changed(*args):
		d.set_key("WebhookURL", webhook_url_val.get())

	placeholder = "https://discord.com/api/webhooks/.../..."

	def add_placeholder(event=None):
		if not webhook_url_val.get():
			url_input.insert(0, placeholder)
			url_input.config(foreground="gray")

	def remove_placeholder(event):
		if webhook_url_val.get() == placeholder:
			url_input.delete(0, tk.END)
			url_input.config(foreground="black")

	webhookUrlFrame = ttk.Frame(notebook, padding=(10,10,10,10))
	notebook.add(webhookUrlFrame, text="Webhook")
	ttk.Label(webhookUrlFrame, text="You can set up a Discord webhook in a server to automatically receive message logs when a biome or merchant is sniped.").pack(padx=10)
	ttk.Label(webhookUrlFrame, text="[WARNING]: Connecting this macro to a webhook in a server with people\n" +
	"you do not know or trust is highly advised against because the snipe logs will reveal where the\n" +
	"biome/merchant was sniped from and the link to the server. The safest option is to only post these\n" +
	"logs to a server where you are the only member. We are not responsible if you are warned/macro banned\n" +
	"from any glitch hunt servers for intentionally or accidentally leaking or sniping.").pack(padx=10, pady=(10,0))
	ttk.Label(webhookUrlFrame, text="Enter a Discord Webhook URL:").pack(padx=10, pady=(10,0))
	webhook_url_val = StringVar(value=d.get_key("WebhookURL", ""))
	url_input = ttk.Entry(webhookUrlFrame, textvariable=webhook_url_val)
	url_input.pack(fill="x", padx=30)
	webhook_url_val.trace_add("write", webhook_url_changed)
	url_input.bind("<FocusIn>", remove_placeholder)
	url_input.bind("<FocusOut>", add_placeholder)
	add_placeholder()