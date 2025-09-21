import React from 'react';
import { ListChecks } from 'lucide-react';

const VerdictReasons = ({ reasons = [] }) => {
  if (!reasons || reasons.length === 0) return null;
  return (
    <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
      <div className="flex items-center space-x-2 mb-2">
        <ListChecks className="w-4 h-4 text-gray-700" />
        <h4 className="text-sm font-semibold text-gray-800">Why this verdict</h4>
      </div>
      <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
        {reasons.slice(0,3).map((r, i) => (
          <li key={i}>{r}</li>
        ))}
      </ul>
    </div>
  );
};

export default VerdictReasons;
