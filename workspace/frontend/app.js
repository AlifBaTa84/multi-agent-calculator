class Calculator {
    constructor(previousOperandTextElement, currentOperandTextElement) {
        this.previousOperandTextElement = previousOperandTextElement;
        this.currentOperandTextElement = currentOperandTextElement;
        this.allClear(); // Initialize the calculator state
    }

    allClear() {
        this.currentOperand = '0';
        this.previousOperand = '';
        this.operation = undefined;
    }

    clear() {
        // Clears the current input/entry
        this.currentOperand = '0';
    }

    inputDigit(digit) {
        if (digit === '.' && this.currentOperand.includes('.')) return;
        // If currentOperand is '0' and the new digit is not '.', replace '0' with the digit.
        // Otherwise, append the digit.
        if (this.currentOperand === '0' && digit !== '.') {
            this.currentOperand = digit;
        } else {
            this.currentOperand = this.currentOperand.toString() + digit.toString();
        }
    }

    inputOperation(operation) {
        if (this.currentOperand === '') return; // Don't allow operations if no current number
        if (this.previousOperand !== '') {
            // If there's a previous operand and operation, compute the result before setting a new operation
            this.equals();
        }
        this.operation = operation;
        this.previousOperand = this.currentOperand; // Move current operand to previous operand
        this.currentOperand = ''; // Clear current operand for new input
    }

    equals() {
        let computation;
        const prev = parseFloat(this.previousOperand);
        const current = parseFloat(this.currentOperand);
        if (isNaN(prev) || isNaN(current)) return; // Don't compute if numbers are invalid

        switch (this.operation) {
            case '+':
                computation = prev + current;
                break;
            case '-':
                computation = prev - current;
                break;
            case '*':
                computation = prev * current;
                break;
            case '/': // Internal representation for division
                computation = prev / current;
                break;
            default:
                return; // No operation chosen
        }
        this.currentOperand = computation;
        this.operation = undefined; // Clear the operation after computation
        this.previousOperand = ''; // Clear previous operand
    }

    getDisplayValue(number) {
        // Formats the number for display, handling decimals and commas
        const stringNumber = number.toString();
        const integerDigits = parseFloat(stringNumber.split('.')[0]);
        const decimalDigits = stringNumber.split('.')[1];
        let integerDisplay;
        if (isNaN(integerDigits)) {
            integerDisplay = '';
        } else {
            integerDisplay = integerDigits.toLocaleString('en', { maximumFractionDigits: 0 });
        }
        if (decimalDigits != null) {
            return `${integerDisplay}.${decimalDigits}`;
        } else {
            return integerDisplay;
        }
    }

    updateDisplay() {
        this.currentOperandTextElement.innerText = this.getDisplayValue(this.currentOperand);
        if (this.operation != null) {
            // Map internal operator to display symbol
            const displayOperation = this.operation === '/' ? '÷' : this.operation === '*' ? '×' : this.operation;
            this.previousOperandTextElement.innerText = 
                `${this.getDisplayValue(this.previousOperand)} ${displayOperation}`;
        } else {
            this.previousOperandTextElement.innerText = '';
        }
    }
}

const numberButtons = document.querySelectorAll('[data-number]');
const operatorButtons = document.querySelectorAll('[data-operator]');
const equalsButton = document.querySelector('[data-equals]');
const clearButton = document.querySelector('[data-clear]'); // 'C'
const allClearButton = document.querySelector('[data-all-clear]'); // 'AC'
const previousOperandTextElement = document.querySelector('[data-previous-operand]');
const currentOperandTextElement = document.querySelector('[data-current-operand]');

const calculator = new Calculator(previousOperandTextElement, currentOperandTextElement);

numberButtons.forEach(button => {
    button.addEventListener('click', () => {
        calculator.inputDigit(button.innerText);
        calculator.updateDisplay();
    });
});

operatorButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Ensure internal representation of operators is consistent (e.g., '*' for '×', '/' for '÷')
        let operation = button.getAttribute('operator-type'); // Get original operator type from data attribute
        switch (operation) {
            case 'division':
                operation = '/';
                break;
            case 'multiplication':
                operation = '*';
                break;
            case 'addition':
                operation = '+';
                break;
            case 'subtract':
                operation = '-';
                break;
        }
        calculator.inputOperation(operation);
        calculator.updateDisplay();
    });
});

equalsButton.addEventListener('click', button => {
    calculator.equals();
    calculator.updateDisplay();
});

allClearButton.addEventListener('click', button => {
    calculator.allClear();
    calculator.updateDisplay();
});

clearButton.addEventListener('click', button => {
    calculator.clear();
    calculator.updateDisplay();
});

// Initial display update
calculator.updateDisplay();
