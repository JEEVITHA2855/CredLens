import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: true
});

export const analyzeClaimAPI = async (input) => {
  try {
    console.log('Sending analysis request:', input);
    const response = await api.post('/analyze', { text: input.text });
    console.log('Received response:', response.data);
    
    // If the response already has the expected structure, return it as-is
    if (response.data && response.data.claim) {
      return response.data;
    }

    // Otherwise, map ultra_simple backend response to the UI-expected schema
    const data = response.data || {};

    const claimText = data.claim_text || input?.text || input?.url || '';
    if (!claimText) {
      throw new Error('Invalid response format');
    }

    // Helper: quick URL check
    const isUrl = (val) => {
      try { new URL(val); return true; } catch (_) { return false; }
    };

    // Map backend status to UI verification status labels
    const statusMap = {
      VERIFIED: 'Likely True',
      DEBUNKED: 'Likely False',
      UNCERTAIN: 'Mixed',
    };
  let uiVerificationStatus = statusMap[data.status] || 'Mixed';

    // Normalize evidence into the richer structure expected by the UI
    const flatEvidence = Array.isArray(data.evidence) ? data.evidence : [];
    const confidenceScore = typeof data.confidence_score === 'number' ? data.confidence_score : 0.5; // 0..1

    const mappedEvidence = flatEvidence.map((item) => {
      // If item is a simple string, convert to structured record
      if (typeof item === 'string') {
        if (isUrl(item)) {
          let host = '';
          try { host = new URL(item).hostname; } catch (_) { host = 'Source'; }
          return {
            text: 'Referenced source',
            source: host,
            url: item,
            nli_label: 'ENTAILMENT',
            confidence: confidenceScore,
            similarity_score: Math.min(1, Math.max(0, confidenceScore)),
          };
        }
        return {
          text: item,
          source: 'AI Analysis',
          nli_label: 'NEUTRAL',
          confidence: 0.6,
          similarity_score: 0.5,
        };
      }
      // If already an object, ensure required fields with sensible defaults
      return {
        text: item.text || 'Evidence',
        source: item.source || 'AI Analysis',
        url: item.url || undefined,
        nli_label: item.nli_label || 'NEUTRAL',
        confidence: typeof item.confidence === 'number' ? item.confidence : confidenceScore,
        similarity_score: typeof item.similarity_score === 'number' ? item.similarity_score : 0.5,
      };
    });

  // Use backend-provided fingerprint if available; otherwise synthesize a basic one
    let fingerprint = data.credibility_fingerprint;
    if (!fingerprint || typeof fingerprint !== 'object') {
      const corroborationCount = mappedEvidence.filter(e => !!e.url).length;
      const overall = Math.min(1, Math.max(0, confidenceScore));
      fingerprint = {
        overall_score: overall,
        source_credibility: overall, // reuse confidence as a proxy
        language_risk: Math.max(0, 1 - overall),
        corroboration_count: corroborationCount,
      };
    }

    if ((mappedEvidence.length === 0 || mappedEvidence.every(e => !e.url)) && (fingerprint.overall_score || 0) < 0.45) {
      uiVerificationStatus = 'Unverified';
    }

    // Provide a simple micro-lesson tip
    let microLesson = data.micro_lesson || 'Always verify information across multiple reliable sources.';
    if (!data.micro_lesson) {
      if (uiVerificationStatus === 'Likely True') {
        microLesson = 'Corroborate with at least two independent, reputable sources.';
      } else if (uiVerificationStatus === 'Likely False') {
        microLesson = 'Be wary of sensational claims—check reputable fact-checkers and primary sources.';
      } else {
        microLesson = 'Seek more reliable sources and check dates, authors, and original context.';
      }
    }

    // Build detective-style reasons
    const reasons = Array.isArray(data.reasons) && data.reasons.length > 0
      ? data.reasons.slice(0, 3)
      : (function() {
          const r = [];
          const hasUrls = mappedEvidence.some(e => !!e.url);
          if (!hasUrls) r.push('Few or no independent sources found; verify with additional reputable sites.');
          if (Array.isArray(data.suspicious_phrases) && data.suspicious_phrases.length > 0) {
            const phrases = data.suspicious_phrases.slice(0,2).map(p => p.phrase).join(', ');
            r.push(`Language uses emotional or clickbait terms (${phrases}).`);
          }
          if (isUrl(input?.text || '')) {
            try {
              const domain = new URL(input.text).hostname;
              r.push(`Source domain: ${domain}`);
            } catch {}
          }
          return r.slice(0,3);
        })();

    const mapped = {
      // Core fields expected by App and components
      claim: claimText,
      extracted_claim: claimText,
      original_input: input?.text || input?.url || claimText,
      credibility_fingerprint: fingerprint,
      evidence: mappedEvidence,
      verification_status: uiVerificationStatus,
  suspicious_phrases: Array.isArray(data.suspicious_phrases) ? data.suspicious_phrases : [],
      micro_lesson: microLesson,
      explanation: data.explanation || 'Analysis completed using Gemini AI',
      reasons,
      metadata: data.metadata || {},
    };

    return mapped;
  } catch (error) {
    console.error('Analysis error:', error);
    
    // Detailed error logging
    if (error.response) {
      console.error('Response error:', error.response.data);
      throw new Error(error.response.data?.error || 'Server error: ' + error.response.status);
    } else if (error.request) {
      console.error('Request error:', error.request);
      throw new Error('Cannot connect to server - please check if the backend is running');
    } else {
      console.error('Other error:', error.message);
      throw new Error(error.message || 'An unexpected error occurred');
    }
  }
};

export const analyzeIndustrialAPI = async (content) => {
  try {
    const response = await api.post('/analyze-industrial', { content });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Industrial analysis failed');
    } else if (error.request) {
      throw new Error('Network error - please check your connection');
    } else {
      throw new Error('Request failed - please try again');
    }
  }
};

export const getHealthAPI = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    throw new Error('Health check failed');
  }
};

export const getStatsAPI = async () => {
  try {
    const response = await api.get('/stats');
    return response.data;
  } catch (error) {
    throw new Error('Stats fetch failed');
  }
};

export default api;