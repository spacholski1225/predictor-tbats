"""
Main script to run the TBATS fertility rate prediction.
"""

import argparse
import os
import sys

from .data_loader import load_data, convert_to_time_series, preprocess_data
from .tbats_predictor import TBATSPredictor
from .utils import (
    format_predictions,
    combine_data,
    save_to_json,
    validate_predictions,
    plot_data
)
from .config import (
    DEFAULT_INPUT_PATH,
    DEFAULT_OUTPUT_PATH,
    DEFAULT_STEPS,
    TBATS_PARAMS
)


def main():
    """
    Main function to run the prediction process.
    
    Returns:
        list: The combined historical and predicted data.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Predict fertility rates using TBATS model')
    parser.add_argument('--input', type=str, default=DEFAULT_INPUT_PATH,
                        help='Path to input JSON file')
    parser.add_argument('--output', type=str, default=DEFAULT_OUTPUT_PATH,
                        help='Path to output JSON file')
    parser.add_argument('--steps', type=int, default=DEFAULT_STEPS,
                        help='Number of years to predict')
    parser.add_argument('--plot', action='store_true',
                        help='Generate a plot of the data and predictions')
    parser.add_argument('--plot-output', type=str, default=None,
                        help='Path to save the plot (if --plot is specified)')
    args = parser.parse_args()
    
    try:
        # Load and preprocess data
        print(f"Loading data from {args.input}...")
        historical_data = load_data(args.input)
        ts_data = convert_to_time_series(historical_data)
        preprocessed_data = preprocess_data(ts_data)
        
        # Train TBATS model
        print("Training TBATS model...")
        predictor = TBATSPredictor(**TBATS_PARAMS)
        fitted_model = predictor.train(preprocessed_data)
        
        # Generate predictions
        print(f"Generating predictions for {args.steps} years...")
        predictions = predictor.predict(steps=args.steps)
        
        # Format and combine predictions with historical data
        last_year = max(item['year'] for item in historical_data)
        formatted_predictions = format_predictions(historical_data, predictions, last_year + 1)
        
        # Validate predictions to ensure they are within reasonable bounds
        validated_predictions = validate_predictions(formatted_predictions)
        
        # Combine historical data with predictions
        combined_data = combine_data(historical_data, validated_predictions)
        
        # Save to file
        print(f"Saving results to {args.output}...")
        result = save_to_json(combined_data, args.output)
        
        # Generate plot if requested
        if args.plot:
            plot_output = args.plot_output
            print(f"Generating plot{' and saving to ' + plot_output if plot_output else ''}...")
            plot_data(historical_data, validated_predictions, plot_output)
        
        print("Prediction completed successfully!")
        return result
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


if __name__ == '__main__':
    main()