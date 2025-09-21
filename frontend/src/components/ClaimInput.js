import React, { useState } from 'react';
import { Search, Link as LinkIcon, Loader2 } from 'lucide-react';
import { isValidUrl } from '../utils/helpers';

const ClaimInput = ({ onAnalyze, loading }) => {
  const [input, setInput] = useState('');
  const [inputType, setInputType] = useState('text'); // auto-detected

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Always send text; backend will fetch URL content if a URL is detected
    const analysisInput = {
      text: input.trim(),
    };
    
    onAnalyze(analysisInput);
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setInput(value);
    
    // Auto-detect input type (url vs text)
    if (isValidUrl(value.trim())) {
      setInputType('url');
    } else {
      setInputType('text');
    }
  };

  const exampleClaims = [
    "Vaccines cause autism in children",
    "Climate change is not caused by human activity", 
    "5G networks spread coronavirus",
    "https://example-news-site.com/breaking-news-article"
  ];

  const handleExampleClick = (example) => {
    setInput(example);
    handleInputChange({ target: { value: example } });
  };

  return (
  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="mb-6">
  <h2 className="text-2xl font-semibold text-gray-900 mb-2">
          Analyze a Claim or Article
        </h2>
  <p className="text-gray-600">
          Enter text or paste a URL to check for misinformation and learn how to verify similar claims.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative">
          <div className="flex items-center space-x-2 mb-2">
            {inputType === 'url' ? (
              <LinkIcon className="w-4 h-4 text-primary-600" />
            ) : (
              <Search className="w-4 h-4 text-primary-600" />
            )}
            <span className="text-sm font-medium text-gray-700">
              {inputType === 'url' ? 'Article URL' : 'Claim Text'}
            </span>
          </div>
          
          <textarea
            value={input}
            onChange={handleInputChange}
            placeholder={inputType === 'url' ? "Paste a news article URL here..." : "Enter a claim or paste a URL to fact-check..."}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none transition-colors"
            rows={inputType === 'url' ? 2 : 4}
            disabled={loading}
          />
          
          {input && (
            <div className="absolute top-14 right-3 text-xs text-gray-400">
              {input.length} characters
            </div>
          )}
        </div>

        <div className="flex justify-between items-center">
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="px-6 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center space-x-2 focus:ring-offset-white dark:focus:ring-offset-gray-900"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Search className="w-4 h-4" />
                <span>Analyze Claim</span>
              </>
            )}
          </button>
          
          <div className="text-sm text-gray-500">
            Analysis typically takes 3-10 seconds
          </div>
        </div>
      </form>

      {/* Example claims */}
  <div className="mt-6 border-t border-gray-200 pt-6">
        <h3 className="text-sm font-medium text-gray-700 mb-3">
          Try these examples:
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {exampleClaims.map((example, index) => (
            <button
              key={index}
              onClick={() => handleExampleClick(example)}
              disabled={loading}
              className="text-left p-3 text-sm text-gray-600 hover:text-primary-600 hover:bg-primary-50 rounded-lg border border-gray-200 hover:border-primary-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {example.length > 60 ? `${example.substring(0, 60)}...` : example}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ClaimInput;