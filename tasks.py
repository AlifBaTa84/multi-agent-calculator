from crewai import Task
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from agents.setup import *

# ==========================================
# 1. DEFINISI PYDANTIC SCHEMA
# ==========================================

class ScopeData(BaseModel):
    in_scope: List[str]
    out_of_scope: List[str]

class PlannerData(BaseModel):
    problem_definition: str
    user_personas: List[str]
    features: Dict[str, List[str]]
    roadmap: Dict[str, List[str]]
    use_cases: List[str]
    user_flow: List[str]
    scope: ScopeData

class PlannerOutput(BaseModel):
    status: str = Field(description="Must be one of: SUCCESS | PARTIAL | FAILED | NEEDS_REVISION")
    agent: str = "planner"
    data: PlannerData

class ArchitectData(BaseModel):
    architecture_type: str
    layers: List[str]
    modules: List[str]
    data_flow: List[str]
    state_design: Dict[str, Any]
    project_structure: Dict[str, Any]
    tech_stack: Dict[str, Any]
    api_spec: List[str]
    security: List[str]
    performance: List[str]

class ArchitectOutput(BaseModel):
    status: str = Field(description="Must be one of: SUCCESS | PARTIAL | FAILED | NEEDS_REVISION")
    agent: str = "architect"
    data: ArchitectData

class TestRecommendation(BaseModel):
    action: str = Field(description="Must be one of: FIX_REQUIRED | REVIEW_REQUIRED | NO_ACTION")
    priority: str
    target: str = Field(description="Specify responsible agent: frontend_dev_agent or backend_dev_agent")
    reason: str

class TestSummary(BaseModel):
    total_tests: int
    passed: int
    failed: int
    status: str

class TesterData(BaseModel):
    test_cases: List[str]
    edge_cases: List[str]
    api_tests: List[str]
    integration_tests: List[str]
    bug_reports: List[str]
    summary: TestSummary
    recommendation: TestRecommendation

class TesterOutput(BaseModel):
    status: str = Field(description="Must be one of: SUCCESS | PARTIAL | FAILED | NEEDS_REVISION")
    agent: str = "tester"
    data: TesterData


# ==========================================
# 2. DEFINISI TASKS
# ==========================================

planner_task = Task(
    description="""
    Analyze the requirements for a web-based calculator application.

    Your responsibilities:
    - Define constraints and assumptions explicitly
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
    expected_output="A structured plan matching the required schema.",
    agent=planner_agent,
    output_pydantic=PlannerOutput,
    output_file="workspace/planner/plan.json"
)

architect_task = Task(
    description="""
    Based on the planning document, design the system architecture
    for a web-based calculator application.

   Input: Read and analyze workspace/planner/plan.json using your read_from_file tool.
    
    Your responsibilities:
    - Define system architecture (layers and approach)
    - Design modules and components
    - Define data flow and state management
    - Propose a suitable tech stack
    - Design project structure
    - Consider performance and security aspects
    - Define error handling strategy

    Constraints:
    - Do NOT invent new requirements
    - Do NOT write code
    - Focus only on HOW to build the system
    """,
    expected_output="A system architecture design matching the required schema.",
    agent=architect_agent,
    output_pydantic=ArchitectOutput,
    output_file="workspace/architect/architecture.json"
)

frontend_task = Task(
    description="""
    Implement the frontend of the calculator application.  

    Input: You MUST read the following files using your read_from_file tool: 
	1. workspace/planner/plan.json 
	2. workspace/architect/architecture.json
    
    Responsibilities:
    - Build UI components based on architecture design 
    - Manage client-side state
    - Handle user interactions based on defined user flow, responsive and user-friendly
    - Ensure the frontend can run by simply opening the HTML file in a browser.
    - Integrate with backend API if available

    Constraints:
    - Output must be a single HTML file with embedded CSS and JavaScript.
    - Use Bootstrap CDN only.
    - MUST follow UI and architecture design.
    - Do NOT implement backend logic.
    - MUST follow API spec strictly
    
    """,
    expected_output="A working frontend application code written to the workspace/frontend/ directory.",
    agent=frontend_dev_agent
)

backend_task = Task(
    description="""
    Implement backend services for the calculator application.

    Input: You MUST read the following files using your read_from_file tool: 
	  1. workspace/planner/plan.json 
	  2. workspace/architect/architecture.json

    Responsibilities:
    - Build API endpoints
    - Handle calculation logic 
    - Handle invalid expressions safely (no eval)
    - Return consistent error format
    - Manage history data


    Constraints:
    - Single file only (python script: server.py or JavaScript: server.js)
    - No database, no authentication, use in-memory data structures if needed
    - MUST follow API design strictly

    """,
    expected_output="A working backend application code written to the workspace/backend/ directory.",
    agent=backend_dev_agent
)

tester_task = Task(
    description="""
    Test the web-based calculator application.

    Input: You MUST read the following files using your read_from_file tool to understand the requirements and inspect the code:
    1. workspace/planner/plan.json
    2. workspace/architect/architecture.json
    3. The generated frontend code in workspace/frontend/
    4. The generated backend code in workspace/backend/

    Responsibilities:
    - Perform testing by analyzing the code (Static Analysis) and writing isolated test scripts.
    - Perform functional testing based on use cases and user flow
    - Validate API endpoints logic (if available) and edge cases
    - Identify edge cases and bugs
    - Provide structured test reports

    Based on test results, generate a recommendation:
    - If critical bugs exist -> action = FIX_REQUIRED
    - If minor issues -> action = REVIEW_REQUIRED
    - If all tests pass -> action = NO_ACTION
    - Target MUST explicitly mention either frontend_dev_agent or backend_dev_agent

    Constraints:
    - You CAN use write_to_file ONLY to create temporary test scripts inside the workspace/test/ directory.
    - DO NOT use write_to_file to write your final report (the report will be generated automatically).
    - You CANNOT open a browser.
    - You must test the frontend by analyzing the HTML/JS source code (Static Analysis).
    - You must test the backend logic by writing and executing isolated unit test scripts using your run_code tool.
    - Do NOT modify source code
    - Only report issues, do not fix them
    - Include invalid input scenarios
    """,
    expected_output="A comprehensive test report and recommendation matching the requested schema.",
    agent=tester_agent,
    output_pydantic=TesterOutput,
    output_file="workspace/test/test_report.json"
)