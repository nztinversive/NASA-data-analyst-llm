from flask import Flask, render_template, request, jsonify
from utils.data_processor import process_query, get_query_suggestions
from utils.db_manager import save_query, get_query_history
from utils.llama_integration import process_with_llama, get_advanced_query_suggestions
import os
from flask_caching import Cache

app = Flask(__name__)

# Configure Flask-Caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Database configuration
app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL')

@app.route('/')
@cache.cached(timeout=300)  # Cache for 5 minutes
def index():
    suggestions = get_query_suggestions() + get_advanced_query_suggestions()
    return render_template('index.html', suggestions=suggestions)

@app.route('/analyze', methods=['POST'])
def analyze():
    query = request.form.get('query')
    if not query:
        return jsonify({'error': 'Query is required'}), 400

    try:
        result = process_query(query)
        if isinstance(result, dict) and 'error' in result:
            return jsonify(result), 500

        save_query(query, result['data'])

        return jsonify({'result': result['data'], 'chart': result['chart']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/advanced_analyze', methods=['POST'])
def advanced_analyze():
    query = request.form.get('query')
    if not query:
        return jsonify({'error': 'Query is required'}), 400

    try:
        result = process_with_llama(query)
        save_query(query, result)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def history():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    queries = get_query_history(page, per_page)
    return jsonify(queries)

@app.route('/suggestions')
@cache.cached(timeout=3600)  # Cache for 1 hour
def suggestions():
    return jsonify(get_query_suggestions() + get_advanced_query_suggestions())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
