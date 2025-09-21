import React, { useState, useEffect } from 'react';
import { CheckSquare, Square } from 'lucide-react';

const items = [
  { key: 'who', label: 'Who is the source?' },
  { key: 'when', label: 'When was it published?' },
  { key: 'where', label: 'Where else is it reported?' },
  { key: 'what', label: "What's the evidence?" },
];

const CredibilityChecklist = ({ metadata = {}, evidence = [] }) => {
  const [checks, setChecks] = useState({ who: false, when: false, where: false, what: false });

  useEffect(() => {
    // Auto-suggest based on metadata/evidence
    setChecks((prev) => ({
      ...prev,
      who: !!metadata.has_author,
      when: !!metadata.has_date,
      where: evidence && evidence.some(e => !!e.url),
      what: evidence && evidence.length > 0,
    }));
  }, [metadata, evidence]);

  const toggle = (key) => setChecks((p) => ({ ...p, [key]: !p[key] }));

  const doneCount = Object.values(checks).filter(Boolean).length;

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-medium text-gray-900">Credibility Checklist</h3>
        <span className="text-sm text-gray-500">{doneCount}/4 checked</span>
      </div>
      <div className="space-y-2">
        {items.map((it) => (
          <button
            key={it.key}
            type="button"
            onClick={() => toggle(it.key)}
            className="w-full flex items-center justify-between p-2 rounded hover:bg-gray-50 border border-gray-200"
          >
            <span className="text-sm text-gray-800">{it.label}</span>
            {checks[it.key] ? (
              <CheckSquare className="w-5 h-5 text-credible-600" />
            ) : (
              <Square className="w-5 h-5 text-gray-400" />
            )}
          </button>
        ))}
      </div>
    </div>
  );
};

export default CredibilityChecklist;
