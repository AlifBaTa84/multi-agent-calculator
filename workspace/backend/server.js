
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors'); // Required for frontend to communicate with backend

const app = express();
const port = 3000;

// Middleware
app.use(bodyParser.json());
app.use(cors()); // Enable CORS for all routes

// In-memory storage for history (no database as per constraints)
let calculationHistory = [];
const MAX_HISTORY_LENGTH = 10;

// --- Core Calculator Engine Logic (Adapted from frontend) ---

// Utility: Apply operator to two numbers
function applyOperator(num1, operator, num2) {
    switch (operator) {
        case '+': return num1 + num2;
        case '-': return num1 - num2;
        case '*': return num1 * num2;
        case '/':
            if (num2 === 0) throw new Error('Divide by zero');
            return num1 / num2;
        default: throw new Error('Unknown operator');
    }
}

// Core Calculator Engine: Evaluate expression without eval()
// Handles +, -, *, / with precedence (no parentheses for MVP)
function evaluateExpression(expression) {
    if (!expression || typeof expression !== 'string' || expression.trim() === '') {
        return { result: 'Error', error: 'Invalid expression input' };
    }

    let cleanExpr = expression.replace(/×/g, '*').replace(/÷/g, '/');

    // Basic validation for allowed characters
    if (!/^[0-9+\-*/.]+$/.test(cleanExpr)) {
        return { result: 'Error', error: 'Invalid characters in expression' };
    }

    const tokens = [];
    let currentNumber = '';

    for (let i = 0; i < cleanExpr.length; i++) {
        const char = cleanExpr[i];
        if ((char >= '0' && char <= '9') || char === '.') {
            currentNumber += char;
        } else {
            if (currentNumber !== '') {
                tokens.push(parseFloat(currentNumber));
                currentNumber = '';
            }
            if (['+', '-', '*', '/'].includes(char)) {
                tokens.push(char);
            } else {
                return { result: 'Error', error: 'Syntax Error: Unexpected character' };
            }
        }
    }
    if (currentNumber !== '') {
        tokens.push(parseFloat(currentNumber));
    }

    if (tokens.length === 0) return { result: '0', error: null };
    // Basic validation: ensure expression doesn't start or end with an operator, or have consecutive operators
    if (['+', '-', '*', '/'].includes(tokens[0]) || ['+', '-', '*', '/'].includes(tokens[tokens.length - 1])) {
        return { result: 'Error', error: 'Syntax Error: Invalid operator placement' };
    }
    for (let i = 0; i < tokens.length - 1; i++) {
        if (typeof tokens[i] !== 'number' && typeof tokens[i+1] !== 'number') {
            return { result: 'Error', error: 'Syntax Error: Consecutive operators' };
        }
    }


    let numbers = [];
    let operators = [];

    const precedence = {'+': 1, '-': 1, '*': 2, '/': 2};

    try {
        for (let i = 0; i < tokens.length; i++) {
            let token = tokens[i];

            if (typeof token === 'number') {
                numbers.push(token);
            } else { // It's an operator
                while (
                    operators.length > 0 &&
                    ['+', '-', '*', '/'].includes(operators[operators.length - 1]) &&
                    precedence[operators[operators.length - 1]] >= precedence[token]
                ) {
                    let op = operators.pop();
                    let num2 = numbers.pop();
                    let num1 = numbers.pop();
                    if (num1 === undefined || num2 === undefined) throw new Error('Syntax Error');
                    numbers.push(applyOperator(num1, op, num2));
                }
                operators.push(token);
            }
        }

        // Apply remaining operators
        while (operators.length > 0) {
            let op = operators.pop();
            let num2 = numbers.pop();
            let num1 = numbers.pop();
            if (num1 === undefined || num2 === undefined) throw new Error('Syntax Error');
            numbers.push(applyOperator(num1, op, num2));
        }

        if (numbers.length !== 1) {
            throw new Error('Syntax Error');
        }

        let result = numbers[0];
        if (isNaN(result) || !isFinite(result)) {
            throw new Error('Calculation Error');
        }
        return { result: result.toString(), error: null };

    } catch (e) {
        return { result: 'Error', error: e.message };
    }
}


// --- API Endpoints ---

/**
 * @api {post} /calculate Evaluate a mathematical expression
 * @apiName Calculate
 * @apiGroup Calculator
 *
 * @apiParam {String} expression The mathematical expression to evaluate (e.g., "2+3*4").
 *
 * @apiSuccess {String} result The calculated result.
 * @apiSuccess {String|null} error Error message if calculation failed, otherwise null.
 *
 * @apiSuccessExample Success-Response:
 *     HTTP/1.1 200 OK
 *     {
 *       "result": "14",
 *       "error": null
 *     }
 *
 * @apiError (Error 400) InvalidExpression The expression provided was invalid.
 * @apiErrorExample Error-Response:
 *     HTTP/1.1 400 Bad Request
 *     {
 *       "result": "Error",
 *       "error": "Syntax Error"
 *     }
 */
app.post('/calculate', (req, res) => {
    const { expression } = req.body;

    if (!expression) {
        return res.status(400).json({ result: 'Error', error: 'Expression is required' });
    }

    const { result, error } = evaluateExpression(expression);

    if (error) {
        return res.status(400).json({ result: 'Error', error: error });
    }

    // Add to history
    if (result !== 'Error') {
        calculationHistory.unshift({
            expression: expression,
            result: result,
            timestamp: new Date().toLocaleString()
        });
        if (calculationHistory.length > MAX_HISTORY_LENGTH) {
            calculationHistory.pop();
        }
    }

    res.json({ result, error });
});

/**
 * @api {get} /history Retrieve calculation history
 * @apiName GetHistory
 * @apiGroup History
 *
 * @apiSuccess {Object[]} history Array of past calculations.
 * @apiSuccess {String} history.expression The expression that was evaluated.
 * @apiSuccess {String} history.result The result of the evaluation.
 * @apiSuccess {String} history.timestamp The timestamp of the calculation.
 *
 * @apiSuccessExample Success-Response:
 *     HTTP/1.1 200 OK
 *     {
 *       "history": [
 *         { "expression": "2+2", "result": "4", "timestamp": "10/26/2023, 10:30:00 AM" },
 *         { "expression": "5*3", "result": "15", "timestamp": "10/26/2023, 10:29:45 AM" }
 *       ]
 *     }
 */
app.get('/history', (req, res) => {
    res.json({ history: calculationHistory });
});

/**
 * @api {delete} /history Clear calculation history
 * @apiName ClearHistory
 * @apiGroup History
 *
 * @apiSuccess {String} message Confirmation message.
 *
 * @apiSuccessExample Success-Response:
 *     HTTP/1.1 200 OK
 *     {
 *       "message": "History cleared successfully"
 *     }
 */
app.delete('/history', (req, res) => {
    calculationHistory = [];
    res.json({ message: 'History cleared successfully' });
});

// Start the server
app.listen(port, () => {
    console.log(`Calculator backend listening at http://localhost:${port}`);
});
