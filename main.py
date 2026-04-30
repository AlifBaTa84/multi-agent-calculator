import json
import os
from crewai import Crew, Task
from tasks import planner_task, architect_task, frontend_task, backend_task, tester_task
from agents.setup import planner_agent, architect_agent, frontend_dev_agent, backend_dev_agent, tester_agent

# 1. Fase Desain (Hanya dijalankan 1 kali di awal)
design_crew = Crew(
    agents=[planner_agent, architect_agent],
    tasks=[planner_task, architect_task],
    verbose=True
)

# 2. Fase Pengembangan Awal (Hanya dijalankan 1 kali)
dev_crew = Crew(
    agents=[frontend_dev_agent, backend_dev_agent],
    tasks=[frontend_task, backend_task],
    verbose=True
)

# 3. Fase Pengujian (Loop dijalankan di sini)
tester_crew = Crew(
    agents=[tester_agent],
    tasks=[tester_task],
    verbose=True
)

def self_improving_loop(max_iter=3):
    print("\n=== PHASE 1: PLANNING & ARCHITECTURE ===")
    design_crew.kickoff()

    print("\n=== PHASE 2: INITIAL DEVELOPMENT ===")
    dev_crew.kickoff()

    for i in range(max_iter):
        print(f"\n=== PHASE 3 - ITERATION {i+1}: TESTING & QA ===\n")
        
        # Menjalankan pengujian
        tester_crew.kickoff()

        # Membaca hasil pengujian dari file yang dibuat oleh tester_agent
        report_path = "workspace/test/test_report.json"
        if not os.path.exists(report_path):
            print("ERROR: Report file tidak ditemukan. Menghentikan loop.")
            break

        try:
            with open(report_path, 'r') as f:
                report = json.load(f)
            
            # Mengambil data rekomendasi dari JSON
            recommendation = report.get("data", {}).get("recommendation", {})
            action = recommendation.get("action", "")
            target_agent_name = recommendation.get("target", "")
            bug_reason = recommendation.get("reason", "")

            if action == "NO_ACTION" :
                print("\nSUCCESS ✅ Semua pengujian berhasil dan tidak ada bug!")
                break
            
            print(f"\nBUG DITEMUKAN ❌ (Iterasi {i+1})")
            print(f"Target: {target_agent_name} | Reason: {bug_reason}")
            print("Memulai proses perbaikan...\n")

            # Menentukan agen mana yang bertugas memperbaiki bug
            if "frontend" in target_agent_name.lower():
                fix_agent = frontend_dev_agent
            elif "backend" in target_agent_name.lower():
                fix_agent = backend_dev_agent
            else:
                print("Target agen perbaikan tidak spesifik. Menghentikan loop.")
                break

            # Membuat Task dinamis khusus untuk perbaikan bug
            fix_task = Task(
                description=(
                    f"Fix the bugs found in the latest testing report.\n"
                    f"Bug details/Reason: {bug_reason}\n"
                    f"Review the full report in: {report_path}\n"
                    f"CRITICAL CONSTRAINT: When using write_to_file tool, you MUST provide the FULL, COMPLETE updated source code. "
                    f"Do NOT provide partial code snippets or diffs, because write_to_file will overwrite the entire file."
                ),
                expected_output="Code has been fixed, tested locally via tools, and files are updated.",
                agent=fix_agent
            )

            # Menjalankan agen developer untuk melakukan perbaikan
            fix_crew = Crew(
                agents=[fix_agent],
                tasks=[fix_task],
                verbose=True
            )
            fix_crew.kickoff()

        except json.JSONDecodeError:
            print("ERROR: Output tester bukan format JSON yang valid. Menghentikan loop.")
            break

if __name__ == "__main__":
    self_improving_loop()