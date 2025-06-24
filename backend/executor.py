import subprocess
import os

def execute_python_code(code):
    path = os.path.join("generated_code", "main.py")
    with open(path, "w") as f:
        f.write(code)
    result = subprocess.run(["python", path], capture_output=True, text=True)
    return result.stdout or result.stderr

def save_java_code(code):
    path = os.path.join("generated_code", "Main.java")
    with open(path, "w") as f:
        f.write(code)
    return path
