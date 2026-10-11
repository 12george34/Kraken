import { useEffect, useRef, useState } from "react";
import { sendChat } from "./api";
import { ChatInput } from "./components/ChatInput";
import { MessageBubble, TypingBubble } from "./components/MessageBubble";
import type { ChatMessage, HistoryMessage } from "./types";

const WELCOME: ChatMessage = {
  id: "welcome",
  role: "assistant",
  content:
    "Hi! Ask me anything about your documents. I'll tell you which document an answer came from.",
};

let nextId = 0;
const makeId = () => `m${nextId++}`;

export default function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([WELCOME]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  // Keep the newest message in view
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSend(question: string) {
    // Backend history = real conversation only: no welcome text, no errors
    const history: HistoryMessage[] = messages
      .filter((m) => m.id !== WELCOME.id && !m.isError)
      .map(({ role, content }) => ({ role, content }));

    setMessages((prev) => [
      ...prev,
      { id: makeId(), role: "user", content: question },
    ]);
    setLoading(true);

    try {
      const answer = await sendChat(question, history);
      setMessages((prev) => [
        ...prev,
        { id: makeId(), role: "assistant", content: answer },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          id: makeId(),
          role: "assistant",
          content:
            "Couldn't reach the server. Check that the backend is running and try again.",
          isError: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleClear() {
    setMessages([WELCOME]);
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Kraken Assistant</h1>
        <button className="ghost" onClick={handleClear} disabled={loading}>
          New chat
        </button>
      </header>

      <main className="messages">
        {messages.map((m) => (
          <MessageBubble key={m.id} message={m} />
        ))}
        {loading && <TypingBubble />}
        <div ref={bottomRef} />
      </main>

      <ChatInput disabled={loading} onSend={handleSend} />
    </div>
  );
}
