import requests
import os, zipfile, sys

DISABLE_SKIP = False
CURRENT = "v1.2.5"

# Set this environment variable to disable the auto updater in that directory
value = os.environ.get("BIOME_SNIPER_DEV_FOLDER")
if value:
	value = value.upper()
else:
	value = "NoFolder"
if DISABLE_SKIP:
	value = value + ".disabled"
folder = os.path.dirname(os.path.abspath(__file__)).upper()

def update_available():
	req = requests.get("https://github.com/Bigmancozmo/Biome-Sniper/releases/latest", allow_redirects=True)
	LATEST = req.url.split("/releases/tag/")[1]
	return (LATEST != CURRENT) and (folder != value)

def update():
	if value in folder:
		print("Disabling auto updater")
	else:
		req = requests.get("https://github.com/Bigmancozmo/Biome-Sniper/releases/latest", allow_redirects=True)
		LATEST = req.url.split("/releases/tag/")[1]
		print("Latest version:", LATEST)
		print("Current version:", CURRENT)

		if CURRENT != LATEST:
			print("Outdated!")
			NEW_FILE = f"https://github.com/Bigmancozmo/Biome-Sniper/releases/download/{LATEST}/BMCs.Biome.Sniper.{LATEST}.zip"
			print("Downloading:", NEW_FILE)
			r = requests.get(NEW_FILE)
			with open("update.zip", "wb") as f:
				f.write(r.content)
			print("Download complete")
			print("Extracting...")
			with zipfile.ZipFile("update.zip", "r") as zip_ref:
				zip_ref.extractall("updated")
			print("Extracted")
			print("Installing...")
			lines = [
				"import os, shutil, time, sys, subprocess\n",
				"print('Cleaning pre-update files...')\n",
				"if os.path.exists('update.zip'):\n",
				"    os.remove('update.zip')\n",
				"if os.path.exists('__pycache__'):\n",
				"    shutil.rmtree('__pycache__')\n",
				"src = 'updated'\n",
				"dst = os.path.dirname(os.path.abspath(__file__))\n",
				"for root, dirs, files in os.walk(src):\n",
				"    relative_path = os.path.relpath(root, src)\n",
				"    target_dir = os.path.join(dst, relative_path)\n",
				"    os.makedirs(target_dir, exist_ok=True)\n",
				"    for file in files:\n",
				"        shutil.copy2(os.path.join(root, file), os.path.join(target_dir, file))\n",
				"time.sleep(1)\n",
				"if os.path.exists('__pycache__'):\n",
				"    shutil.rmtree('__pycache__')\n",
				"if os.path.exists('updated'):\n",
				"    shutil.rmtree('updated')\n",
				"time.sleep(2)\n",
				"os.system(f'{sys.executable} gui.pyw')"
			]
			with open("apply-update.py", "w") as f:
				f.writelines(lines)
			os.system(f"{sys.executable} apply-update.py")
		else:
			print("Up to date")
