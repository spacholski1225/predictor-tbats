"""
Configuration parameters for the TBATS fertility rate prediction API.
"""

# Prediction parameters
DEFAULT_STEPS = 10  # Number of years to predict

# TBATS model parameters
# Using default parameters as specified in the implementation plan
TBATS_PARAMS = {
    'use_box_cox': None,  # Let the model decide
    'use_trend': None,    # Let the model decide
    'use_damped_trend': None  # Let the model decide
}