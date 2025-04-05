import React from 'react';
import './ChatBubble.css';

interface ChatBubbleProps {
  text: string;
  sender: 'user' | 'bot';
}

const ChatBubble: React.FC<ChatBubbleProps> = ({ text, sender }) => {
  return (
    <div className={`chat-bubble ${sender}`}>
      <div className="bubble">{text}</div>
    </div>
  );
};

export default ChatBubble;
