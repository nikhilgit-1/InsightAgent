import React, { useState } from 'react';
import DbConnectionManager from './components/DbConnectionManager';
import ChatInterface from './components/ChatInterface'; // Naya component import kiya

function App() {
  const [activeConnection, setActiveConnection] = useState(null);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-white shadow-sm p-4 border-b">
        <h1 className="text-2xl font-extrabold text-blue-600">InsightAgent</h1>
      </header>

      <main className="flex-1 max-w-5xl mx-auto w-full p-6">
        <DbConnectionManager onSaveConnection={setActiveConnection} />
        
        {/* Yahan purana green div hata diya gaya hai aur Chat UI lagaya hai */}
        <ChatInterface activeConnection={activeConnection} />
      </main>
    </div>
  );
}

export default App;