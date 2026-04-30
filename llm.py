import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API KEY TIDAK TERBACA")

llm = LLM(
    model="gemini-2.5-flash",
    google_api_key=api_key, 
    temperature=0
)

# llm = LLM(
#    model="ollama/qwen2.5-coder:3b",  # Sesuaikan dengan model yang kamu unduh
#    base_url="http://localhost:11434" # Port default Ollama
# )