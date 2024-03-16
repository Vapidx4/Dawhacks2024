from flask import Flask, render_template, jsonify
import urllib.request
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getData")
def returnJoke():
    return

app.run(host="0.0.0.0", port=80)