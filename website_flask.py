from flask import Flask, redirect, url_for, render_template, request
from music import *

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
	if request.method == "POST":
		lnk = request.form["lnk"]
		return redirect(url_for("graph", link=lnk))
	else:
		return render_template("index.html")

@app.route("/graph/<link>", methods=["POST", "GET"])
def graph(link):
	if request.method == "POST":
		lnk = request.form["lnk"]
		return redirect(url_for("graph", link=lnk, ))
	else:
		return render_template("graph.html", link = link)

@app.route("/data/<link>", methods=["GET"])
def data(link):
	average_qualities = avg_playlist_vals(link)
	name = get_playlist_name(link)
	data = []
	for key, value in average_qualities.items():
		if not (value > 1 or value < -1):
			data.append({'label':key, 'y': value})
	return {'data':data, 'name': name, "raw_data": average_qualities}

@app.route("/prediction", methods=["POST"])
def prediction():
	data = request.get_json(force=True)
	avg_qualities = audio_features_to_vector(data["data"])
	categories = data["input"].lower().split(", ")
	prediction = most_similar_song_over_categories(categories, avg_qualities)
	return {"result": "Name: " + str(prediction[0]) + " <br>Audio Features: " + str(prediction[1])}
if __name__ == "__main__":
	app.run(debug=True)