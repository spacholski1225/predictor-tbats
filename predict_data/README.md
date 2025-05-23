# TBATS Fertility Rate Predictor

This application uses the TBATS (Trigonometric Seasonality, Box-Cox transformation, ARMA errors, Trend, and Seasonal components) model to predict fertility rates in Poland for the next 5 years.

## Installation

1. Ensure you have Python 3.7+ installed
2. Install the required dependencies:

```bash
pip install tbats pandas numpy matplotlib flask flask-cors
```

## Usage

### Flask API Server

The application now provides a Flask API server that allows you to make predictions via HTTP requests:

```bash
python -m predict_data.run_server
```

This will start a Flask server on port 5000 with the following endpoint:

- **Endpoint**: `/predictData`
- **Method**: POST
- **Content-Type**: application/json
- **Request Body**: Array of objects with `year` and `tfr` fields
- **Response**: Combined historical data and predictions

Example request using curl:

```bash
curl -X POST -H "Content-Type: application/json" -d @get_data/fertility_poland_1939_2023.json http://localhost:5000/predictData
```

Example request using Python:

```python
import requests
import json

# Load data from file
with open('get_data/fertility_poland_1939_2023.json', 'r') as f:
    data = json.load(f)

# Send request to API
response = requests.post('http://localhost:5000/predictData', json=data)

# Get predictions
predictions = response.json()
print(predictions)
```

### Command Line Usage (Legacy)

You can still run the prediction with the command line interface:

```bash
python -m predict_data.main
```

This will:
- Load historical fertility rate data from `download_tfr/fertility_poland_1939_2023.json`
- Train a TBATS model on the historical data
- Predict fertility rates for the next 10 years
- Save the combined historical and predicted data to `predict_data/fertility_poland_prediction.json`

#### Command Line Options

The application supports several command line options:

```bash
python -m predict_data.main --input INPUT_PATH --output OUTPUT_PATH --steps YEARS --plot [--plot-output PLOT_PATH]
```

- `--input`: Path to the input JSON file (default: `download_tfr/fertility_poland_1939_2023.json`)
- `--output`: Path to save the output JSON file (default: `predict_data/fertility_poland_prediction.json`)
- `--steps`: Number of years to predict (default: 5)
- `--plot`: Generate a plot of the historical data and predictions
- `--plot-output`: Path to save the plot (if `--plot` is specified)

#### Example

Generate predictions for the next 10 years and create a plot:

```bash
python -m predict_data.main --steps 10 --plot --plot-output fertility_plot.png
```

## Output Format

The output JSON file contains a list of objects, each with the following structure:

```json
[
  {
    "year": 1939,
    "tfr": 2.5
  },
  ...
  {
    "year": 2028,
    "tfr": 1.32
  }
]
```

## Project Structure

- `__init__.py`: Package initialization
- `config.py`: Configuration parameters
- `data_loader.py`: Functions to load and preprocess data
- `tbats_predictor.py`: TBATS model implementation
- `main.py`: Main script to run the prediction
- `utils.py`: Utility functions

## TBATS Model Description and Parameters

### About TBATS Model

TBATS (Trigonometric Seasonality, Box-Cox transformation, ARMA errors, Trend, and Seasonal components) is an advanced statistical model for time series forecasting. The model is designed to handle various time series features such as:

- Linear or non-linear trends
- Seasonality (including multiple seasonal patterns)
- Cyclicality
- Irregularities and noise

TBATS is particularly useful for data that exhibits complex seasonal patterns or when traditional methods like ARIMA do not provide satisfactory results.

### Model Parameters

In the predictor-tbats project, the TBATS model is implemented in the `TBATSPredictor` class in the `tbats_predictor.py` file. The main parameters that can be adjusted are:

- **use_box_cox**: Determines whether to apply Box-Cox transformation to the data. Can take values:
  - `None` - The model automatically decides whether to use the transformation
  - `True` - Always use the transformation
  - `False` - Never use the transformation
  - `float` - Apply the transformation with a specific lambda parameter

- **use_trend**: Determines whether to include a trend component. Can take values:
  - `None` - The model automatically decides whether to include a trend
  - `True` - Always include a trend
  - `False` - Never include a trend

- **use_damped_trend**: Determines whether to use a damped trend. Can take values:
  - `None` - The model automatically decides whether to use a damped trend
  - `True` - Always use a damped trend
  - `False` - Never use a damped trend

### Customizing Model Parameters

The TBATS model parameters are defined in the `config.py` file in the `TBATS_PARAMS` variable:

```python
TBATS_PARAMS = {
    'use_box_cox': None,  # Let the model decide
    'use_trend': None,    # Let the model decide
    'use_damped_trend': None  # Let the model decide
}
```

To customize the model parameters, you can modify this variable in the `config.py` file or pass parameters directly to the `TBATSPredictor` constructor:

```python
from predict_data.tbats_predictor import TBATSPredictor

# Example of customizing parameters
predictor = TBATSPredictor(
    use_box_cox=True,
    use_trend=True,
    use_damped_trend=False
)
```

Additionally, the `TBATSPredictor` class offers methods to generate confidence intervals for predictions:

```python
# Generate predictions with confidence intervals
lower_bounds, upper_bounds = predictor.get_confidence_intervals(
    steps=5,
    confidence_level=0.95
)
```

## Programmatic Usage Examples

### Using the Module Directly

Here's an example of how to use the prediction module programmatically:

```python
from predict_data.data_loader import load_data, convert_to_time_series, preprocess_data
from predict_data.tbats_predictor import TBATSPredictor
from predict_data.utils import format_predictions, combine_data

# Load data
historical_data = load_data('download_tfr/fertility_poland_1939_2023.json')
ts_data = convert_to_time_series(historical_data)
preprocessed_data = preprocess_data(ts_data)

# Train model with custom parameters
predictor = TBATSPredictor(use_box_cox=True, use_trend=True, use_damped_trend=False)
fitted_model = predictor.train(preprocessed_data)

# Generate predictions for 7 years
predictions = predictor.predict(steps=7)

# Format and combine predictions with historical data
last_year = max(item['year'] for item in historical_data)
formatted_predictions = format_predictions(historical_data, predictions, last_year + 1)
combined_data = combine_data(historical_data, formatted_predictions)

# Process the results
print(f"Predicted {len(formatted_predictions)} years of fertility rates")
for pred in formatted_predictions:
    print(f"Year {pred['year']}: {pred['tfr']}")
```

### Using the API Client

Here's an example of how to use the API from another Python application:

```python
import requests
import json
import matplotlib.pyplot as plt

# Prepare data (or load from file)
data = [
    {"year": 2000, "tfr": 1.37},
    {"year": 2001, "tfr": 1.31},
    # ... more data points
    {"year": 2023, "tfr": 1.158}
]

# Send request to API
response = requests.post('http://localhost:5000/predictData', json=data)

# Check if request was successful
if response.status_code == 200:
    # Get predictions
    result = response.json()
    
    # Extract historical and prediction data
    years = [item['year'] for item in result]
    tfr_values = [item['tfr'] for item in result]
    
    # Find where predictions start (after the last historical year)
    last_historical_year = max(item['year'] for item in data)
    historical_years = [y for y in years if y <= last_historical_year]
    historical_tfr = [tfr_values[i] for i, y in enumerate(years) if y <= last_historical_year]
    
    prediction_years = [y for y in years if y > last_historical_year]
    prediction_tfr = [tfr_values[i] for i, y in enumerate(years) if y > last_historical_year]
    
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
    plt.show()
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

## Notes

- The TBATS model is configured with default parameters, which should work well for most cases
- Predictions are validated to ensure they are within reasonable bounds (0 to 10)
- The application can generate plots to visualize the historical data and predictions
- The model automatically handles missing values through interpolation
- For large datasets or complex seasonal patterns, the model training may take some time