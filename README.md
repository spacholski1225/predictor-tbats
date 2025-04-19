# predictor-tbats

A Python application that uses the TBATS (Trigonometric Seasonality, Box-Cox transformation, ARMA errors, Trend, and Seasonal components) model to predict fertility rates in Poland for the next 5 years.

## Project Structure

```
predictor-tbats/
├── download_tfr/                  # Data download and preparation
│   ├── download_tfr.py            # Script to download fertility rate data
│   ├── fertility_poland_1939_2023.csv  # Historical data in CSV format
│   └── fertility_poland_1939_2023.json # Historical data in JSON format
│
├── predict_data/                  # Prediction application
│   ├── __init__.py                # Package initialization
│   ├── config.py                  # Configuration parameters
│   ├── data_loader.py             # Functions to load and preprocess data
│   ├── tbats_predictor.py         # TBATS model implementation
│   ├── main.py                    # Main script to run the prediction
│   ├── utils.py                   # Utility functions
│   └── README.md                  # Detailed documentation for the prediction module
│
├── run_prediction.py              # Wrapper script to run the prediction
└── README.md                      # This file
```

## Installation

1. Ensure you have Python 3.7+ installed
2. Install the required dependencies:

```bash
pip install tbats pandas numpy matplotlib
```

## Usage

### Quick Start

Run the prediction with default settings:

```bash
python run_prediction.py
```

This will:
- Load historical fertility rate data from `download_tfr/fertility_poland_1939_2023.json`
- Train a TBATS model on the historical data
- Predict fertility rates for the next 5 years
- Save the combined historical and predicted data to `predict_data/fertility_poland_prediction.json`

### Command Line Options

The application supports several command line options:

```bash
python run_prediction.py --input INPUT_PATH --output OUTPUT_PATH --steps YEARS --plot [--plot-output PLOT_PATH]
```

- `--input`: Path to the input JSON file (default: `download_tfr/fertility_poland_1939_2023.json`)
- `--output`: Path to save the output JSON file (default: `predict_data/fertility_poland_prediction.json`)
- `--steps`: Number of years to predict (default: 5)
- `--plot`: Generate a plot of the historical data and predictions
- `--plot-output`: Path to save the plot (if `--plot` is specified)

### Example

Generate predictions for the next 10 years and create a plot:

```bash
python run_prediction.py --steps 10 --plot --plot-output fertility_plot.png
```

## Features

- Uses the TBATS model for time series forecasting
- Handles historical fertility rate data from 1939 to 2023
- Predicts fertility rates for future years
- Validates predictions to ensure they are within reasonable bounds
- Can generate plots to visualize historical data and predictions
- Outputs results in JSON format

## Implementation Details

For detailed information about the implementation, see the [predict_data/README.md](predict_data/README.md) file.

## Data Source

The historical fertility rate data for Poland from 1939 to 2023 is included in the `download_tfr` directory. The data is available in both CSV and JSON formats.