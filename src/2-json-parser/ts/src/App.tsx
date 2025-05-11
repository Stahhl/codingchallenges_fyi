import { useEffect, useState } from 'react'

function App() {
  const [text, setText] = useState('');
  const [submittedText, setSubmittedText] = useState('');

  const handleSubmit = () => {
    setSubmittedText(text);
  };

  // Keyboard shortcut Ctrl+Enter
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.ctrlKey && e.key === 'Enter') {
        e.preventDefault();
        handleSubmit();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [text]);

  return (
    <div className="flex flex-col h-screen bg-gray-600 text-black transition-colors duration-300">
      {/* Top Bar */}
      <div className="h-14 bg-gray-800 text-white flex items-center px-4 shadow">
        <h1 className="text-lg font-semibold">My App</h1>
        <div className="ml-auto flex items-center gap-4">
          <button
            onClick={handleSubmit}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
          >
            Submit (Ctrl+Enter)
          </button>
        </div>
      </div>

      {/* Panels */}
      <div className="flex flex-1 p-4 gap-4">
        {/* Left Panel */}
        <div className="w-1/2 bg-white p-4 rounded-lg shadow">
          <textarea
            className="w-full h-full resize-none p-2 text-base border rounded bg-white"
            placeholder="Input..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
        </div>

        {/* Right Panel */}
        <div className="w-1/2 bg-white p-4 rounded-lg shadow">
            {submittedText || <span className="text-gray-400">Output…</span>}
        </div>
      </div>
    </div>
  );
}

export default App
