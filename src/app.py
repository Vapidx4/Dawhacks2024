from flask import Flask, render_template, request, jsonify
import base64
import json
import requests

app = Flask(__name__)

def getPlantData(headers, payload):

    print(headers)
    print(payload)

    url = 'https://plant.id/api/v3/identification'

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    print(response)
    print(response.json())

    return response.json()

def parseJson(result):

    dataDict = {}

    jsonResponse = result

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
        print("Route is called")
        headers = request.headers
        payload = request.json
        jsonData = getPlantData(headers, payload)
        print(jsonData)
        data = parseJson(jsonData)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
