import os
import traceback
from openai import OpenAI

# Constants
PROBLEM_DIR = "problems"
OUTPUT_FILE = "deepseek_v3_full.txt"
MODEL_ID = "deepseek-chat"
BASE_URL = "https://api.deepseek.com/v1"
API_KEY = "sk-c933b9e9e56e4f06a49c1be96b66cf5d"  # Replace with your actual key

# Connect to DeepSeek API
client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

# Clear or create output file
with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
    for i in range(61, 91):
        filename = os.path.join(PROBLEM_DIR, f"{i:02d}_logic_based_problem.txt")
        print(f"Processing Problem {i} from {filename}...")  # log to stdout
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if len(lines) < 2:
                    prompt = ""
                    print(f"Warning: Problem {i} has fewer than 2 lines.")
                else:
                    prompt = lines[1].strip()

                out_f.write(f"=== Problem {i} ===\n")
                out_f.write(f"Prompt:\n{prompt}\n")

                # Stream response from DeepSeek
                response = client.chat.completions.create(
                    model=MODEL_ID,
                    messages=[
                        {"role": "system", "content": "answer the questions, only give answer"},
                        {"role": "user", "content": prompt}
                    ],
                    stream=True
                )

                reasoning_content = ""
                final_content = ""

                print("[Thought Process]", flush=True)
                for chunk in response:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                        reasoning_content += delta.reasoning_content
                        print(delta.reasoning_content, end="", flush=True)
                    elif hasattr(delta, "content") and delta.content:
                        final_content += delta.content
                        print(delta.content, end="", flush=True)

                print("\n")  # separate output
                out_f.write("[Thought Process]\n")
                out_f.write(reasoning_content + "\n\n")
                out_f.write("[Final Answer]\n")
                out_f.write(final_content + "\n\n")

        except Exception as e:
            print(f"Error with Problem {i}: {str(e)}")
            traceback.print_exc()
            out_f.write(f"Error processing {filename}: {str(e)}\n\n")
