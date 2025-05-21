# Updated Implementation Plan for Fertility Rate Chart

## Overview of Changes

We need to update the presentation_chart project to fetch data from the new endpoint `http://52.17.53.243:5000/predictData` using a POST request and use the `predicted` flag to differentiate between historical and prediction data.

## Key Modifications

1. Change the endpoint from `http://localhost:5000/getData` to `http://52.17.53.243:5000/predictData`
2. Switch from GET to POST request and include historical data in the request body
3. Update data filtering to use the `predicted` flag instead of checking year values
4. Update error messages to reference the new endpoint

## Complete Implementation for script.js

```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Historical data to send in the POST request (up to 2023)
    const historicalData = [
      {
        "year": 1960,
        "tfr": 2.98
      },
      {
        "year": 1961,
        "tfr": 2.83
      },
      {
        "year": 1962,
        "tfr": 2.72
      },
      {
        "year": 1963,
        "tfr": 2.7
      },
      {
        "year": 1964,
        "tfr": 2.57
      },
      {
        "year": 1965,
        "tfr": 2.52
      },
      {
        "year": 1966,
        "tfr": 2.34
      },
      {
        "year": 1967,
        "tfr": 2.33
      },
      {
        "year": 1968,
        "tfr": 2.24
      },
      {
        "year": 1969,
        "tfr": 2.2
      },
      {
        "year": 1970,
        "tfr": 2.2
      },
      {
        "year": 1971,
        "tfr": 2.25
      },
      {
        "year": 1972,
        "tfr": 2.24
      },
      {
        "year": 1973,
        "tfr": 2.26
      },
      {
        "year": 1974,
        "tfr": 2.26
      },
      {
        "year": 1975,
        "tfr": 2.27
      },
      {
        "year": 1976,
        "tfr": 2.3
      },
      {
        "year": 1977,
        "tfr": 2.23
      },
      {
        "year": 1978,
        "tfr": 2.21
      },
      {
        "year": 1979,
        "tfr": 2.28
      },
      {
        "year": 1980,
        "tfr": 2.28
      },
      {
        "year": 1981,
        "tfr": 2.24
      },
      {
        "year": 1982,
        "tfr": 2.34
      },
      {
        "year": 1983,
        "tfr": 2.42
      },
      {
        "year": 1984,
        "tfr": 2.37
      },
      {
        "year": 1985,
        "tfr": 2.33
      },
      {
        "year": 1986,
        "tfr": 2.22
      },
      {
        "year": 1987,
        "tfr": 2.15
      },
      {
        "year": 1988,
        "tfr": 2.13
      },
      {
        "year": 1989,
        "tfr": 2.08
      },
      {
        "year": 1990,
        "tfr": 2.06
      },
      {
        "year": 1991,
        "tfr": 2.07
      },
      {
        "year": 1992,
        "tfr": 1.95
      },
      {
        "year": 1993,
        "tfr": 1.87
      },
      {
        "year": 1994,
        "tfr": 1.81
      },
      {
        "year": 1995,
        "tfr": 1.62
      },
      {
        "year": 1996,
        "tfr": 1.59
      },
      {
        "year": 1997,
        "tfr": 1.51
      },
      {
        "year": 1998,
        "tfr": 1.44
      },
      {
        "year": 1999,
        "tfr": 1.37
      },
      {
        "year": 2000,
        "tfr": 1.37
      },
      {
        "year": 2001,
        "tfr": 1.31
      },
      {
        "year": 2002,
        "tfr": 1.25
      },
      {
        "year": 2003,
        "tfr": 1.22
      },
      {
        "year": 2004,
        "tfr": 1.23
      },
      {
        "year": 2005,
        "tfr": 1.24
      },
      {
        "year": 2006,
        "tfr": 1.27
      },
      {
        "year": 2007,
        "tfr": 1.31
      },
      {
        "year": 2008,
        "tfr": 1.39
      },
      {
        "year": 2009,
        "tfr": 1.4
      },
      {
        "year": 2010,
        "tfr": 1.41
      },
      {
        "year": 2011,
        "tfr": 1.33
      },
      {
        "year": 2012,
        "tfr": 1.33
      },
      {
        "year": 2013,
        "tfr": 1.29
      },
      {
        "year": 2014,
        "tfr": 1.32
      },
      {
        "year": 2015,
        "tfr": 1.32
      },
      {
        "year": 2016,
        "tfr": 1.39
      },
      {
        "year": 2017,
        "tfr": 1.48
      },
      {
        "year": 2018,
        "tfr": 1.46
      },
      {
        "year": 2019,
        "tfr": 1.44
      },
      {
        "year": 2020,
        "tfr": 1.39
      },
      {
        "year": 2021,
        "tfr": 1.33
      },
      {
        "year": 2022,
        "tfr": 1.29
      },
      {
        "year": 2023,
        "tfr": 1.158
      }
    ];
    
    // Fetch data from the new API endpoint with POST request
    fetch('http://52.17.53.243:5000/predictData', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(historicalData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Process and display the data
        createChart(data);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        document.querySelector('.chart-container').innerHTML = 
            '<div class="error">Error loading data. Please make sure the API server is running at http://52.17.53.243:5000</div>';
    });
});

function createChart(data) {
    // Split data based on 'predicted' flag
    const historicalData = data.filter(item => !item.predicted);
    const predictionData = data.filter(item => item.predicted);
    
    // Prepare datasets
    const years = data.map(item => item.year);
    const historicalYears = historicalData.map(item => item.year);
    const predictionYears = predictionData.map(item => item.year);
    
    const historicalTFR = historicalData.map(item => item.tfr);
    const predictionTFR = predictionData.map(item => item.tfr);
    
    // Get the chart canvas
    const ctx = document.getElementById('fertilityChart').getContext('2d');
    
    // Create the chart
    const fertilityChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: years,
            datasets: [
                {
                    label: 'Dane historyczne | Historical Data',
                    data: [...historicalTFR, ...Array(predictionYears.length).fill(null)],
                    borderColor: function(context) {
                        const chart = context.chart;
                        const {ctx, chartArea} = chart;
                        if (!chartArea) {
                            return 'rgba(54, 162, 235, 1)';
                        }
                        const gradient = ctx.createLinearGradient(0, 0, 0, chartArea.bottom);
                        gradient.addColorStop(0, 'rgba(54, 162, 235, 1)');
                        gradient.addColorStop(1, 'rgba(54, 162, 235, 0.6)');
                        return gradient;
                    },
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    borderWidth: 3,
                    tension: 0.2,
                    pointRadius: 3,
                    pointBackgroundColor: 'rgba(54, 162, 235, 1)',
                    pointHoverRadius: 6,
                    pointHoverBackgroundColor: 'white',
                    pointHoverBorderWidth: 2
                },
                {
                    label: 'Dane prognozowane | Predicted Data',
                    data: [...Array(historicalYears.length).fill(null), ...predictionTFR],
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.1)',
                    borderWidth: 3,
                    borderDash: [6, 6],
                    tension: 0.2,
                    pointRadius: 3,
                    pointBackgroundColor: 'rgba(255, 99, 132, 1)',
                    pointHoverRadius: 6,
                    pointHoverBackgroundColor: 'white',
                    pointHoverBorderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Wskaźnik Dzietności w Polsce (TFR) - Dane historyczne i prognozowane',
                    font: {
                        size: 18,
                        weight: 'bold',
                        family: "'Roboto', sans-serif"
                    },
                    padding: {
                        top: 10,
                        bottom: 20
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            const dataIndex = context.dataIndex;
                            const datasetIndex = context.datasetIndex;
                            
                            // Add prediction indicator for predicted data
                            if (datasetIndex === 1 && predictionData.some(item => item.year == years[dataIndex])) {
                                return `${context.dataset.label}: ${context.formattedValue} (Prognoza)`;
                            }
                            return `${context.dataset.label}: ${context.formattedValue}`;
                        }
                    }
                },
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Year'
                    },
                    ticks: {
                        callback: function(value, index) {
                            // Show fewer x-axis labels for better readability
                            return index % 5 === 0 ? years[index] : '';
                        }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Total Fertility Rate (TFR)'
                    },
                    min: 0,
                    suggestedMax: 3.5
                }
            }
        }
    });
}
```

## Key Changes Explained

1. **Data Fetching:**
   - Changed endpoint URL to `http://52.17.53.243:5000/predictData`
   - Changed request method from GET to POST
   - Added request headers to specify JSON content type
   - Included historical data in the request body
   - Updated error message to reference the new endpoint

2. **Data Processing:**
   - Changed filtering logic from year-based (`item.year <= 2023`) to flag-based (`!item.predicted`)
   - Maintained the same chart structure and visual style

3. **Enhanced Tooltip:**
   - Added a custom tooltip callback to indicate when data is predicted
   - This provides additional clarity beyond the visual styling

## Testing Instructions

1. Replace the current `script.js` file with this new implementation
2. Open the `index.html` file in a browser
3. Check that:
   - The chart loads data correctly
   - Historical data appears as a solid blue line
   - Predicted data appears as a dashed red line
   - Hovering over data points shows appropriate tooltips with prediction indicators

## Notes for Implementation

- The implementation handles the separation of historical and predicted data based on the `predicted` flag
- Error handling is robust and will display a user-friendly message if the API cannot be reached
- The tooltip enhancement provides additional clarity about which data points are predictions

## Additional Information

This implementation maintains the same visual style and user experience as the original, but adapts to the new data source and structure. The chart will continue to effectively communicate the distinction between historical and predicted fertility rates.