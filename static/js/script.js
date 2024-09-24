document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('query-form');
    const resultDiv = document.getElementById('result');
    const chartDiv = document.getElementById('chart');
    const historyDiv = document.getElementById('history');
    const suggestionLinks = document.querySelectorAll('.suggestion');
    const analyzeBtn = document.getElementById('analyze-btn');
    const advancedAnalyzeBtn = document.getElementById('advanced-analyze-btn');

    let currentPage = 1;
    const itemsPerPage = 10;

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
        
        Plotly.newPlot('chart', parsedChartData.data, parsedChartData.layout, {
            responsive: true,
            scrollZoom: true,
            displayModeBar: true,
            modeBarButtonsToAdd: ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d']
        });

        addColorCustomization(parsedChartData);

        function resizeChart() {
            Plotly.Plots.resize('chart');
        }

        window.addEventListener('resize', resizeChart);
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
                'marker.color': [parsedChartData.data.map(trace => selectedScheme[trace.name] || trace.marker.color)]
            });
        });
    }

    function showError(message) {
        resultDiv.innerHTML = `<p class="error">${message}</p>`;
        resultDiv.style.display = 'block';
        chartDiv.style.display = 'none';
    }

    function loadQueryHistory() {
        fetch(`/history?page=${currentPage}&per_page=${itemsPerPage}`)
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

            // Add pagination controls
            const paginationDiv = document.createElement('div');
            paginationDiv.className = 'pagination';
            
            const prevButton = document.createElement('button');
            prevButton.textContent = 'Previous';
            prevButton.addEventListener('click', () => {
                if (currentPage > 1) {
                    currentPage--;
                    loadQueryHistory();
                }
            });
            
            const nextButton = document.createElement('button');
            nextButton.textContent = 'Next';
            nextButton.addEventListener('click', () => {
                currentPage++;
                loadQueryHistory();
            });
            
            paginationDiv.appendChild(prevButton);
            paginationDiv.appendChild(nextButton);
            historyDiv.appendChild(paginationDiv);
        })
        .catch(error => {
            historyDiv.innerHTML = '<p class="error">Failed to load query history</p>';
        });
    }

    loadQueryHistory();
});
