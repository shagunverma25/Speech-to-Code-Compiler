def generate_python_code(commands):
    code = ""
    for cmd in commands:
        if cmd["type"] == "function":
            name = cmd["name"]
            params = cmd.get("params", [])
            if cmd.get("operation") == "add":
                code += f"def {name}({', '.join(params)}):\n    return {params[0]} + {params[1]}\n"
                code += f"result = {name}(5, 3)\nprint('Result:', result)\n"
            elif cmd.get("operation") == "multiply":
                code += f"def {name}({', '.join(params)}):\n    return {params[0]} * {params[1]}\n"
                code += f"result = {name}(5, 3)\nprint('Result:', result)\n"
            elif cmd.get("operation") == "subtract":
                code += f"def {name}({', '.join(params)}):\n    return {params[0]} - {params[1]}\n"
                code += f"result = {name}(8, 2)\nprint('Result:', result)\n"
            elif cmd.get("operation") == "divide":
                code += f"def {name}({', '.join(params)}):\n    return {params[0]} / {params[1]}\n"
                code += f"result = {name}(10, 2)\nprint('Result:', result)\n"
            else:
                code += f"def {name}():\n    print('Function {name} called')\n{name}()\n\n"

        elif cmd["type"] == "variable":
            code += f"{cmd['name']} = {cmd['value']}\nprint({cmd['name']})\n"

        elif cmd["type"] == "loop":
            code += f"for i in range({cmd['start']}, {cmd['end']} + 1):\n    print(i)\n"

        elif cmd["type"] == "if":
            code += f"{cmd['var']} = 40  # example value\n"
            code += f"if {cmd['var']} > {cmd['value']}:\n    print('{cmd['var']} is greater than {cmd['value']}')\n"

    return code

def generate_java_code(commands):
    code = "public class Main {\n    public static void main(String[] args) {\n"
    
    for cmd in commands:
        if cmd["type"] == "function":
            name = cmd["name"]
            params = cmd.get("params", [])

            if cmd.get("operation") == "add":
                code += f"        System.out.println({name}(5, 3));\n"
                code += f"    }}\n\n    public static int {name}(int a, int b) {{\n        return a + b;\n    }}\n"
                return code

            elif cmd.get("operation") == "multiply":
                code += f"        System.out.println({name}(4, 2));\n"
                code += f"    }}\n\n    public static int {name}(int a, int b) {{\n        return a * b;\n    }}\n"
                return code

            elif cmd.get("operation") == "subtract":
                code += f"        System.out.println({name}(10, 3));\n"
                code += f"    }}\n\n    public static int {name}(int a, int b) {{\n        return a - b;\n    }}\n"
                return code

            elif cmd.get("operation") == "divide":
                code += f"        System.out.println({name}(8, 2));\n"
                code += f"    }}\n\n    public static double {name}(int a, int b) {{\n        return a / (double)b;\n    }}\n"
                return code

            else:
                code += f"        System.out.println(\"Function {name} called\");\n"

        elif cmd["type"] == "variable":
            code += f"        int {cmd['name']} = {cmd['value']};\n        System.out.println({cmd['name']});\n"

        elif cmd["type"] == "loop":
            code += f"        for (int i = {cmd['start']}; i <= {cmd['end']}; i++) {{\n"
            code += f"            System.out.println(i);\n        }}\n"

        elif cmd["type"] == "if":
            code += f"        int {cmd['var']} = 40;\n"
            code += f"        if ({cmd['var']} > {cmd['value']}) {{\n"
            code += f"            System.out.println(\"{cmd['var']} is greater than {cmd['value']}\");\n        }}\n"

    code += "    }\n}"
    return code

def generate_c_code(commands):
    code = "#include <stdio.h>\n\nint main() {\n"

    for cmd in commands:
        if cmd["type"] == "function":
            name = cmd["name"]
            if cmd.get("operation") == "add":
                return (
                    "#include <stdio.h>\n\n"
                    "int add(int a, int b) {\n    return a + b;\n}\n\n"
                    "int main() {\n    int result = add(5, 3);\n"
                    "    printf(\"Result: %d\\n\", result);\n    return 0;\n}"
                )
            else:
                code += f'    printf("Function {name} called\\n");\n'

        elif cmd["type"] == "variable":
            code += f"    int {cmd['name']} = {cmd['value']};\n"
            code += f"    printf(\"%d\\n\", {cmd['name']});\n"

        elif cmd["type"] == "loop":
            code += f"    for (int i = {cmd['start']}; i <= {cmd['end']}; i++) {{\n"
            code += f"        printf(\"%d\\n\", i);\n    }}\n"

        elif cmd["type"] == "if":
            code += f"    int {cmd['var']} = 40;\n"
            code += f"    if ({cmd['var']} > {cmd['value']}) {{\n"
            code += f"        printf(\"{cmd['var']} is greater than {cmd['value']}\\n\");\n    }}\n"

    code += "    return 0;\n}"
    return code
