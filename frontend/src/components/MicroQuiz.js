import React, { useMemo, useState } from 'react';

const MicroQuiz = ({ suspiciousPhrases = [], metadata = {}, evidence = [], questionOverride = null }) => {
  const question = useMemo(() => {
    if (questionOverride && questionOverride.q && Array.isArray(questionOverride.options)) {
      return questionOverride;
    }
    const hasUrgency = suspiciousPhrases.some(p => ['urgent','act now','limited time','last chance','immediately'].includes((p.phrase||'').toLowerCase()));
    if (hasUrgency) {
      return {
        q: 'A post says “Act now! Limited time!” and asks for your OTP. What should you do?',
        options: ['Reply with the OTP to avoid losing access', 'Ignore the message and verify through the official app/website'],
        a: 1,
      };
    }
    const hasClickbait = suspiciousPhrases.some(p => ['shocking','secret','you won\'t believe','exposed','miracle'].includes((p.phrase||'').toLowerCase()));
    if (hasClickbait) {
      return {
        q: 'An article claims a “miracle cure.” What’s the best first step?',
        options: ['Share quickly to help others', 'Check if reputable medical sources report the same claim'],
        a: 1,
      };
    }
    const noAuthor = metadata && metadata.has_author === false;
    if (noAuthor) {
      return {
        q: 'The article has no author listed. Which action increases credibility?',
        options: ['Accept it if it matches your beliefs', 'Look for an author or an official organizational byline'],
        a: 1,
      };
    }
    const noEvidence = !evidence || evidence.length === 0 || evidence.every(e => !e.url);
    if (noEvidence) {
      return {
        q: 'The article provides no citations or links. What should you do?',
        options: ['Trust the claim if it’s viral', 'Look for multiple, independent reputable sources'],
        a: 1,
      };
    }
    return {
      q: 'No sources are linked in the article. What should you do?',
      options: ['Assume it’s true if it sounds plausible', 'Check for citations or multiple independent sources'],
      a: 1,
    };
  }, [suspiciousPhrases, metadata, evidence, questionOverride]);

  const [choice, setChoice] = useState(null);
  const [submitted, setSubmitted] = useState(false);

  const submit = () => setSubmitted(true);

  return (
    <div className="bg-white rounded-lg border border-amber-200 p-4 mt-4">
      <h4 className="text-sm font-semibold text-amber-900 mb-2">Quick Micro-Quiz</h4>
      <p className="text-sm text-amber-900 mb-2">{question.q}</p>
      <div className="space-y-2">
        {question.options.map((opt, idx) => (
          <label key={idx} className="flex items-center space-x-2 text-sm text-amber-800">
            <input type="radio" name="microquiz" checked={choice===idx} onChange={() => setChoice(idx)} />
            <span>{opt}</span>
          </label>
        ))}
      </div>
      <button onClick={submit} disabled={choice===null} className="mt-2 px-3 py-1.5 bg-amber-600 text-white rounded disabled:opacity-50">Submit</button>
      {submitted && (
        <div className={`mt-2 text-sm ${choice===question.a ? 'text-green-700' : 'text-red-700'}`}>
          {choice===question.a ? 'Correct! Nice critical thinking.' : 'Not quite—look for official sources and avoid urgent requests.'}
        </div>
      )}
    </div>
  );
};

export default MicroQuiz;
