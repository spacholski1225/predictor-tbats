document.addEventListener('DOMContentLoaded', function() {
    // File input related elements
    const fileInput = document.getElementById('dataFileInput');
    const fileNameDisplay = document.getElementById('fileName');
    const loadButton = document.getElementById('loadDataButton');
    const statusMessage = document.getElementById('statusMessage');
    
    // Store chart instance to destroy it before creating a new one
    let fertilityChart = null;
    
    // Default historical data (will be used as fallback if needed)
    const defaultHistoricalData = [
      {
        "year": 1960,
        "tfr": 2.98
      },
      {
        "year": 1961,
        "tfr": 2.83
      },
      // ... more data would be here, truncated for brevity
      {
        "year": 2023,
        "tfr": 1.158
      }
    ];
    
    // Add event listeners for file input
    fileInput.addEventListener('change', function(e) {
        const fileName = e.target.files[0] ? e.target.files[0].name : 'Nie wybrano pliku';
        fileNameDisplay.textContent = fileName;
        
        // Enable or disable load button based on file selection
        loadButton.disabled = !e.target.files[0];
    });
    
    // Add event listener for load button
    loadButton.addEventListener('click', function() {
        const file = fileInput.files[0];
        if (!file) {
            displayStatus('error', 'Proszę najpierw wybrać plik');
            return;
        }
        
        // Display loading status
        displayStatus('loading', 'Ładowanie danych...');
        
        // Read file
        const reader = new FileReader();
        reader.onload = function(e) {
            try {
                // Parse JSON content
                const jsonData = JSON.parse(e.target.result);
                
                // Validate the JSON structure
                if (!Array.isArray(jsonData)) {
                    throw new Error('Dane muszą być tablicą');
                }
                
                // Check if each item has year and tfr properties
                for (let i = 0; i < jsonData.length; i++) {
                    if (typeof jsonData[i].year === 'undefined' || typeof jsonData[i].tfr === 'undefined') {
                        throw new Error(`Element ${i} nie zawiera wymaganych pól 'year' i 'tfr'`);
                    }
                }
                
                // Process the data
                fetchPrediction(jsonData);
                
            } catch (error) {
                console.error('Błąd parsowania pliku JSON:', error);
                displayStatus('error', 'Błąd parsowania pliku JSON: ' + error.message);
            }
        };
        
        reader.onerror = function() {
            displayStatus('error', 'Błąd odczytu pliku');
        };
        
        reader.readAsText(file);
    });
    
    // Function to display status messages
    function displayStatus(type, message) {
        statusMessage.textContent = message;
        statusMessage.className = 'status-message ' + type;
    }
    
    // Function to fetch prediction data from API
    function fetchPrediction(historicalData) {
        console.log('Próba pobrania danych z API przy użyciu przesłanych danych...');
        
        // Clear any previous warnings
        const existingWarnings = document.querySelectorAll('.warning');
        existingWarnings.forEach(warning => warning.remove());
        
        // Attempt to fetch from the API
        fetch('http://52.17.53.243:5000/predictData', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(historicalData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Odpowiedź sieciowa nie była poprawna');
            }
            return response.json();
        })
        .then(data => {
            // Process and display the data
            createChart(data);
            displayStatus('success', 'Dane załadowane pomyślnie');
        })
        .catch(error => {
            console.error('Błąd pobierania danych z API:', error);
            
            // Use fallback mechanism
            handleApiError(error, historicalData);
        });
    }
    
    // Function to handle API errors with fallback
    function handleApiError(error, historicalData) {
        console.log('Używanie lokalnego mechanizmu awaryjnego...');
        
        // Create fallback data with predicted flag
        const fallbackData = [
            // Historical data (from uploaded file)
            ...historicalData.map(item => ({...item, predicted: false})),
            
            // Predicted data (hardcoded based on expected response)
            {"predicted": true, "tfr": 1.099, "year": 2024},
            {"predicted": true, "tfr": 1.035, "year": 2025},
            {"predicted": true, "tfr": 0.973, "year": 2026},
            {"predicted": true, "tfr": 0.913, "year": 2027},
            {"predicted": true, "tfr": 0.854, "year": 2028},
            {"predicted": true, "tfr": 0.797, "year": 2029},
            {"predicted": true, "tfr": 0.741, "year": 2030},
            {"predicted": true, "tfr": 0.688, "year": 2031},
            {"predicted": true, "tfr": 0.635, "year": 2032},
            {"predicted": true, "tfr": 0.585, "year": 2033}
        ];
        
        // Use the fallback data to create the chart
        createChart(fallbackData);
        
        // Check if it's a CORS error
        const isCorsError = error.message.includes('CORS') ||
                           (error instanceof TypeError && error.message === 'Failed to fetch');
        
        if (isCorsError) {
            displayStatus('error', 'Błąd CORS: Używamy lokalnych danych. To normalne przy otwieraniu pliku HTML bezpośrednio z dysku.');
        } else {
            displayStatus('error', 'Uwaga: Używamy lokalnych danych, ponieważ nie można połączyć się z API.');
        }
        
        // Show a warning message that we're using fallback data
        const warningEl = document.createElement('div');
        warningEl.className = 'warning';
        
        if (isCorsError) {
            warningEl.innerHTML = '<strong>Błąd CORS:</strong> Używamy lokalnych danych, ponieważ przeglądarka zablokowała dostęp do API ze względów bezpieczeństwa. ' +
                                 'To normalne przy otwieraniu pliku HTML bezpośrednio z dysku.';
        } else {
            warningEl.innerHTML = 'Uwaga: Używamy lokalnych danych, ponieważ nie można połączyć się z API. ' +
                                 'Dane prognozy mogą nie być aktualne.';
        }
        
        document.querySelector('.chart-container').insertAdjacentElement('beforebegin', warningEl);
    }
    
    // Load default data on page load (optional)
    // Uncomment the following line if you want to load data automatically on page load
    // fetchPrediction(defaultHistoricalData);
    
    // Function to create or update the chart
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
    
    // Destroy existing chart if it exists
    if (fertilityChart) {
        fertilityChart.destroy();
    }
    
    // Create the chart
    fertilityChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: years,
            datasets: [
                {
                    label: 'Dane historyczne',
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
                    label: 'Dane prognozowane',
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
                        text: 'Rok'
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
                        text: 'Wskaźnik Dzietności (TFR)'
                    },
                    min: 0,
                    suggestedMax: 3.5
                }
            }
        }
    });
}
});