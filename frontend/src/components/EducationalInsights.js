import React from 'react';
import { Lightbulb, BookOpen, AlertTriangle } from 'lucide-react';
import { highlightSuspiciousPhrases } from '../utils/helpers';
import ManipulationTactics from './ManipulationTactics';
import QuickTips from './QuickTips';
import ResourceLinks from './ResourceLinks';
import ImageVerificationTips from './ImageVerificationTips';
import MicroQuiz from './MicroQuiz';

const EducationalInsights = ({ microLesson, suspiciousPhrases, extractedClaim, originalInput, metadata = {}, evidence = [] }) => {
  const getCategoryIcon = (category) => {
    if (!category) return <Lightbulb className="w-5 h-5" />;
    
    switch (category) {
      case 'source_verification':
        return <BookOpen className="w-5 h-5" />;
      case 'language_analysis':
        return <AlertTriangle className="w-5 h-5" />;
      default:
        return <Lightbulb className="w-5 h-5" />;
    }
  };

  const getCategoryColor = (category) => {
    if (!category) return 'text-primary-600';
    
    switch (category) {
      case 'source_verification':
        return 'text-blue-600';
      case 'language_analysis':
        return 'text-orange-600';
      case 'cross_referencing':
        return 'text-green-600';
      case 'evidence_evaluation':
        return 'text-purple-600';
      case 'bias_awareness':
        return 'text-red-600';
      default:
        return 'text-primary-600';
    }
  };

  const getCategoryBg = (category) => {
    if (!category) return 'bg-primary-50 border-primary-200';
    
    switch (category) {
      case 'source_verification':
        return 'bg-blue-50 border-blue-200';
      case 'language_analysis':
        return 'bg-orange-50 border-orange-200';
      case 'cross_referencing':
        return 'bg-green-50 border-green-200';
      case 'evidence_evaluation':
        return 'bg-purple-50 border-purple-200';
      case 'bias_awareness':
        return 'bg-red-50 border-red-200';
      default:
        return 'bg-primary-50 border-primary-200';
    }
  };

  const formatCategoryName = (category) => {
    if (!category) {
      return 'Verification';
    }
    return category
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-gray-900 mb-2">
          Educational Insights
        </h2>
        <p className="text-gray-600">
          Learn how to verify similar claims and spot potential misinformation.
        </p>
      </div>

      {/* Micro Lesson */}
      {microLesson && (
        <div className={`p-4 rounded-lg mb-6 border ${getCategoryBg(microLesson.category)}`}> 
          <div className="flex items-start space-x-3">
            <div className={`p-2 rounded-lg bg-white ${getCategoryColor(microLesson.category)}`}>
              {getCategoryIcon(microLesson.category)}
            </div>
            <div className="flex-1">
              <h3 className={`font-medium mb-2 ${getCategoryColor(microLesson.category)}`}>
                💡 {formatCategoryName(microLesson.category)} Tip
              </h3>
              <p className="text-gray-700 leading-relaxed">
                {microLesson.tip || "Always verify information across multiple reliable sources."}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Claim Breakdown */}
      <div className="mb-6">
        <h3 className="text-lg font-medium text-gray-900 mb-3">Claim Analysis</h3>
        <div className="bg-gray-50 rounded-lg p-4 border">
          <div className="mb-4">
            <h4 className="text-sm font-medium text-gray-700 mb-2">Original Input:</h4>
            <div 
              className="text-gray-800 text-sm leading-relaxed"
              dangerouslySetInnerHTML={{ 
                __html: highlightSuspiciousPhrases(originalInput, suspiciousPhrases) 
              }}
            />
          </div>
          
          {extractedClaim !== originalInput && (
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-2">Extracted Claim:</h4>
              <p className="text-gray-800 text-sm italic leading-relaxed">
                "{extractedClaim}"
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Suspicious Phrases Analysis */}
      {suspiciousPhrases && suspiciousPhrases.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-medium text-gray-900 mb-3">
            Language Analysis
          </h3>
          <div className="bg-yellow-50 rounded-lg p-4 border border-yellow-200">
            <div className="flex items-center space-x-2 mb-3">
              <AlertTriangle className="w-5 h-5 text-yellow-600" />
              <span className="font-medium text-yellow-800">
                Potentially Suspicious Language Detected
              </span>
            </div>
            <div className="space-y-2">
              {suspiciousPhrases.map((phrase, index) => (
                <div key={index} className="flex items-center justify-between text-sm">
                  <span className="font-mono bg-yellow-200 px-2 py-1 rounded">
                    "{phrase.phrase}"
                  </span>
                  <span className="text-yellow-700">
                    {phrase.reason}
                  </span>
                </div>
              ))}
            </div>
            <p className="text-yellow-800 text-sm mt-3">
              Emotional or sensational language can be used to bypass critical thinking. 
              Look for neutral, fact-based reporting instead.
            </p>
          </div>
        </div>
      )}

  {/* Manipulation Tactics */}
  <ManipulationTactics suspiciousPhrases={suspiciousPhrases} metadata={metadata} evidence={evidence} />

      {/* General Verification Tips */}
      <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
        <h4 className="font-medium text-blue-900 mb-3">General Fact-Checking Tips:</h4>
        <ul className="text-sm text-blue-800 space-y-2">
          <li className="flex items-start space-x-2">
            <span className="font-bold">•</span>
            <span>Check the date: Old stories are sometimes shared as current news</span>
          </li>
          <li className="flex items-start space-x-2">
            <span className="font-bold">•</span>
            <span>Look for original sources: Trace claims back to their primary sources</span>
          </li>
          <li className="flex items-start space-x-2">
            <span className="font-bold">•</span>
            <span>Cross-reference: Compare information across multiple reliable sources</span>
          </li>
          <li className="flex items-start space-x-2">
            <span className="font-bold">•</span>
            <span>Use fact-checking sites: Consult Snopes, PolitiFact, or FactCheck.org</span>
          </li>
          <li className="flex items-start space-x-2">
            <span className="font-bold">•</span>
            <span>Consider context: Partial truths can be misleading without full context</span>
          </li>
        </ul>
      </div>

      {/* Extra Educational Blocks */}
      <QuickTips />
      <ImageVerificationTips />
      <ResourceLinks />
  <MicroQuiz suspiciousPhrases={suspiciousPhrases} metadata={metadata} evidence={evidence} />
    </div>
  );
};

export default EducationalInsights;