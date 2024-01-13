import pandas
from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from datetime import datetime
import csv
import config
from config import *
import requests
from langchain_core.messages import HumanMessage
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.7)


app = Flask(__name__)
CORS(app)
def log(query):
    df = pandas.read_csv("static/assets/userdata.csv")
    df_filtered = df[df['name'] == 'shubh']
    print(df_filtered)
    gender = df_filtered["gender"].values[0]
    weight = int(df_filtered["weight"].values[0])
    height = int(df_filtered["height"].values[0])
    age = int(df_filtered["age"].values[0])
    parameters = {
        "gender": gender,
        "weight": weight,
        "height": height,
        "age": age
    }
    print("Parameters:", parameters)  # Add debug print statements
    return parameters


def getworkoutplan(query):
    result = llm.invoke(f"Create me a workout plan for {query} donot format with *")
    return result.content

def getkhana(query):
    result = llm.invoke(f"Create me a healthy recipie for {query} give me the name of item, list of ingredients and then the steps to make this and the nutritional value in all of this donot format with *")
    return result.content

@app.route('/getworkout', methods=['POST'])
def generate_workout():
    print("Called ai Response")
    try:
        print("inside try  ")
        data = request.json
        print(data)
        query = data.get('prompt', '')
        print(data,query)
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

@app.route('/logworkout',methods=['POST'])
def log_the_workout():
    print("Called ai Response")
    try:
        data = request.json
        query = data.get('prompt', '')
        response_text = log(query)

        print("Response Text:", response_text)  # Add debug print statements

        return jsonify({'response': response_text})
    except Exception as e:
        print("Error:", str(e))  # Print the error for debugging
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4000)
