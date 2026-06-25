import os
from dotenv import load_dotenv
import anthropic


load_dotenv()
anthropic_key = os.getenv("ANTHROPIC_API_KEY")

def chat(question, chunks):
    client = anthropic.Anthropic(api_key=anthropic_key)

    context = '\n\n'.join(chunks)

    response = client.messages.create(
        model='claude-haiku-4-5-20251001',
        max_tokens=1024,
        system="You are a helpful assistant for a business. Answer the user's question using only the context provided. If the answer is not in the context, say 'I dont have that information.'",
        messages=[
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
    )
    
    return response.content[0].text


if __name__ == "__main__":
    from search import search

    question = input("Ask a question: ")
    chunks = search(question)
    answer = chat(question, chunks)
    print(f"\nAnswer: {answer}")