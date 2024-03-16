from flask import Flask, render_template, request
import base64
import json
import requests

app = Flask(__name__)

apiKey = "Kw7ifd2qzz7X8d2mvLzLwSE0Msm0VVFHYHT0g2GS3C6vRJii7N"

with open("static/plant2.jpg", "rb") as image2string:
    encodedString = base64.b64encode(image2string.read())

payload = {
    "images": ["data:image/jpg;base64," + encodedString.decode("utf-8")],
    "similar_images": True,
    "health": "all"
}

headers = {
    'Api-Key': apiKey,
    'Content-Type': 'application/json'
}

url = 'https://plant.id/api/v3/identification'

response = requests.post(url, headers=headers, data=json.dumps(payload))

with open("data.json", "w") as file:
    json.dump(response.json(), file, indent=4)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Handle image upload and species recognition here
        # Save the uploaded image
        # Use species recognition model to identify the species
        # Update user points and database accordingly
        return "Image uploaded and species recognized successfully!"

if __name__ == '__main__':
    app.run(debug=True)
