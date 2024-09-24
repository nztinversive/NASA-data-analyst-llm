// Wait for the DOM to be fully loaded before executing the script
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('mission-form');
    const resultContent = document.getElementById('result-content');
    const chartContent = document.getElementById('chart-content');
    const historyDiv = document.getElementById('history');
    const suggestionLinks = document.querySelectorAll('.suggestion');
    const analyzeBtn = document.getElementById('analyze-btn');
    const advancedAnalyzeBtn = document.getElementById('advanced-analyze-btn');

    let currentPage = 1;
    const itemsPerPage = 10;

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const mission = document.getElementById('mission').value;
        
        if (!mission.trim()) {
            showError('Please enter a mission');
            return;
        }

        analyzeMission(mission, false);
    });

    advancedAnalyzeBtn.addEventListener('click', function(e) {
        e.preventDefault();
        const mission = document.getElementById('mission').value;
        
        if (!mission.trim()) {
            showError('Please enter a mission');
            return;
        }

        analyzeMission(mission, true);
    });

    suggestionLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const mission = this.textContent.trim();
            document.getElementById('mission').value = mission;
            analyzeMission(mission, false);
        });
    });

    function analyzeMission(mission, isAdvanced) {
        showLoading();
        const endpoint = isAdvanced ? '/advanced_analyze' : '/analyze';
        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `mission=${encodeURIComponent(mission)}`
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => {
                    throw new Error(`HTTP error! status: ${response.status}, message: ${text}`);
                });
            }
            return response.json();
        })
        .then(data => {
            hideLoading();
            if (data.error) {
                showError(data.error);
            } else {
                displayResults(data.result, data.chart);
                loadMissionHistory();
            }
        })
        .catch(error => {
            hideLoading();
            showError('An error occurred while processing your request: ' + error.message);
            console.error('Fetch error:', error);
        });
    }

    function displayResults(result, chartData) {
        resultContent.innerHTML = '';
        
        if (Array.isArray(result)) {
            result.forEach(item => {
                const resultItem = document.createElement('div');
                resultItem.className = 'result-item';
                resultItem.innerHTML = `
                    <h4>${item.name || 'Result'}</h4>
                    <p>${formatText(item.value || item)}</p>
                `;
                resultContent.appendChild(resultItem);
            });
        } else if (typeof result === 'object') {
            for (const [key, value] of Object.entries(result)) {
                const resultItem = document.createElement('div');
                resultItem.className = 'result-item';
                resultItem.innerHTML = `
                    <h4>${key}</h4>
                    <p>${formatText(value)}</p>
                `;
                resultContent.appendChild(resultItem);
            }
        } else {
            resultContent.innerHTML = `<p>${formatText(result)}</p>`;
        }

        if (chartData) {
            Plotly.newPlot('chart-content', JSON.parse(chartData));
            chartContent.style.display = 'block';
        } else {
            chartContent.style.display = 'none';
        }

        document.getElementById('analysis-results').style.display = 'block';
    }

    function formatText(text) {
        // Split the text into sentences
        const sentences = text.split(/(?<=[.!?])\s+/);
        // Join sentences with line breaks
        return sentences.join('<br><br>');
    }

    function showLoading() {
        resultContent.innerHTML = '<div class="loading">Processing your cosmic mission...</div>';
        resultContent.style.display = 'block';
        chartContent.style.display = 'none';
    }

    function hideLoading() {
        const loadingElement = resultContent.querySelector('.loading');
        if (loadingElement) {
            loadingElement.remove();
        }
    }

    function showError(message) {
        if (resultContent) {
            resultContent.innerHTML = `<p class="error">${message}</p>`;
            resultContent.style.display = 'block';
        }
        if (chartContent) {
            chartContent.style.display = 'none';
        }
    }

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

    function updatePaginationButtons(hasNextPage) {
        const prevButton = document.getElementById('prev-page');
        const nextButton = document.getElementById('next-page');

        prevButton.disabled = currentPage === 1;
        nextButton.disabled = !hasNextPage;
    }

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

    loadMissionHistory();
});
