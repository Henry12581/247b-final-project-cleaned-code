from pathlib import Path
import math
import re

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

# Path to current directory
working_dir = Path(__file__).parent
gold_file = working_dir / "weight_correct_answers.txt"

# Read answers once
gold_lines = gold_file.read_text(encoding="utf-8").strip().splitlines()

# Find all prediction files
pred_files = list(working_dir.glob("*_extracted_llm_answers.txt"))

for pred_file in pred_files:
    prefix = pred_file.stem.replace("_extracted_llm_answers", "")
    output_file = working_dir / f"{prefix}_weight_score.txt"

    try:
        pred_lines = pred_file.read_text(encoding="utf-8").strip().splitlines()
    except Exception as e:
        print(f"Skipping {pred_file.name}: {e}")
        continue

    score = 0
    total = min(len(pred_lines), len(gold_lines))
    wrong_problems = []

    for i in range(total):
        try:
            def extract_answer(line):
                if ":" in line:
                    return line.split(":", 1)[1].strip()
                elif "." in line:
                    return line.split(".", 1)[1].strip()
                else:
                    raise ValueError("Line format invalid, no separator found")


            pred_raw = extract_answer(pred_lines[i])
            gold_raw = extract_answer(gold_lines[i])

            pred_val = parse_value(pred_raw)
            gold_val = parse_value(gold_raw)

            correct = False
            if isinstance(pred_val, bool) or isinstance(gold_val, bool):
                correct = pred_val == gold_val
            else:
                pred_float = float(pred_val)
                gold_float = float(gold_val)
                if abs(pred_float - gold_float) <= 0.0001 * abs(gold_float):
                    correct = True

            if correct:
                score += 1
            else:
                wrong_problems.append(f"{i + 21}. Predicted: {pred_raw} | Correct: {gold_raw}")
        except Exception:
            wrong_problems.append(f"{i + 21}. ERROR parsing prediction or gold line")

    # Write score file
    with output_file.open("w", encoding="utf-8") as f:
        f.write(f"Score: {score}/{total}\n\n")
        f.write("Wrong Problems:\n")
        for line in wrong_problems:
            f.write(line + "\n")

    print(f"Scored {prefix}: {score}/{total}")
