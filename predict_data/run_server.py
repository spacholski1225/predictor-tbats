"""
Script to run the TBATS prediction Flask server.
"""

from .app import app

if __name__ == '__main__':
    print("Starting TBATS Prediction API Server...")
    print("API endpoint available at: http://localhost:5000/predictData")
    app.run(debug=True, host='0.0.0.0', port=5000)