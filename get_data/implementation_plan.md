# Flask API Implementation Plan

## Overview
Create a Flask API in the `get_data` folder that serves fertility data from the existing JSON file through an API endpoint.

## Requirements
- Create a Flask application with CORS enabled
- Implement a GET endpoint `/getUnpredictedData` that returns the content of `fertility_poland_1939_2023.json` as proper JSON
- Include basic error handling
- Configure the application to listen on all interfaces (0.0.0.0) for EC2 deployment

## Application Structure
```
get_data/
├── app.py                           # Flask application (to be created)
└── fertility_poland_1939_2023.json  # Data file (already exists)
```

## Implementation Details

### app.py
```python
from flask import Flask, jsonify
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/getUnpredictedData', methods=['GET'])
def get_unpredicted_data():
    try:
        # Path to the JSON file (relative to the current file)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(current_dir, 'fertility_poland_1939_2023.json')
        
        # Read the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        # Return the JSON data
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in data file"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

## Running the Application
To run the application:
```
cd get_data
python app.py
```

This will start the Flask server on port 5000, accessible at:
- Local: http://localhost:5000/getUnpredictedData
- On EC2: http://<EC2-IP>:5000/getUnpredictedData

## Notes for EC2 Deployment
- Ensure Flask and flask-cors are installed: `pip install Flask flask-cors`
- For production deployment, consider using a WSGI server like Gunicorn