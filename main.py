from flask import Flask, send_file

app = Flask(__name__)

appSettings = {}
with open("settings.json", "r") as f:
	json.loads(f)

@app.route("/")
@app.route("/index.html")
@app.route("/index")
def http_index():
	return send_file("./assets/index.html")

if __name__ == "__main__":
	app.run(port=4515, debug=False)