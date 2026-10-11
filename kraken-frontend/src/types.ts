// Matches the shape your FastAPI backend expects in `history`
export type Role = "user" | "assistant";

export interface HistoryMessage {
  role: Role;
  content: string;
}

// UI-only message: same as history, plus an id and an error flag
export interface ChatMessage extends HistoryMessage {
  id: string;
  isError?: boolean;
}

// Matches ChatRequest in api.py
export interface ChatRequest {
  question: string;
  history: HistoryMessage[];
}

// Matches the return value of chat_endpoint in api.py
export interface ChatResponse {
  answer: string;
}
