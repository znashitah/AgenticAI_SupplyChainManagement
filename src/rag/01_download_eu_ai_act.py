from pathlib import Path
import requests

URL = "https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1689"
OUTPUT_FILE = Path("data/raw/eu_ai_act.html")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

response = requests.get(
    URL,
    timeout=60,
    headers=headers
)

response.raise_for_status()

print(f"HTTP status: {response.status_code}")
print(f"Downloaded characters: {len(response.text)}")

if len(response.text) == 0:
    raise RuntimeError("Downloaded HTML is empty. Source was not saved.")

OUTPUT_FILE.write_text(response.text, encoding="utf-8")

print(f"Saved source to {OUTPUT_FILE}")
