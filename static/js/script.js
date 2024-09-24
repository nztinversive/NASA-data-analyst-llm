document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('query-form');
    const resultDiv = document.getElementById('result');
    const chartDiv = document.getElementById('chart');
    const historyDiv = document.getElementById('history');
    const suggestionLinks = document.querySelectorAll('.suggestion');
    const analyzeBtn = document.getElementById('analyze-btn');
    const advancedAnalyzeBtn = document.getElementById('advanced-analyze-btn');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const query = document.getElementById('query').value;
        
        if (!query.trim()) {
            showError('Please enter a query');
            return;
        }

        analyzeQuery(query, false);
    });

    advancedAnalyzeBtn.addEventListener('click', function(e) {
        e.preventDefault();
        const query = document.getElementById('query').value;
        
        if (!query.trim()) {
            showError('Please enter a query');
            return;
        }

        analyzeQuery(query, true);
    });

    suggestionLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const query = this.textContent;
            document.getElementById('query').value = query;
            analyzeQuery(query, false);
        });
    });

    function analyzeQuery(query, isAdvanced) {
        const endpoint = isAdvanced ? '/advanced_analyze' : '/analyze';
        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `query=${encodeURIComponent(query)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
            } else {
                showResult(data.result);
                if (data.chart) {
                    showChart(data.chart);
                } else {
                    chartDiv.style.display = 'none';
                }
            }
        })
        .catch(error => {
            showError('An error occurred while processing your request');
        });
    }

    function showResult(result) {
        resultDiv.innerHTML = `<h2>Analysis Result:</h2><pre>${typeof result === 'string' ? result : JSON.stringify(result, null, 2)}</pre>`;
        resultDiv.style.display = 'block';
    }

    function showChart(chartData) {
        chartDiv.style.display = 'block';
        const parsedChartData = JSON.parse(chartData);
        
        // Create a responsive layout
        const layout = {
            autosize: true,
            margin: { l: 50, r: 30, b: 50, t: 50, pad: 4 },
            updatemenus: parsedChartData[0].layout.updatemenus
        };

        // Create the plot with all chart types
        Plotly.newPlot('chart', parsedChartData.map(chart => chart.data).flat(), layout, {
            scrollZoom: true,
            editable: true,
            modeBarButtonsToAdd: ['hoverClosestGl2d', 'toggleSpikelines', 'resetScale2d'],
            responsive: true
        });

        // Add event listener for button clicks
        parsedChartData[0].layout.updatemenus[0].buttons.forEach((button, index) => {
            button.click = function() {
                Plotly.update('chart', 
                    {'visible': parsedChartData.map((_, i) => i === index)},
                    {'title': button.args[1].title}
                );
            };
        });

        // Make the chart responsive
        function resizeChart() {
            const chartContainer = document.getElementById('chart');
            Plotly.relayout('chart', {
                width: chartContainer.clientWidth,
                height: Math.max(300, window.innerHeight * 0.6)
            });
        }

        window.addEventListener('resize', resizeChart);
        resizeChart();

        // Add color customization
        addColorCustomization(parsedChartData);
    }

    function addColorCustomization(parsedChartData) {
        const colorSchemes = {
            'Default': {'Completed': '#1f77b4', 'Ongoing': '#ff7f0e'},
            'High Contrast': {'Completed': '#000000', 'Ongoing': '#ff0000'},
            'Pastel': {'Completed': '#b3e2cd', 'Ongoing': '#fdcdac'}
        };

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

        colorSchemeSelect.addEventListener('change', function() {
            const selectedScheme = colorSchemes[this.value];
            Plotly.restyle('chart', {
                'marker.color': [parsedChartData[0].data.map(trace => selectedScheme[trace.name] || trace.marker.color)]
            });
        });
    }

    function showError(message) {
        resultDiv.innerHTML = `<p class="error">${message}</p>`;
        resultDiv.style.display = 'block';
        chartDiv.style.display = 'none';
    }

    function loadQueryHistory() {
        fetch('/history')
        .then(response => response.json())
        .then(data => {
            historyDiv.innerHTML = '<h2>Query History:</h2>';
            const ul = document.createElement('ul');
            data.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `Query: ${item.query}, Result: ${JSON.stringify(item.result)}`;
                ul.appendChild(li);
            });
            historyDiv.appendChild(ul);
        })
        .catch(error => {
            historyDiv.innerHTML = '<p class="error">Failed to load query history</p>';
        });
    }

    loadQueryHistory();
});
