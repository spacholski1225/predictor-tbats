# TBATS Fertility Rate Predictor

This application uses the TBATS (Trigonometric Seasonality, Box-Cox transformation, ARMA errors, Trend, and Seasonal components) model to predict fertility rates in Poland for the next 5 years.

## Installation

1. Ensure you have Python 3.7+ installed
2. Install the required dependencies:

```bash
pip install tbats pandas numpy matplotlib
```

## Usage

### Basic Usage

Run the prediction with default settings:

```bash
python -m predict_data.main
```

This will:
- Load historical fertility rate data from `download_tfr/fertility_poland_1939_2023.json`
- Train a TBATS model on the historical data
- Predict fertility rates for the next 5 years
- Save the combined historical and predicted data to `predict_data/fertility_poland_prediction.json`

### Command Line Options

The application supports several command line options:

```bash
python -m predict_data.main --input INPUT_PATH --output OUTPUT_PATH --steps YEARS --plot [--plot-output PLOT_PATH]
```

- `--input`: Path to the input JSON file (default: `download_tfr/fertility_poland_1939_2023.json`)
- `--output`: Path to save the output JSON file (default: `predict_data/fertility_poland_prediction.json`)
- `--steps`: Number of years to predict (default: 5)
- `--plot`: Generate a plot of the historical data and predictions
- `--plot-output`: Path to save the plot (if `--plot` is specified)

### Example

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

## Notes

- The TBATS model is configured with default parameters, which should work well for most cases
- Predictions are validated to ensure they are within reasonable bounds (0 to 10)
- The application can generate plots to visualize the historical data and predictions