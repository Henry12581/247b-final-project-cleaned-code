## 📚 Project Summary: LLM Evaluation via Z3 Code Generation

This project establishes a pipeline to evaluate various Large Language Models (LLMs) based on their ability to generate logically correct Z3 SMT solver code. The evaluation process includes generating Z3 code, cleaning it for execution, running the code, and scoring the logical correctness of the results. This process validates how effectively LLMs can integrate symbolic reasoning.
---

### 🛠️ Supported LLM Integration Methods

The pipeline can integrate with models using the following methods:

* **DeepSeek API:** Utilizes the API provided by DeepSeek.
* **LM Studio Pipeline:** Runs models locally using the LM Studio environment.

---

### 📂 Project Structure & Key Components

The project is organized around different task types (logic, math, weight) and core pipeline scripts.

| Folder/File | Purpose | Task/Type |
| :--- | :--- | :--- |
| `problems/` | Contains all the logic and math questions used as input prompts for the LLMs. | Input |
| `llm_output_logic` | Contains the raw LLM text outputs for **logic** tasks. | Output (Raw) |
| `llm_output_math` | Contains the raw LLM text outputs for **math** tasks. | Output (Raw) |
| `llm_output_weight` | Contains the raw LLM text outputs for **weight** tasks. | Output (Raw) |
| `llm_logic_z3_code_output` | Contains the extracted Z3 code for **logic** tasks, ready for cleaning/execution. | Output (Z3) |
| `llm_math_z3_code_output` | Contains the extracted Z3 code for **math** tasks, ready for cleaning/execution. | Output (Z3) |
| `llm_weight_z3_code_output` | Contains the extracted Z3 code for **weight** tasks, ready for cleaning/execution. | Output (Z3) |
| `deepseek_api_pipeline.py` | Main script for running the evaluation using the **DeepSeek API**. | Pipeline |
| `deepseek_api_pipeline_z3.py` | Z3 processing within the DeepSeek pipeline. | Pipeline |
| `lmstudio_pipeline.py` | Main script for running the evaluation using the **LM Studio** local model pipeline. | Pipeline |
| `lmstudio_pipeline_z3.py` | Z3 processing within the LM Studio pipeline. | Pipeline |
| `run_z3.py` | a debug script, i simply copy paste z3 code genmerated by llm to see where the z3 code is wrong. 
| `deepseek_v3_math_z3.txt` | raw deepseek file were outputed derectlly to the main  directory. | Data/Config |
| `readme.md` | The current project documentation file. | Documentation |

---

### 📝 Meaning of `_z3` in Filenames

The suffix `_z3` indicates that the file strictly adheres to the following conditions:

> The file contains **only Z3 code** with **no explanation or natural language text**.

---

### 📊 Output Files for Each LLM

For every model evaluated, four specific files are generated to track the process from raw output to final score (using `llama_3.1_8b` as an example):

| Output File Name | Description | Stage |
| :--- | :--- | :--- |
| `llama_3.1_8b_z3` | The **raw Z3 code output** generated directly by the LLM. | **Generation** |
| `llama_3.1_8b_z3_cleaned_by_api` | The **debugged and cleaned** version of the Z3 code, processed by the cleaning pipeline or API. | **Cleaning** |
| `llama_3.1_8b_z3_extracted_llm_answers` | The **execution results** from running the cleaned Z3 code via `test.exe`. Contains the computed answers. | **Execution** |
| `llama_3.1_8b_z3_logic_score` | The **final evaluation score** for the model, including incorrect answers for debugging purposes. | **Scoring** |
