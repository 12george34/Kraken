from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from search import search
from chat import chat


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str
    history: list = []

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    chunks, metadatas = search(req.question)
    answer = chat(req.question, chunks, metadatas, req.history)
    return {"answer": answer}