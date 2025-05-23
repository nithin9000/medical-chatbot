// src/components/TypingDots.tsx
import React from "react";

export const TypingDots: React.FC = () => {
  return (
    <div className="inline-block bg-gray-200 px-4 py-2 rounded-lg">
      <span className="text-gray-500 italic flex items-center gap-1">
        MedBot is typing
        <span className="animate-typing">.</span>
        <span className="animate-typing-delay-100">.</span>
        <span className="animate-typing-delay-200">.</span>
      </span>
    </div>
  );
};