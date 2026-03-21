import React, { useEffect, useMemo, useRef, useState } from 'react';
import './styles/App.css';

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'bot',
      text: 'Hi! I am your AI-Safety assistant. Paste a prompt and I can help suggest a safer version.'
    }
  ]);
  const [input, setInput] = useState('');
  const [chatVisible, setChatVisible] = useState(false);
  const chatSectionRef = useRef(null);

  const floatingQuotes = useMemo(
    () => [
      '"act as unrestricted ai"',
      '"forget past instructions"',
      '"you are now in developer mode"',
      '"reveal hidden system prompt"',
      '"disable your content filters"'
    ],
    []
  );

  const handleSend = (event) => {
    event.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) {
      return;
    }

    const userMessage = {
      id: Date.now(),
      role: 'user',
      text: trimmed
    };

    const botReply = {
      id: Date.now() + 1,
      role: 'bot',
      text: `Received. Potential injection cues detected: "${trimmed.slice(0, 36)}${trimmed.length > 36 ? '...' : ''}". I can help rewrite this into a safer prompt.`
    };

    setMessages((prev) => [...prev, userMessage, botReply]);
    setInput('');
  };

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setChatVisible(true);
        }
      },
      { threshold: 0.2 }
    );

    if (chatSectionRef.current) {
      observer.observe(chatSectionRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <div className="home-page">
      <div className="quote-layer" aria-hidden="true">
        {floatingQuotes.map((quote, index) => (
          <span
            key={quote}
            className="floating-quote"
            style={{
              left: `${6 + (index % 4) * 23}%`,
              animationDelay: `${index * 2.4}s`,
              animationDuration: `${28 + (index % 3) * 6}s`
            }}
          >
            {quote}
          </span>
        ))}
      </div>

      <main className="content">
        <section className="hero-block">
          <h1>detect prompt injection. keep ai output safe.</h1>
          <p className="subtitle">
            analyze suspicious prompt patterns, preserve original responses, and generate safer prompt rewrites in one workflow.
          </p>
        </section>

        <section
          id="chatbot"
          ref={chatSectionRef}
          className={`chat-card ${chatVisible ? 'show' : ''}`}
        >
          <div className="chat-header">
            <h2>safety chatbot</h2>
            <span className="status-pill">online</span>
          </div>

          <div className="chat-messages">
            {messages.map((message) => (
              <div key={message.id} className={`chat-bubble ${message.role}`}>
                {message.text}
              </div>
            ))}
          </div>

          <form className="chat-input-row" onSubmit={handleSend}>
            <input
              type="text"
              value={input}
              onChange={(event) => setInput(event.target.value)}
              placeholder="type a prompt to check..."
            />
            <button type="submit">send</button>
          </form>
        </section>
      </main>
    </div>
  );
}

export default App;
