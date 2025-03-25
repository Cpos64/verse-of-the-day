# 📦 Importing required libraries
import requests  # For making HTTP requests to the Bible API
import random    # For choosing random books, chapters, and verses
import json      # For saving and loading the verse of the day to a file
import os        # For checking if the cache file exists
import argparse  # For parsing command-line arguments
from datetime import datetime  # For working with today's date
from rich.console import Console  # For pretty terminal output
from rich.markdown import Markdown  # To format verse display as Markdown

# 🎨 Initialize console for rich output
console = Console()

# 🌐 API and file setup
BIBLE_API_URL = "https://bible-api.com/"
DATA_FILE = "verse_of_the_day.json"

# 📚 Load structure and themes
with open("bible_structure.json", "r") as f:
    BOOKS = json.load(f)

with open("themes.json", "r") as f:
    THEMES = json.load(f)

# 🔄 Random verse from anywhere
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

# 🎯 Themed verse lookup
def get_themed_verse(theme):
    verses = THEMES.get(theme.lower())
    if not verses:
        return None
    reference = random.choice(verses)
    verse_url = f"{BIBLE_API_URL}{reference.replace(' ', '%20')}"

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
        console.print(f"[red]❌ Error fetching themed verse: {e}[/red]")
        return None

# 💾 Load cached verse
def load_cached_verse():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            if data.get("date") == datetime.today().strftime('%Y-%m-%d'):
                return data
    return None

# 💾 Save verse
def save_verse_of_the_day(verse_data):
    with open(DATA_FILE, "w") as file:
        json.dump(verse_data, file, indent=4)

# 🔗 Bible Hub commentary link
def generate_biblehub_link(reference):
    try:
        book_chapter, verse = reference.split(":")
        parts = book_chapter.strip().split(" ")
        chapter = parts[-1]
        book = "-".join(parts[:-1]).lower().replace(" ", "-")
        return f"https://biblehub.com/{book}/{chapter}-{verse}.htm"
    except Exception:
        return None

# 📖 Main display logic
def display_verse(theme=None, force_new=False):
    verse_data = None if force_new else load_cached_verse()

    if not verse_data:
        if theme:
            verse_data = get_themed_verse(theme)
        if not verse_data:
            verse_data = get_random_verse()
        if verse_data:
            save_verse_of_the_day(verse_data)

    if verse_data:
        console.print(Markdown(f"### 📖 {verse_data['reference']}"))
        console.print(Markdown(f"> {verse_data['text']}"))
        link = generate_biblehub_link(verse_data['reference'])
        if link:
            console.print(f"\n🔍 [link={link}]Read commentary on BibleHub[/link]")
    else:
        console.print("[bold red]⚠️ Failed to retrieve or load verse.[/bold red]")

# 🚀 CLI entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verse of the Day CLI")
    parser.add_argument("--theme", type=str, help="Get a verse from a specific theme (e.g., hope, peace, love)")
    parser.add_argument("--new", action="store_true", help="Force a new verse even if today's verse is cached")
    parser.add_argument("--list", action="store_true", help="List all available themes and exit")
    args = parser.parse_args()

    if args.list:
        console.print("📚 Available Themes:")
        for t in THEMES:
            console.print(f" - {t}")
    else:
        display_verse(theme=args.theme, force_new=args.new)