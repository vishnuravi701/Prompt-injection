import React, { useState } from 'react';
import PromptAnalyzer from './pages/PromptAnalyzer';
import './styles/App.css';

function App() {
  return (
    <div className="App">
      <header className="app-header">
        <h1>🛡️ Prompt Injection Prevention & Education</h1>
        <p>Learn how to identify and defend against prompt injection attacks</p>
      </header>
      <main>
        <PromptAnalyzer />
      </main>
      <footer className="app-footer">
        <p>&copy; 2024 Prompt Injection Prevention Project. Educational purposes.</p>
      </footer>
    </div>
  );
}

export default App;
