import os
import re
import sys
import atexit
import traceback
from openai import OpenAI


# Redirect stdout to terminal and file
class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            try:
                stream.write(data)
                stream.flush()
            except ValueError:
                # Skip closed streams
                pass

    def flush(self):
        for stream in self.streams:
            try:
                stream.flush()
            except ValueError:
                # Skip closed streams
                pass


stdout_log = open("llama_3.1_8b_z3_cleaned_by_api.txt", "w", encoding="utf-8")
sys.stdout = Tee(sys.__stdout__, stdout_log)
def cleanup():
    try:
        stdout_log.close()
    except:
        pass


atexit.register(cleanup)

# CONFIG
INPUT_FILE = "llama_3.1_8b_z3.txt"
OUTPUT_FILE = "out.txt"
MODEL_ID = "deepseek-chat"
BASE_URL = "https://api.deepseek.com/v1"
API_KEY = "sk-xxxxx"  # Replace with your actual key

# Connect to DeepSeek API
client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

# Instruction prompt to clean to only one valid python block
CLEAN_INSTRUCTION = (
    "You will be given a problem and a response with multiple code blocks. "
    "Please clean it by keeping only a single valid Python code block that solves the problem. "
    "Do not return any explanation or markdown. Just return the code like this:\n\n"
    "```python\n<cleaned working code>\n```"
)


def extract_problems(text):
    return re.split(r"(?=== Problem \d+ ===)", text)


def clean_problem_with_deepseek_stream(problem_text):
    try:
        prompt = CLEAN_INSTRUCTION + "\n\n" + problem_text

        print("\n", flush=True)
        full_response = ""

        stream = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": "Clean,debug and retain one working z3 python block only, make sure it prints the result"},
                {"role": "user", "content": prompt}
            ],
            stream=True,
            temperature=0,
        )

        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                print(delta.content, end="", flush=True)
                full_response += delta.content

        return problem_text.strip() + "\n" + full_response.strip()

    except Exception as e:
        print(f"\n[Error cleaning problem]: {e}")
        traceback.print_exc()
        return problem_text + "\n[Error cleaning this problem]\n"


def main():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            raw_text = f.read()

        problems = extract_problems(raw_text)

        output_dir = os.path.dirname(OUTPUT_FILE)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
            for idx, prob in enumerate(problems):
                if not prob.strip():
                    continue
                print(f"\n== Problem {idx + 60} ===")  # Fixed: changed idx + 0 to idx + 1
                cleaned = clean_problem_with_deepseek_stream(prob)
                out_f.write(cleaned + "\n\n")

    except Exception as e:
        print(f"Error in main: {e}")
        traceback.print_exc()
    finally:
        # Ensure proper cleanup
        try:
            sys.stdout = sys.__stdout__  # Restore original stdout
            stdout_log.close()
        except:
            pass


if __name__ == "__main__":
    main()