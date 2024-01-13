from flask import Flask, request, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def getworkoutplan(query):
    return "hello what is up brother"

@app.route('/getworkout', methods=['POST'])
def generate_response():
    print("Called ai Response")
    try:
        data = request.json
        query = data.get('prompt', '')

        response_text = getworkoutplan(query)

        return jsonify({'response': response_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4000)
