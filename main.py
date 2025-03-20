import requests
import random
from rich.console import Console
from rich.markdown import Markdown

# Initialize rich console for better CLI formatting
console = Console()

# API URL for fetching Bible verses
BIBLE_API_URL = "https://bible-api.com/"

# Dictionary with books and the number of chapters, plus a dictionary of verses per chapter
BOOKS = {
    "Genesis": {1: 31, 2: 25, 3: 24, 4: 26, 5: 32, 6: 22, 7: 24, 8: 22, 9: 29, 10: 32},
    "Psalms": {1: 6, 2: 12, 3: 8, 4: 8, 5: 12, 6: 10, 7: 17, 8: 9, 9: 20, 10: 18, 11: 7, 12: 8, 13: 6, 14: 7, 15: 5, 16: 11, 17: 15, 18: 50, 19: 14, 20: 9, 21: 13, 22: 31, 23: 6, 24: 10, 25: 22},  # Example
    "Proverbs": {1: 33, 2: 22, 3: 35, 4: 27, 5: 23, 6: 35, 7: 27, 8: 36, 9: 18, 10: 32, 11: 31, 12: 28},
    "Matthew": {1: 25, 2: 23, 3: 17, 4: 25, 5: 48, 6: 34, 7: 29, 8: 34, 9: 38, 10: 42},
    "John": {1: 51, 2: 25, 3: 36, 4: 54, 5: 47, 6: 71, 7: 53, 8: 59, 9: 41, 10: 42},
    "Romans": {1: 32, 2: 29, 3: 31, 4: 25, 5: 21, 6: 23, 7: 25, 8: 39, 9: 33, 10: 21},
    "1 Corinthians": {1: 31, 2: 16, 3: 23, 4: 21, 5: 13, 6: 20, 7: 40, 8: 13, 9: 27, 10: 33},
}

def get_random_verse():
    """Fetches a single random Bible verse with correct chapter-verse selection."""
    book = random.choice(list(BOOKS.keys()))  # Pick a random book
    chapter = random.choice(list(BOOKS[book].keys()))  # Pick a valid chapter
    max_verse = BOOKS[book][chapter]  # Get the max verses for that chapter
    verse = random.randint(1, max_verse)  # Pick a random verse

    verse_url = f"{BIBLE_API_URL}{book} {chapter}:{verse}"  # Format API URL

    try:
        response = requests.get(verse_url, timeout=10)  # Add timeout to prevent long waits
        response.raise_for_status()  # Raise an error if request fails
        data = response.json()

        verse_text = data["text"].strip()
        verse_reference = data["reference"]
        return verse_text, verse_reference

    except requests.RequestException as e:
        console.print("[red]❌ Error fetching verse:[/red]", str(e))
        return None, None

def display_verse():
    """Displays a random Bible verse in the terminal."""
    verse, reference = get_random_verse()
    if verse and reference:
        console.print(Markdown(f"### 📖 {reference}"))
        console.print(Markdown(f"> {verse}"))
    else:
        console.print("[bold red]⚠️ Failed to retrieve a verse.[/bold red]")

if __name__ == "__main__":
    display_verse()
