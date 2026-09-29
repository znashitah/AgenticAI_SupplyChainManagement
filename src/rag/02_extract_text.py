from pathlib import Path
from bs4 import BeautifulSoup

INPUT_FILE = Path("data/raw/eu_ai_act.html")
OUTPUT_FILE = Path("data/processed/eu_ai_act.txt")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

html = INPUT_FILE.read_text(encoding="utf-8")
soup = BeautifulSoup(html, "lxml")

for element in soup(["script", "style", "noscript"]):
    element.decompose()

text = soup.get_text("\n")
lines = [line.strip() for line in text.splitlines()]
lines = [line for line in lines if line]

clean_text = "\n".join(lines)
OUTPUT_FILE.write_text(clean_text, encoding="utf-8")

print(f"Saved cleaned text to {OUTPUT_FILE}")
print(f"Characters: {len(clean_text)}")
