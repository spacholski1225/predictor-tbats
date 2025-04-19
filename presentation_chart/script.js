document.addEventListener('DOMContentLoaded', function() {
    // Fetch data from the API
    fetch('http://localhost:5000/getData')
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
                '<div class="error">Error loading data. Please make sure the API server is running at http://localhost:5000</div>';
        });
});

function createChart(data) {
    // Split data into historical and prediction
    const historicalData = data.filter(item => item.year <= 2023);
    const predictionData = data.filter(item => item.year > 2023);
    
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
                    label: 'Dane historyczne (1960-2023) | Historical Data',
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
                    label: 'Dane prognozowane (2024-2033) | Predicted Data',
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
                    intersect: false
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