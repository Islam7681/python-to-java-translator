import re

class PythonToJavaTranslator:
    def __init__(self):
        self.translations = {
            'if': 'if',
            'elif': 'else if',
            'else': 'else',
            'True': 'true',
            'False': 'false',
            'None': 'null',
            'print': 'System.out.println'
        }
        self.indent_stack = [0]
        self.in_function = False  # Track if inside a function

    def translate_line(self, line):
        original_line = line
        for py_construct, java_construct in self.translations.items():
            line = re.sub(r'\b' + py_construct + r'\b', java_construct, line)

        # Variable translation: detect type and translate accordingly
        if re.match(r'^\s*\w+\s*=\s*.*', line) and not re.match(r'^\s*def\s+\w+\(.*\):', line):
            variable_name, variable_value = re.match(r'^\s*(\w+)\s*=\s*(.*)', line).groups()
            java_type = self.detect_type(variable_value)
            line = f'{java_type} {variable_name} = {variable_value};'

        if re.match(r'^\s*def\s+\w+\(.*\):', line):
            self.in_function = True
            line = re.sub(r'^\s*def\s+(\w+)\((.*)\):',
                          lambda m: f'public static void {m.group(1)}({self.handle_parameters(m.group(2))})' + ' {',
                          line)

        if re.match(r'^\s*if\s+.*:', line):
            line = re.sub(r'^\s*if\s+(.*):', r'if (\1) {', line)

        if re.match(r'^\s*elif\s+.*:', line):
            line = re.sub(r'^\s*elif\s+(.*):', r'else if (\1) {', line)

        if re.match(r'^\s*else\s*:', line):
            line = re.sub(r'^\s*else\s*:', r'else {', line)

        if re.match(r'^\s*for\s+\w+\s+in\s+range\(\d+,\s*\d+\):', line):
            line = re.sub(r'^\s*for\s+(\w+)\s+in\s+range\((\d+),\s*(\d+)\):', r'for (int \1 = \2; \1 < \3; \1++) {',
                          line)
        elif re.match(r'^\s*for\s+\w+\s+in\s+.*:', line):
            line = re.sub(r'^\s*for\s+(\w+)\s+in\s+(.*):', r'for (Object \1 : \2) {', line)

        if re.match(r'^\s*while\s+.*:', line):
            line = re.sub(r'^\s*while\s+(.*):', r'while (\1) {', line)

        if re.match(r'^\s*(\w+)\s*-\=\s*1', line):
            line = re.sub(r'^\s*(\w+)\s*-\=\s*1', r'\1--', line)

        if re.match(r'^\s*return\s+.*', line):
            line = re.sub(r'^\s*return\s+(.*)', r'return \1;', line)

        if re.match(r'^\s*[^{}\s].*[^{};]\s*$', line):
            line += ';'

        current_indent = len(re.match(r'^\s*', original_line).group())
        while self.indent_stack and self.indent_stack[-1] > current_indent:
            self.indent_stack.pop()
            line = "}" + "\n" + line
        if self.indent_stack and self.indent_stack[-1] < current_indent:
            self.indent_stack.append(current_indent)

        if self.in_function and not re.match(r'^\s+', original_line):
            self.in_function = False
            line = "}" + "\n" + line

        return line.strip()

    def handle_parameters(self, params):
        param_list = params.split(',')
        java_params = []
        for param in param_list:
            param = param.strip()
            if param:
                java_params.append(f'int {param}')
        return ', '.join(java_params)

    def detect_type(self, value):
        if re.match(r'^-?\d+$', value):
            return 'int'
        elif re.match(r'^-?\d+\.\d+$', value):
            return 'double'
        elif re.match(r'^["\'].*["\']$', value):
            return 'String'
        elif value in ['true', 'false']:
            return 'boolean'
        else:
            return 'Object'

    def translate(self, code):
        lines = code.split('\n')
        translated_code = ["public class TranslatedCode {", "public static void main(String[] args) {"]
        function_code = []
        for line in lines:
            translated_line = self.translate_line(line)
            if translated_line:
                if self.in_function:
                    function_code.append(translated_line)
                else:
                    translated_code.append(translated_line)
        while len(self.indent_stack) > 1:
            translated_code.append("}")
            self.indent_stack.pop()
        translated_code.append("}")
        translated_code += function_code
        translated_code.append("}")
        return '\n'.join(translated_code)


# Read input from input.txt with error handling
try:
    with open('input.txt', 'r') as file:
        python_code = file.read()
except FileNotFoundError:
    print("Error: input.txt not found.")
    python_code = ""

translator = PythonToJavaTranslator()
java_code = translator.translate(python_code)

try:
    with open('output.txt', 'w') as file:
        file.write(java_code)
except IOError:
    print("Error: Unable to write to output.txt.")