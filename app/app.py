from flask import Flask, request, jsonify
from flask_cors import CORS
from models.forecaster import TBATSForecaster
from utils.data_handler import preprocess_data, postprocess_results

app = Flask(__name__)
# Włączenie CORS dla wszystkich źródeł
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/predictData', methods=['POST'])
def predict_data():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate input data
        if not data or not isinstance(data, list):
            return jsonify({"error": "Invalid input: Expected a JSON array"}), 400
            
        # Preprocess data for TBATS model
        processed_data = preprocess_data(data)
        
        # Initialize forecaster and make predictions
        forecaster = TBATSForecaster()
        predictions = forecaster.forecast(processed_data)
        
        # Combine historical and predicted data
        result = postprocess_results(data, predictions)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)