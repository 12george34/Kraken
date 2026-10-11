import { useState } from "react";
import type { FormEvent, KeyboardEvent } from "react";

interface Props {
  disabled: boolean;
  onSend: (text: string) => void;
}

export function ChatInput({ disabled, onSend }: Props) {
  const [text, setText] = useState("");

  function submit() {
    const trimmed = text.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setText("");
  }

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    submit();
  }

  // Enter sends, Shift+Enter adds a new line
  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  }

  return (
    <form className="input-bar" onSubmit={handleSubmit}>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask a question about your documents..."
        rows={1}
        disabled={disabled}
      />
      <button type="submit" disabled={disabled || !text.trim()}>
        Send
      </button>
    </form>
  );
}
