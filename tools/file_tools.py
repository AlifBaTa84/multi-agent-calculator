from crewai.tools import tool
import os
import subprocess

@tool
def write_to_file(file_path: str, content: str) -> str:
    """
    Write content to a file at the specified file path.
    Creates directories if they do not exist.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(content)
    return f"Content has been written to {file_path}"

@tool
def read_from_file(file_path: str) -> str:
    """
    Read and return the content of a file from the given file path.
    """
    if not os.path.exists(file_path):
        return f"File {file_path} does not exist."
    with open(file_path, 'r') as file:
        content = file.read()
    return content

@tool
def run_code(file_path: str) -> str:
    """
    Execute a Python file and return its output or error.
    """
    if not os.path.exists(file_path):
        return f"File {file_path} does not exist."
    try:
        result = subprocess.run(['python', file_path], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)
    
