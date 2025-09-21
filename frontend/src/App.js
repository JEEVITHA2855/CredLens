import React, { useState } from 'react';
import Header from './components/Header';
import ClaimInput from './components/ClaimInput';
import CredibilityFingerprint from './components/CredibilityFingerprint';
import EvidenceDisplay from './components/EvidenceDisplay';
import EducationalInsights from './components/EducationalInsights';
import ComparativeHighlight from './components/ComparativeHighlight';
import { LoadingState, ErrorState, EmptyState } from './components/States';
import { analyzeClaimAPI } from './utils/api';
import './index.css';

function App() {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentInput, setCurrentInput] = useState(null);

  const handleAnalyze = async (input) => {
    setLoading(true);
    setError(null);
    setCurrentInput(input);
    
    try {
      console.log('Starting analysis:', input);
      
      // Call the API
      const result = await analyzeClaimAPI(input);
      console.log('Received analysis result:', result);
      
      // Validate the response
      if (!result || !result.claim) {
        throw new Error('Invalid response from server');
      }
      
      // Set the analysis result
      setAnalysis(result);
    } catch (err) {
      console.error('Analysis error:', err);
      setError(err.message);
      setAnalysis(null);
    } finally {
      setLoading(false);
    }
  };

  const handleRetry = () => {
    if (currentInput) {
      handleAnalyze(currentInput);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
  <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Input Section */}
        <div className="mb-8">
          <ClaimInput onAnalyze={handleAnalyze} loading={loading} />
        </div>
        
  {/* Results Section */}
  <div className="space-y-8" id="detection-section">
          {loading && <LoadingState />}
          
          {error && !loading && (
            <ErrorState error={error} onRetry={handleRetry} />
          )}
          
          {!analysis && !loading && !error && <EmptyState />}
          
          {analysis && !loading && (
            <>
              {/* Credibility Fingerprint */}
              <div className="animate-fade-in">
                <CredibilityFingerprint fingerprint={analysis.credibility_fingerprint} />
              </div>
              
              {/* Evidence Analysis */}
              <div className="animate-fade-in" style={{ animationDelay: '0.2s' }}>
                <EvidenceDisplay
                  evidence={analysis.evidence}
                  verificationStatus={analysis.verification_status}
                  explanation={analysis.explanation}
                  reasons={analysis.reasons}
                  metadata={analysis.metadata}
                />
              </div>
              
              {/* Educational Insights */}
              <div className="animate-fade-in" style={{ animationDelay: '0.4s' }} id="insights-section">
                <EducationalInsights
                  microLesson={
                    typeof analysis.micro_lesson === 'string'
                      ? { tip: analysis.micro_lesson, category: 'source_verification' }
                      : analysis.micro_lesson || { tip: 'Always verify information across multiple reliable sources.', category: 'source_verification' }
                  }
                  suspiciousPhrases={analysis.suspicious_phrases}
                  extractedClaim={analysis.extracted_claim}
                  originalInput={analysis.original_input}
                  metadata={analysis.metadata}
                  evidence={analysis.evidence}
                />
              </div>

              {/* Comparative Source Highlighting */}
              {Array.isArray(analysis.evidence) && analysis.evidence.some(e => e.url) && (
                <div className="animate-fade-in" style={{ animationDelay: '0.6s' }}>
                  {(() => {
                    const best = analysis.evidence.find(e => e.url);
                    return <ComparativeHighlight claimText={analysis.claim} bestSource={best} metadata={analysis.metadata} />;
                  })()}
                </div>
              )}

              {/* Practice Mode removed as requested */}
            </>
          )}
        </div>
      </main>
      
      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">CredLens</h3>
            <p className="text-gray-600 mb-4">
              AI-powered misinformation detection and media literacy education
            </p>
            <div className="flex justify-center space-x-6 text-sm text-gray-500">
              <span>• Semantic fact-checking</span>
              <span>• Educational micro-lessons</span>
              <span>• Credibility fingerprinting</span>
              <span>• Source verification</span>
            </div>
            <div className="mt-4 text-xs text-gray-400">
              Built with React, Tailwind CSS, FastAPI, and Hugging Face Transformers
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;