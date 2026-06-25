import voyageai
import chromadb
from pypdf import PdfReader
import os 
from dotenv import load_dotenv

load_dotenv()
voyage_key = os.getenv("VOYAGE_API_KEY")


def load_pdf(path):
    reader = PdfReader(path)
    text=""
    for page in reader.pages:
        text += page.extract_text()
    return text


def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


def embed_chunks(chunks):
    vo = voyageai.Client(api_key=voyage_key)
    embeddings = vo.embed(chunks, model="voyage-2").embeddings
    return embeddings


def store_in_chroma(chunks, embeddings):
    chroma_client = chromadb.PersistentClient(path="chroma_db")
    collection = chroma_client.get_or_create_collection(name='Kraken')

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        collection.add(
            ids=[str(i)],
            documents=[chunk],
            embeddings=[embedding]
        )
    print(f"Stored {len(chunks)} chunks in chorma")



if __name__ == "__main__":
    for filename in os.listdir("documents"):
        if filename.endswith(".pdf"):
            path = os.path.join("documents", filename)
            text = load_pdf(path)
            chunks = chunk_text(text)
            embeddings = embed_chunks(chunks)
            store_in_chroma(chunks, embeddings)
            print(f"Ingested: {filename}")





