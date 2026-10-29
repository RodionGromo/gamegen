from flask import Flask, send_file, request
import os, json
import requests

app = Flask(__name__)

appSettings = {}
with open("settings.json", "r") as f:
	appSettings = json.load(f)

systemprompt = ""
with open("sysprompt.txt", "r", encoding="utf-8") as f:
	systemprompt = f.read()

testgame = ""
try:
	with open("gametest.txt", "r", encoding="utf-8") as f:
		testgame = json.load(f)
except FileNotFoundError:
	testgame = {}

@app.route("/")
@app.route("/index.html")
@app.route("/index")
def http_index():
	return send_file("./assets/index.html")

@app.route("/files/<filename>")
def http_file(filename: str):
	if os.path.isfile("./assets/" + filename):
		return send_file("./assets/" + filename)
	return "file not found!", 404

@app.route("/bootstrap/<folder>/<filename>")
def http_bootstrap(folder: str, filename: str):
	if os.path.isfile("./assets/bootstrap/" + folder + "/" + filename):
		return send_file("./assets/bootstrap/" + folder + "/" + filename)
	return "bootstrap file not found!", 404

@app.route("/api/testCode")
def http_testgame():
	return testgame["choices"][0]["message"]["content"]

@app.route("/api/generate", methods=["POST"])
def http_gamegen():
	data = request.get_json(silent=True)
	if data is None:
		return "Invalid data!", 400

	if "game_prompt" not in data.keys():
		return "Invalid content!", 400

	if len(data["game_prompt"]) < 16:
		return "Invalid content!", 400
	print("Got correct request to generate a game! Starting process...")
	# send request
	req = requests.post("https://api.teamorouter.com/v1/chat/completions",
		headers={"Content-Type": "application/json", "Authorization": "Bearer " + appSettings["ai_api_key"]},
		json={
			"model":"deepseek-v4-flash-free", "messages":[{"role": "system", "content": systemprompt}, {"role": "user", "content": data["game_prompt"]}]
		}
	)
	res = None
	try:
		res = req.json()
		if "choices" in res and len(res["choices"]) > 0:
			data = res["choices"][0]["message"]["content"]
			with open("gametest.txt", "w") as f:
				f.write(json.dumps(res))
				testgame = res
			return data
	except Exception as e:
		print("error occured on getting json:", e)
		return "Response parse error", 500

if __name__ == "__main__":
	app.run(port=appSettings["port"], debug=False)