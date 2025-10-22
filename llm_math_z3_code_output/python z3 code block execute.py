import re
import traceback
import io
import contextlib

INPUT_FILE = "deepseek_r1_distill_llama_8b_z3_cleaned_by_api.txt"

def extract_single_code_blocks_per_problem(text):
    # Split by each problem block
    problems = re.split(r"== Problem \d+ ===", text)
    code_blocks = []

    for problem in problems:
        if not problem.strip():
            continue

        # Extract the first Python code block only (under Response:)
        match = re.search(r"Response:\s*```python\s*(.*?)```", problem, re.DOTALL)
        if match:
            code = match.group(1).strip()
            if code.lower() != "<code>":
                code_blocks.append(code)

    return code_blocks

def execute_code_and_capture_output(code):
    exec_globals = {
        "__builtins__": __builtins__,
    }
    try:
        import math, sympy as sp, numpy as np, decimal
        exec_globals.update({
            "math": math,
            "sp": sp,
            "np": np,
            "decimal": decimal
        })
        # Capture stdout
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            exec(code, exec_globals)
        output = buffer.getvalue().strip()
        return output.splitlines()[-1] if output else "[no output]"
    except Exception as e:
        return f"[error] {e}"

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    code_blocks = extract_single_code_blocks_per_problem(content)

    for idx, code in enumerate(code_blocks):
        result = execute_code_and_capture_output(code)
        print(f"{idx + 1}. {result}")

if __name__ == "__main__":
    main()
