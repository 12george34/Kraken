import os
from dotenv import load_dotenv
import anthropic


load_dotenv()
anthropic_key = os.getenv("ANTHROPIC_API_KEY")

def chat(question, chunks, metadatas, history=[]):
    client = anthropic.Anthropic(api_key=anthropic_key)

    context = '\n\n'.join([f"{chunk}\nSource: {meta['source']}" for chunk, meta in zip(chunks, metadatas)])

    messages = history + [
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]

    response = client.messages.create(
        model='claude-haiku-4-5-20251001',
        max_tokens=1024,
        system="You are a helpful assistant for a business. When the answer is clearly in the context provided, use it and mention which document it came from. When the answer is not in the context, use your general knowledge to help but clearly say 'This is not from your documents, but generally speaking...'",
        messages=messages
    )
    
    return response.content[0].text


if __name__ == "__main__":
    from search import search

    history = []
    while True:
        question = input("Ask a question: ")
        chunks, metadatas = search(question)
        answer = chat(question, chunks, metadatas, history)
        print(f"\nAnswer: {answer}")
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": answer})