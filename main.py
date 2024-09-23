from flask import Flask, render_template, request, jsonify
from utils.data_processor import process_query
from utils.db_manager import save_query, get_query_history
import os

app = Flask(__name__)

# Database configuration
app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    query = request.form.get('query')
    if not query:
        return jsonify({'error': 'Query is required'}), 400

    try:
        result = process_query(query)
        save_query(query, result)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def history():
    queries = get_query_history()
    return jsonify(queries)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
