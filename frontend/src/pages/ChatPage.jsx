import { useState, useRef, useEffect } from 'react';
import { HiOutlinePaperAirplane, HiOutlineChatAlt2, HiOutlinePlus } from 'react-icons/hi';
import { useAuth } from '../hooks/useAuth';
import api from '../api/axios';
import '../styles/chat.css';
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function ChatPage() {
  const { user } = useAuth();
  const [conversations, setConversations] = useState([]);
  const [activeConvoId, setActiveConvoId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [loadingMessages, setLoadingMessages] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Fetch existing conversations on mount
  useEffect(() => {
    const fetchConversations = async () => {
      try {
        const res = await api.get('/ai/conversations');
        setConversations(res.data);
      } catch (err) {
        console.error('Failed to fetch conversations:', err);
      }
    };
    fetchConversations();
  }, []);

  // Load messages when activeConvoId changes (from sidebar click)
  useEffect(() => {
    if (!activeConvoId) return;
    const fetchMessages = async () => {
      setLoadingMessages(true);
      try {
        const res = await api.get(`/ai/conversations/${activeConvoId}/messages`);
        setMessages(
          res.data.map((m) => ({ sender: m.sender, content: m.content }))
        );
      } catch (err) {
        console.error('Failed to fetch messages:', err);
        setMessages([]);
      } finally {
        setLoadingMessages(false);
      }
    };
    fetchMessages();
  }, [activeConvoId]);

  const getInitials = (name) => {
    if (!name) return '?';
    return name.split(' ').map((w) => w[0]).join('').toUpperCase().slice(0, 2);
  };

  const handleNewChat = () => {
    setActiveConvoId(null);
    setMessages([]);
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || sending) return;

    const userMsg = input.trim();
    setInput('');
    setSending(true);

    // Add user message to UI immediately
    setMessages((prev) => [...prev, { sender: 'user', content: userMsg }]);

    try {
      const payload = { message: userMsg };
      if (activeConvoId) payload.conversation_id = activeConvoId;

      const res = await api.post('/ai/chat', payload);
      const data = res.data;

      // Set conversation id if new
      if (!activeConvoId && data.conversation_id) {
        setActiveConvoId(data.conversation_id);
        setConversations((prev) => {
          // Avoid duplicate if already in list
          if (prev.some((c) => c.id === data.conversation_id)) return prev;
          return [
            { id: data.conversation_id, title: data.title || userMsg.slice(0, 40) },
            ...prev,
          ];
        });
      }

      // Add AI response
      if (data.responses && data.responses.length > 0) {
        data.responses.forEach((r) => {
          setMessages((prev) => [...prev, { sender: 'assistant', content: r }]);
        });
      }
    } catch (err) {
      const detail = err.response?.data?.detail || 'Sorry, something went wrong. Please try again.';
      console.error('Chat error:', detail, err);
      setMessages((prev) => [
        ...prev,
        { sender: 'assistant', content: detail },
      ]);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="chat-page">
      {/* Sidebar */}
      <div className="chat-sidebar">
        <div className="chat-sidebar-header">
          <button className="btn btn-primary" style={{ width: '100%' }} onClick={handleNewChat}>
            <HiOutlinePlus /> New Chat
          </button>
        </div>
        <div className="chat-sidebar-list">
          {conversations.length === 0 ? (
            <div className="chat-sidebar-empty">No conversations yet</div>
          ) : (
            conversations.map((c) => (
              <div
                key={c.id}
                className={`chat-sidebar-item ${c.id === activeConvoId ? 'chat-sidebar-item-active' : ''}`}
                onClick={() => setActiveConvoId(c.id)}
              >
                <HiOutlineChatAlt2 />
                <span className="chat-sidebar-item-title">{c.title}</span>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Main Chat */}
      <div className="chat-main">
        <div className="chat-messages">
          {loadingMessages ? (
            <div className="chat-empty">
              <div className="spinner" />
              <p>Loading messages...</p>
            </div>
          ) : messages.length === 0 ? (
            <div className="chat-empty">
              <div className="chat-empty-icon">
                <HiOutlineChatAlt2 />
              </div>
              <h2>Start a conversation</h2>
              <p>Ask CronaAI about your career goals, skills, roadmap, or anything about your personal growth.</p>
            </div>
          ) : (
            messages.map((msg, i) => (
              <div key={i} className={`chat-message chat-message-${msg.sender}`}>
                <div className="chat-message-avatar">
                  {msg.sender === 'user' ? getInitials(user?.full_name) : 'AI'}
                </div>
                <div className="chat-message-bubble">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {msg.content}
                  </ReactMarkdown>
                </div>
              </div>
            ))
          )}

          {sending && (
            <div className="chat-message chat-message-assistant">
              <div className="chat-message-avatar" style={{ background: 'var(--accent-gradient)' }}>AI</div>
              <div className="chat-message-bubble">
                <div className="chat-typing">
                  <span className="chat-typing-dot" />
                  <span className="chat-typing-dot" />
                  <span className="chat-typing-dot" />
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="chat-input-area">
          <form className="chat-input-form" onSubmit={handleSend}>
            <textarea
              className="chat-input"
              placeholder="Ask CronaAI anything..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend(e);
                }
              }}
              rows={1}
            />
            <button type="submit" className="chat-send-btn" disabled={!input.trim() || sending}>
              <HiOutlinePaperAirplane />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
