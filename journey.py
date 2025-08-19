import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
import time
import re
from datetime import datetime, timedelta

# --- Setup ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-pro")

# --- Constants ---
DATA_DIR = "./data"
INPUT_CHAT_FILE = os.path.join(DATA_DIR, "all_chats.json")
OUTPUT_EPISODES_FILE = os.path.join(DATA_DIR, "journey_episodes.json")
PROMPT_FILE = "./prompts/journey_summary.md"
MAX_RETRIES = 3

def clean_and_parse_json(raw_text: str):
    """Cleans the raw text to extract and parse a JSON object."""
    match = re.search(r'\{.*\}', raw_text, re.DOTALL)
    if not match:
        raise ValueError("No valid JSON object found in the model's output.")
    json_str = match.group(0)
    return json.loads(json_str)

def group_messages_by_week(messages):
    """Groups messages into weekly chunks."""
    if not messages:
        return []

    weekly_chunks = []
    start_date = datetime.fromisoformat(messages[0]['ts']).date()
    end_of_week = start_date + timedelta(days=6 - start_date.weekday())
    
    current_chunk = []
    for msg in messages:
        msg_date = datetime.fromisoformat(msg['ts']).date()
        if msg_date <= end_of_week:
            current_chunk.append(msg)
        else:
            if current_chunk:
                weekly_chunks.append(current_chunk)
            current_chunk = [msg]
            start_date = msg_date
            end_of_week = start_date + timedelta(days=6 - start_date.weekday())
    
    if current_chunk:
        weekly_chunks.append(current_chunk)
        
    return weekly_chunks

def generate_episode(message_chunk):
    """Generates a single journey episode summary from a chunk of messages."""
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    # Convert the message chunk back to a JSON string for the prompt
    messages_json_str = json.dumps(message_chunk, indent=2)
    full_prompt = f"{prompt_template}\n\n## Messages to Summarize:\n{messages_json_str}"

    for attempt in range(MAX_RETRIES):
        try:
            print(f"  - Attempt {attempt + 1}/{MAX_RETRIES}...")
            result = model.generate_content(full_prompt)
            
            if not result.parts:
                raise ValueError("Response was blocked or empty.")

            episode = clean_and_parse_json(result.text.strip())
            return episode

        except Exception as e:
            print(f"    - Error on attempt {attempt + 1}: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(5 * (attempt + 1))
            else:
                print(f"    - All retries failed for this chunk.")
                return None
    return None

def main():
    """Main function to process chats and generate journey episodes."""
    print(f"⏳ Loading chats from {INPUT_CHAT_FILE}...")
    try:
        with open(INPUT_CHAT_FILE, "r", encoding="utf-8") as f:
            all_messages = json.load(f)
    except FileNotFoundError:
        print(f"🔴 Error: Input file not found at {INPUT_CHAT_FILE}. Please generate chats first.")
        return

    print("📚 Grouping messages into weekly chunks...")
    weekly_chunks = group_messages_by_week(all_messages)
    print(f"📊 Found {len(weekly_chunks)} weeks of conversation.")

    journey_episodes = []
    for i, chunk in enumerate(weekly_chunks):
        first_date = chunk[0]['ts'].split(' ')[0]
        last_date = chunk[-1]['ts'].split(' ')[0]
        print(f"\n⏳ Processing Week {i+1} ({first_date} to {last_date})...")
        
        episode = generate_episode(chunk)
        if episode:
            journey_episodes.append(episode)
            print(f"✅ Successfully generated episode for Week {i+1}.")
        else:
            print(f"🔴 Failed to generate episode for Week {i+1}. Skipping.")

        # Pause to respect API rate limits
        if i < len(weekly_chunks) - 1:
            print("--- Pausing for 20 seconds ---")
            time.sleep(20)

    if not journey_episodes:
        print("🔴 No journey episodes were generated. Exiting.")
        return

    with open(OUTPUT_EPISODES_FILE, "w", encoding="utf-8") as f:
        json.dump(journey_episodes, f, indent=2, ensure_ascii=False)

    print(f"\n\n🎉 Success! All episodes saved to {OUTPUT_EPISODES_FILE}.")
    print(f"Total episodes generated: {len(journey_episodes)}")

if __name__ == "__main__":
    main()