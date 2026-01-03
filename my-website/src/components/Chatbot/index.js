import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

function Chatbot() {
  const [messages, setMessages] = useState([
    {
      text: "Hello! I'm your AI assistant for robotics and AI topics. To get started, please ask me questions about robotics, AI, ROS 2, digital twins, NVIDIA Isaac, or Vision-Language-Action systems. Note: I can only answer questions based on the content of ingested books, so make sure the system has been properly set up with book content.",
      sender: 'bot'
    }
  ]);
  const [input, setInput] = useState('');
  const [backendStatus, setBackendStatus] = useState('checking'); // checking, connected, disconnected

  // Check backend status on component mount
  useEffect(() => {
    checkBackendStatus();
  }, []);

  const checkBackendStatus = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/health');
      if (response.ok) {
        setBackendStatus('connected');
      } else {
        setBackendStatus('disconnected');
      }
    } catch (error) {
      setBackendStatus('disconnected');
    }
  };

  const sendMessage = async () => {
    if (input.trim() === '') return;

    const newMessages = [...messages, { text: input, sender: 'user' }];
    setMessages(newMessages);
    setInput('');

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: input }),
      });
      const data = await response.json();
      setMessages([...newMessages, { text: data.answer, sender: 'bot' }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages([...newMessages, {
        text: 'Error: Could not connect to the chatbot. Please make sure the backend server is running on port 8000.',
        sender: 'bot'
      }]);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className={styles.chatbotContainer}>
      <div className={styles.statusBar}>
        <div className={`${styles.statusIndicator} ${styles[backendStatus]}`}></div>
        <span className={styles.statusText}>
          {backendStatus === 'connected' ? 'Connected to backend' :
           backendStatus === 'checking' ? 'Checking connection...' :
           'Backend disconnected - please start the server'}
        </span>
      </div>
      <div className={styles.messagesContainer}>
        {messages.map((msg, index) => (
          <div key={index} className={`${styles.message} ${styles[msg.sender]}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className={styles.inputContainer}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask about robotics, AI, ROS 2, digital twins..."
          className={styles.textInput}
        />
        <button onClick={sendMessage} className={styles.sendButton}>Send</button>
      </div>
      <div className={styles.infoText}>
        Note: This chatbot answers questions based on ingested book content.
        Make sure to ingest a book using the backend API for best results.
      </div>
    </div>
  );
}

export default Chatbot;

