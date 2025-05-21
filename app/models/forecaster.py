import pandas as pd
import numpy as np
from tbats import TBATS

class TBATSForecaster:
    def __init__(self):
        # Default TBATS model configuration
        self.model_params = {
            'use_box_cox': True,
            'use_trend': True,
            'use_damped_trend': False,
        }
    
    def forecast(self, data, forecast_periods=10):
        """
        Train TBATS model on historical data and generate forecasts
        
        Args:
            data (pd.DataFrame): DataFrame with 'year' and 'tfr' columns
            forecast_periods (int): Number of periods to forecast
            
        Returns:
            pd.DataFrame: DataFrame with forecasted values
        """
        # Create and fit TBATS model
        estimator = TBATS(**self.model_params)
        model = estimator.fit(data['tfr'])
        
        # Generate forecasts
        forecast = model.forecast(steps=forecast_periods)
        
        # Round forecasted values to 3 decimal places
        forecast = np.round(forecast, 3)
        
        # Create DataFrame with forecasted values
        next_years = range(data['year'].max() + 1, data['year'].max() + forecast_periods + 1)
        forecast_df = pd.DataFrame({
            'year': next_years,
            'tfr': forecast,
            'predicted': True
        })
        
        return forecast_df