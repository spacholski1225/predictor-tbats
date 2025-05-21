import pandas as pd
import numpy as np

def preprocess_data(json_data):
    """
    Convert JSON input to pandas DataFrame for model processing
    
    Args:
        json_data (list): List of dictionaries with year and tfr values
        
    Returns:
        pd.DataFrame: DataFrame with year and tfr columns
    """
    # Convert to DataFrame
    df = pd.DataFrame(json_data)
    
    # Verify required columns
    if 'year' not in df.columns or 'tfr' not in df.columns:
        raise ValueError("Input data must contain 'year' and 'tfr' fields")
    
    # Sort by year to ensure chronological order
    df = df.sort_values('year')
    
    # Round tfr values to 3 decimal places
    df['tfr'] = df['tfr'].round(3)
    
    return df

def postprocess_results(original_data, predictions):
    """
    Combine original data with predictions and format for response
    
    Args:
        original_data (list): Original JSON input data
        predictions (pd.DataFrame): DataFrame with predicted values
        
    Returns:
        list: Combined list of dictionaries for JSON response
    """
    # Add predicted=False flag to historical data and round tfr values
    for item in original_data:
        item['predicted'] = False
        item['tfr'] = round(item['tfr'], 3)
    
    # Convert predictions to list of dictionaries
    prediction_list = predictions.to_dict(orient='records')
    
    # Combine historical and predicted data
    combined_data = original_data + prediction_list
    
    return combined_data