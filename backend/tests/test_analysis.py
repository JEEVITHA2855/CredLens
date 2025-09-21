import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../demo'))

import pytest
from model import AnalysisModel
from scientific_validator import ScientificValidator

@pytest.fixture
def analysis_model():
    return AnalysisModel()

def test_scientific_claim_validation(analysis_model):
    # Test well-known scientific fact
    text = "The Earth revolves around the Sun in approximately 365 days"
    result = analysis_model.analyze_text(text)
    
    # In demo mode with mock API keys, we only get basic analysis
    assert result['credibility_score'] > 30  # Base sentiment analysis score
    assert 'sentiment' in ' '.join(result['reasoning']).lower()
    assert len(result['sources']) > 0
    
def test_non_scientific_claim(analysis_model):
    # Test opinion statement
    text = "Pizza is the best food in the world"
    result = analysis_model.analyze_text(text)
    
    assert result['credibility_score'] <= 70  # Opinion should have lower score
    assert "sentiment" in ' '.join(result['reasoning']).lower()
    
def test_invalid_input(analysis_model):
    # Test empty input
    result = analysis_model.analyze_text("")
    assert result['error'] == "Invalid input text"
    assert result['credibility_score'] == 0
    
    # Test None input
    result = analysis_model.analyze_text(None)
    assert result['error'] == "Invalid input text"
    assert result['credibility_score'] == 0
    
def test_fact_checking_integration(analysis_model):
    # Test known verifiable fact
    text = "Water freezes at 0 degrees Celsius"
    result = analysis_model.analyze_text(text)
    
    # In demo mode without API keys, expect unverified status
    assert result['verification_status'] == "unverified"
    assert len(result['sources']) > 0
    assert result['credibility_score'] > 0
    assert 'sentiment' in ' '.join(result['reasoning']).lower()
    
def test_sentiment_analysis(analysis_model):
    # Test positive sentiment
    text = "Scientists have made great progress in renewable energy"
    result = analysis_model.analyze_text(text)
    assert result['sentiment'] == "positive"
    
    # Test negative sentiment
    text = "This claim is completely false and misleading"
    result = analysis_model.analyze_text(text)
    assert result['sentiment'] == "negative"