# FactLoop-LLM
Python implementation of a Self-Reflection loop designed to improve the factuality and consistency of medical AI responses.
This repository, provides a modular Python implementation of a **Self-Reflection loop** designed to improve the factuality and consistency of medical AI responses.

By leveraging **NVIDIA NIM** (specifically the `gpt-oss-20b` model) and an **LLM-as-a-Judge** evaluation framework, the system iteratively generates background knowledge, critiques its own accuracy, and refines its final answers to reduce hallucinations in medical queries. The codebase is organized into five self-contained modules (`config`, `llm_utils`, `evaluation`, `loops`, `main`) for easy deployment and testing on platforms like Google Colab.
