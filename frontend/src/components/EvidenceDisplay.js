import React from 'react';
import { CheckCircle, XCircle, AlertCircle, HelpCircle, ExternalLink } from 'lucide-react';
import { getVerificationStatusColor, getVerificationStatusBg } from '../utils/helpers';
import { getDomainScore } from '../utils/trustedSources';
import VerdictReasons from './VerdictReasons';
import CredibilityChecklist from './CredibilityChecklist';

const EvidenceDisplay = ({ evidence, verificationStatus, explanation, reasons = [], metadata = {} }) => {
  const getStatusIcon = (status) => {
    switch (status) {
      case 'Likely True':
        return <CheckCircle className="w-6 h-6 text-credible-600" />;
      case 'Likely False':
        return <XCircle className="w-6 h-6 text-danger-600" />;
      case 'Mixed':
        return <AlertCircle className="w-6 h-6 text-warning-600" />;
      default:
        return <HelpCircle className="w-6 h-6 text-gray-600" />;
    }
  };

  const getNLIIcon = (label) => {
    switch (label) {
      case 'ENTAILMENT':
        return <CheckCircle className="w-4 h-4 text-credible-600" />;
      case 'CONTRADICTION':
        return <XCircle className="w-4 h-4 text-danger-600" />;
      default:
        return <HelpCircle className="w-4 h-4 text-gray-600" />;
    }
  };

  const getNLILabel = (label) => {
    switch (label) {
      case 'ENTAILMENT':
        return 'Supports';
      case 'CONTRADICTION':
        return 'Contradicts';
      default:
        return 'Neutral';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-gray-900 mb-2">
          Evidence Analysis
        </h2>
        <p className="text-gray-600">
          Fact-checks and sources analyzed to verify this claim.
        </p>
      </div>

      {/* Verification Status */}
      <div className={`p-4 rounded-lg mb-6 ${getVerificationStatusBg(verificationStatus)} border border-gray-200`}>
        <div className="flex items-center space-x-3 mb-3">
          {getStatusIcon(verificationStatus)}
          <div>
            <h3 className={`text-lg font-semibold ${getVerificationStatusColor(verificationStatus)}`}>
              {verificationStatus}
            </h3>
            <p className="text-sm text-gray-600">Overall Assessment</p>
          </div>
        </div>
        <p className="text-gray-700">{explanation}</p>
        <VerdictReasons reasons={reasons} />
      </div>

      {/* Evidence Cards + Checklist */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2">
      {/* Evidence Cards */}
      {evidence && evidence.length > 0 ? (
        <div className="space-y-4">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            Supporting Evidence ({evidence.length} sources found)
          </h3>
          
          {evidence.map((item, index) => (
            <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center space-x-2">
                  {getNLIIcon(item.nli_label)}
                  <span className={`font-medium text-sm ${
                    item.nli_label === 'ENTAILMENT' ? 'text-credible-600' :
                    item.nli_label === 'CONTRADICTION' ? 'text-danger-600' : 'text-gray-600'
                  }`}>
                    {getNLILabel(item.nli_label)}
                  </span>
                </div>
                <div className="text-right text-sm text-gray-500">
                  <div>Confidence: {Math.round(item.confidence * 100)}%</div>
                  <div>Similarity: {Math.round(item.similarity_score * 100)}%</div>
                </div>
              </div>
              
              <p className="text-gray-700 mb-3 leading-relaxed">
                {item.text}
              </p>
              
              <div className="flex items-center justify-between text-sm">
                <div className="text-gray-600">
                  <span className="font-medium">Source:</span> {item.source}
                  {item.url && (() => {
                    const info = getDomainScore(item.url);
                    const label = info.score >= 0.8 ? 'Trusted' : info.score >= 0.6 ? 'Neutral' : 'Low';
                    const cls = info.score >= 0.8 ? 'bg-credible-100 text-credible-700' : info.score >= 0.6 ? 'bg-yellow-100 text-yellow-700' : 'bg-danger-100 text-danger-700';
                    return (
                      <span className={`ml-2 inline-block px-2 py-0.5 rounded text-xs ${cls}`} title={info.reason}>
                        {label}
                      </span>
                    );
                  })()}
                </div>
                {item.url && (
                  <a
                    href={item.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center space-x-1 text-primary-600 hover:text-primary-800 transition-colors"
                  >
                    <ExternalLink className="w-3 h-3" />
                    <span>View Source</span>
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-8 text-gray-500">
          <HelpCircle className="w-12 h-12 mx-auto mb-3 text-gray-400" />
          <h3 className="text-lg font-medium text-gray-700 mb-2">No Evidence Found</h3>
          <p className="text-gray-600 max-w-md mx-auto">
            We couldn't find specific fact-checks or sources for this claim in our database. 
            This doesn't necessarily mean the claim is false, but additional verification is recommended.
          </p>
        </div>
      )}

      {/* Evidence Interpretation Guide */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <h4 className="font-medium text-blue-900 mb-2">Understanding Evidence Labels:</h4>
        <div className="text-sm text-blue-800 space-y-1">
          <div className="flex items-center space-x-2">
            <CheckCircle className="w-3 h-3 text-credible-600" />
            <span><strong>Supports:</strong> Evidence confirms or aligns with the claim</span>
          </div>
          <div className="flex items-center space-x-2">
            <XCircle className="w-3 h-3 text-danger-600" />
            <span><strong>Contradicts:</strong> Evidence disputes or refutes the claim</span>
          </div>
          <div className="flex items-center space-x-2">
            <HelpCircle className="w-3 h-3 text-gray-600" />
            <span><strong>Neutral:</strong> Evidence is related but neither confirms nor denies</span>
          </div>
        </div>
      </div>
        </div>
        <div>
          <CredibilityChecklist metadata={metadata} evidence={evidence} />
        </div>
      </div>

      {/* Provenance */}
      <div className="mt-4 text-xs text-gray-500">
        <div>Provider: {metadata?.provider || 'unknown'} • Model: {metadata?.model || 'gemini-1.5-flash'} • Time: {metadata?.timestamp || 'n/a'}</div>
        {metadata?.source_domain && (
          <div>Source domain: {metadata.source_domain} {metadata?.has_author ? '• Author found' : '• No author'} {metadata?.has_date ? '• Date present' : '• No date'}</div>
        )}
      </div>
    </div>
  );
};

export default EvidenceDisplay;