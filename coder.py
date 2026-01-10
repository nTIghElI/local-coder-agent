import ollama
import os

# --- CONFIG ---
MODEL = "qwen2.5-coder:14b"

def generate_code(prompt):
    """
    Asks the AI to write a specific Python script.
    """
    print(f"\n[Coder] Drafting code for: '{prompt}'...")
    
    response = ollama.chat(model=MODEL, messages=[
        {'role': 'system', 'content': 'You are an expert Python developer. Output ONLY valid Python code. Do not add Markdown formatting (no backticks). Do not add explanations.'},
        {'role': 'user', 'content': f"Write a Python script that does the following: {prompt}"}
    ])
    
    raw_content = response['message']['content']
    
    # --- CLEANING STEP ---
    # Strip out the Markdown wrapping paper if the AI adds it anyway
    clean_content = raw_content.replace("```python", "").replace("```", "").strip()
    
    return clean_content

def review_code(code_snippet):
    """
    Asks the AI to look for bugs in what it just wrote.
    """
    print("\n[Coder] Reviewing for bugs...")
    
    response = ollama.chat(model=MODEL, messages=[
        {'role': 'user', 'content': f"Review this Python code for errors. If it is good, reply 'PASS'. If it has bugs, describe them briefly: \n\n{code_snippet}"}
    ])
    
    return response['message']['content']

def main():
    print("=== LOCAL AI CODER ===")
    user_request = input("What script should I write? (e.g., 'A snake game'): ")
    
    # 1. Draft
    draft_code = generate_code(user_request)
    
    print("\n--- DRAFT CODE ---")
    print(draft_code[:500] + "...\n(truncated)") 
    
    # 2. Review
    critique = review_code(draft_code)
    print(f"\n--- AI CRITIQUE ---\n{critique}")
    
    # 3. Save
    if "PASS" in critique.upper() or input("\nSave anyway? (y/n): ").lower() == 'y':
        filename = "generated_script.py"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(draft_code)
        print(f"\nSuccess! Saved to {filename}")
    else:
        print("\nDiscarded.")

if __name__ == "__main__":
    main()