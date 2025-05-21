"""
Flask API server for TBATS fertility rate prediction.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json

from .data_loader import convert_to_time_series, preprocess_data
from .tbats_predictor import TBATSPredictor
from .utils import format_predictions, combine_data, validate_predictions
from .config import DEFAULT_STEPS, TBATS_PARAMS

app = Flask(__name__)
CORS(app)

@app.route('/predictData', methods=['POST'])
def predict_data():
    """
    API endpoint to predict fertility rates using TBATS model.
    
    Expects a JSON array of objects with 'year' and 'tfr' fields.
    Returns the combined historical data and predictions.
    """
    try:
        # Get JSON data from request
        request_data = request.get_json()
        
        # Validate input format
        if not isinstance(request_data, list):
            return jsonify({"error": "Input must be a list of year/tfr objects"}), 400
            
        if not all(isinstance(item, dict) and 'year' in item and 'tfr' in item for item in request_data):
            return jsonify({"error": "Each item must contain 'year' and 'tfr' fields"}), 400
        
        # Process the input data
        ts_data = convert_to_time_series(request_data)
        preprocessed_data = preprocess_data(ts_data)
        
        # Train TBATS model and generate predictions
        predictor = TBATSPredictor(**TBATS_PARAMS)
        fitted_model = predictor.train(preprocessed_data)
        predictions = predictor.predict(steps=DEFAULT_STEPS)
        
        # Format predictions
        last_year = max(item['year'] for item in request_data)
        formatted_predictions = format_predictions(request_data, predictions, last_year + 1)
        
        # Validate predictions to ensure they are within reasonable bounds
        validated_predictions = validate_predictions(formatted_predictions)
        
        # Combine historical data with predictions
        combined_data = combine_data(request_data, validated_predictions)
        
        # Return the combined result
        return jsonify(combined_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)