from flask import Flask, render_template, request, jsonify
import base64
import json
import requests

app = Flask(__name__)

def getPlantData():
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

    ## with open("data.json", "w") as file:
        ## json.dump(response.json(), file, indent=4)

    return response.json()

def parseJson():

    dataDict = {}

    jsonResponse = getPlantData()

    isHealthy = jsonResponse["result"]["is_healthy"]["binary"]

    isPlant = jsonResponse["result"]["is_plant"]["binary"]

    classifications = jsonResponse["result"]["classification"]["suggestions"]

    classificationDict = {
        "name": [],
        "probability": []
    }
    similarityDict = {
        "similarImage": [],
        "similarity": []
    }

    for classification in classifications:
        if classification["probability"] >= 0.20:
            classificationDict["name"].append(classification["name"])
            classificationDict["probability"].append(str(round(float(classification["probability"]) * 10000)/100) + "%")
            for similarImage in classification["similar_images"]:
                if (similarImage["similarity"]) >= 0.50:
                    similarityDict["similarImage"].append(similarImage["url"])
                    similarityDict["similarity"].append(str(round(float(similarImage["similarity"]) * 10000)/100) + "%")
    
    diseases = jsonResponse["result"]["disease"]["suggestions"]

    diseaseDict = {
        "disease": [],
        "probability": []
    }

    for disease in diseases:
        if disease["probability"] >= 0.20:

            diseaseDict["disease"].append(disease["name"])
            diseaseDict["probability"].append(str(round(float(disease["probability"]) * 10000)/100) + "%")

    dataDict["isHealthy"] = isHealthy
    dataDict["isPlant"] = isPlant
    dataDict["classification"] = classificationDict
    dataDict["similarImages"] = similarityDict
    dataDict["diseases"] = diseaseDict

    # jsonData = json.dumps(dataDict)

    return dataDict



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        data = parseJson()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
