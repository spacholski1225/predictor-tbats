"""
Test script for the TBATS prediction API.
"""

import requests
import json
import os
import sys
import matplotlib.pyplot as plt

def test_api(data_file, api_url="http://localhost:5000/predictData"):
    """
    Test the TBATS prediction API with data from a file.
    
    Args:
        data_file (str): Path to the JSON file containing fertility rate data.
        api_url (str): URL of the API endpoint.
    """
    # Load data from file
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
        print(f"Loaded {len(data)} data points from {data_file}")
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return
    
    # Send request to API
    try:
        print(f"Sending request to {api_url}...")
        response = requests.post(api_url, json=data)
    except Exception as e:
        print(f"Error sending request: {str(e)}")
        return
    
    # Check if request was successful
    if response.status_code == 200:
        # Get predictions
        result = response.json()
        print(f"Received {len(result)} data points (including predictions)")
        
        # Extract historical and prediction data
        years = [item['year'] for item in result]
        tfr_values = [item['tfr'] for item in result]
        
        # Find where predictions start (after the last historical year)
        last_historical_year = max(item['year'] for item in data)
        historical_years = [y for y in years if y <= last_historical_year]
        historical_tfr = [tfr_values[i] for i, y in enumerate(years) if y <= last_historical_year]
        
        prediction_years = [y for y in years if y > last_historical_year]
        prediction_tfr = [tfr_values[i] for i, y in enumerate(years) if y > last_historical_year]
        
        print(f"Historical data: {len(historical_years)} years")
        print(f"Predictions: {len(prediction_years)} years")
        
        # Print the predictions
        print("\nPredictions:")
        for i, year in enumerate(prediction_years):
            print(f"Year {year}: {prediction_tfr[i]}")
        
        # Plot the results
        plt.figure(figsize=(12, 6))
        plt.plot(historical_years, historical_tfr, 'b-', label='Historical Data')
        plt.plot(prediction_years, prediction_tfr, 'r--', label='Predictions')
        plt.axvline(x=last_historical_year, color='gray', linestyle='--', alpha=0.7)
        plt.xlabel('Year')
        plt.ylabel('Total Fertility Rate')
        plt.title('Poland Fertility Rate: Historical Data and Predictions')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Save or display the plot
        plt.savefig('api_test_result.png')
        print(f"Plot saved to api_test_result.png")
        
        try:
            plt.show()
        except:
            print("Could not display plot (no display available)")
        
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == '__main__':
    # Get data file from command line argument or use default
    data_file = sys.argv[1] if len(sys.argv) > 1 else '../get_data/fertility_poland_1939_2023.json'
    
    # Check if file exists
    if not os.path.exists(data_file):
        print(f"Error: File {data_file} not found")
        print("Usage: python test_api.py [data_file]")
        sys.exit(1)
    
    # Test the API
    test_api(data_file)