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
    Execute a code file based on its extension and return its output or error.
    Currently supports: Python (.py) and JavaScript (.js)
    """
    if not os.path.exists(file_path):
        return f"File {file_path} does not exist."

    # Mapping ekstensi file ke interpreter/command yang sesuai
    runners = {
        '.py': 'python', # Gunakan 'python3' jika environment mewajibkannya
        '.js': 'node',
    }

    # Pisahkan nama file dan ekstensinya (misal: mendapatkan '.js' dari 'app.js')
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    # Validasi apakah ekstensi didukung oleh sistem kita
    if file_extension not in runners:
        return f"Error: Unsupported file extension '{file_extension}'."

    command = runners[file_extension]

    try:
        # Menjalankan command sesuai dengan ekstensi file
        result = subprocess.run([command, file_path], capture_output=True, text=True, timeout=10)
        return result.stdout if result.returncode == 0 else result.stderr
    except FileNotFoundError:
        return f"Error: The command '{command}' was not found. Is it installed and in your PATH?"
    except Exception as e:
        return f"Execution error: {str(e)}"
    
