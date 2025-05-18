import { useState } from "react";
import { TypingDots } from "./components/TypingDots";
import { ThemeToggle } from './components/ThemeToggle';
import "./index.css"; // or index.css if you're importing Tailwind here

export type ChatMessage = {
  role: "user" | "bot";
  text: string;
};

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg: ChatMessage = { role: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMsg.text }),
      });

      const data = await res.json();
      const botMsg: ChatMessage = { role: "bot", text: data.response };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "❌ Failed to get response." },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-2xl mx-auto bg-white rounded shadow p-4 flex flex-col">
        <h1 className="text-xl font-bold text-center mb-4">🩺 MedBot</h1>
		<ThemeToggle />

        <div className="flex-1 overflow-y-auto mb-4 space-y-2 max-h-[70vh]">
          {messages.map((msg, i) => (
            <div key={i} className={msg.role === "user" ? "text-right" : "text-left"}>
              <div className={`inline-block px-4 py-2 rounded-lg ${msg.role === "user" ? "bg-blue-100" : "bg-gray-200"}`}>
                <pre className="whitespace-pre-wrap">{msg.text}</pre>
              </div>
            </div>
          ))}

          {loading && (
            <div className="text-left">
              <TypingDots />
            </div>
          )}
        </div>

        <form onSubmit={handleSend} className="flex">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1 px-4 py-2 border rounded-l-md focus:outline-none"
            placeholder="Type your question..."
          />
          <button type="submit" className="bg-blue-600 text-white px-4 rounded-r-md hover:bg-blue-700">
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;