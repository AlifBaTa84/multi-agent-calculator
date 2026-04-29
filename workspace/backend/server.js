const express = require('express');
const path = require('path');
const app = express();
const port = 3000;

// In-memory history storage
let calculationHistory = [];

// Middleware to parse JSON bodies
app.use(express.json());

// Serve static files from the 'workspace/frontend' directory
app.use(express.static(path.join(__dirname, '..', 'frontend')));

// API endpoint for getting calculation history
app.get('/api/history', (req, res) => {
    res.json(calculationHistory);
});

// API endpoint for adding a calculation to history
app.post('/api/history', (req, res) => {
    const { expression, result } = req.body;

    // Basic validation
    if (!expression || !result) {
        return res.status(400).json({ error: 'Expression and result are required.' });
    }

    const newEntry = { expression, result, timestamp: new Date().toISOString() };
    calculationHistory.push(newEntry);
    res.status(201).json(newEntry);
});

// API endpoint for clearing calculation history
app.delete('/api/history', (req, res) => {
    calculationHistory = [];
    res.status(204).send(); // 204 No Content for successful deletion
});

// Catch-all to serve index.html for any client-side routes (SPA behavior)
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '..', 'frontend', 'index.html'));
});

app.listen(port, () => {
    console.log(`Calculator backend server listening at http://localhost:${port}`);
    console.log(`Serving frontend from: ${path.join(__dirname, '..', 'frontend')}`);
});
