# Poland Fertility Rate Chart

This web application displays Poland's fertility rate data from 1960 to 2033, with historical data shown as a solid blue line and predictions shown as a dashed red line.

## Features

- Sends historical fertility rate data to the API and receives both historical and predicted data
- Displays data in an interactive chart using Chart.js
- Clearly distinguishes between historical and predicted data based on the `predicted` flag
- Responsive design that works on desktop and mobile devices
- Fallback mechanism that uses local data if the API is unreachable

## Setup and Usage

1. Make sure the API server is running at http://52.17.53.243:5000
2. Open `index.html` in a web browser

## Dependencies

- Chart.js (loaded from CDN)

## Data Source

The application sends historical fertility rate data (1960-2023) to the `/predictData` endpoint at http://52.17.53.243:5000 using a POST request. The API returns both the historical data and predicted values for future years, with a `predicted` flag to distinguish between them.

If the API is unreachable (due to network issues, server downtime, or other connectivity issues), the application will automatically use local fallback data to ensure the chart still displays properly. A warning message will be shown to indicate that local data is being used.

### CORS Support

The backend API server has been updated to support CORS (Cross-Origin Resource Sharing), which allows the frontend to communicate with the API even when opened directly from the file system.

If you're still experiencing CORS issues:
1. Make sure the Flask server is running with the updated code that includes Flask-CORS
2. Check that you've installed the Flask-CORS extension (`pip install flask-cors`)
3. Verify in the browser console that the request is being made to the correct endpoint

The application still includes a fallback mechanism that will:
1. Detect CORS errors automatically
2. Fall back to local data if needed
3. Display a specific message explaining any issues

## Implementation Details

- Historical data is displayed as a solid blue line
- Predicted data is displayed as a dashed red line
- Tooltips show additional information when hovering over data points, including an indicator for predicted values
- The chart is fully responsive and adapts to different screen sizes