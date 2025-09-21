import React from 'react';
import { Search, Shield, BookOpen } from 'lucide-react';

const Header = () => {
  const scrollTo = (id) => {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="flex items-center justify-center w-10 h-10 bg-primary-600 rounded-lg">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">CredLens</h1>
                <p className="text-xs text-gray-500">Verify, Learn, Share Wisely</p>
              </div>
            </div>
          </div>
          
          <nav className="hidden md:flex items-center space-x-8">
            <button
              type="button"
              onClick={() => scrollTo('detection-section')}
              className="flex items-center space-x-2 text-sm text-gray-700 hover:text-primary-700 transition-colors"
              aria-label="Go to AI-Powered Detection"
            >
              <Search className="w-4 h-4" />
              <span>AI-Powered Detection</span>
            </button>
            <button
              type="button"
              onClick={() => scrollTo('insights-section')}
              className="flex items-center space-x-2 text-sm text-gray-700 hover:text-primary-700 transition-colors"
              aria-label="Go to Educational Insights"
            >
              <BookOpen className="w-4 h-4" />
              <span>Educational Insights</span>
            </button>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;