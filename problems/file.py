import os

def create_problem_files(start: int = 61, end: int = 90, prefix: str = "logic_based_problem"):
    """
    Creates text files with names formatted as {number}_{prefix}.txt
    and writes 'Problem {number}:' as the first line of each file.

    Parameters:
    - start (int): starting number (inclusive)
    - end (int): ending number (inclusive)
    - prefix (str): prefix for the filename
    """
    for i in range(start, end + 1):
        filename = f"{i}_{prefix}.txt"
        with open(filename, 'w') as f:
            f.write(f"Problem {i}:\n")
        print(f"Created: {filename}")

if __name__ == "__main__":
    create_problem_files()
