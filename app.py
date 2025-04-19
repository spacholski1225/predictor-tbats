from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

@app.route('/getData', methods=['GET'])
def get_data():
    # Path to the JSON file
    json_file_path = os.path.join('predict_data', 'fertility_poland_prediction.json')
    
    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # Return the JSON data
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)