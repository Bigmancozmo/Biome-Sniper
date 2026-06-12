import os, sys

SYSTEM = sys.platform

def log(text):
	os.system("echo " + text)

def clear():
	if SYSTEM == "win32":
		os.system("cls")
	else:
		os.system("clear")