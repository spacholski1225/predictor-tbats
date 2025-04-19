"""
Functions to load and preprocess fertility rate data.
"""

import json
import pandas as pd
import numpy as np


def load_data(file_path):
    """
    Load fertility rate data from JSON file.
    
    Args:
        file_path (str): Path to the JSON file containing fertility rate data.
        
    Returns:
        list: List of dictionaries containing year and tfr (total fertility rate) data.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def convert_to_time_series(data):
    """
    Convert JSON data to time series format.
    
    Args:
        data (list): List of dictionaries containing year and tfr data.
        
    Returns:
        pd.Series: Pandas Series with years as index and tfr as values.
    """
    # Extract years and fertility rates
    years = [item['year'] for item in data]
    tfr = [item['tfr'] for item in data]
    
    # Create a pandas Series with years as index
    ts_data = pd.Series(tfr, index=years)
    return ts_data


def preprocess_data(ts_data):
    """
    Preprocess time series data for TBATS model.
    
    Args:
        ts_data (pd.Series): Time series data with years as index and tfr as values.
        
    Returns:
        pd.Series: Preprocessed time series data ready for TBATS model.
    """
    # Ensure data is sorted by year
    ts_data = ts_data.sort_index()
    
    # Handle any missing values if needed
    if ts_data.isnull().any():
        ts_data = ts_data.interpolate()
    
    return ts_data