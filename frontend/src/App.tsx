import { useEffect, useRef, useState } from "react";
import { v4 as uuidv4 } from "uuid";
import EmailConfirmation from "./EmailConfirmation";


export type ChatMessage = {
  role: "user" | "bot";
  text: string;
  timestamp: string;
};

export type ChatSession = {
  id: string;
  title: string;
  messages: ChatMessage[];
};

function App() {
  const [chatSessions, setChatSessions] = useState<ChatSession[]>([]);
  const [currentChatId, setCurrentChatId] = useState<string>("");
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const currentSession = chatSessions.find(chat => chat.id === currentChatId);
  const messages = currentSession?.messages || [];

  useEffect(() => {
    const id = uuidv4();
    const initialSession: ChatSession = {
      id,
      title: "New Chat",
      messages: [],
    };
    setChatSessions([initialSession]);
    setCurrentChatId(id);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const userMsg: ChatMessage = {
      role: "user",
      text: input,
      timestamp: now,
    };

    // Update chat sessions with new user message
    const updatedChats = chatSessions.map(chat => {
      if (chat.id === currentChatId) {
        const newMessages = [...chat.messages, userMsg];
        return {
          ...chat,
          title: chat.title === "New Chat" ? input.slice(0, 30) : chat.title,
          messages: newMessages,
        };
      }
      return chat;
    });

    setChatSessions(updatedChats);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          message: userMsg.text,
          session_id: currentChatId // Send current chat session id
        }),
      });

      const data = await res.json();

      const botMsg: ChatMessage = {
        role: "bot",
        text: data.response,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      // Append bot's response to chat
      setChatSessions(prev =>
        prev.map(chat =>
          chat.id === currentChatId
            ? { ...chat, messages: [...chat.messages, botMsg] }
            : chat
        )
      );
    } catch {
      const failMsg: ChatMessage = {
        role: "bot",
        text: "❌ Failed to get response.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setChatSessions(prev =>
        prev.map(chat =>
          chat.id === currentChatId
            ? { ...chat, messages: [...chat.messages, failMsg] }
            : chat
        )
      );
    }

    setLoading(false);
  };

  const startNewChat = () => {
    const id = uuidv4();
    const newChat: ChatSession = {
      id,
      title: "New Chat",
      messages: [],
    };
    setChatSessions([newChat, ...chatSessions]);
    setCurrentChatId(id);
  };

  const handleDeleteChat = (id: string) => {
    const updated = chatSessions.filter(chat => chat.id !== id);
    setChatSessions(updated);

    if (id === currentChatId && updated.length > 0) {
      setCurrentChatId(updated[0].id);
    } else if (updated.length === 0) {
      setCurrentChatId("");
    }
  };

  return (
    <div className="flex flex-col h-screen bg-[#343541] text-white">
      {/* Top bar */}
      <header className="bg-[#202123] text-white py-3 text-xl font-bold shadow-md flex justify-center items-center">
        🩺 MedBot
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <aside className="w-64 bg-[#202123] text-white border-r border-gray-700 p-4 overflow-y-auto">
          <h2 className="text-lg font-bold mb-4">💬 Chat History</h2>
          <button
            onClick={startNewChat}
            className="w-full bg-[#10a37f] hover:bg-[#0b7c62] text-white px-3 py-2 rounded mb-4"
          >
            + New Chat
          </button>
          <ul className="space-y-2">
            {chatSessions.map(session => (
              <li
                key={session.id}
                className={`flex justify-between items-center truncate px-3 py-2 rounded hover:bg-[#444654] ${
                  session.id === currentChatId ? "bg-[#40414f]" : ""
                }`}
              >
                <div
                  className="flex-1 cursor-pointer truncate"
                  onClick={() => setCurrentChatId(session.id)}
                  title={session.title}
                >
                  {session.title}
                </div>
                <button
                  onClick={() => handleDeleteChat(session.id)}
                  className="text-red-400 hover:text-red-600 ml-2 text-sm cursor-pointer"
                  title="Delete chat"
                >
                  ✖
                </button>
              </li>
            ))}
          </ul>
        </aside>

        {/* Chat Area */}
        <main className="flex-1 flex flex-col bg-[#343541]">
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                <div className={`flex items-start max-w-[75%] ${msg.role === "user" ? "flex-row-reverse space-x-reverse" : "space-x-2"}`}>
                  {/* Avatar */}
                  <div className="w-8 h-8 rounded-full flex items-center justify-center text-lg font-bold">
                    {msg.role === "bot" ? "🤖" : "💀"}
                  </div>

                  {/* Message + timestamp */}
                  <div className="flex flex-col">
                    {msg.role === "bot" && msg.text.includes("<a ")
                      ? (
                        <div
                          className="bg-[#444654] text-white p-3 rounded-lg text-sm leading-relaxed"
                          dangerouslySetInnerHTML={{ __html: msg.text }}
                        />
                      ) : (
                        <div
                          className={`p-3 rounded-lg text-sm leading-relaxed whitespace-pre-wrap ${
                            msg.role === "user"
                              ? "bg-[#10a37f] text-white"
                              : "bg-[#444654] text-white"
                          }`}
                        >
                          {msg.text}
                        </div>
                      )}
                    <span className="text-xs text-gray-400 mt-1 text-right">{msg.timestamp}</span>
                  </div>
                </div>
              </div>
            ))}
            {loading && (
              <div className="text-sm italic text-gray-400">MedBot is typing...</div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <form onSubmit={handleSend} className="p-4 bg-[#40414f] flex border-t border-gray-700">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="flex-1 p-3 rounded-l-md border border-gray-600 bg-[#40414f] text-white focus:outline-none"
              placeholder="Type your medical question..."
            />
            <button
              type="submit"
              className="bg-[#10a37f] text-white px-5 py-3 rounded-r-md hover:bg-[#0b7c62]"
            >
              Send
            </button>
          </form>
        </main>
      </div>
    </div>
  );
}

export default App;
