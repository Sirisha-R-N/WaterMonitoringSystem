from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

THINGSPEAK_API_KEY = "YOUR_READ_API_KEY"
THINGSPEAK_CHANNEL_ID = "YOUR_CHANNEL_ID"
THINGSPEAK_URL = f"https://api.thingspeak.com/channels/2907494/feeds.json?api_key=4GPY4B2SO5J9ADJI&results=2"

@app.route("/")
def index():
    return render_template("index.html", thingSpeakUrl=THINGSPEAK_URL)

if __name__ == "__main__":
    app.run(debug=True)
