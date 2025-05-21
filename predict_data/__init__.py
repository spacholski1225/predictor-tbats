"""
TBATS Model for Fertility Rate Prediction.

This package contains modules for predicting fertility rates in Poland
using the TBATS (Trigonometric Seasonality, Box-Cox transformation, ARMA errors,
Trend, and Seasonal components) model.

The package now includes a Flask API server that provides a REST API
for making predictions using the TBATS model.
"""

from .app import app