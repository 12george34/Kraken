import type { ChatRequest, ChatResponse, HistoryMessage } from "./types";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

// Calls POST /chat on the FastAPI backend.
// `history` is everything said BEFORE this question; the backend adds the
// new question (plus retrieved context) itself.
export async function sendChat(
  question: string,
  history: HistoryMessage[],
): Promise<string> {
  const body: ChatRequest = { question, history };

  const res = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    throw new Error(`Server returned ${res.status}`);
  }

  const data = (await res.json()) as ChatResponse;
  return data.answer;
}
