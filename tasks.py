from crewai import Task
from agents.setup import *

planner_task = Task(
    description="""
    Analyze the requirements for a web-based calculator application.

    Your responsibilities:
    - Define user personas
    - Identify and categorize features (core, advanced, enhancement)
    - Create a prioritized roadmap (MVP first)
    - Define use cases and user flow
    - Clearly define project scope

    Constraints:
    - Do NOT define any technology stack
    - Do NOT design system architecture
    - Do NOT write code
    - Focus only on WHAT to build
    - Avoid over-engineering

    """,
    expected_output="""    
    JSON format:
    {
      "status": "SUCCESS | PARTIAL | FAILED",
      "agent": "planner",
      "data": {
        "problem_definition": "",
        "user_personas": [],
        "features": {
          "core": [],
          "advanced": [],
          "enhancement": []
        },
        "roadmap": {
          "mvp": [],
          "phase_2": [],
          "phase_3": []
        },
        "use_cases": [],
        "user_flow": [],
        "scope": {
          "in_scope": [],
          "out_of_scope": []
        }
      }
    }

    - Output MUST be valid JSON
    - No explanation outside JSON
    - Create file: workspace/planner/plan.json
    """,

    agent=planner_agent
)

architect_task = Task(
    description="""
    Based on the planning document, design the system architecture
    for a web-based calculator application.

    Your responsibilities:
    - Define system architecture (layers and approach)
    - Design modules and components
    - Define data flow and state management
    - Propose a suitable tech stack
    - Design project structure
    - Consider performance and security aspects

    Constraints:
    - Do NOT write code
    - Do NOT change the defined requirements
    - Do NOT introduce unnecessary complexity
    - Focus only on HOW to build the system

    """,
    expected_output=""" 
    JSON format:
    {
      "status": "SUCCESS",
      "agent": "architect",
      "data": {
        "architecture_type": "",
        "layers": [],
        "modules": [],
        "data_flow": [],
        "state_design": {},
        "project_structure": {},
        "tech_stack": {},
        "api_spec": [],
        "security": [],
        "performance": []
      }
    }
    - Output MUST be valid JSON
    - No explanation outside JSON
    - Create file: workspace/architect/architecture.json
    """,
    agent=architect_agent
)

frontend_task = Task(
    description="""
    Implement the frontend of the calculator application.  

    Responsibilities:
    - Build UI components based on architecture design 
    - Manage client-side state
    - Handle user interactions based on defined user flow
    - Integrate with backend API if available

    Constraints:
    - MUST follow UI and architecture design
    - Do NOT implement backend logic
    - Do NOT change API contract
    - Keep UI responsive and clean based on material design principles and usability best practices
    - Ensure code is modular and maintainable

    Ensure the application is responsive and user-friendly.
    """,
    expected_output="""
    - A working frontend application that meets the defined requirements and architecture.
    - Create file based on architecture design in workspace/frontend/.
    """,
    agent=frontend_dev_agent
)

backend_task = Task(
    description="""
    Implement backend services for the calculator application.
    
    Responsibilities:
    - Build API endpoints
    - Handle calculation logic (if required)
    - Manage history data
    - Ensure validation and security

    Constraints:
    - MUST follow API design strictly
    - Do NOT change request/response format
    - Do NOT implement frontend logic
    - Keep backend lightweight (avoid over-engineering)
    - Ensure input validation and security

    """,
    expected_output="""
    - A working backend application that meets the defined requirements and architecture.
    - Provide working and testable endpoints.
    - Create file based on architecture design in workspace/backend/.
    """,
    agent=backend_dev_agent
)

tester_task = Task(
    description="""
    Test the web-based calculator application.

    Responsibilities:
    - Perform functional testing
    - Test user interactions
    - Validate API endpoints (if available)
    - Identify edge cases and bugs
    - Provide structured test reports

    Constraints:
    - Do NOT modify source code
    - Do NOT redesign system
    - Only report issues, do not fix them
    - Base testing strictly on requirements and architecture
    - Clearly separate PASS and FAIL results
    - Provide reproducible bug reports

    """,
    expected_output="""
    JSON format:
    {
      "status": "SUCCESS",
      "agent": "tester",
      "data": {
        "test_cases": [],
        "edge_cases": [],
        "api_tests": [],
        "integration_tests": [],
        "bug_reports": [],
        "summary": {
          "total_tests": 0,
          "passed": 0,
          "failed": 0,
          "status": ""
        }
      }
    }

    - Output MUST be valid JSON
    - No explanation outside JSON
    - Clearly indicate PASS/FAIL and provide detailed bug reports.
    - Create file: workspace/test/test_report.json
    """,
    agent=tester_agent
)

debugger_task = Task(
    description="""
    Analyze and fix errors in the calculator application code.

    Responsibilities:
    - Detect bugs (syntax, logic, runtime)
    - Perform root cause analysis
    - Fix issues with minimal changes
    - Ensure the code runs correctly after fixes

    Constraints:
    - MUST preserve existing architecture and design
    - Do NOT add new features
    - Do NOT refactor large parts of the system
    - Only fix bugs and errors
    - Keep changes minimal and targeted
    - Do NOT change API contracts
    - Clearly explain each fix

    """,
    expected_output="""
    JSON format:
    {
    "status": "SUCCESS",
      "agent": "debugger",
      "data": {
        "detected_errors": [],
        "root_cause_analysis": [],
        "fixes_applied": [],
        "validation_results": [],
        "summary": {
          "total_errors": 0,
          "fixed": 0,
          "remaining": 0,
          "status": ""
        }
      }
    }

    - Output MUST be valid JSON
    - No explanation outside JSON
    - Clearly explain each fix and its impact on the system.
    - Create file: workspace/debugger/debug_report.json
    """,
    agent=debugger_agent
)

