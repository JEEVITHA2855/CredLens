export const getCredibilityColor = (score) => {
  if (score >= 0.8) return 'text-credible-600';
  if (score >= 0.5) return 'text-warning-600';
  return 'text-danger-600';
};

export const getCredibilityBg = (score) => {
  if (score >= 0.8) return 'bg-credible-100';
  if (score >= 0.5) return 'bg-warning-100';
  return 'bg-danger-100';
};

export const getCredibilityBorder = (score) => {
  if (score >= 0.8) return 'border-credible-300';
  if (score >= 0.5) return 'border-warning-300';
  return 'border-danger-300';
};

export const getVerificationStatusColor = (status) => {
  const colors = {
    'Likely True': 'text-credible-600',
    'Mixed': 'text-warning-600',
    'Likely False': 'text-danger-600',
    'Unverified': 'text-gray-600'
  };
  return colors[status] || 'text-gray-600';
};

export const getVerificationStatusBg = (status) => {
  const colors = {
    'Likely True': 'bg-credible-100',
    'Mixed': 'bg-warning-100',
    'Likely False': 'bg-danger-100',
    'Unverified': 'bg-gray-100'
  };
  return colors[status] || 'bg-gray-100';
};

export const formatScore = (score) => {
  return Math.round(score * 100);
};

export const truncateText = (text, maxLength = 100) => {
  if (text.length <= maxLength) return text;
  return text.substr(0, maxLength) + '...';
};

export const isValidUrl = (string) => {
  try {
    new URL(string);
    return true;
  } catch (_) {
    return false;
  }
};

export const highlightSuspiciousPhrases = (text, suspiciousPhrases) => {
  if (!suspiciousPhrases || suspiciousPhrases.length === 0) {
    return text;
  }

  let highlightedText = text;
  
  // Sort phrases by start position in descending order to avoid offset issues
  const sortedPhrases = [...suspiciousPhrases].sort((a, b) => b.start_pos - a.start_pos);
  
  sortedPhrases.forEach(phrase => {
    const before = highlightedText.substring(0, phrase.start_pos);
    const highlighted = highlightedText.substring(phrase.start_pos, phrase.end_pos);
    const after = highlightedText.substring(phrase.end_pos);
    
    highlightedText = before + 
      `<span class="bg-yellow-200 px-1 rounded text-sm font-medium" title="${phrase.reason}">${highlighted}</span>` + 
      after;
  });
  
  return highlightedText;
};