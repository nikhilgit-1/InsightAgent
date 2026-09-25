import React, { useState } from 'react';

function DbConnectionManager({ onSaveConnection }) {
  const [dbType, setDbType] = useState('sql');
  const [status, setStatus] = useState('Disconnected');

  // SQL State
  const [sqlUrl, setSqlUrl] = useState('');
  
  // NoSQL State
  const [nosqlUri, setNosqlUri] = useState('');
  const [nosqlDbName, setNosqlDbName] = useState('');

  const handleConnect = (e) => {
    e.preventDefault();
    
    // Form submit hone par hum details App.jsx ko bhej denge
    if (dbType === 'sql' && sqlUrl) {
      onSaveConnection({ sql_db_url: sqlUrl, nosql_uri: null, nosql_db_name: null });
      setStatus('SQL Connected');
    } else if (dbType === 'nosql' && nosqlUri && nosqlDbName) {
      onSaveConnection({ sql_db_url: null, nosql_uri: nosqlUri, nosql_db_name: nosqlDbName });
      setStatus('NoSQL Connected');
    } else {
      alert("Please fill all the required fields!");
      return;
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md mb-6 border border-gray-200">
      <h2 className="text-xl font-bold text-gray-800 mb-4">⚙️ Connect Your Database</h2>
      
      <div className="flex gap-4 mb-6">
        <button 
          className={`px-4 py-2 rounded-md font-semibold transition ${dbType === 'sql' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
          onClick={() => setDbType('sql')}
        >
          SQL (MySQL / SQLite)
        </button>
        <button 
          className={`px-4 py-2 rounded-md font-semibold transition ${dbType === 'nosql' ? 'bg-green-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
          onClick={() => setDbType('nosql')}
        >
          NoSQL (MongoDB)
        </button>
      </div>

      <form onSubmit={handleConnect} className="space-y-4">
        {dbType === 'sql' ? (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">SQL Connection URL</label>
            <input 
              type="text" 
              value={sqlUrl}
              onChange={(e) => setSqlUrl(e.target.value)}
              placeholder="e.g., mysql+pymysql://root:password@localhost:3306/aml" 
              className="w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p className="text-xs text-gray-500 mt-1">Format: mysql+pymysql://username:password@host:port/dbname</p>
          </div>
        ) : (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">MongoDB URI</label>
              <input 
                type="text" 
                value={nosqlUri}
                onChange={(e) => setNosqlUri(e.target.value)}
                placeholder="mongodb+srv://..." 
                className="w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Database Name</label>
              <input 
                type="text" 
                value={nosqlDbName}
                onChange={(e) => setNosqlDbName(e.target.value)}
                placeholder="e.g., my_nosql_db" 
                className="w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>
          </div>
        )}

        <div className="flex items-center gap-4 pt-2">
          <button 
            type="submit" 
            className={`px-6 py-2 rounded-md font-semibold text-white transition ${dbType === 'sql' ? 'bg-blue-600 hover:bg-blue-700' : 'bg-green-600 hover:bg-green-700'}`}
          >
            Save Connection
          </button>
          <span className={`font-medium ${status.includes('Connected') ? 'text-green-600' : 'text-gray-500'}`}>
            Status: {status}
          </span>
        </div>
      </form>
    </div>
  );
}

export default DbConnectionManager;