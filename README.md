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

## Key Concepts Implemented 
 
- Multi-Agent Systems (MAS)
- Agent Orchestration (CrewAI)
- Prompt Engineering
- Tool-Augmented AI
- Structured Output Control

## Known Limitations

- Still relies on LLM reasoning (may hallucinate edge cases)
- Requires clear input format
- No advanced validation layer (yet)
