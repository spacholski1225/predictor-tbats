"""
TBATS model implementation for fertility rate prediction.
"""

from tbats import TBATS
import numpy as np
import pandas as pd


class TBATSPredictor:
    """
    A class for predicting time series data using the TBATS model.
    
    TBATS (Trigonometric Seasonality, Box-Cox transformation, ARMA errors, 
    Trend, and Seasonal components) is a forecasting method for time series data.
    """
    
    def __init__(self, use_box_cox=None, use_trend=None, use_damped_trend=None):
        """
        Initialize TBATS predictor with optional parameters.
        
        Args:
            use_box_cox (bool, optional): Whether to use Box-Cox transformation.
                If None, the model will automatically determine whether to use it.
            use_trend (bool, optional): Whether to include a trend component.
                If None, the model will automatically determine whether to include it.
            use_damped_trend (bool, optional): Whether to use a damped trend.
                If None, the model will automatically determine whether to use it.
        """
        self.model = None
        self.fitted_model = None
        self.model_params = {
            'use_box_cox': use_box_cox,
            'use_trend': use_trend,
            'use_damped_trend': use_damped_trend,
        }
    
    def train(self, ts_data):
        """
        Train TBATS model on historical data.
        
        Args:
            ts_data (pd.Series): Time series data with years as index and values to predict.
            
        Returns:
            tbats.tbats.TBATS_Model: Fitted TBATS model.
        """
        # Initialize TBATS model with parameters
        self.model = TBATS(**self.model_params)
        
        # Convert pandas Series to numpy array if needed
        if isinstance(ts_data, pd.Series):
            data = ts_data.values
        else:
            data = ts_data
            
        # Fit the model to the data
        self.fitted_model = self.model.fit(data)
        
        return self.fitted_model
    
    def predict(self, steps=5):
        """
        Generate predictions for specified number of steps.
        
        Args:
            steps (int, optional): Number of time steps to predict. Defaults to 5.
            
        Returns:
            np.ndarray: Array of predicted values.
            
        Raises:
            ValueError: If the model has not been trained yet.
        """
        if self.fitted_model is None:
            raise ValueError("Model must be trained before making predictions")
        
        # Generate forecast
        forecast = self.fitted_model.forecast(steps=steps)
        
        return forecast
    
    def get_confidence_intervals(self, steps=5, confidence_level=0.95):
        """
        Generate prediction intervals for the forecast.
        
        Args:
            steps (int, optional): Number of time steps to predict. Defaults to 5.
            confidence_level (float, optional): Confidence level for intervals. Defaults to 0.95.
            
        Returns:
            tuple: Lower and upper bounds of the prediction intervals.
            
        Raises:
            ValueError: If the model has not been trained yet.
        """
        if self.fitted_model is None:
            raise ValueError("Model must be trained before generating confidence intervals")
        
        # Generate forecast with confidence intervals
        _, confidence_intervals = self.fitted_model.forecast(steps=steps, confidence_level=confidence_level)
        
        lower_bounds = confidence_intervals["lower_bound"]
        upper_bounds = confidence_intervals["upper_bound"]
        
        return lower_bounds, upper_bounds