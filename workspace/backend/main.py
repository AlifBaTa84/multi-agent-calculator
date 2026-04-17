from flask import Flask, request, jsonify
from flask_cors import CORS # Import CORS
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# In-memory storage for calculation history
# In a real application, this would be a database
calculation_history = []

@app.route('/history', methods=['GET'])
def get_history():
    """
    Returns all stored calculation history entries.
    """
    return jsonify(calculation_history)

@app.route('/history', methods=['POST'])
def add_history_entry():
    """
    Adds a new calculation history entry.
    Request body should contain 'expression' and 'result'.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    
    expression = data.get('expression')
    result = data.get('result')

    if not all([expression, result]):
        return jsonify({"error": "Missing 'expression' or 'result' in request body"}), 400

    # Basic input validation to ensure they are strings for expression and convertible for result
    if not isinstance(expression, str):
        return jsonify({"error": "'expression' must be a string."}), 400
    
    try:
        # Try to convert result to a string if it's not already
        result_str = str(result)
    except Exception:
        return jsonify({"error": "'result' could not be converted to a string."}), 400

    new_entry = {
        "id": str(uuid.uuid4()),
        "expression": expression,
        "result": result_str,
        "timestamp": datetime.now().isoformat()
    }
    calculation_history.append(new_entry)
    return jsonify(new_entry), 201

@app.route('/history', methods=['DELETE'])
def clear_history():
    """
    Clears all calculation history entries.
    """
    global calculation_history
    calculation_history = []
    return jsonify({"message": "Calculation history cleared"}), 200

@app.route('/health', methods=['GET'])
def health_check():
    """
    Basic health check endpoint.
    """
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    # For local development, run with `python main.py`
    # In a production environment, use a WSGI server like Gunicorn
    app.run(debug=True, port=5000)