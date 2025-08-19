import json

with open("./data/chats_January.json", "r", encoding="utf-8") as f:
    chat = json.load(f)

print("Valid JSON ✅", len(chat), "messages")