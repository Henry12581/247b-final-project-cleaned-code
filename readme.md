LLM–Z3 Evaluation Pipeline

This repository implements a full pipeline for evaluating large language models (LLMs) on logic-reasoning tasks using Z3 SMT solver code generation, automated debugging, execution, and scoring. It supports both:

DeepSeek API (remote inference)

LM Studio Pipeline (local inference)

All generated artifacts, intermediate files, and evaluation results are stored systematically for each model.

Project Overview
Core Concepts

Questions are stored in the problems/ directory.

Each LLM produces raw Z3 code (_z3 suffix).

A cleaning pipeline fixes syntax errors or malformed Z3 code.

Code is executed to extract answers.

A scoring and evaluation module compares generated answers against ground truth.

Results are recorded and graphed automatically.

This project enables end-to-end benchmarking across multiple LLMs under consistent conditions.

File Meaning (Per Model)

Inside llm_output/<model>/, you will always see four files:

1. <model>_z3

Raw output generated directly by the model.

Contains Z3 solver code only.

No explanations.

May contain syntax errors or incomplete code.

2. <model>_z3_cleaned_by_api

Cleaned and debugged Z3 code.

Fixed by DeepSeek API or LM Studio pipeline.

Ensures syntactic correctness.

Removes hallucinations, text, or Markdown.

3. <model>_z3_extracted_llm_answers

Execution results.

Runs the cleaned Z3 code against each problem.

Stores the final boolean/number/date/etc. answers.

Used by scorers.

4. <model>_z3_logic_score

Final evaluation report.

Correct / incorrect summary

Per-question results

Incorrect cases for manual debugging

Supports 0–100% or raw (e.g., 17/20)

DeepSeek API Integration

The project supports remote inference using the official DeepSeek API.

Features:

Direct Z3-only output (_z3)

Automatic retry on validation error

Automatic hand-off to cleaning module

Consistent formatting across remote and local pipelines

Use when:

Cloud inference needed

Running large context models

Reproducible results preferred

LM Studio Local Pipeline

Local inference through LM Studio is fully supported.

Capabilities:

GPU-accelerated model inference

Controlled experiment environment

Deterministic temperature and sampling settings

Identical output structure as API pipeline

Use when:

You prefer offline processing

You want to benchmark many runs

You want low latency or batch inference

Automated Cleaning & Debugging

Located in scoring/llm_cleaning/.

This module:

Reads raw _z3 output

Uses an LLM to repair invalid code

Normalizes solver setup and variable declarations

Ensures reproducibility

Writes cleaned output to <model>_z3_cleaned_by_api

Execution & Answer Extraction

test.exe runs each cleaned Z3 file and extracts the final answer for each problem.

Produces:
<model>_z3_extracted_llm_answers

Key features:

Catches runtime failures

Captures stdout/stderr

Enforces timeouts for infinite loops or solver hang

Provides unified answer format for scoring

All-In-One Evaluation

aio_scoring/ computes the final score.

Outputs:

Correct, incorrect counts

Percentage score

Weighted or unweighted scoring

List of incorrect questions for debugging

Final output file:
<model>_z3_logic_score

Graphing & Analytics

graphing/make_graph.py supports:

Raw score mode (e.g., 17/20)

Percentage mode (e.g., 85%)

Multiple models per chart

Comparison across parameter sizes

Supports:

Line graph

Bar graph

Ranking table

Workflow Summary
              ┌─────────────────┐
              │  problems/       │
              └────────┬────────┘
                       │
                 LLM Inference
                       │
      ┌────────────────▼─────────────────┐
      │         Raw Output (_z3)         │
      └────────────────┬─────────────────┘
                       │
                Cleaning Module
                       │
      ┌────────────────▼────────────────────┐
      │     Cleaned Z3 Code (no errors)     │
      └────────────────┬────────────────────┘
                       │
               Execution Module
                       │
      ┌────────────────▼────────────────────┐
      │   Extracted Answers per Problem     │
      └────────────────┬────────────────────┘
                       │
                  Scoring Engine
                       │
      ┌────────────────▼────────────────────┐
      │ Final Score + Error Cases (JSON)    │
      └────────────────┬────────────────────┘
                       │
                 Graph Generator

Key Suffixes Explained
Suffix	Meaning
_z3	Raw LLM output; contains ONLY Z3 code
_z3_cleaned_by_api	Cleaned, corrected Z3 code
_z3_extracted_llm_answers	Execution results from cleaned code
_z3_logic_score	Final evaluation and scoring
Questions / Extensions

This pipeline can easily be extended to:

Multi-step reasoning analysis

Graph-theory visualization of error patterns

Meta-evaluation comparing different LLM families

Reverse-engineering failure categories

Adding new LLM inference backends (OpenAI, Groq, vLLM, etc.)
