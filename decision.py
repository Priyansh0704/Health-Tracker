import os
import re
import json
import time
import google.generativeai as genai
from dotenv import load_dotenv

# ------------------------
# Gemini Setup
# ------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-pro")

# --- Constants ---
DATA_DIR = "./data"
PROMPT_FILE = "./prompts/decision_trace.md"
OUTPUT_DIR = os.path.join(DATA_DIR, "decisions")
MAX_RETRIES = 3

def clean_and_parse_json(raw_text: str):
    """Cleans the raw text to extract and parse a JSON object."""
    match = re.search(r'\{.*\}', raw_text, re.DOTALL)
    if not match:
        raise ValueError("No valid JSON object found in the model's output.")
    json_str = match.group(0)
    return json.loads(json_str)

def process_month(month: str, prompt_template: str):
    """Finds all decisions in a month and generates a trace for each."""
    chat_file = os.path.join(DATA_DIR, f"chats_{month}.json")
    if not os.path.exists(chat_file):
        print(f"ℹ️ No chat file for {month}. Skipping.")
        return

    with open(chat_file, "r", encoding="utf-8") as f:
        messages = json.load(f)

    # Create a quick lookup map for message IDs
    message_map = {msg['id']: msg for msg in messages}
    
    decisions_to_process = []
    for msg in messages:
        if "[DECISION:id=" in msg["text"]:
            decision_match = re.search(r"\[DECISION:id=([^\]]+)\]", msg["text"])
            drivers_match = re.search(r"drivers:([M\d,]+)", msg["text"])
            
            if decision_match:
                decision_id = decision_match.group(1)
                driver_ids = drivers_match.group(1).split(',') if drivers_match else []
                decisions_to_process.append({
                    "decision_id": decision_id,
                    "decision_message": msg,
                    "driver_ids": driver_ids
                })

    if not decisions_to_process:
        print(f"ℹ️ No decisions found in {month}.")
        return

    print(f"Found {len(decisions_to_process)} decisions in {month}. Processing...")

    for decision in decisions_to_process:
        # Check if trace file already exists
        out_path = os.path.join(OUTPUT_DIR, f"{decision['decision_id']}.json")
        if os.path.exists(out_path):
            print(f"✔️ Trace for {decision['decision_id']} already exists. Skipping.")
            continue

        # Gather the full driver messages for context
        driver_messages = [message_map[did] for did in decision["driver_ids"] if did in message_map]

        full_prompt = (
            f"{prompt_template}\n\n"
            f"## Input to Analyze:\n\n"
            f"### Decision Message:\n"
            f"{json.dumps(decision['decision_message'], indent=2)}\n\n"
            f"### Driver Messages (Context):\n"
            f"{json.dumps(driver_messages, indent=2)}"
        )
        
        for attempt in range(MAX_RETRIES):
            print(f"  ⏳ Generating trace for {decision['decision_id']} (Attempt {attempt+1})...")
            try:
                result = model.generate_content(full_prompt)
                if not result.parts:
                    raise ValueError("Response was blocked or empty.")
                
                trace_json = clean_and_parse_json(result.text.strip())
                
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(trace_json, f, indent=2, ensure_ascii=False)
                
                print(f"  ✅ Decision trace saved: {out_path}")
                break # Success, break retry loop

            except Exception as e:
                print(f"    🔴 Error on attempt {attempt+1}: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(5)
                else:
                    print(f"    🔴 Failed to generate trace for {decision['decision_id']}.")
        
        # Pause to respect API rate limits
        time.sleep(10)

def main():
    """Main function to generate decision traces for all months."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    try:
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            prompt_template = f.read()
    except FileNotFoundError:
        print(f"🔴 Critical Error: Prompt file not found at {PROMPT_FILE}")
        return

    months = ["January", "February", "March", "April", "May", "June", "July", "August"]
    for m in months:
        process_month(m, prompt_template)
        print("-" * 20)

if __name__ == "__main__":
    main()