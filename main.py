import requests
import random
import json
import os
from datetime import datetime
from rich.console import Console
from rich.markdown import Markdown

console = Console()

BIBLE_API_URL = "https://bible-api.com/"
DATA_FILE = "verse_of_the_day.json"

BOOKS = {
    "Genesis": {1: 31, 2: 25, 3: 24, 4: 26, 5: 32},
    "Psalms": {1: 6, 2: 12, 3: 8, 4: 8, 5: 12},
    "Proverbs": {1: 33, 2: 22, 3: 35, 4: 27, 5: 23},
    "Matthew": {1: 25, 2: 23, 3: 17, 4: 25, 5: 48},
    "John": {1: 51, 2: 25, 3: 36, 4: 54, 5: 47},
    "Romans": {1: 32, 2: 29, 3: 31, 4: 25, 5: 21},
    "1 Corinthians": {1: 31, 2: 16, 3: 23, 4: 21, 5: 13},
}

def get_random_verse():
    book = random.choice(list(BOOKS.keys()))
    chapter = random.choice(list(BOOKS[book].keys()))
    verse = random.randint(1, BOOKS[book][chapter])
    verse_url = f"{BIBLE_API_URL}{book} {chapter}:{verse}"

    try:
        response = requests.get(verse_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "text": data["text"].strip(),
            "reference": data["reference"],
            "date": datetime.today().strftime('%Y-%m-%d')
        }
    except requests.RequestException as e:
        console.print(f"[red]❌ Error fetching verse: {e}[/red]")
        return None

def load_cached_verse():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            if data.get("date") == datetime.today().strftime('%Y-%m-%d'):
                return data
    return None

def save_verse_of_the_day(verse_data):
    with open(DATA_FILE, "w") as file:
        json.dump(verse_data, file, indent=4)

def generate_biblehub_link(reference):
    """Converts a reference like 'John 3:16' into a Bible Hub URL."""
    try:
        book_chapter, verse = reference.split(":")
        parts = book_chapter.strip().split(" ")
        chapter = parts[-1]
        book = "-".join(parts[:-1]).lower().replace(" ", "-")
        return f"https://biblehub.com/{book}/{chapter}-{verse}.htm"
    except Exception as e:
        return None

def display_verse():
    verse_data = load_cached_verse()
    if not verse_data:
        verse_data = get_random_verse()
        if verse_data:
            save_verse_of_the_day(verse_data)

    if verse_data:
        console.print(Markdown(f"### 📖 {verse_data['reference']}"))
        console.print(Markdown(f"> {verse_data['text']}"))

        # Add commentary link
        commentary_url = generate_biblehub_link(verse_data['reference'])
        if commentary_url:
            console.print(f"\n🔍 [link={commentary_url}]Read commentary on BibleHub[/link]")
        else:
            console.print("❓ Could not generate commentary link.")
    else:
        console.print("[bold red]⚠️ Failed to retrieve or load verse.[/bold red]")

if __name__ == "__main__":
    display_verse()
