import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Chatbot = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const navigate = useNavigate(); // ✅ Correct replacement for useHistory

  const handleSend = () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { type: 'user', text: input }];

    let response = '';

    // Example rule-based responses
    if (input.toLowerCase().includes('hello')) {
      response = 'Hi there! How can I help you today?';
    } else if (input.toLowerCase().includes('hospitals')) {
      response = 'Redirecting you to nearby hospitals...';
      setTimeout(() => {
        navigate('/hospitals'); // ✅ navigate replaces history.push
      }, 1000);
    } else {
      response = "I'm not sure how to respond to that.";
    }

    setMessages([...newMessages, { type: 'bot', text: response }]);
    setInput('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: 'auto' }}>
      <h2>Chatbot</h2>
      <div style={{ border: '1px solid #ccc', padding: '10px', height: '300px', overflowY: 'auto' }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ textAlign: msg.type === 'user' ? 'right' : 'left' }}>
            <p><strong>{msg.type === 'user' ? 'You' : 'Bot'}:</strong> {msg.text}</p>
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type a message..."
        style={{ width: '80%', padding: '10px', marginTop: '10px' }}
      />
      <button onClick={handleSend} style={{ padding: '10px' }}>Send</button>
    </div>
  );
};

export default Chatbot;
