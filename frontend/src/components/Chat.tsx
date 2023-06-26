import React, { useState, useEffect } from 'react';

const Chat: React.FC = () => {
  const [inputValue, setInputValue] = useState('');
  const [conversation, setConversation] = useState<Array<[string, string]>>([]);

  useEffect(() => {
    fetchConversation();
  }, []);

  const fetchConversation = () => {
  fetch('http://localhost:8000/submit-message')
    .then(response => response.json())
    .then(data => setConversation(data.conversation));
};

const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
  event.preventDefault();

  fetch('http://localhost:8000/chat/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ input_user: inputValue }),
  })
    .then(response => response.json())
    .then(data => {
      console.log(data); // Log the response data for inspection
      setInputValue('');
      const aiResponse = data.response; // Extract the AI's response from the 'response' key
      const updatedConversation: Array<[string, string]> = [
        ...conversation,
        ['user', inputValue],
        ['AI', aiResponse]
      ];
      setConversation(updatedConversation);
    });
};


  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label htmlFor="input_user">Your message:</label>
        <input
          type="text"
          id="input_user"
          name="input_user"
          value={inputValue}
          onChange={event => setInputValue(event.target.value)}
        />
        <br />
        <button type="submit">Send</button>
      </form>

      <div>
        <h2>Conversation</h2>
        <div className="chat-container">
          {conversation.map((message, index) => (
            <div
              key={index}
              className={`message ${message[0] === 'user' ? 'user-message' : 'ai-message'}`}
            >
              <span className="message-sender">{message[0]}</span>
              <span className="message-text">{message[1]}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Chat;