from crewai import Crew
from tasks import *

crew = Crew(
    agents=[planner_agent, architect_agent, frontend_dev_agent, backend_dev_agent, debugger_agent, tester_agent],
    tasks=[planner_task, architect_task, frontend_task, backend_task, debugger_task, tester_task],
    verbose=True        
)

def self_improving_loop(max_iter=3):
    for i in range(max_iter):
        print(f"\n=== ITERATION {i+1} ===\n")

        # Generate code
        crew.kickoff()

        # Test
        result = tester_agent.run("Run all tests")

        print("TEST RESULT:\n", result)

        # Debug jika error
        if "error" in result.lower():
            fix = debugger_agent.run(result)
            print("FIX:\n", fix)
        else:
            print("SUCCESS ✅")
            break

if __name__ == "__main__":
    self_improving_loop()