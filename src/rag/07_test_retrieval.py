import chromadb

DB_PATH = "data/chroma_db"
COLLECTION_NAME = "eu_regulations"

# Connect to the existing ChromaDB database
client = chromadb.PersistentClient(
    path=DB_PATH
)

# Open the existing collection
collection = client.get_collection(
    name=COLLECTION_NAME
)

# Test compliance questions
queries = [
    {
        "name": "Risk Management",
        "query": "What requirements apply to risk management for a high-risk AI system?",
        "expected_article": 9
    },
    {
        "name": "Human Oversight",
        "query": "What requirements apply to human oversight of a high-risk AI system?",
        "expected_article": 14
    },
    {
        "name": "Technical Documentation",
        "query": "What requirements apply to technical documentation for a high-risk AI system?",
        "expected_article": 11
    }
]

print("=" * 70)
print("EU AI ACT RAG RETRIEVAL EVALUATION")
print("=" * 70)

correct = 0

for test in queries:

    print("\n")
    print("=" * 70)
    print(f"TEST: {test['name']}")
    print("=" * 70)

    print(f"\nQuery: {test['query']}")
    print(f"Expected Article: {test['expected_article']}")

    results = collection.query(
        query_texts=[test["query"]],
        n_results=5
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    first_article = metadatas[0].get("article_number")

    if first_article == test["expected_article"]:
        status = "PASS"
        correct += 1
    else:
        status = "CHECK"

    print(f"\nTop result Article: {first_article}")
    print(f"Status: {status}")
    print(f"Distance: {distances[0]:.4f}")

    print("\nTop 5 retrieved Articles:")

    for rank, metadata in enumerate(
        metadatas,
        start=1
    ):
        print(
            f"{rank}. Article "
            f"{metadata.get('article_number')} — "
            f"{metadata.get('article_title')}"
        )

print("\n")
print("=" * 70)
print("EVALUATION SUMMARY")
print("=" * 70)

print(f"Tests passed: {correct}/{len(queries)}")

accuracy = correct / len(queries)

print(f"Top-1 retrieval accuracy: {accuracy:.2%}")
