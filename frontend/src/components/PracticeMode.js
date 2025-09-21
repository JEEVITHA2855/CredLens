import React, { useState } from 'react';

const SAMPLE = [
  { text: 'A miracle cure can reverse diabetes in 7 days', answer: 'false', hint: 'Too-good-to-be-true health claim' },
  { text: 'WHO says handwashing reduces disease transmission', answer: 'true', hint: 'Authoritative source' },
  { text: 'This old photo is used to claim a new event', answer: 'false', hint: 'Out-of-context image' },
];

const PracticeMode = () => {
  const [idx, setIdx] = useState(0);
  const [result, setResult] = useState(null);
  const [streak, setStreak] = useState(0);
  const [badges, setBadges] = useState([]);

  const current = SAMPLE[idx];

  const answer = (val) => {
    const correct = val === current.answer;
    setResult(correct ? 'Correct!' : `Try again. Hint: ${current.hint}`);
    if (correct) {
      const newStreak = streak + 1;
      setStreak(newStreak);
      if (newStreak === 2) {
        setBadges((b) => Array.from(new Set([...b, 'Source Detective'])));
      }
    } else {
      setStreak(0);
    }
  };

  const next = () => {
    setIdx((i) => (i + 1) % SAMPLE.length);
    setResult(null);
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-medium text-gray-900">Practice Mode</h3>
        <button onClick={next} className="text-sm text-primary-600 hover:text-primary-800">Next</button>
      </div>
      <p className="text-gray-800 mb-4">{current.text}</p>
      <div className="space-x-2">
        <button className="px-3 py-2 bg-credible-600 text-white rounded" onClick={() => answer('true')}>True</button>
        <button className="px-3 py-2 bg-danger-600 text-white rounded" onClick={() => answer('false')}>False</button>
      </div>
      {result && <div className="mt-3 text-sm text-gray-700">{result}</div>}
      {badges.length > 0 && (
        <div className="mt-3 text-xs text-gray-600">Badges: {badges.join(', ')}</div>
      )}
    </div>
  );
};

export default PracticeMode;
