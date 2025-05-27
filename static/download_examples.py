import os
import json
import urllib.request
from urllib.error import HTTPError

# List of datasets
datasets = [
    ("ART", "dialogues_qwen2.5-72B/art_22_4"),
    ("BOOKS", "dialogues_qwen2.5-72B/books_89_4"),
    ("CARS", "dialogues_qwen2.5-72B/cars_5_3"),
    ("CELEBRITIES", "dialogues_qwen2.5-72B/celebrities_69_4"),
    ("CODING", "dialogues_qwen2.5-72B/coding_55_4"),
    ("COOKING", "dialogues_qwen2.5-72B/cooking_71_5"),
    ("EDUCATION", "dialogues_llama3-70B_qwen2.5-72B/education_77_7"),
    ("EVENTS", "dialogues_llama3-70B_qwen2.5-72B/events_70_6"),
    ("FASHION", "dialogues_llama3-70B_qwen2.5-72B/fashion_81_3"),
    ("FINANCE", "dialogues_llama3-70B_qwen2.5-72B/finance_1_5"),
    ("FITNESS", "dialogues_llama3-70B_qwen2.5-72B/fitness_2_8"),
    ("FOOD", "dialogues_llama3-70B_qwen2.5-72B/food_28_3"),
    ("GAMING", "dialogues_llama3-70B_qwen2.5-72B/gaming_74_4"),
    ("GARDENING", "dialogues_llama3-70B_qwen2.5-72B/gardening_13_6"),
    ("HEALTH", "dialogues_llama3-70B_qwen2.5-72B/health_92_5"),
    ("HISTORY", "dialogues_llama3-70B_qwen2.5-72B/history_8_5")
]

# Base URLs
base_url_orpheus = "https://huggingface.co/datasets/SALT-Research/DeepDialogue-orpheus/resolve/main/data/"
base_url_xtts = "https://huggingface.co/datasets/SALT-Research/DeepDialogue-xtts/resolve/main/data/"
base_url_json = "https://huggingface.co/datasets/SALT-Research/DeepDialogue-orpheus/raw/main/data/"

# Initialize conversations.json structure
conversations = {"domains": {}}

# Base directory
base_dir = "static/conversations"

for domain, path in datasets:
    # Extract IDs
    file_id = path.split("/")[-1]       # e.g. art_22_4
    file_subid = file_id.split("_", 1)[-1]  # e.g. 22_4

    # Paths
    domain_dir = os.path.join(base_dir, domain.capitalize())
    subdir = os.path.join(domain_dir, file_subid)
    os.makedirs(subdir, exist_ok=True)

    json_filename = f"{file_subid}.json"
    orpheus_filename = f"{file_subid}_orpheus.wav"
    xtts_filename = f"{file_subid}_xtts.wav"

    json_url = f"{base_url_json}{path}.json"
    orpheus_url = f"{base_url_orpheus}{path}/{file_id}_full.wav?download=true"
    xtts_url = f"{base_url_xtts}{path}/{file_id}_full.wav?download=true"

    json_dest = os.path.join(subdir, json_filename)
    orpheus_dest = os.path.join(subdir, orpheus_filename)
    xtts_dest = os.path.join(subdir, xtts_filename)

    # Download files
    try:
        print(f"Downloading JSON: {json_url}")
        urllib.request.urlretrieve(json_url, json_dest)
    except HTTPError as e:
        print(f"Failed to download {json_url}: {e}")
        continue

    try:
        print(f"Downloading Orpheus TTS: {orpheus_url}")
        urllib.request.urlretrieve(orpheus_url, orpheus_dest)
    except HTTPError as e:
        print(f"Failed to download {orpheus_url}: {e}")
        continue

    try:
        print(f"Downloading XTTS TTS: {xtts_url}")
        urllib.request.urlretrieve(xtts_url, xtts_dest)
    except HTTPError as e:
        print(f"Failed to download {xtts_url}: {e}")
        continue

    # Update conversations.json
    entry = {
        "id": "1",  # Can be replaced with unique IDs if needed
        "json_path": f"{base_dir}/{domain.capitalize()}/{file_subid}/{json_filename}",
        "orpheus_tts": f"{base_dir}/{domain.capitalize()}/{file_subid}/{orpheus_filename}",
        "xtts_tts": f"{base_dir}/{domain.capitalize()}/{file_subid}/{xtts_filename}"
    }

    if domain.capitalize() not in conversations["domains"]:
        conversations["domains"][domain.capitalize()] = []

    conversations["domains"][domain.capitalize()].append(entry)

# Write conversations.json
conversations_path = os.path.join(base_dir, "conversations.json")
with open(conversations_path, "w") as f:
    json.dump(conversations, f, indent=2)

print("\n✅ All files downloaded and conversations.json updated.")
