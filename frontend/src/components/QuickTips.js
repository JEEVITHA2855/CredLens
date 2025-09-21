import React from 'react';
import { Lightbulb } from 'lucide-react';

const QuickTips = () => {
  const tips = [
    'Check the date — old stories often resurface as breaking news.',
    'Look for an author and bio — anonymity can signal low credibility.',
    'Scan for sources — credible articles link to primary documents.',
    'Compare headlines to body — clickbait titles often overstate the content.',
  ];
  return (
    <div className="bg-white rounded-lg border border-blue-200 p-4 mt-6">
      <div className="flex items-center space-x-2 mb-2">
        <Lightbulb className="w-4 h-4 text-blue-700" />
        <h4 className="text-sm font-semibold text-blue-900">Quick Tips</h4>
      </div>
      <ul className="list-disc list-inside text-sm text-blue-800 space-y-1">
        {tips.map((t, i) => <li key={i}>{t}</li>)}
      </ul>
    </div>
  );
};

export default QuickTips;
