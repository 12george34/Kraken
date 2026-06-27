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


def chunk_text(text, max_size=500):
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks = []
    current = ""

    for paragraph in paragraphs:
        if len(current) + len(paragraph) <= max_size:
            current += " " + paragraph
        else:
            if current:
                chunks.append(current.strip())
            current = paragraph
    
    if current:
        chunks.append(current.strip())

    return chunks
    


def embed_chunks(chunks):
    vo = voyageai.Client(api_key=voyage_key)
    embeddings = vo.embed(chunks, model="voyage-2").embeddings
    return embeddings


def store_in_chroma(chunks, embeddings, filename):
    chroma_client = chromadb.PersistentClient(path="chroma_db")
    collection = chroma_client.get_or_create_collection(name='Kraken')

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        collection.add(
            ids=[f"{filename}_{i}"],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{"source": filename, "chunk_index": i}]
        )
    print(f"Stored {len(chunks)} chunks in chorma")



if __name__ == "__main__":
    for filename in os.listdir("documents"):
        if filename.endswith(".pdf"):
            path = os.path.join("documents", filename)
            text = load_pdf(path)
            chunks = chunk_text(text)
            embeddings = embed_chunks(chunks)
            store_in_chroma(chunks, embeddings, filename)
            print(f"Ingested: {filename}")





