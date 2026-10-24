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
	return "file not found on server!", 404

@app.route("/bootstrap/<folder>/<file>")
def http_bootstrap(folder: str, filename: str):
	path = "./assets/bootstrap/" + folder + "/" + filename
	if os.path.isfile(path):
		return send_file(path)
	return "bootstrap file not found on server!", 404

if __name__ == "__main__":
	app.run(port=4515, debug=False)