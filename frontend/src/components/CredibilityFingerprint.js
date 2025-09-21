import React from 'react';
import { Shield, Users, AlertTriangle } from 'lucide-react';
import { formatScore, getCredibilityColor, getCredibilityBg } from '../utils/helpers';

const CredibilityFingerprint = ({ fingerprint }) => {
  const { source_credibility, corroboration_count, language_risk, overall_score } = fingerprint;

  const FingerprintCard = ({ icon: Icon, label, value, description, isRisk = false }) => {
    const score = isRisk ? 100 - Math.round(value * 100) : formatScore(value);
    const colorClass = isRisk ? getCredibilityColor(1 - value) : getCredibilityColor(value);
    const bgClass = isRisk ? getCredibilityBg(1 - value) : getCredibilityBg(value);
    
    return (
  <div className={`p-4 rounded-lg border ${bgClass} ${colorClass.replace('text-', 'border-')}`}>
        <div className="flex items-center space-x-3 mb-2">
          <div className={`p-2 rounded-lg ${colorClass.replace('text-', 'bg-').replace('600', '100')}`}>
            <Icon className={`w-5 h-5 ${colorClass}`} />
          </div>
          <div>
            <h3 className="font-medium text-gray-900">{label}</h3>
            <p className="text-sm text-gray-600">{description}</p>
          </div>
        </div>
        <div className="mt-3">
          {label === 'Corroboration' ? (
            <div className="flex items-center space-x-2">
              <span className={`text-2xl font-bold ${colorClass}`}>
                {corroboration_count}
              </span>
              <span className="text-sm text-gray-600">supporting sources</span>
            </div>
          ) : (
            <div className="flex items-center justify-between">
              <span className={`text-2xl font-bold ${colorClass}`}>
                {score}%
              </span>
              <div className="flex-1 ml-3">
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all duration-500 ${colorClass.replace('text-', 'bg-')}`}
                    style={{ width: `${score}%` }}
                  ></div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-gray-900 mb-2">
          Credibility Fingerprint
        </h2>
        <p className="text-gray-600">
          A comprehensive assessment of the claim's reliability based on multiple factors.
        </p>
      </div>

      {/* Overall Score */}
  <div className={`p-6 rounded-lg mb-6 ${getCredibilityBg(overall_score)} border ${getCredibilityColor(overall_score).replace('text-', 'border-')}`}>
        <div className="text-center">
          <div className="flex items-center justify-center mb-3">
            <Shield className={`w-8 h-8 ${getCredibilityColor(overall_score)}`} />
          </div>
          <div className={`text-4xl font-bold ${getCredibilityColor(overall_score)} mb-2`}>
            {formatScore(overall_score)}%
          </div>
          <div className="text-lg font-medium text-gray-900">
            Overall Credibility Score
          </div>
          <div className="text-sm text-gray-600 mt-1">
            {overall_score >= 0.8 ? 'Highly Credible' : 
             overall_score >= 0.5 ? 'Moderately Credible' : 'Low Credibility'}
          </div>
        </div>
      </div>

      {/* Individual Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <FingerprintCard
          icon={Shield}
          label="Source Trust"
          value={source_credibility}
          description="Reliability of information sources"
        />
        
        <FingerprintCard
          icon={Users}
          label="Independent Sources"
          value={corroboration_count}
          description="Number of separate sources that back this claim"
        />
        
        <FingerprintCard
          icon={AlertTriangle}
          label="Language Safety"
          value={language_risk}
          description="Absence of sensational language"
          isRisk={true}
        />
      </div>

      {/* Interpretation Guide */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <h4 className="font-medium text-blue-900 mb-2">How to Read This Fingerprint:</h4>
        <div className="text-sm text-blue-800 space-y-1">
          <div><strong>Source Trust:</strong> Higher scores indicate information comes from reliable sources</div>
          <div><strong>Independent Sources:</strong> More separate, reputable sources backing the claim increases reliability</div>
          <div><strong>Language Safety:</strong> Lower risk scores suggest objective, non-sensational language</div>
        </div>
      </div>
    </div>
  );
};

export default CredibilityFingerprint;