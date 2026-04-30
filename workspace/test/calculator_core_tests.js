
// workspace/test/calculator_core_tests.js
let errorState = { isError: false, message: '' };

const CalculatorCore = {
    calculate: function(expression) {
        try {
            // Basic validation to prevent arbitrary code execution (limited for eval)
            // This is a simple client-side calculator, so eval is used for convenience.
            // For a production app, a safer math expression parser would be needed.
            if (!/^[0-9+\-*/().\s^e\piM]+$/.test(expression)) {
                throw new Error('Invalid characters in expression.');
            }

            let evalExpression = expression
                .replace(/sin\(/g, 'Math.sin(')
                .replace(/cos\(/g, 'Math.cos(')
                .replace(/tan\(/g, 'Math.tan(')
                .replace(/log\(/g, 'Math.log10(') // Common log base 10
                .replace(/ln\(/g, 'Math.log(')    // Natural log
                .replace(/sqrt\(/g, 'Math.sqrt(')
                .replace(/\^/g, '**') // Power operator
                .replace(/pi/g, 'Math.PI')
                .replace(/e/g, 'Math.E');

            let result = eval(evalExpression);

            if (isNaN(result) || !isFinite(result)) {
                throw new Error('Invalid mathematical operation.');
            }
            return result.toString();
        } catch (e) {
            errorState = { isError: true, message: e.message };
            return 'Error';
        }
    }
};

function runTest(name, expression, expectedResult, expectedError = false) {
    errorState = { isError: false, message: '' }; // Reset error state for each test
    const actualResult = CalculatorCore.calculate(expression);
    const testPassed = (actualResult === expectedResult && errorState.isError === expectedError);
    console.log(`Test: ${name}`);
    console.log(`  Expression: ${expression}`);
    console.log(`  Expected: ${expectedResult} (Error: ${expectedError})`);
    console.log(`  Actual: ${actualResult} (Error: ${errorState.isError})`);
    console.log(`  Status: ${testPassed ? 'PASSED' : 'FAILED'}\n`);
    return testPassed;
}

let totalTests = 0;
let passedTests = 0;
let failedTests = 0;

function assert(name, expression, expectedResult, expectedError = false) {
    totalTests++;
    if (runTest(name, expression, expectedResult, expectedError)) {
        passedTests++;
    } else {
        failedTests++;
    }
}

console.log("--- CalculatorCore.calculate Tests ---");

// Basic Arithmetic
assert("Addition 1", "1+1", "2");
assert("Addition 2 (decimals)", "10.5+20.5", "31");
assert("Subtraction 1", "5-3", "2");
assert("Subtraction 2 (decimals)", "10.5-2.3", "8.2");
assert("Multiplication 1", "2*3", "6");
assert("Multiplication 2 (decimals)", "1.5*4", "6");
assert("Division 1", "10/2", "5");
assert("Division 2 (decimals)", "7/3", "2.3333333333333335"); // JavaScript float precision
assert("Mixed operations 1", "1+2*3", "7");
assert("Mixed operations 2 (parentheses)", "(1+2)*3", "9");

// Scientific Functions (Radians for sin/cos/tan)
assert("sin(0)", "sin(0)", "0");
assert("sin(PI/2)", `sin(${Math.PI}/2)`, "1");
assert("cos(0)", "cos(0)", "1");
assert("cos(PI)", `cos(${Math.PI})`, "-1");
assert("tan(0)", "tan(0)", "0");
assert("log(100) (base 10)", "log(100)", "2");
assert("ln(e) (natural log)", "ln(Math.E)", "1");
assert("sqrt(9)", "sqrt(9)", "3");
assert("Power 2^3", "2^3", "8");
assert("PI constant", "pi", `${Math.PI}`);
assert("E constant", "e", `${Math.E}`);

// Edge Cases
assert("Division by zero", "10/0", "Error", true);
assert("Invalid expression 1", "10 + * 5", "Error", true);
assert("sqrt(-1)", "sqrt(-1)", "Error", true);
assert("log(0)", "log(0)", "Error", true);
assert("Very large numbers", "1e100 * 1e100", "1e+200");
assert("Very small numbers", "1e-100 / 1e100", "1e-200");
assert("Decimal precision issue (example)", "0.1 + 0.2", "0.30000000000000004");

console.log("\n--- Test Summary ---");
console.log(`Total Tests: ${totalTests}`);
console.log(`Passed: ${passedTests}`);
console.log(`Failed: ${failedTests}`);

// Output for structured data
console.log(JSON.stringify({ totalTests, passedTests, failedTests }));
