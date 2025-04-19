# Poland Fertility Rate Chart

This web application displays Poland's fertility rate data from 1960 to 2033, with historical data up to 2023 shown as a solid blue line and predictions from 2024 to 2033 shown as a dashed red line.

## Features

- Fetches fertility rate data from a local API endpoint
- Displays data in an interactive chart using Chart.js
- Clearly distinguishes between historical and predicted data
- Responsive design that works on desktop and mobile devices

## Setup and Usage

1. Make sure the API server is running at http://localhost:5000
2. Open `index.html` in a web browser

## Dependencies

- Chart.js (loaded from CDN)

## Data Source

The application fetches data from the `/getData` endpoint at localhost:5000, which provides fertility rate data for Poland from 1960 to 2033.