export type ChatMessage = {
  role: "user" | "bot";
  text: string;
};

export type ChatSession = {
  id: string;
  title: string;
  messages: ChatMessage[];
};