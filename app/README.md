# TBATS Forecasting Flask Server

A Flask-based REST API server that uses the TBATS (Trigonometric Seasonality, Box-Cox transformation, ARMA errors, Trend, and Seasonal components) model to forecast time series data.

## Features

- Single endpoint `/predictData` for time series forecasting
- Uses TBATS model for accurate forecasting
- Returns both historical and predicted data in a consistent format
- Supports Cross-Origin Resource Sharing (CORS) for browser access

## Installation

1. Clone this repository:
```
git clone <repository-url>
cd tbats-flask-server
```

2. Create a virtual environment (optional but recommended):
```
python -m venv venv
```

3. Activate the virtual environment:
   - Windows:
   ```
   venv\Scripts\activate
   ```
   - macOS/Linux:
   ```
   source venv/bin/activate
   ```

4. Install dependencies:
```
pip install -r requirements.txt
```

5. If you've updated from a previous version, make sure Flask-CORS is installed:
```
pip install flask-cors
```

## Usage

1. Start the Flask server:
```
python app.py
```

2. The server will start on `http://localhost:5000`

3. Send a POST request to the `/predictData` endpoint with your time series data:

```bash
curl -X POST -H "Content-Type: application/json" -d @sample_data.json http://localhost:5000/predictData
```

Where `sample_data.json` contains your time series data in the following format:

```json
[
  {"year": 1960, "tfr": 2.98},
  {"year": 1961, "tfr": 2.83},
  ...
]
```

4. The server will respond with the combined historical and predicted data:

```json
[
  {"year": 1960, "tfr": 2.98, "predicted": false},
  ...
  {"year": 2023, "tfr": 1.158, "predicted": false},
  {"year": 2024, "tfr": 1.123, "predicted": true},
  {"year": 2025, "tfr": 1.102, "predicted": true},
  ...
]
```

## API Reference

### POST /predictData

Forecasts the next 10 data points based on the provided historical data.

**Request Body:**
- JSON array of objects with `year` and `tfr` fields

**Response:**
- JSON array of objects including both historical and predicted data
- Each object includes a `predicted` field (true/false)

**Error Responses:**
- 400 Bad Request: Invalid JSON or missing required fields
- 500 Internal Server Error: Model training or prediction errors

### CORS Support

This API supports Cross-Origin Resource Sharing (CORS), allowing it to be accessed from web browsers even when the frontend is hosted on a different domain or opened directly from the file system. This is enabled through the Flask-CORS extension.

## Production Deployment

For production deployment, it's recommended to use Gunicorn as a WSGI HTTP server:

```
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Dependencies

- Flask: Web framework
- TBATS: Time series forecasting model
- Pandas: Data manipulation
- NumPy: Numerical operations
- Gunicorn: WSGI HTTP Server for production