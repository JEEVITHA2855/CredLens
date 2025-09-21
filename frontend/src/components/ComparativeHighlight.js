import React from 'react';

const ComparativeHighlight = ({ claimText, bestSource, metadata = {} }) => {
  if (!bestSource) return null;
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Compare with Authoritative Source</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="border border-gray-200 rounded p-3">
          <h4 className="text-sm font-semibold text-gray-700 mb-2">Suspicious Claim</h4>
          <p className="text-gray-800 text-sm leading-relaxed">{claimText}</p>
          <div className="mt-2 text-xs text-gray-500">
            {!metadata?.has_author && <span className="mr-2">• No author</span>}
            {!metadata?.has_date && <span>• No publication date</span>}
          </div>
        </div>
        <div className="border border-gray-200 rounded p-3">
          <h4 className="text-sm font-semibold text-gray-700 mb-2">Authoritative Reporting</h4>
          <p className="text-gray-800 text-sm leading-relaxed">{bestSource.text || 'Summary not available'}</p>
          {bestSource.url && (
            <a href={bestSource.url} target="_blank" rel="noopener noreferrer" className="text-primary-600 text-sm mt-2 inline-block">Visit source →</a>
          )}
        </div>
      </div>
    </div>
  );
};

export default ComparativeHighlight;
