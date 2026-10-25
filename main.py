from flask import Flask, send_file
import os, json

app = Flask(__name__)

appSettings = {}
with open("settings.json", "r") as f:
	json.load(f)

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

if __name__ == "__main__":
	app.run(port=4515, debug=False)