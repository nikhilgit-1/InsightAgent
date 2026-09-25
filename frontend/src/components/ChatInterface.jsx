import React, { useState } from 'react';
import axios from 'axios';

function ChatInterface({ activeConnection }) {
  const [query, setQuery] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!query.trim() || !activeConnection) return;

    const newHistory = [...chatHistory, { sender: 'user', text: query }];
    setChatHistory(newHistory);
    setQuery('');
    setIsLoading(true);

    try {
      const payload = {
        user_query: query,
        sql_db_url: activeConnection.sql_db_url,
        nosql_uri: activeConnection.nosql_uri,
        nosql_db_name: activeConnection.nosql_db_name
      };

      const response = await axios.post('http://localhost:8000/api/chat', payload);
      
      let agentReply = response.data.reply;
      
      // Clean Text Extractor Logic
      if (Array.isArray(agentReply)) {
        // Agar response Array hai (jaisa screenshot mein aaya), toh uske pehle item ka 'text' nikalo
        agentReply = agentReply[0]?.text || JSON.stringify(agentReply);
      } else if (typeof agentReply === 'object' && agentReply !== null) {
        // Agar object hai, toh uska 'text' nikalo
        agentReply = agentReply.text || JSON.stringify(agentReply);
      }

      if (response.data.status === 'success') {
        setChatHistory([...newHistory, { sender: 'agent', text: String(agentReply) }]);
      } else {
        setChatHistory([...newHistory, { sender: 'agent', text: String(agentReply) }]); 
      }
    } catch (error) {
      console.error(error);
      setChatHistory([...newHistory, { sender: 'agent', text: 'Backend API se connect karne mein error aaya.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!activeConnection) {
    return (
      <div className="bg-yellow-50 text-yellow-800 p-4 rounded-md text-center border border-yellow-200 shadow-sm mt-6">
        Agent se baat karne ke liye pehle upar apna Database Connection save karein.
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 flex flex-col h-[500px] mt-6">
      <div className="p-4 bg-gray-50 border-b border-gray-200 font-bold text-gray-700">
        💬 Chat with InsightAgent
      </div>
      
      <div className="flex-1 p-4 overflow-y-auto space-y-4">
        {chatHistory.length === 0 ? (
          <div className="text-gray-400 text-center mt-10">Mujhe apne data ke baare mein kuch bhi puchiye...</div>
        ) : (
          chatHistory.map((msg, index) => (
            <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[80%] p-3 rounded-lg ${msg.sender === 'user' ? 'bg-blue-600 text-white rounded-br-none' : 'bg-gray-100 text-gray-800 rounded-bl-none'}`}>
                <pre className="whitespace-pre-wrap font-sans">{msg.text}</pre>
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 text-gray-500 p-3 rounded-lg rounded-bl-none animate-pulse font-medium">
              Agent is analyzing your database...
            </div>
          </div>
        )}
      </div>

      <form onSubmit={handleSendMessage} className="p-4 border-t border-gray-200 flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="E.g., Count the total number of records in my table..."
          className="flex-1 border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading}
          className="bg-blue-600 text-white px-6 py-2 rounded-md font-semibold hover:bg-blue-700 transition disabled:bg-blue-400"
        >
          Send
        </button>
      </form>
    </div>
  );
}

export default ChatInterface;