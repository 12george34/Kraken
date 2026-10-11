import type { ChatMessage } from "../types";

export function MessageBubble({ message }: { message: ChatMessage }) {
  const cls = [
    "bubble",
    message.role === "user" ? "bubble-user" : "bubble-assistant",
    message.isError ? "bubble-error" : "",
  ].join(" ");

  return (
    <div className={`row row-${message.role}`}>
      <div className={cls}>{message.content}</div>
    </div>
  );
}

export function TypingBubble() {
  return (
    <div className="row row-assistant">
      <div className="bubble bubble-assistant typing" aria-label="Assistant is typing">
        <span />
        <span />
        <span />
      </div>
    </div>
  );
}
