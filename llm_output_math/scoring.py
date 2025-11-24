from pathlib import Path
import math
import re

# Set the model prefix here
prefix = "deepseek_v3_full"

# Construct file paths based on prefix
pred_file = Path(f"{prefix}_extracted_llm_answers.txt")
gold_file = Path("math_correct_answers.txt")
output_file = Path(f"{prefix}_math_score.txt")

def parse_value(value):
    """Convert string to float if possible, handling fractions and radicals."""
    value = value.strip()
    try:
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False
        if "√" in value:
            expr = re.sub(r"√(\d+)", lambda m: str(math.sqrt(int(m.group(1)))), value)
            return eval(expr)
        if "/" in value:
            return float(eval(value))  # handles fractions like 2/3
        return float(value)
    except Exception:
        return value  # return as-is if unparseable

# Read lines
pred_lines = pred_file.read_text(encoding="utf-8").strip().splitlines()
gold_lines = gold_file.read_text(encoding="utf-8").strip().splitlines()

score = 0
total = min(len(pred_lines), len(gold_lines))
wrong_problems = []

for i in range(total):
    pred_raw = pred_lines[i].split(".", 1)[1].strip()
    gold_raw = gold_lines[i].split(".", 1)[1].strip()

    pred_val = parse_value(pred_raw)
    gold_val = parse_value(gold_raw)

    correct = False
    if isinstance(pred_val, bool) or isinstance(gold_val, bool):
        correct = pred_val == gold_val
    else:
        try:
            pred_float = float(pred_val)
            gold_float = float(gold_val)
            if abs(pred_float - gold_float) <= 0.001 * abs(gold_float):
                correct = True
        except Exception:
            correct = False

    if correct:
        score += 1
    else:
        wrong_problems.append(f"{i+1}. Predicted: {pred_raw} | Correct: {gold_raw}")

# Write results
with output_file.open("w", encoding="utf-8") as f:
    f.write(f"Score: {score}/{total}\n\n")
    f.write("Wrong Problems:\n")
    for line in wrong_problems:
        f.write(line + "\n")
