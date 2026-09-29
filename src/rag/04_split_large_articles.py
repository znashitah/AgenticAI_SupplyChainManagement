from pathlib import Path
import json
import re

INPUT_FILE = Path("data/processed/eu_ai_act_chunks.json")
OUTPUT_FILE = Path("data/processed/eu_ai_act_final_chunks.json")

MAX_CHARS = 8000

articles = json.loads(
    INPUT_FILE.read_text(encoding="utf-8")
)

final_chunks = []

for article in articles:
    text = article["text"]

    # Keep smaller articles as one chunk
    if len(text) <= MAX_CHARS:
        final_chunks.append(article)
        continue

    # Find numbered paragraphs
    paragraph_pattern = re.compile(
        r"(?m)^(?P<number>\d+)\.\s+"
    )

    matches = list(
        paragraph_pattern.finditer(text)
    )

    if not matches:
        final_chunks.append(article)
        continue

    for index, match in enumerate(matches):
        start = match.start()

        end = (
            matches[index + 1].start()
            if index + 1 < len(matches)
            else len(text)
        )

        paragraph_text = text[start:end].strip()

        paragraph_number = int(
            match.group("number")
        )

        # Use the chunk position as well as the paragraph number.
        # This guarantees unique IDs even when the same paragraph
        # number appears more than once in an Article.
        chunk_id = (
            f"eu_ai_act_article_"
            f"{article['article_number']}_"
            f"paragraph_{paragraph_number}_"
            f"chunk_{index + 1}"
        )

        chunk = {
            "id": chunk_id,
            "regulation": article["regulation"],
            "article_number": article["article_number"],
            "article_title": article["article_title"],
            "chapter": article["chapter"],
            "paragraph": paragraph_number,
            "text": paragraph_text,
            "source": article["source"],
            "source_url": article["source_url"]
        }

        final_chunks.append(chunk)

print(f"Original article chunks: {len(articles)}")
print(f"Final RAG chunks: {len(final_chunks)}")

OUTPUT_FILE.write_text(
    json.dumps(
        final_chunks,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)

print(f"Saved final chunks to: {OUTPUT_FILE}")
