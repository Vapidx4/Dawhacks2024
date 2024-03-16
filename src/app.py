from flask import Flask, render_template, request, jsonify
import base64
import json
import requests

app = Flask(__name__)

def getPlantData(data):
    apiKey = "Kw7ifd2qzz7X8d2mvLzLwSE0Msm0VVFHYHT0g2GS3C6vRJii7N"
     
    

    headers = {
        'Api-Key': apiKey,
        'Content-Type': 'application/json'
    }

    url = 'https://plant.id/api/v3/identification'
    
    #convert the data to a dictionary
    data = json.loads(data)
    #print the keys of the dictionary
    print(data.keys())
    
    

    response = requests.post(url, headers=headers, data=data)

    ## with open("data.json", "w") as file:
        ## json.dump(response.json(), file, indent=4)

    return response.json()

def parseJson(data):

    dataDict = {}

    jsonResponse = getPlantData(data)

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
    print("Request received")
    
    try:
        body = request.get_json()
        # print(body)
        #print the type of the body
        print(type(body))
        
        # Attempt to parse the JSON
        data = json.dumps(body)
        print(type(data))
        # print(data)
        
        results = parseJson(data)
        print(results)
        # return jsonify(results)
    except json.JSONDecodeError:
        # If parsing fails, return an error response
        return jsonify({"error": "Invalid JSON format in request body"}), 400
    
    
    
    
    # data = parseJson(body)
    
    # if request.method == 'POST':
    #     body =  request.json
    #     print(body)
    #     data = parseJson()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
