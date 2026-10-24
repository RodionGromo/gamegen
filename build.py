import requests, sys, os, shutil, subprocess, json
from pathlib import Path

print("1. Checking platform...")
# don't bother with macOS, rarely used
# used to decide with what we unpack a zip file
is_win = True if sys.platform == "win32" else False
if is_win:
	print("\tDetected: Windows, using powershell to unpack")
else:
	print("\tDetected: Linux, using unzip to unpack")


print("\n2. Checking if Bootstrap is present...")
downloadBootstrap = False
if os.path.exists("./assets/bootstrap") and os.path.isfile("./assets/bootstrap/js/bootstrap.bundle.min.js") and os.path.isfile("./assets/bootstrap/css/bootstrap.css"):
			print("\tRequires files exist! Continuing...")
else:
	print("\tNo files found, download required")
	downloadBootstrap = True

if downloadBootstrap:
	print("2.1. Downloading Bootstrap...")
	# load bootstrap, unpack it
	bootstrap_zip = "https://github.com/twbs/bootstrap/releases/download/v6.0.0-alpha.1/bootstrap-6.0.0-alpha.1-dist.zip"
	resp = requests.get(bootstrap_zip)

	if resp.status_code == 200:
		if not os.path.exists("./temp"): os.makedirs("./temp")
		with open("./temp/bootstrap.zip", "wb") as file:
			file.write(resp.content)
		print("\tBootstrap downloaded! Unpacking...")
		
		working_dir = Path.cwd()
		if not os.path.exists("./temp/bootstrap"): os.makedirs("./temp/bootstrap")
		zip_path = str(working_dir / 'temp' / 'bootstrap.zip')
		zip_output = str(working_dir / 'temp' / 'bootstrap')
		if is_win:
			subprocess.run(
				["powershell", "-NoProfile", "-Command", f'Expand-Archive -Path "{zip_path}" -DestinationPath "{zip_output}"'],
				capture_output=False
			)
		else:
			res = subprocess.run(
				["unzip", "-o", "-q", f"{zip_path}", "-d", f"{zip_output}"],
				capture_output=False
			)
			if res.returncode != 0:
				raise Exception("unzip failed, install unzip if not installed, code: " + str(res.returncode))
		print("\tUnpacked, moving to correct position..")
		shutil.move("./temp/bootstrap/bootstrap-6.0.0-alpha.1-dist/js", "./assets/bootstrap/js")
		shutil.move("./temp/bootstrap/bootstrap-6.0.0-alpha.1-dist/css", "./assets/bootstrap/css")
		shutil.rmtree("./temp")
		print("\tSuccess! Continuing...")

print("3. Checking settings file...")
required_keys = ("port", "host", "ai_api_key")
correct = True
if os.path.isfile("./settings.json"):
	print("\tFile found, checking contents...")
	with open("./settings.json", "r") as f:
		data = json.load(f)
		for key in required_keys:
			if key not in list(data.keys()):
				print(f"\t{key} not found in file! Regenerating from scratch...")
				correct = False
				break
		if correct:
			print("\tSettings file is OK")
else:
	print("\tFile not found, regenerating...")
	correct = False

if not correct:
	data = {
		"port": None,
		"host": None,
		"ai_api_key": None
	}
	with open("./settings.json", "w") as f:
		f.write(json.dumps(data))
	print("\tFile created! Please replace nulls with actual data before starting the server")
input("Good to go! Press Enter to close...")
