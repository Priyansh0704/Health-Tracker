import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
import time
import re

# --- Setup ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-pro")

# --- Constants ---
MAX_RETRIES = 3
MONTHS_TO_GENERATE = ["January", "February", "March", "April", "May", "June", "July", "August"]
DATA_DIR = "./data"

def clean_and_parse_json(raw_text: str):
    """Cleans the raw text to extract and parse the main JSON array."""
    match = re.search(r'\[.*\]', raw_text, re.DOTALL)
    if not match:
        raise ValueError("No valid JSON array found in the model's output.")
    json_str = match.group(0)
    return json.loads(json_str)

def generate_chat(month: str, prev_summary: str = ""):
    """Generates, validates, and saves chat messages and their summary for a given month."""
    with open("./prompts/chat_generation.md", "r", encoding="utf-8") as f:
        prompt_template = f.read()

    full_prompt = (
        f"{prompt_template}\n\n"
        f"Last month summary: {prev_summary if prev_summary else 'This is the first month.'}\n\n"
        f"Now generate ~120–150 chat messages for {month} 2025. "
        f"Strict JSON array only, no explanation."
    )

    for attempt in range(MAX_RETRIES):
        print(f"\n⏳ Generating chats for {month} (Attempt {attempt + 1}/{MAX_RETRIES})...")
        try:
            result = model.generate_content(full_prompt)
            if not result.parts:
                print(f"⚠️ Attempt {attempt + 1} failed for {month}: Response was blocked or empty.")
                time.sleep(5 * (attempt + 1))
                continue
            
            content = result.text.strip()
            messages = clean_and_parse_json(content)
            
            if len(messages) < 120:
                # Handle continuation...
                time.sleep(5)
                # (omitted for brevity, your existing continuation logic is fine here)

            if len(messages) > 150:
                messages = messages[:150]

            # On success, save both chat and summary
            chat_file_path = os.path.join(DATA_DIR, f"chats_{month}.json")
            summary_file_path = os.path.join(DATA_DIR, f"summary_{month}.txt")

            with open(chat_file_path, "w", encoding="utf-8") as f:
                json.dump(messages, f, indent=2, ensure_ascii=False)
            print(f"✅ Chat for {month} saved at {chat_file_path}")

            time.sleep(5)
            summary_prompt = f"Summarize key events from these chats in 3-4 sentences:\n\n{json.dumps(messages)}"
            summary_result = model.generate_content(summary_prompt)
            month_summary = summary_result.text.strip()

            with open(summary_file_path, "w", encoding="utf-8") as f:
                f.write(month_summary)
            print(f"✅ Summary for {month} saved at {summary_file_path}")
            
            return month_summary

        except Exception as e:
            print(f"🔴 Attempt {attempt + 1} failed for {month} with error: {e}")
            if "quota" in str(e).lower():
                print("🔴 Quota error. Waiting longer before next attempt...")
                time.sleep(60)
            elif attempt < MAX_RETRIES - 1:
                time.sleep(5 * (attempt + 1))
            else:
                print(f"🔴 All attempts failed for {month}. Skipping.")
                return None
    return None

def generate_all_months():
    """Loops through all months, using cached summaries where possible."""
    os.makedirs(DATA_DIR, exist_ok=True)
    prev_summary = ""
    for month in MONTHS_TO_GENERATE:
        chat_file_path = os.path.join(DATA_DIR, f"chats_{month}.json")
        summary_file_path = os.path.join(DATA_DIR, f"summary_{month}.txt")

        if os.path.exists(chat_file_path):
            print(f"\n✔️ Chat file for {month} already exists.")
            if os.path.exists(summary_file_path):
                print(f"✔️ Loading summary for {month} from cache.")
                with open(summary_file_path, "r", encoding="utf-8") as f:
                    prev_summary = f.read()
            else:
                print(f"⏳ Generating summary for existing {month} chat file...")
                try:
                    with open(chat_file_path, "r", encoding="utf-8") as f:
                        existing_data = json.load(f)
                    summary_prompt = f"Summarize key events from these chats in 3-4 sentences:\n\n{json.dumps(existing_data)}"
                    summary_result = model.generate_content(summary_prompt)
                    prev_summary = summary_result.text.strip()
                    with open(summary_file_path, "w", encoding="utf-8") as f:
                        f.write(prev_summary)
                    print(f"✅ Summary for {month} saved.")
                except Exception as e:
                    print(f"🔴 Could not generate summary for {month} due to error: {e}")
                    print("🔴 Stopping to prevent further errors.")
                    return # Stop if we hit an error here
            continue

        # If chat file does not exist, generate it
        month_summary = generate_chat(month, prev_summary)
        if month_summary:
            prev_summary = month_summary
        else:
            prev_summary = f"Summary for {month} could not be generated."
        
        print("\n--- Pausing for 65 seconds to respect API rate limits ---")
        time.sleep(65)

def consolidate_chats():
    # ... (This function remains unchanged)
    print("\n⏳ Consolidating all generated chat files...")
    all_messages = []
    for month in MONTHS_TO_GENERATE:
        file_path = os.path.join(DATA_DIR, f"chats_{month}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                monthly_data = json.load(f)
                all_messages.extend(monthly_data)
                print(f"✔️ Loaded {file_path}")
        else:
            print(f"⚠️ File not found: {file_path}. It will be skipped.")
    if not all_messages:
        print("No messages to consolidate. Exiting.")
        return
    consolidated_file_path = os.path.join(DATA_DIR, "all_chats.json")
    with open(consolidated_file_path, "w", encoding="utf-8") as f:
        json.dump(all_messages, f, indent=2, ensure_ascii=False)
    print(f"✅ All chats consolidated into {consolidated_file_path} ({len(all_messages)} total messages)")


if __name__ == "__main__":
    # IMPORTANT: Wait for your daily quota to reset before running this.
    # This might mean waiting until tomorrow.
    generate_all_months()
    consolidate_chats()