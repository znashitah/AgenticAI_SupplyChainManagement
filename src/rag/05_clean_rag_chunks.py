from pathlib import Path
import json
import re

INPUT_FILE = Path("data/processed/eu_ai_act_final_chunks.json")
OUTPUT_FILE = Path("data/processed/eu_ai_act_rag_chunks.json")

chunks = json.loads(INPUT_FILE.read_text(encoding="utf-8"))

cleaned_chunks = []

for chunk in chunks:
    text = chunk["text"]

    # Replace non-breaking spaces with normal spaces
    text = text.replace("\xa0", " ")

    # Remove stray backticks
    text = text.replace("`", "")

    # Clean excessive spaces while preserving line breaks
    text = re.sub(r"[ \t]+", " ", text)

    # Remove unnecessary blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Clean spaces at the beginning/end of lines
    text = "\n".join(line.strip() for line in text.splitlines())
    text = text.strip()

    # Extract the article title from the second line when available
    lines = text.splitlines()

    article_title = chunk["article_title"].replace("\xa0", " ").strip()

    if len(lines) >= 2:
        article_number = chunk["article_number"]
        title = lines[1].strip()

        article_title = f"Article {article_number} — {title}"

    cleaned_chunk = {
        "id": chunk["id"],
        "regulation": chunk["regulation"],
        "article_number": chunk["article_number"],
        "article_title": article_title,
        "chapter": chunk["chapter"],
        "paragraph": chunk["paragraph"],
        "text": text,
        "source": chunk["source"],
        "source_url": chunk["source_url"]
    }

    cleaned_chunks.append(cleaned_chunk)

OUTPUT_FILE.write_text(
    json.dumps(cleaned_chunks, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"Input chunks: {len(chunks)}")
print(f"Cleaned chunks: {len(cleaned_chunks)}")
print(f"Saved to: {OUTPUT_FILE}")
