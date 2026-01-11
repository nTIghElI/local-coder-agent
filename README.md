# Local Agentic Coder 🤖💻

An autonomous coding assistant that runs locally. Unlike standard autocomplete, this agent uses a **Self-Healing Loop** to draft code, review it for errors, and automatically attempt fixes before saving.

## 🧠 Core Logic

1.  **Drafting:** The agent generates Python code based on a natural language prompt.
2.  **Static Analysis (Hard Check):** Validates syntax using Python's `ast` module to catch compilation errors immediately.
3.  **Semantic Review (Soft Check):** The LLM critiques its own code for logic bugs or hallucinated libraries.
4.  **Self-Correction:** If any check fails, the error is fed back into the model to generate a corrected version (up to 3 retries).

## ⚙️ Requirements

* **Python 3.10+**
* **Ollama** running `qwen2.5-coder:14b`
* **GPU:** Recommended 12GB+ VRAM for the 14B model (Runs on CPU but slower).

## 🚀 Quick Start

1.  **Run the Agent:**
    ```bash
    python coder.py
    ```
2.  **Enter a Prompt:**
    > *"Write a script that scans the current folder for .txt files and renames them with a timestamp."*
3.  **Watch the Loop:**
    The agent will print its drafting process, its self-critique (`PASS` or `FAIL`), and any auto-correction attempts.
4.  **Execute:**
    Once approved, the code is saved to `generated_script.py`.

## 🛡️ Safety
The agent operates in **Safe Mode** by default. It writes code but does not execute it.
* *Experimental:* An execution sandbox function is included in the source code but commented out for safety. Enable only inside Docker/VM environments.