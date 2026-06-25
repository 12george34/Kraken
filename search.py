import os 
from dotenv import load_dotenv
import voyageai
import chromadb

load_dotenv()
voyage_key = os.getenv("VOYAGE_API_KEY")

def search(question, top_k=3):
    vo = voyageai.Client(api_key=voyage_key)
    question_embedding = vo.embed([question], model='voyage-2').embeddings[0]

    chroma_client = chromadb.PersistentClient(path="chroma_db")
    collection = chroma_client.get_or_create_collection(name='Kraken')  

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    return results['documents'][0]


if __name__ == "__main__":
    question = input("Ask the question: ")
    results = search(question)
    for chunk in results:
        print("\n---")
        print(chunk)