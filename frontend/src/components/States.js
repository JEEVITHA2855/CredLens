import React from 'react';
import { AlertCircle, Wifi } from 'lucide-react';

const LoadingState = ({ message = "Analyzing claim..." }) => (
  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
    <div className="flex flex-col items-center justify-center text-center">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mb-4"></div>
      <h3 className="text-lg font-medium text-gray-900 mb-2">{message}</h3>
      <p className="text-gray-600 max-w-md">
        Our AI is analyzing the claim against our fact-check database and evaluating source credibility.
      </p>
      <div className="mt-4 flex items-center space-x-4 text-sm text-gray-500">
        <div className="flex items-center space-x-1">
          <div className="w-2 h-2 bg-primary-600 rounded-full animate-pulse"></div>
          <span>Extracting claim</span>
        </div>
        <div className="flex items-center space-x-1">
          <div className="w-2 h-2 bg-primary-600 rounded-full animate-pulse" style={{animationDelay: '0.5s'}}></div>
          <span>Retrieving evidence</span>
        </div>
        <div className="flex items-center space-x-1">
          <div className="w-2 h-2 bg-primary-600 rounded-full animate-pulse" style={{animationDelay: '1s'}}></div>
          <span>Scoring credibility</span>
        </div>
      </div>
    </div>
  </div>
);

const ErrorState = ({ error, onRetry }) => (
  <div className="bg-white rounded-lg shadow-sm border border-red-200 p-8">
    <div className="flex flex-col items-center justify-center text-center">
      <AlertCircle className="h-12 w-12 text-red-500 mb-4" />
      <h3 className="text-lg font-medium text-gray-900 mb-2">Analysis Failed</h3>
      <p className="text-gray-600 mb-4 max-w-md">
        {error || "We encountered an error while analyzing your claim. Please try again."}
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 transition-colors"
        >
          Try Again
        </button>
      )}
    </div>
  </div>
);

const EmptyState = () => (
  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
    <div className="flex flex-col items-center justify-center text-center">
      <div className="flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-4">
        <Wifi className="w-8 h-8 text-primary-600" />
      </div>
      <h3 className="text-lg font-medium text-gray-900 mb-2">Ready to Analyze</h3>
      <p className="text-gray-600 max-w-md">
        Enter a claim or paste an article URL above to get started with our AI-powered fact-checking analysis.
      </p>
      
      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
        <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
          <div className="font-medium text-blue-900 mb-1">1. Input Analysis</div>
          <div className="text-blue-800">We extract the main factual claim from your text or URL</div>
        </div>
        <div className="p-4 bg-green-50 rounded-lg border border-green-200">
          <div className="font-medium text-green-900 mb-1">2. Evidence Matching</div>
          <div className="text-green-800">Our AI finds relevant fact-checks and credible sources</div>
        </div>
        <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
          <div className="font-medium text-purple-900 mb-1">3. Educational Insights</div>
          <div className="text-purple-800">Learn how to verify similar claims yourself</div>
        </div>
      </div>
    </div>
  </div>
);

export { LoadingState, ErrorState, EmptyState };