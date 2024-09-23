document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('query-form');
    const resultDiv = document.getElementById('result');
    const historyDiv = document.getElementById('history');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const query = document.getElementById('query').value;
        
        if (!query.trim()) {
            showError('Please enter a query');
            return;
        }

        fetch('/analyze', {
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
            }
        })
        .catch(error => {
            showError('An error occurred while processing your request');
        });
    });

    function showResult(result) {
        resultDiv.innerHTML = `<h2>Analysis Result:</h2><pre>${JSON.stringify(result, null, 2)}</pre>`;
        resultDiv.style.display = 'block';
    }

    function showError(message) {
        resultDiv.innerHTML = `<p class="error">${message}</p>`;
        resultDiv.style.display = 'block';
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
