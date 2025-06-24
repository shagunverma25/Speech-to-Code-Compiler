from simple_compiler import lexically_analyze, syntax_check
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from speech_to_text import speech_to_text
from lexer_parser import tokenize_input, parse_tokens
from code_generator import generate_python_code, generate_java_code, generate_c_code
from executor import execute_python_code, save_java_code
import os
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process_audio():
    try:
        file = request.files['audio']
        language = request.form.get("language", "python")
        
        # Save the audio file
        path = "temp.wav"
        file.save(path)

        # Transcribe speech from audio file
        spoken_text = speech_to_text(path)
        tokens = tokenize_input(spoken_text)
        commands = parse_tokens(tokens)

        # Generate code based on selected language
        if language == "python":
            code = generate_python_code(commands)
            file_name = "main.py"

        elif language == "java":
            code = generate_java_code(commands)
            file_name = "Main.java"

            # Save Java code to file
            with open(file_name, "w") as f:
                f.write(code)

        elif language == "c":
            code = generate_c_code(commands)
            file_name = "main.c"

            # Save C code to file
            with open(file_name, "w") as f:
                f.write(code)

        else:
            return jsonify({"error": "Unsupported language"}), 400

        # ⛏️ Compiler simulation
        tokens_lex = lexically_analyze(code)
        is_valid, syntax_message = syntax_check(code, language)
        if not is_valid:
            return jsonify({
                "speech": spoken_text,
                "tokens": tokens,
                "lexicalTokens": tokens_lex,
                "code": code,
                "output": syntax_message,
                "fileName": file_name
            })

        # 🏃 Execution logic
        if language == "python":
            output = execute_python_code(code)

        elif language == "java":
            try:
                subprocess.run(["javac", file_name], check=True)
                result = subprocess.run(["java", "Main"], capture_output=True, text=True)
                output = result.stdout.strip() or "✅ Code ran but didn’t produce any output."
            except subprocess.CalledProcessError as e:
                output = f"❌ Java Code Execution Error: {e}"

        elif language == "c":
            try:
                subprocess.run(["gcc", file_name, "-o", "main_exe"], check=True)
                run_cmd = ["./main_exe"] if os.name != "nt" else ["main_exe.exe"]
                result = subprocess.run(run_cmd, capture_output=True, text=True)
                output = result.stdout.strip() or "✅ Code ran but didn’t produce any output."
            except subprocess.CalledProcessError as e:
                output = f"❌ C Code Execution Error: {e}"

        # ✅ Final response
        return jsonify({
            "speech": spoken_text,
            "tokens": tokens,
            "lexicalTokens": tokens_lex,
            "code": code,
            "output": output,
            "fileName": file_name
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/download/<filename>', methods=['GET'])
def download_code(filename):
    return send_from_directory("generated_code", filename, as_attachment=True)

if __name__ == '__main__':
    os.makedirs("generated_code", exist_ok=True)
    app.run(debug=True)