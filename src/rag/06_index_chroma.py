from pathlib import Path
import json
import chromadb

CHUNKS_FILE = Path(
    "data/processed/eu_ai_act_rag_chunks.json"
)

DB_PATH = "data/chroma_db"

COLLECTION_NAME = "eu_regulations"

# Load the cleaned RAG chunks
chunks = json.loads(
    CHUNKS_FILE.read_text(encoding="utf-8")
)

print(f"Loaded {len(chunks)} chunks")

# Create a persistent ChromaDB client
client = chromadb.PersistentClient(
    path=DB_PATH
)

# Create the collection if it does not already exist
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={
        "description": "EU AI Act regulatory chunks",
        "source": "Regulation (EU) 2024/1689"
    }
)

# Store documents and metadata
collection.upsert(
    ids=[
        chunk["id"]
        for chunk in chunks
    ],
    documents=[
        chunk["text"]
        for chunk in chunks
    ],
    metadatas=[
        {
            "regulation": chunk["regulation"],
            "article_number": chunk["article_number"],
            "article_title": chunk["article_title"],
            "chapter": chunk["chapter"] or "",
            "paragraph": (
                chunk["paragraph"]
                if chunk["paragraph"] is not None
                else ""
            ),
            "source": chunk["source"],
            "source_url": chunk["source_url"]
        }
        for chunk in chunks
    ]
)

print(f"Indexed {len(chunks)} chunks")
print(f"Collection count: {collection.count()}")
print(f"Database path: {DB_PATH}")
print(f"Collection name: {COLLECTION_NAME}")
