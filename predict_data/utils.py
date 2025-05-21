"""
Utility functions for the TBATS fertility rate prediction application.
"""

import json
import pandas as pd
import numpy as np


def format_predictions(historical_data, predictions, start_year):
    """
    Format predictions to match the structure of historical data.
    
    Args:
        historical_data (list): List of dictionaries containing historical data.
        predictions (np.ndarray): Array of predicted values.
        start_year (int): The first year for predictions.
        
    Returns:
        list: List of dictionaries with formatted predictions.
    """
    formatted_predictions = []
    
    for i, pred in enumerate(predictions):
        year = start_year + i
        # Ensure prediction is non-negative and rounded to 3 decimal places
        tfr_value = max(0, round(float(pred), 3))
        
        formatted_predictions.append({
            "year": year,
            "tfr": tfr_value
        })
    
    return formatted_predictions


def combine_data(historical_data, predictions):
    """
    Combine historical data with predictions.
    
    Args:
        historical_data (list): List of dictionaries containing historical data.
        predictions (list): List of dictionaries containing predictions.
        
    Returns:
        list: Combined list of historical data and predictions.
    """
    combined_data = historical_data.copy()
    combined_data.extend(predictions)
    return combined_data



def validate_predictions(predictions, min_value=0.0, max_value=10.0):
    """
    Validate predictions to ensure they are within reasonable bounds.
    
    Args:
        predictions (list): List of dictionaries containing predictions.
        min_value (float, optional): Minimum acceptable value. Defaults to 0.0.
        max_value (float, optional): Maximum acceptable value. Defaults to 10.0.
        
    Returns:
        list: Validated predictions.
    """
    validated_predictions = []
    
    for pred in predictions:
        tfr = pred["tfr"]
        # Ensure prediction is within reasonable bounds
        if tfr < min_value:
            tfr = min_value
        elif tfr > max_value:
            tfr = max_value
            
        validated_predictions.append({
            "year": pred["year"],
            "tfr": tfr
        })
    
    return validated_predictions


def plot_data(historical_data, predictions=None, output_path=None):
    """
    Plot historical data and predictions.
    
    Args:
        historical_data (list): List of dictionaries containing historical data.
        predictions (list, optional): List of dictionaries containing predictions.
        output_path (str, optional): Path to save the plot. If None, the plot is displayed.
        
    Returns:
        None
    """
    try:
        import matplotlib.pyplot as plt
        
        # Extract years and fertility rates from historical data
        years = [item['year'] for item in historical_data]
        tfr = [item['tfr'] for item in historical_data]
        
        # Create figure and plot historical data
        plt.figure(figsize=(12, 6))
        plt.plot(years, tfr, 'b-', label='Historical Data')
        
        # Plot predictions if provided
        if predictions:
            pred_years = [item['year'] for item in predictions]
            pred_tfr = [item['tfr'] for item in predictions]
            plt.plot(pred_years, pred_tfr, 'r--', label='Predictions')
            
            # Add vertical line to separate historical data from predictions
            if years and pred_years:
                plt.axvline(x=max(years), color='gray', linestyle='--', alpha=0.7)
        
        # Add labels and title
        plt.xlabel('Year')
        plt.ylabel('Total Fertility Rate')
        plt.title('Poland Fertility Rate: Historical Data and Predictions')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Save or display the plot
        if output_path:
            plt.savefig(output_path)
        else:
            plt.show()
            
        plt.close()
        
    except ImportError:
        print("Matplotlib is not installed. Cannot create plot.")