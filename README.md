# Multi-Agent Calculator Web-based System (CrewAI + Gemini)

A multi-agent web-based system for solving mathematical problems using **CrewAI orchestration** and **Google Gemini (Flash)** as the LLM.

---

## Overview

This project demonstrates how multiple AI agents can collaborate to:
- Understand a math problem
- Break it into structured steps
- Execute calculations programmatically
- Validate results

Built with:
- **CrewAI** (multi-agent orchestration)
- **Google Gemini 2.5 Flash** (LLM)
- **Python 3.12** (Interpreter)

---

## Key Concepts Implemented 
 
- Multi-Agent Systems (MAS)
- Agent Orchestration (CrewAI)
- Intent Engineering
- Tool-Augmented AI
- Structured Output Control

---

## Known Limitations

- Still relies on LLM reasoning (may hallucinate edge cases)
- Requires clear input format
- No advanced validation layer (yet)

---

## Architecture

The system uses a multi-agent approach:

### 1. Planner Agent
- Create a structured plan and feature roadmap for a web-based calculator application

### 2. Architect Agent
- Design a scalable and modular architecture for a web-based calculator application

### 3. Backend Agent
- Develop backend services and APIs for the calculator application

### 4. Frontend Agent
- Build the user interface and client-side logic for a web-based calculator application

### 5. Debugger Agent
- Identify, analyze, and fix errors in the application code while preserving system design

### 6. Tester Agent
- Ensure the calculator application works correctly and meets all requirements

---

## Project Structure

multi-agent-calculator/
│
├── agents/            # Agent definitions
├── tools/             # Custom tools (file, execution, etc.)
├── tasks.py           # Task definitions
├── llm.py             # LLM configuration
├── config.py          # Environment config
├── main.py            # Entry point
├── test_llm.py        # LLM test
├── .env               # API Key (ignored)
└── README.md

---

## 🔑 Environment Setup

Create `.env` file:

GOOGLE_API_KEY=your_google_api_key

---

## Installation

# Clone repository
git clone https://github.com/AlifBata84/multi-agent-calculator.git

cd multi-agent-calculator

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

---

## Usage 

Run the system : 
python main.py

---

## LLM Testing 

Run the test : 
python test_llm.py

---

## Developer

Alif Finandhita

