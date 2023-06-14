import React, { useState, useEffect } from 'react';

const Chat: React.FC = () => {
  const [inputValue, setInputValue] = useState('');
  const [conversation, setConversation] = useState<Array<[string, string]>>([]);

  useEffect(() => {
    fetch('/chat/')
      .then(response => response.json())
      .then(data => setConversation(data.conversation));
  }, []);

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    // Get the CSRF token from the cookie
    const csrfToken = document.cookie
      .split(';')
      .map(c => c.trim())
      .filter(c => c.startsWith('csrftoken='))[0]
      .split('=')[1];

    fetch('/chat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken, // Add the CSRF token to the headers
      },
      body: JSON.stringify({ input_user: inputValue }),
    })
      .then(response => response.json())
      .then(data => {
        setInputValue('');
        setConversation(data.conversation);
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
        {conversation.map((message, index) => (
          <p key={index}>
            {message[0] === 'user' ? 'User' : 'AI'}: {message[1]}
          </p>
        ))}
      </div>
    </div>
  );
};

export default Chat;