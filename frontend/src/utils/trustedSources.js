// Simple trusted source index: domain -> { score: 0..1, reason }
// This is heuristic and for demo purposes; in production, fetch from a maintained list.
export const DOMAIN_INDEX = {
  'who.int': { score: 0.95, reason: 'World Health Organization' },
  'cdc.gov': { score: 0.94, reason: 'Centers for Disease Control and Prevention' },
  'nih.gov': { score: 0.92, reason: 'National Institutes of Health' },
  'un.org': { score: 0.9, reason: 'United Nations' },
  'pib.gov.in': { score: 0.9, reason: 'Press Information Bureau (India)' },
  'factcheck.org': { score: 0.9, reason: 'Fact-checker' },
  'snopes.com': { score: 0.88, reason: 'Fact-checker' },
  'politifact.com': { score: 0.88, reason: 'Fact-checker' },
  'reuters.com': { score: 0.85, reason: 'Newswire' },
  'apnews.com': { score: 0.85, reason: 'Newswire' },
  'bbc.com': { score: 0.83, reason: 'Public broadcaster' },
  'theguardian.com': { score: 0.8, reason: 'Mainstream media' },
};

export function getDomain(hostname = '') {
  return hostname?.toLowerCase() || '';
}

export function getDomainScore(url) {
  try {
    const u = new URL(url);
    const host = getDomain(u.hostname);
    const exact = DOMAIN_INDEX[host];
    if (exact) return { host, ...exact };
    // heuristic: official domains end with .gov or .edu
    if (host.endsWith('.gov') || host.endsWith('.gov.in') || host.endsWith('.edu')) {
      return { host, score: 0.85, reason: 'Official/educational domain' };
    }
    // default neutral
    return { host, score: 0.6, reason: 'Unknown domain (verify independently)' };
  } catch {
    return { host: '', score: 0.5, reason: 'Invalid URL' };
  }
}
