import React from 'react';
import { Info } from 'lucide-react';

const ManipulationTactics = ({ suspiciousPhrases = [], metadata = {}, evidence = [] }) => {
  const tactics = [];
  if (Array.isArray(suspiciousPhrases) && suspiciousPhrases.length > 0) {
    tactics.push({ label: 'Clickbait/emotional wording', tip: 'Emotional language can bypass critical thinking.' });
  }
  if (metadata && metadata.has_author === false) {
    tactics.push({ label: 'No author attribution', tip: 'Reliable reporting usually names an author or organization.' });
  }
  if (metadata && metadata.has_date === false) {
    tactics.push({ label: 'No publication date', tip: 'Missing dates can hide outdated content shared as current.' });
  }
  if (!evidence || evidence.length === 0) {
    tactics.push({ label: 'Uncited claims', tip: 'Look for links to primary sources or independent reports.' });
  }
  if (tactics.length === 0) return null;
  return (
    <div className="mt-6">
      <h3 className="text-lg font-medium text-gray-900 mb-3">Manipulation Tactics</h3>
      <div className="space-y-2">
        {tactics.map((t, i) => (
          <div key={i} className="flex items-start space-x-2 text-sm text-gray-700">
            <Info className="w-4 h-4 text-orange-600 mt-0.5" />
            <div>
              <span className="font-medium">{t.label}:</span> {t.tip}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ManipulationTactics;
