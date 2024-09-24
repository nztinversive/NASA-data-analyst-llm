// Wait for the DOM to be fully loaded before executing the script
document.addEventListener('DOMContentLoaded', function() {
    // Cache DOM elements for better performance
    const form = document.getElementById('mission-form');
    const resultDiv = document.getElementById('result');
    const chartDiv = document.getElementById('chart');
    const historyDiv = document.getElementById('history');
    const suggestionLinks = document.querySelectorAll('.suggestion');
    const analyzeBtn = document.getElementById('analyze-btn');
    const advancedAnalyzeBtn = document.getElementById('advanced-analyze-btn');

    // Initialize pagination variables
    let currentPage = 1;
    const itemsPerPage = 10;

    // Event listener for form submission (standard analysis)
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const mission = document.getElementById('mission').value;
        
        if (!mission.trim()) {
            showError('Please enter a mission');
            return;
        }

        analyzeMission(mission, false);
    });

    // Event listener for advanced analysis button
    advancedAnalyzeBtn.addEventListener('click', function(e) {
        e.preventDefault();
        const mission = document.getElementById('mission').value;
        
        if (!mission.trim()) {
            showError('Please enter a mission');
            return;
        }

        analyzeMission(mission, true);
    });

    // Add click event listeners to suggestion links
    suggestionLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const mission = this.textContent;
            document.getElementById('mission').value = mission;
            analyzeMission(mission, false);
        });
    });

    // Function to send mission to server for analysis
    function analyzeMission(mission, isAdvanced) {
        const endpoint = isAdvanced ? '/advanced_analyze' : '/analyze';
        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `mission=${encodeURIComponent(mission)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
            } else {
                displayResults(data.result, data.chart);
                loadMissionHistory(); // Refresh the mission history
            }
        })
        .catch(error => {
            showError('An error occurred while processing your request');
        });
    }

    // Function to display analysis results
    function displayResults(result, chartData) {
        const resultContent = document.getElementById('result-content');
        const chartContent = document.getElementById('chart-content');
        const analysisResults = document.getElementById('analysis-results');

        resultContent.innerHTML = '';
        
        if (Array.isArray(result)) {
            result.forEach(item => {
                const resultItem = document.createElement('div');
                resultItem.className = 'result-item';
                resultItem.innerHTML = `
                    <h4>${item.name || 'Result'}</h4>
                    <p>${item.value || item}</p>
                `;
                resultContent.appendChild(resultItem);
            });
        } else if (typeof result === 'object') {
            for (const [key, value] of Object.entries(result)) {
                const resultItem = document.createElement('div');
                resultItem.className = 'result-item';
                resultItem.innerHTML = `
                    <h4>${key}</h4>
                    <p>${value}</p>
                `;
                resultContent.appendChild(resultItem);
            }
        } else {
            resultContent.innerHTML = `<p>${result}</p>`;
        }

        if (chartData) {
            Plotly.newPlot('chart-content', JSON.parse(chartData));
            chartContent.style.display = 'block';
        } else {
            chartContent.style.display = 'none';
        }

        analysisResults.style.display = 'block';
    }

    // Function to display chart using Plotly
    function showChart(chartData) {
        chartDiv.style.display = 'block';
        const parsedChartData = JSON.parse(chartData);
        
        // Create a new plot with Plotly
        Plotly.newPlot('chart', parsedChartData.data, parsedChartData.layout, {
            responsive: true,
            scrollZoom: true,
            displayModeBar: true,
            modeBarButtonsToAdd: ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d']
        });

        // Add color customization options
        addColorCustomization(parsedChartData);

        // Resize chart on window resize
        function resizeChart() {
            Plotly.Plots.resize('chart');
        }

        window.addEventListener('resize', resizeChart);
    }

    // Function to add color customization options to the chart
    function addColorCustomization(parsedChartData) {
        const colorSchemes = {
            'Default': {'Completed': '#1f77b4', 'Ongoing': '#ff7f0e'},
            'High Contrast': {'Completed': '#000000', 'Ongoing': '#ff0000'},
            'Pastel': {'Completed': '#b3e2cd', 'Ongoing': '#fdcdac'}
        };

        // Create color scheme selection dropdown
        const colorSchemeSelect = document.createElement('select');
        colorSchemeSelect.id = 'color-scheme-select';
        Object.keys(colorSchemes).forEach(scheme => {
            const option = document.createElement('option');
            option.value = scheme;
            option.textContent = scheme;
            colorSchemeSelect.appendChild(option);
        });

        const colorSchemeLabel = document.createElement('label');
        colorSchemeLabel.htmlFor = 'color-scheme-select';
        colorSchemeLabel.textContent = 'Color Scheme: ';

        const colorSchemeContainer = document.createElement('div');
        colorSchemeContainer.appendChild(colorSchemeLabel);
        colorSchemeContainer.appendChild(colorSchemeSelect);

        chartDiv.insertBefore(colorSchemeContainer, chartDiv.firstChild);

        // Event listener for color scheme changes
        colorSchemeSelect.addEventListener('change', function() {
            const selectedScheme = colorSchemes[this.value];
            Plotly.restyle('chart', {
                'marker.color': [parsedChartData.data.map(trace => selectedScheme[trace.name] || trace.marker.color)]
            });
        });
    }

    // Function to display error messages
    function showError(message) {
        resultDiv.innerHTML = `<p class="error">${message}</p>`;
        resultDiv.style.display = 'block';
        chartDiv.style.display = 'none';
    }

    // Function to load and display mission history
    function loadMissionHistory() {
        fetch(`/history?page=${currentPage}&per_page=${itemsPerPage}`)
        .then(response => response.json())
        .then(data => {
            displayMissionHistory(data);
            updatePaginationButtons(data.length === itemsPerPage);
        })
        .catch(error => {
            console.error('Error loading mission history:', error);
        });
    }

    // Function to display mission history
    function displayMissionHistory(missions) {
        const historyList = document.getElementById('history-list');
        historyList.innerHTML = '';

        missions.forEach(mission => {
            const li = document.createElement('li');
            li.textContent = mission.mission;
            li.addEventListener('click', () => {
                document.getElementById('mission').value = mission.mission;
                analyzeMission(mission.mission, false);
            });
            historyList.appendChild(li);
        });
    }

    // Function to update pagination buttons
    function updatePaginationButtons(hasNextPage) {
        const prevButton = document.getElementById('prev-page');
        const nextButton = document.getElementById('next-page');

        prevButton.disabled = currentPage === 1;
        nextButton.disabled = !hasNextPage;
    }

    // Add event listeners for pagination buttons
    document.getElementById('prev-page').addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            loadMissionHistory();
        }
    });

    document.getElementById('next-page').addEventListener('click', () => {
        currentPage++;
        loadMissionHistory();
    });

    // Load mission history when the page loads
    loadMissionHistory();
});
