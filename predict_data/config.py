"""
Configuration parameters for the TBATS fertility rate prediction application.
"""

import os

# File paths
DEFAULT_INPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                 'download_tfr', 'fertility_poland_1939_2023.json')
DEFAULT_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 'fertility_poland_prediction.json')

# Prediction parameters
DEFAULT_STEPS = 5  # Number of years to predict

# TBATS model parameters
# Using default parameters as specified in the implementation plan
TBATS_PARAMS = {
    'use_box_cox': None,  # Let the model decide
    'use_trend': None,    # Let the model decide
    'use_damped_trend': None  # Let the model decide
}