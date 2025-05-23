# simple_compiler.py

import re

def lexically_analyze(code: str):
    tokens = []
    lines = code.split('\n')
    for line in lines:
        line = line.strip()
        if line:
            # Split by space, brackets, or operators
            tokens += re.findall(r'\w+|[=+\-*/(){};<>]', line)
    return tokens

def syntax_check(code: str, language: str):
    if language == "python":
        try:
            compile(code, '<string>', 'exec')
            return True, "✅ Syntax is valid."
        except SyntaxError as e:
            return False, f"❌ Syntax Error: {e}"
    elif language == "java":
        # Simple Java syntax check: check for class and main
        if "class" in code and "public static void main" in code:
            return True, "✅ Java syntax seems valid."
        return False, "❌ Missing main class or structure."
    elif language == "c":
        if "main()" in code or "int main" in code:
            return True, "✅ C syntax seems valid."
        return False, "❌ C main() function not found."
    return False, "❌ Unknown language"