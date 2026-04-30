from flask import Flask, request, jsonify
import math
import re

app = Flask(__name__)

# In-memory data structures
history = []
memory = 0.0
current_theme = "light" # Placeholder, theme is mostly client-side

# Consistent error format
def error_response(message, status_code=400):
    return jsonify({"error": message}), status_code

# Operator precedence and associativity
OPERATORS = {
    '+': {'precedence': 1, 'associativity': 'left'},
    '-': {'precedence': 1, 'associativity': 'left'},
    '*': {'precedence': 2, 'associativity': 'left'},
    '/': {'precedence': 2, 'associativity': 'left'},
    '^': {'precedence': 3, 'associativity': 'right'},
}

# Functions (treated as operators with high precedence)
FUNCTION_PRECEDENCE = 4 # Higher than all binary operators

FUNCTIONS_MAP = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log10, # Base 10
    'ln': math.log,   # Natural log
    'sqrt': math.sqrt,
}

CONSTANTS_MAP = {
    'pi': math.pi,
    'e': math.e,
}

# Helper to get precedence and associativity for a token
def get_token_info(token):
    if token in OPERATORS:
        return OPERATORS[token]['precedence'], OPERATORS[token]['associativity']
    if token in FUNCTIONS_MAP:
        return FUNCTION_PRECEDENCE, 'right' # Functions are typically right-associative (e.g., sin(cos(x)))
    return None, None # Not an operator or function

# Tokenizer
def robust_tokenize(expression_str):
    tokens = []
    token_specs = [
        ('NUMBER',   r'\d+\.\d+|\d+'),
        ('FUNCTION', r'|'.join(re.escape(f) for f in sorted(FUNCTIONS_MAP.keys(), key=len, reverse=True))),
        ('CONSTANT', r'|'.join(re.escape(c) for c in sorted(CONSTANTS_MAP.keys(), key=len, reverse=True))),
        ('OPERATOR', r'\+|\-|\*|\/|\^'),
        ('LPAREN',   r'\('),
        ('RPAREN',   r'\)'),
        ('WHITESPACE', r'\s+'),
    ]

    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specs)
    get_token = re.compile(token_regex).match

    i = 0
    while i < len(expression_str):
        match = get_token(expression_str, i)
        if match:
            token_type = match.lastgroup
            token_value = match.group(token_type)
            
            if token_type == 'WHITESPACE':
                pass
            else:
                tokens.append(token_value)
            
            i = match.end()
        else:
            return None, f"Invalid character in expression: '{expression_str[i]}' at position {i}"
    
    return tokens, None

# Shunting-Yard Algorithm (Infix to Postfix)
def shunting_yard(tokens):
    output_queue = []
    operator_stack = []

    for token in tokens:
        if token in CONSTANTS_MAP:
            output_queue.append(CONSTANTS_MAP[token])
        elif token in FUNCTIONS_MAP:
            operator_stack.append(token)
        elif token.replace('.', '', 1).isdigit(): # Check if it's a number (int or float)
            output_queue.append(float(token))
        elif token in OPERATORS:
            op1_precedence, op1_associativity = get_token_info(token)
            
            while (operator_stack and 
                   operator_stack[-1] != '(' and
                   get_token_info(operator_stack[-1])[0] is not None): # Ensure stack top is an operator/function
                
                op2_precedence, op2_associativity = get_token_info(operator_stack[-1])
                
                if ((op2_precedence > op1_precedence) or
                    (op2_precedence == op1_precedence and op1_associativity == 'left')):
                    output_queue.append(operator_stack.pop())
                else:
                    break
            operator_stack.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            if not operator_stack:
                return None, "Mismatched parentheses"
            operator_stack.pop() # Pop '('
            if operator_stack and operator_stack[-1] in FUNCTIONS_MAP: # If function was before '(', pop it
                output_queue.append(operator_stack.pop())
        else:
            return None, f"Unknown token: {token}"

    while operator_stack:
        if operator_stack[-1] == '(':
            return None, "Mismatched parentheses"
        output_queue.append(operator_stack.pop())
    
    return output_queue, None

# RPN Evaluator
def evaluate_rpn(rpn_tokens):
    value_stack = []
    
    for token in rpn_tokens:
        if isinstance(token, (int, float)):
            value_stack.append(token)
        elif token in OPERATORS:
            if len(value_stack) < 2:
                return None, "Invalid expression: not enough operands for operator"
            operand2 = value_stack.pop()
            operand1 = value_stack.pop()
            
            try:
                if token == '+':
                    result = operand1 + operand2
                elif token == '-':
                    result = operand1 - operand2
                elif token == '*':
                    result = operand1 * operand2
                elif token == '/':
                    if operand2 == 0:
                        return None, "Division by zero"
                    result = operand1 / operand2
                elif token == '^':
                    result = operand1 ** operand2
                else:
                    return None, f"Unknown operator: {token}"
                value_stack.append(result)
            except OverflowError:
                return None, "Calculation resulted in a number too large or too small"
            except Exception as e:
                return None, f"Calculation error: {str(e)}"
        elif token in FUNCTIONS_MAP:
            if len(value_stack) < 1:
                return None, "Invalid expression: not enough operands for function"
            operand = value_stack.pop()
            try:
                if token == 'sqrt' and operand < 0:
                    return None, "Cannot take square root of a negative number"
                if token in ['log', 'ln'] and operand <= 0:
                    return None, "Cannot take logarithm of a non-positive number"
                
                result = FUNCTIONS_MAP[token](operand)
                value_stack.append(result)
            except ValueError as e:
                return None, f"Mathematical error: {str(e)}"
            except Exception as e:
                return None, f"Function calculation error: {str(e)}"
        else:
            return None, f"Unknown token in RPN: {token}"
            
    if len(value_stack) != 1:
        return None, "Invalid expression: too many operands or operators"
    
    return value_stack[0], None

def calculate_expression(expression):
    tokens, error = robust_tokenize(expression)
    if error:
        return None, error

    # Handle unary minus by inserting '0'
    processed_tokens = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '-':
            # It's unary if it's at the beginning, or after an opening parenthesis, or after another operator
            is_unary = (i == 0 or 
                        tokens[i-1] == '(' or 
                        (tokens[i-1] in OPERATORS and tokens[i-1] != ')')) # Exclude ')' to avoid '5- -2' -> '5-0-2'
            
            # Ensure the next token is a number, function, or constant
            if is_unary and i + 1 < len(tokens) and (tokens[i+1].replace('.', '', 1).isdigit() or tokens[i+1] in FUNCTIONS_MAP or tokens[i+1] in CONSTANTS_MAP):
                processed_tokens.append('0')
        processed_tokens.append(token)
        i += 1
    tokens = processed_tokens

    rpn_tokens, error = shunting_yard(tokens)
    if error:
        return None, error
    
    result, error = evaluate_rpn(rpn_tokens)
    if error:
        return None, error
    
    return result, None

# --- API Endpoints ---

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expression = data.get('expression')

    if not expression:
        return error_response("Expression is required.")

    result, error = calculate_expression(expression)

    if error:
        return error_response(error)
    
    # Add to history
    history.append({"expression": expression, "result": str(result)})
    # Keep history size manageable, e.g., last 20 entries
    if len(history) > 20:
        history.pop(0) # Remove oldest entry

    return jsonify({"result": str(result)})

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify({"history": history})

@app.route('/history/add', methods=['POST'])
def add_history_entry():
    data = request.get_json()
    expression = data.get('expression')
    result = data.get('result')

    if not expression or result is None:
        return error_response("Expression and result are required.")
    
    history.append({"expression": expression, "result": str(result)})
    if len(history) > 20:
        history.pop(0)
    
    return jsonify({"message": "History entry added successfully."}))

@app.route('/history/clear', methods=['POST'])
def clear_history():
    global history
    history = []
    return jsonify({"message": "History cleared successfully."})

@app.route('/memory/add', methods=['POST'])
def memory_add():
    global memory
    data = request.get_json()
    value = data.get('value')

    if value is None:
        return error_response("Value is required.")
    
    try:
        memory += float(value)
    except ValueError:
        return error_response("Invalid value for memory operation.")
    
    return jsonify({"message": "Value added to memory.", "memory": memory})

@app.route('/memory/subtract', methods=['POST'])
def memory_subtract():
    global memory
    data = request.get_json()
    value = data.get('value')

    if value is None:
        return error_response("Value is required.")
    
    try:
        memory -= float(value)
    except ValueError:
        return error_response("Invalid value for memory operation.")
    
    return jsonify({"message": "Value subtracted from memory.", "memory": memory})

@app.route('/memory/recall', methods=['GET'])
def memory_recall():
    return jsonify({"memory": memory})

@app.route('/memory/clear', methods=['POST'])
def memory_clear():
    global memory
    memory = 0.0
    return jsonify({"message": "Memory cleared successfully."})

@app.route('/theme', methods=['POST'])
def set_theme():
    global current_theme
    data = request.get_json()
    theme = data.get('theme')

    if theme not in ['light', 'dark']:
        return error_response("Invalid theme. Must be 'light' or 'dark'.")
    
    current_theme = theme
    return jsonify({"message": f"Theme set to {current_theme}.", "theme": current_theme})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
