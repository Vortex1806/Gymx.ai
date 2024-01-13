from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from config import GOOGLE_API_KEY
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.7)


app = Flask(__name__)
CORS(app)
# def logworkout(query):
#     headers = {
#         "x-app-id": APP_ID,
#         "x-app-key": API_KEY,
#         "Content-Type": "application/json",
#     }
#     url = "https://trackapi.nutritionix.com/v2/natural/exercise"
#     parameters = {
#         "query": query,
#         "gender": GENDER,
#         "weight_kg": WEIGHT,
#         "height_cm": HEIGHT,
#         "age": AGE
#     }
#     response = requests.post(url=url, headers=headers, json=parameters)
#     response = response.json()
#     for exercise in response["exercises"]:
#         add_to_sheet(exercise["name"].title(), exercise["duration_min"], exercise["nf_calories"])

def getworkoutplan(query):
    result = llm.invoke(f"Create me a workout plan for {query}")
    return result.content

def getkhana(query):
    result = llm.invoke(f"Create me a healthy recipie for {query} give me the name of item, list of ingredients and then the steps to make this and the nutritional value in all of this")
    return result.content

@app.route('/getworkout', methods=['POST'])
def generate_workout():
    print("Called ai Response")
    try:
        data = request.json
        query = data.get('prompt', '')

        response_text = getworkoutplan(query)

        return jsonify({'response': response_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/getkhana',methods=['POST'])
def generate_recipie():
    print("Called ai Response")
    try:
        data = request.json
        query = data.get('prompt', '')

        response_text = getkhana(query)

        return jsonify({'response': response_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @app.route('/getlog',methods=['POST'])
# def generate_recipie():
#     print("Called ai Response")
#     try:
#         data = request.json
#         query = data.get('prompt', '')
#
#         response_text = logworkout(query)
#
#         return jsonify({'response': response_text})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4000)
