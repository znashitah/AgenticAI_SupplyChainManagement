from pathlib import Path
import re
import json

INPUT_FILE = Path("data/processed/eu_ai_act_clean.txt")
OUTPUT_FILE = Path("data/processed/eu_ai_act_chunks.json")

text = INPUT_FILE.read_text(encoding="utf-8")

pattern = re.compile(
    r"(?m)^(Article\s+\d+[^\n]*)$"
)

matches = list(pattern.finditer(text))

chunks = []

for index, match in enumerate(matches):
    start = match.start()
    end = matches[index + 1].start() if index + 1 < len(matches) else len(text)

    article_heading = match.group(1).strip()
    article_text = text[start:end].strip()

    number_match = re.search(
        r"Article\s+(\d+)",
        article_heading
    )

    article_number = (
        int(number_match.group(1))
        if number_match
        else None
    )

    chunks.append({
        "id": f"eu_ai_act_article_{article_number}",
        "regulation": "EU_AI_ACT",
        "article_number": article_number,
        "article_title": article_heading,
        "chapter": None,
        "paragraph": None,
        "text": article_text,
        "source": "Regulation (EU) 2024/1689",
        "source_url": "https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1689"
    })

OUTPUT_FILE.write_text(
    json.dumps(chunks, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"Article headings found: {len(matches)}")
print(f"Created {len(chunks)} article chunks")
print(f"Saved chunks to: {OUTPUT_FILE}")
