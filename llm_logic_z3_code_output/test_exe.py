#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import io
import math
import re
import sys
from typing import Dict, List, Optional, Tuple

ProblemNum = int

HEADER_RE = re.compile(r"^==\s*Problem\s+(\d+)\s*===", re.MULTILINE)
CLEANING_RE = re.compile(r"^===\s*Cleaning Problem\s+(\d+)\s*===", re.MULTILINE)
PY_FENCE_RE = re.compile(r"```python\s*\n(.*?)\n```", re.DOTALL)

def read_text_with_fallback(path: str) -> str:
    encs = ["utf-8", "utf-8-sig", "latin-1", "cp1252", "iso-8859-1"]
    for enc in encs:
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    # Last resort: binary with ignore
    with open(path, "rb") as f:
        return f.read().decode("utf-8", errors="ignore")

def find_problem_spans(text: str) -> List[Tuple[ProblemNum, int, int]]:
    """
    Return list of (problem_number, start_idx, end_idx) slices covering each Problem section.
    Excludes "Cleaning Problem" blocks by delimiting only with true Problem headers.
    """
    matches = list(HEADER_RE.finditer(text))
    spans: List[Tuple[ProblemNum, int, int]] = []
    for i, m in enumerate(matches):
        num = int(m.group(1))
        start = m.end()  # start after the header line
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        spans.append((num, start, end))
    return spans

def extract_code_blocks(section_text: str) -> List[str]:
    """Return all python code blocks inside a given problem section."""
    return [blk for blk in PY_FENCE_RE.findall(section_text) if blk.strip()]

def safe_exec(code: str) -> str:
    """
    Execute python code and capture stdout.
    If nothing printed, tries to surface a 'result' variable or first user var.
    """
    old_stdout = sys.stdout
    buf = io.StringIO()
    sys.stdout = buf
    try:
        globals_dict = {"__builtins__": __builtins__, "math": math}
        locals_dict: Dict[str, object] = {}
        exec(code, globals_dict, locals_dict)
        out = buf.getvalue().strip()
        if out:
            return out

        # Fallbacks if nothing printed
        if "result" in locals_dict:
            return str(locals_dict["result"])
        for name, val in locals_dict.items():
            if not name.startswith("_") and name not in ("math",):
                return str(val)
        return ""
    except Exception as e:
        return f"Error: {e}"
    finally:
        sys.stdout = old_stdout

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", "-i", default="llama_3.1_8b_z3_cleaned_by_api.txt")
    ap.add_argument("--output", "-o", default="llama_3.1_8b_z3_extracted_llm_answers.txt")
    ap.add_argument("--selection", choices=["first", "last"], default="last",
                    help="Which code fence to execute within a problem")
    ap.add_argument("--start", type=int, default=None, help="Min problem number to include")
    ap.add_argument("--end", type=int, default=None, help="Max problem number to include")
    args = ap.parse_args()

    text = read_text_with_fallback(args.input)

    # Build problem sections
    spans = find_problem_spans(text)
    if not spans:
        print("No '== Problem N ===' headers found.")
        sys.exit(1)

    # Optionally filter by problem number range
    if args.start is not None:
        spans = [s for s in spans if s[0] >= args.start]
    if args.end is not None:
        spans = [s for s in spans if s[0] <= args.end]

    results: List[str] = []
    for num, start, end in spans:
        section = text[start:end]

        # Stop this section at any intervening "Cleaning Problem" header (defensive)
        c = CLEANING_RE.search(section)
        if c:
            section = section[:c.start()]

        blocks = extract_code_blocks(section)
        if not blocks:
            line = f"{num}. No code block found"
            print(line)
            results.append(line)
            continue

        code = blocks[0] if args.selection == "first" else blocks[-1]
        out = safe_exec(code)
        # Keep exactly one line per problem
        line = f"{num}. {out}".rstrip()
        print(line)
        results.append(line)

    # Write
    try:
        with open(args.output, "w", encoding="utf-8") as f:
            for line in results:
                f.write(line + "\n")
        print(f"\nResults saved to: {args.output}")
    except Exception as e:
        print(f"Error writing output: {e}")

if __name__ == "__main__":
    main()
