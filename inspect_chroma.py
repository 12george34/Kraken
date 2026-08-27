import chromadb
import json

chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(name='Kraken')

# get() with no filter pulls everything in the collection
results = collection.get(include=["documents", "metadatas"])

output = []
for chunk_id, chunk_text, metadata in zip(results["ids"], results["documents"], results["metadatas"]):
    output.append({
        "id": chunk_id,
        "text": chunk_text,
        "source": metadata["source"],
        "chunk_index": metadata["chunk_index"]
    })

with open("chunks_preview.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print(f"Wrote {len(output)} chunks to chunks_preview.json")
