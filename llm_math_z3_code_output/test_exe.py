import re
import math
import sys
from io import StringIO

INPUT_FILE = "deepseek_v3_full_z3_cleaned_by_api.txt"
OUTPUT_FILE = "deepseek_v3_full_z3_extracted_llm_answers.txt"


def execute_python_code(code):
    """Execute Python code and capture output"""
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()

    try:
        # Create a local namespace with math module
        local_namespace = {'math': math}

        # Execute the code
        exec(code, {'__builtins__': __builtins__, 'math': math}, local_namespace)

        # Get printed output
        output = captured_output.getvalue().strip()

        # If no output was printed, try to get the result variable
        if not output and 'result' in local_namespace:
            output = str(local_namespace['result'])

        # If still no output, check for any variables that might contain the result
        if not output:
            for var_name, var_value in local_namespace.items():
                if var_name not in ['math', '__builtins__'] and not var_name.startswith('_'):
                    output = str(var_value)
                    break

        return output

    except Exception as e:
        return f"Error: {str(e)}"

    finally:
        # Restore stdout
        sys.stdout = old_stdout


def read_and_execute_code(filename):
    """Read the text file and execute all Python code blocks"""
    try:
        # Try different encodings to handle the file
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
        content = None

        for encoding in encodings:
            try:
                with open(filename, 'r', encoding=encoding) as file:
                    content = file.read()
                break
            except UnicodeDecodeError:
                continue

        if content is None:
            # If all encodings fail, try reading as binary and decode with errors='ignore'
            with open(filename, 'rb') as file:
                content = file.read().decode('utf-8', errors='ignore')
            print("Read file using binary mode with error handling")

        # Find all code blocks between ```python and ```
        pattern = r'```python\n(.*?)\n```'
        code_blocks = re.findall(pattern, content, re.DOTALL)

        # Filter out the placeholder text
        valid_code_blocks = []
        for code in code_blocks:
            if code.strip() != '<cleaned working code>':
                valid_code_blocks.append(code)

        # Execute each code block and format output
        results = []
        for i, code in enumerate(valid_code_blocks, 1):
            result = execute_python_code(code)
            output_line = f"{i}. {result}"
            results.append(output_line)
            print(output_line)  # Still print to console

        # Write results to output file
        try:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as output_file:
                for line in results:
                    output_file.write(line + '\n')
            print(f"\nResults saved to: {OUTPUT_FILE}")
        except Exception as e:
            print(f"Error writing to output file: {str(e)}")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error reading file: {str(e)}")


if __name__ == "__main__":
    read_and_execute_code(INPUT_FILE)