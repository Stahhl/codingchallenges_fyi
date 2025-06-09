import { useEffect, useState } from 'react'
import { Scanner } from './lib/scanner';
import { Parser } from './lib/parser';
import { JavascriptConverter } from './lib/converters/javascriptConverter';

function App() {
  const [text, setText] = useState('');
  const [submittedText, setSubmittedText] = useState('');
  // Dropdown state
  const options = [
    "Validate json",
    "Convert to javascript",
  ];
  const [isOpen, setIsOpen] = useState(false);
  const [selectedOption, setSelectedOption] = useState(options[0]);


  const handleSelectOption = (option: string) => {
    setSelectedOption(option);
    setIsOpen(false);
  };

  const handleSubmit = () => {
    const scanner = new Scanner(text);
    const tokens = scanner.scan();

    const parser = new Parser(tokens);
    const elements = parser.parse();

    const validationResult = (scanner.errors.length > 0 || parser.errors.length > 0) ? JSON.stringify({ erros: { scanner: scanner.errors, parser: parser.errors } }, null, 2) : '';
    console.log(validationResult);

   
    if(validationResult != '') {
      setSubmittedText(validationResult);
    }
    else if(selectedOption == options[0]) {
      setSubmittedText('Valid ✅');
    }
    else if(selectedOption == options[1]){
      const converter = new JavascriptConverter(elements);
      const js = converter.convert();
      setSubmittedText(js);
    }
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
          {/* Integrated Dropdown */}
          <div className="relative">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="px-3 py-1.5 bg-gray-700 hover:bg-gray-600 text-white text-sm rounded border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors min-w-32"
            >
              <div className="flex items-center justify-between">
                <span className="truncate">{selectedOption}</span>
                <span className={`ml-2 transform transition-transform ${isOpen ? "rotate-180" : ""}`}>
                  ▼
                </span>
              </div>
            </button>

            {/* Dropdown Menu */}
            {isOpen && (
              <div className="absolute top-full right-0 mt-1 bg-white border border-gray-300 rounded shadow-lg z-10 min-w-40">
                {options.map((option, index) => (
                  <button
                    key={index}
                    onClick={() => handleSelectOption(option)}
                    className="w-full px-3 py-2 text-left text-gray-700 text-sm hover:bg-gray-50 focus:bg-gray-50 focus:outline-none first:rounded-t last:rounded-b transition-colors"
                  >
                    {option}
                  </button>
                ))}
              </div>
            )}
          </div>
          
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
