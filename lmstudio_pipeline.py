import os
import sys
import time
import traceback
from multiprocessing import Process, Pipe
from openai import OpenAI

# Constants
PROBLEM_DIR = "problems"
OUTPUT_DIR = "llm_output_logic"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "llama_3.1_8b.txt")
MODEL_ID = "model-identifier"
BASE_URL = "http://10.0.0.77:12334/v1"
API_KEY = "lm-studio"
TIMEOUT_SECONDS = 60

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Connect to local LM Studio server
client = OpenAI(base_url=BASE_URL, api_key=API_KEY)


def generate_response_worker(prompt, conn):
    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": "answer the question"},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            stream=True,
        )
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta.content is not None:
                conn.send(delta.content)
        conn.send(None)  # End of stream marker
    except Exception as e:
        conn.send(f"[ERROR] {str(e)}")
        conn.send(None)
    finally:
        conn.close()


if __name__ == "__main__":
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
        for i in range(61, 91):
            filename = os.path.join(PROBLEM_DIR, f"{i:02d}_logic_based_problem.txt")
            print(f"\nProcessing Problem {i} from {filename}...")
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    prompt = lines[1].strip() if len(lines) >= 2 else ""

                header = f"=== Problem {i} ==="
                prompt_line = f"Prompt:\n{prompt}"
                print(header)
                print(prompt_line)

                out_f.write(header + "\n")
                # out_f.write(prompt_line + "\n")
                out_f.write("Response:\n")

                parent_conn, child_conn = Pipe()
                p = Process(target=generate_response_worker, args=(prompt, child_conn))
                p.start()

                start_time = time.time()
                full_answer = ""
                end_of_stream = False

                while True:
                    if parent_conn.poll():
                        chunk = parent_conn.recv()
                        if chunk is None:
                            end_of_stream = True
                        else:
                            print(chunk, end='', flush=True)
                            out_f.write(chunk)
                            full_answer += chunk

                    # Stop only when stream is finished AND process ended
                    if end_of_stream and not p.is_alive():
                        break

                    if time.time() - start_time > TIMEOUT_SECONDS:
                        print(f"\nTimeout: Problem {i} exceeded {TIMEOUT_SECONDS} seconds.")
                        out_f.write(f"\nTimeout after {TIMEOUT_SECONDS} seconds.\n")
                        p.terminate()
                        break

                    time.sleep(0.001)  # Avoid busy waiting

                p.join()
                out_f.write("\n\n")

            except Exception as e:
                error_msg = f"Error with Problem {i}: {str(e)}"
                print(error_msg)
                out_f.write(f"Error processing {filename}: {error_msg}\n\n")
