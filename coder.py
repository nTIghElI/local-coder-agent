import ollama
import os
import ast  # Library for abstract syntax trees (Safe syntax checking)
import subprocess # Required for the dangerous execution step

# --- CONFIG ---
MODEL = "qwen2.5-coder:14b"
MAX_RETRIES = 3

def generate_code(prompt, error_context=None):
    """
    Asks the AI to write Python code.
    """
    if error_context:
        print(f"\n[Coder] Fixing code based on error: {error_context}...")
        instruction = f"The previous code had this error: {error_context}. Rewrite the code to fix it. Output ONLY valid Python code."
    else:
        print(f"\n[Coder] Drafting code for: '{prompt}'...")
        instruction = f"Write a Python script that does the following: {prompt}. Output ONLY valid Python code. Do not use Markdown backticks."

    response = ollama.chat(model=MODEL, messages=[
        {'role': 'system', 'content': 'You are an expert Python developer. Output ONLY valid Python code.'},
        {'role': 'user', 'content': instruction}
    ])
    
    # Clean output
    raw = response['message']['content']
    return raw.replace("```python", "").replace("```", "").strip()

def check_syntax(code_string):
    """
    HARD LOGIC: Uses Python's built-in compiler to check for syntax errors.
    This does NOT run the code, it just checks if it is readable.
    """
    try:
        ast.parse(code_string)
        return True, "Syntax OK"
    except SyntaxError as e:
        return False, f"Syntax Error on line {e.lineno}: {e.msg}"

def review_code_llm(code_snippet):
    """
    SOFT LOGIC: Asks the LLM to spot logical errors or hallucinated libraries.
    """
    print("[Coder] AI reviewing logic...")
    prompt = f"Review this code. Check for: 1. Infinite loops. 2. Non-existent libraries (e.g. fake_library_xyz). 3. Logic errors. If OK, say PASS. Else describe the error:\n\n{code_snippet}"
    
    response = ollama.chat(model=MODEL, messages=[
        {'role': 'user', 'content': prompt}
    ])
    return response['message']['content']

# ==============================================================================
#  DANGER ZONE: EXECUTION CAPABILITY
#  Uncomment this function ONLY if running inside a Docker container or VM.
#  This allows the AI to actually run the code to find 'ModuleNotFound' errors.
# ==============================================================================
# def execute_and_capture_error(code_string):
#     filename = "temp_execution_test.py"
#     with open(filename, "w", encoding="utf-8") as f:
#         f.write(code_string)
#     
#     try:
#         # Runs the code with a 5-second timeout to prevent infinite loops
#         result = subprocess.run(
#             ["python", filename], 
#             capture_output=True, 
#             text=True, 
#             timeout=5
#         )
#         
#         # If return code is 0, it ran successfully
#         if result.returncode == 0:
#             return True, "Execution Successful"
#         else:
#             # It crashed! Return the error message so the AI can fix it.
#             return False, f"Runtime Error: {result.stderr}"
#             
#     except subprocess.TimeoutExpired:
#         return False, "Runtime Error: Code timed out (Possible infinite loop)"
#     except Exception as e:
#         return False, f"System Error: {str(e)}"
#     finally:
#         if os.path.exists(filename):
#             os.remove(filename)
# ==============================================================================


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== LOCAL AGENTIC CODER (Safe Mode) ===")
    user_request = input("What script should I write? ")
    
    current_code = generate_code(user_request)
    
    for attempt in range(MAX_RETRIES):
        print(f"\n--- Cycle {attempt+1}/{MAX_RETRIES} ---")
        
        # 1. HARD CHECK (Syntax)
        is_valid_syntax, syntax_msg = check_syntax(current_code)
        if not is_valid_syntax:
            print(f"❌ Failed Syntax Check: {syntax_msg}")
            current_code = generate_code(user_request, error_context=syntax_msg)
            continue # Skip to next attempt
            
        # 2. SOFT CHECK (LLM Review)
        llm_verdict = review_code_llm(current_code)
        if "PASS" not in llm_verdict.upper():
            print(f"⚠️ AI Critique: {llm_verdict}")
            current_code = generate_code(user_request, error_context=llm_verdict)
            continue
            
        # 3. RUNTIME CHECK (Optional - Currently Disabled)
        # To enable, uncomment the function above and this block:
        # success, runtime_msg = execute_and_capture_error(current_code)
        # if not success:
        #     print(f"💥 Runtime Failure: {runtime_msg}")
        #     current_code = generate_code(user_request, error_context=runtime_msg)
        #     continue

        print("\n✅ Code passed all active checks.")
        break

    # Final Output
    print("\n" + "="*30)
    print(current_code[:500] + "...\n(truncated)" if len(current_code) > 500 else current_code)
    print("="*30)

    if input("\nSave this script? (y/n): ").lower() == 'y':
        with open("generated_script.py", "w", encoding="utf-8") as f:
            f.write(current_code)
        print("Saved to generated_script.py")

if __name__ == "__main__":
    main()