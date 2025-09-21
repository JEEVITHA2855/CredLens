"""
Enhanced Real-Time AI Misinformation Detection System
Uses transformer models and real-time evidence collection for accurate analysis
"""
import re
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import numpy as np
from ..models.claim import VerificationStatus, CredibilityFingerprint, Evidence
from .evidence_collector import RealTimeEvidenceCollector

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
    print("Successfully loaded sentence-transformers")
except ImportError:
    print("Warning: sentence-transformers not available, falling back to basic embedding")
    from transformers import AutoModel, AutoTokenizer
    SENTENCE_TRANSFORMERS_AVAILABLE = False

class EnhancedFactChecker:
    def __init__(self):
        print("Initializing Enhanced Fact Checker...")
        
        # Setup device for computation
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Device set to use {device}")
        
        try:
            # Load NLI model for claim verification
            self.nli_model = pipeline(
                'zero-shot-classification',
                model='facebook/bart-large-mnli',
                device=0 if torch.cuda.is_available() else -1
            )
            
            # Load models for semantic analysis
            if SENTENCE_TRANSFORMERS_AVAILABLE:
                self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
                print("Using sentence-transformers for embeddings")
            else:
                # Fallback to using base transformers
                model_name = 'sentence-transformers/all-MiniLM-L6-v2'
                self.semantic_tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.semantic_model = AutoModel.from_pretrained(model_name)
                if torch.cuda.is_available():
                    self.semantic_model = self.semantic_model.to('cuda')
                print("Using basic transformer model for embeddings")
            
            # Initialize evidence collector
            self.evidence_collector = RealTimeEvidenceCollector()
            
            print("Models and services loaded successfully")
        except Exception as e:
            print(f"Warning: Error initializing some components: {e}")
            # Ensure basic functionality works even if some models fail to load
            self.nli_model = None
            self.semantic_model = None
        
        # Misinformation pattern detection
        self.misinfo_patterns = {
            'sensational': [
                r'SHOCKING', r'UNBELIEVABLE', r'STUNNING',
                r'THEY DON\'T WANT YOU TO KNOW', r'WAKE UP',
                r'DOCTORS HATE', r'ONE WEIRD TRICK'
            ],
            'conspiracy': [
                r'COVER.?UP', r'CONSPIRACY', r'SHADOW',
                r'ILLUMINATI', r'NEW WORLD ORDER', r'DEEP STATE'
            ],
            'false_authority': [
                r'EXPERTS AGREE', r'STUDIES PROVE',
                r'RESEARCH SHOWS', r'SCIENTISTS CONFIRM'
            ]
        }
        
    def _load_health_knowledge(self) -> Dict[str, List[Dict]]:
        """Load validated health knowledge"""
        return {
            'vaccines': [
                {
                    'claim': 'Vaccines are safe and effective through clinical trials',
                    'evidence': 'Large-scale clinical trials and extensive real-world data have consistently demonstrated vaccine safety and efficacy',
                    'sources': ['who.int', 'cdc.gov', 'nih.gov'],
                    'confidence': 0.95
                },
                {
                    'claim': 'Vaccines cause autism',
                    'evidence': 'Multiple large studies have conclusively shown no link between vaccines and autism',
                    'sources': ['who.int', 'cdc.gov', 'nejm.org'],
                    'confidence': 0.95,
                    'contradicts': True
                }
            ],
            'nutrition': [
                {
                    'claim': 'A balanced diet promotes health',
                    'evidence': 'Scientific consensus supports benefits of balanced nutrition',
                    'sources': ['nih.gov', 'who.int'],
                    'confidence': 0.90
                }
            ]
        }

    def _load_tech_knowledge(self) -> Dict[str, List[Dict]]:
        """Load validated technology knowledge"""
        return {
            '5g': [
                {
                    'claim': '5G networks spread viruses',
                    'evidence': 'Radio waves cannot transmit biological viruses. This claim contradicts basic principles of biology and physics',
                    'sources': ['who.int', 'fcc.gov', 'ieee.org'],
                    'confidence': 0.95,
                    'contradicts': True
                }
            ],
            'ai': [
                {
                    'claim': 'AI models analyze large datasets efficiently',
                    'evidence': 'Modern AI systems can process and analyze vast amounts of data using optimized algorithms',
                    'sources': ['nature.com', 'science.org', 'arxiv.org'],
                    'confidence': 0.90
                }
            ]
        }

    def _load_science_knowledge(self) -> Dict[str, List[Dict]]:
        """Load validated scientific knowledge"""
        return {
            'physics': [
                {
                    'claim': 'Earth is flat',
                    'evidence': 'Multiple independent observations, satellite data, and physics experiments confirm Earth is spherical',
                    'sources': ['nasa.gov', 'esa.int', 'science.org'],
                    'confidence': 0.99,
                    'contradicts': True
                }
            ],
            'space': [
                {
                    'claim': 'Moon landing in July 1969',
                    'evidence': 'Extensive documentation, physical samples, and independent verification confirm the Apollo moon landing',
                    'sources': ['nasa.gov', 'science.org', 'smithsonian.org'],
                    'confidence': 0.99
                },
                {
                    'claim': 'Moon landing was fake',
                    'evidence': 'Multiple lines of evidence, including moon rocks, photos, and independent verification confirm authenticity',
                    'sources': ['nasa.gov', 'science.org', 'noaa.gov'],
                    'confidence': 0.95,
                    'contradicts': True
                }
            ]
        }

    def _load_environment_knowledge(self) -> Dict[str, List[Dict]]:
        """Load validated environmental knowledge"""
        return {
            'climate': [
                {
                    'claim': 'Human activities contribute to climate change',
                    'evidence': 'Overwhelming scientific evidence from multiple independent sources confirms human impact on climate',
                    'sources': ['nasa.gov', 'epa.gov', 'un.org'],
                    'confidence': 0.95
                },
                {
                    'claim': 'Climate change is a hoax',
                    'evidence': 'Climate change is supported by extensive scientific data, measurements, and global research',
                    'sources': ['nasa.gov', 'noaa.gov', 'ipcc.ch'],
                    'confidence': 0.95,
                    'contradicts': True
                }
            ],
            'pollution': [
                {
                    'claim': 'Industrial emissions affect climate',
                    'evidence': 'Measured correlations between industrial emissions and global temperature changes',
                    'sources': ['epa.gov', 'who.int', 'noaa.gov'],
                    'confidence': 0.90
                }
            ]
        }

    def analyze_claim(self, claim: str) -> Dict[str, Any]:
        """
        Analyze a claim using real-time evidence collection and verification
        """
        analysis_start = datetime.now()
        
        try:
            if not self.nli_model or not self.semantic_model:
                return {
                    'verification_status': VerificationStatus.AMBIGUOUS,
                    'credibility_fingerprint': {
                        'overall_credibility': 0,
                        'source_trust': 0,
                        'language_safety': 0,
                        'corroboration_count': 0,
                        'contradiction_count': 0
                    },
                    'evidence': [],
                    'suspicious_phrases': [],
                    'micro_lesson': None,
                    'explanation': 'Service is initializing. Required models are not yet loaded.'
                }

            # 1. Extract main factual claim(s)
            claim_data = self._extract_claim_data(claim)
            
            # 2. Collect real-time evidence 
            try:
                evidence_list = self.evidence_collector.collect_evidence(claim)
            except Exception as e:
                print(f"Error collecting evidence: {e}")
                evidence_list = []
            
            # 3. Analyze evidence using NLI and calculate source reliability
            try:
                evidence_analysis = self._analyze_evidence(claim, evidence_list)
            except Exception as e:
                print(f"Error analyzing evidence: {e}")
                evidence_analysis = {
                    'supporting': [],
                    'contradicting': [],
                    'evidence_list': evidence_list
                }
            
            # 4. Calculate comprehensive credibility scores
            try:
                credibility_scores = self._calculate_credibility_scores(evidence_analysis)
            except Exception as e:
                print(f"Error calculating scores: {e}")
                credibility_scores = CredibilityFingerprint(
                    overall_credibility=50,
                    source_trust=50,
                    corroboration_count=0,
                    contradiction_count=0,
                    language_safety=50
                )
            
            # 5. Generate final verdict and explanation
            try:
                verdict_data = self._generate_verdict(evidence_analysis, credibility_scores)
            except Exception as e:
                print(f"Error generating verdict: {e}")
                verdict_data = {
                    'verdict': VerificationStatus.AMBIGUOUS,
                    'explanation': 'Unable to generate verdict due to an error in analysis.'
                }
            
            # 6. Format evidence list with required fields
            formatted_evidence = []
            for ev in evidence_list:
                ev_type = self._determine_evidence_type(ev)
                ev_dict = {
                    'text': ev.text,
                    'source': ev.source,
                    'url': ev.url if hasattr(ev, 'url') else None,
                    'type': ev_type,
                    'reliability_score': float(ev.confidence * 100) if hasattr(ev, 'confidence') else 70.0,
                    'verification_method': self._determine_verification_method(ev)
                }
                # Optional fields
                if hasattr(ev, 'date'):
                    ev_dict['date'] = ev.date
                if hasattr(ev, 'region'):
                    ev_dict['region'] = ev.region
                formatted_evidence.append(ev_dict)
            
            analysis_time = (datetime.now() - analysis_start).total_seconds()
            
            # Convert CredibilityFingerprint to dict and ensure all fields are present
            credibility_dict = {
                'overall_credibility': float(credibility_scores.overall_credibility),
                'source_trust': float(credibility_scores.source_trust),
                'language_safety': float(credibility_scores.language_safety),
                'corroboration_count': int(credibility_scores.corroboration_count),
                'contradiction_count': int(credibility_scores.contradiction_count)
            }
            
            # Get the verdict status and ensure it's one of the allowed values
            try:
                final_verdict = verdict_data.get('verdict', VerificationStatus.AMBIGUOUS)
            except:
                final_verdict = VerificationStatus.AMBIGUOUS
                
            # Simple micro-lesson as an object with tip and category properties
            micro_lesson = {
                "tip": "Always verify information across multiple reliable sources.",
                "category": "source_verification"
            }
                
            return {
                'verification_status': final_verdict,
                'credibility_fingerprint': credibility_dict,
                'evidence': formatted_evidence,
                'suspicious_phrases': [],  # List of strings for now
                'micro_lesson': micro_lesson,
                'explanation': "Analysis completed successfully."
            }
            
        except Exception as e:
            print(f"Error analyzing claim: {e}")
            raise ValueError(f"Failed to analyze claim: {str(e)}")
        
        return result

    def _analyze_evidence(self, claim: str, evidence_list: List[Evidence]) -> Dict[str, Any]:
        """
        Analyze evidence using NLI and calculate source reliability
        """
        analysis_result = {
            'supporting': [],
            'contradicting': [],
            'contextual': [],
            'total_reliability': 0.0,
            'evidence_list': evidence_list
        }
        
        try:
            for evidence in evidence_list:
                # Prepare text for classification
                hypothesis = evidence.text[:512]  # Truncate to avoid token length issues
                
                # Classify evidence using NLI
                result = self.nli_model(hypothesis, [claim], multi_label=False)
                labels = result['labels']
                scores = result['scores']
                
                # Use the highest confidence classification
                max_score_idx = scores.index(max(scores))
                prediction = labels[max_score_idx]
                
                # Add evidence to appropriate category and set type
                if prediction == 'entailment':
                    evidence.type = 'SUPPORT'
                    analysis_result['supporting'].append(evidence)
                elif prediction == 'contradiction':
                    evidence.type = 'CONTRADICT'
                    analysis_result['contradicting'].append(evidence)
                else:
                    evidence.type = 'CONTEXT'
                    analysis_result['contextual'].append(evidence)
                
                # Update reliability scores
                reliability = getattr(evidence, 'reliability_score', 70.0)
                analysis_result['total_reliability'] += reliability
        
        except Exception as e:
            print(f"Error in evidence analysis: {e}")
            # Ensure we have a valid result even if analysis fails
            for evidence in evidence_list:
                evidence.type = 'CONTEXT'
                analysis_result['contextual'].append(evidence)
                analysis_result['total_reliability'] += getattr(evidence, 'reliability_score', 70.0)
        
        return analysis_result

    def _calculate_credibility_scores(self, evidence_analysis: Dict[str, Any]) -> CredibilityFingerprint:
        """
        Calculate comprehensive credibility scores based on evidence analysis
        """
        # Calculate source trust score
        if evidence_list := (
            evidence_analysis['supporting'] +
            evidence_analysis['contradicting'] +
            evidence_analysis['contextual']
        ):
            avg_reliability = evidence_analysis['total_reliability'] / len(evidence_list)
        else:
            avg_reliability = 50.0  # Default score when no evidence
            
        # Count supporting and contradicting sources
        support_count = len(evidence_analysis['supporting'])
        contradict_count = len(evidence_analysis['contradicting'])
        
        # Calculate overall credibility
        if support_count + contradict_count > 0:
            # Weight based on source reliability and evidence counts
            credibility = (
                (support_count * 100) / (support_count + contradict_count * 2)  # Contradictions count double
            ) * (avg_reliability / 100)  # Scale by source reliability
        else:
            credibility = 50.0  # Neutral score when no clear evidence
            
        # Language safety score (100 is safest)
        language_safety = 100.0
        for evidence in evidence_list:
            if evidence.type == 'CONTRADICT':
                language_safety -= 10  # Penalize for contradictions
            
        return CredibilityFingerprint(
            overall_credibility=max(0, min(100, credibility)),
            source_trust=avg_reliability,
            corroboration_count=support_count,
            contradiction_count=contradict_count,
            language_safety=max(0, min(100, language_safety))
        )

    def _generate_verdict(self, evidence_analysis: Dict[str, Any], scores: CredibilityFingerprint) -> Dict[str, Any]:
        """
        Generate final verdict and explanation based on evidence analysis
        """
        try:
            # Initialize with default values
            verdict = VerificationStatus.AMBIGUOUS
            explanation = "Insufficient evidence to make a definitive conclusion."
            
            # Determine verdict based on evidence and scores
            if (isinstance(evidence_analysis, dict) and 
                len(evidence_analysis.get('supporting', [])) > 0 and 
                scores.overall_credibility >= 80):
                verdict = VerificationStatus.TRUE
                explanation = "This claim appears to be accurate based on available evidence."
            elif (isinstance(evidence_analysis, dict) and 
                  len(evidence_analysis.get('contradicting', [])) > 0 or 
                  scores.overall_credibility <= 40):
                verdict = VerificationStatus.FALSE
                explanation = "This claim appears to be false or misleading based on available evidence."
            
            # Add source information
            if isinstance(evidence_analysis, dict) and evidence_analysis.get('evidence_list', []):
                explanation += "\n\nSources analyzed:"
                for evidence in evidence_analysis['evidence_list'][:3]:  # Show top 3 sources
                    explanation += f"\n- {evidence.source}"
                    if hasattr(evidence, 'date') and evidence.date:
                        explanation += f" (Date: {evidence.date})"
            
            # Add reliability context
            explanation += f"\n\nSource Trust Score: {scores.source_trust:.0f}%"
            if scores.corroboration_count > 0:
                explanation += f"\nCorroborating Sources: {scores.corroboration_count}"
            if scores.contradiction_count > 0:
                explanation += f"\nContradicting Sources: {scores.contradiction_count}"
                
            return {
                'verdict': verdict,
                'explanation': explanation
            }
            
        except Exception as e:
            print(f"Error generating verdict: {e}")
            return {
                'verdict': VerificationStatus.AMBIGUOUS,
                'explanation': "Unable to generate verdict due to an error in analysis."
            }
    def _determine_evidence_type(self, evidence: Any) -> str:
        """Determine the type of evidence (SUPPORT, CONTRADICT, or CONTEXT)"""
        # Use confidence scores if available
        if hasattr(evidence, 'stance'):
            if evidence.stance == 'supporting':
                return 'SUPPORT'
            elif evidence.stance == 'contradicting':
                return 'CONTRADICT'
            
        # Default to CONTEXT if can't determine
        return 'CONTEXT'

    def _determine_verification_method(self, evidence: Any) -> str:
        """Determine how the evidence was verified"""
        if hasattr(evidence, 'verification_method'):
            return evidence.verification_method
        
        # Try to infer from source or type
        source = evidence.source.lower() if hasattr(evidence, 'source') else ''
        
        if any(x in source for x in ['journal', 'research', 'study']):
            return 'peer-review'
        elif any(x in source for x in ['fact-check', 'factcheck']):
            return 'fact-check'
        elif any(x in source for x in ['news', 'article']):
            return 'news-article'
            
        return 'automated-verification'

    def _extract_claim_data(self, claim: str) -> Dict[str, Any]:
        """Extract structured data from claim"""
        return {
            'text': claim,
            'tokens': claim.split(),
            'length': len(claim)
        }
        
        return {
            'text': claim,
            'numbers': numbers,
            'entities': entities,
            'dates': dates,
            'word_count': len(claim.split())
        }

    def _semantic_analysis(self, claim: str) -> Dict[str, Any]:
        """Perform semantic analysis of claim"""
        # Encode claim using transformer
        claim_embedding = self.semantic_model.encode([claim])[0]
        
        # Determine claim category
        categories = {
            'HEALTH': ['health', 'medical', 'disease', 'treatment', 'vaccine'],
            'TECH': ['technology', 'digital', 'computer', 'internet', '5g'],
            'SCIENCE': ['scientific', 'physics', 'chemistry', 'biology'],
            'ENVIRONMENT': ['climate', 'pollution', 'environment', 'emissions']
        }
        
        claim_lower = claim.lower()
        category = 'GENERAL'
        for cat, keywords in categories.items():
            if any(word in claim_lower for word in keywords):
                category = cat
                break
        
        return {
            'category': category,
            'embedding': claim_embedding
        }

    def _verify_against_knowledge(self, claim: str, category: str) -> Dict[str, Any]:
        """Verify claim against knowledge base"""
        claim_lower = claim.lower()
        
        # Pre-check for known false claims
        known_false_patterns = {
            'HEALTH': [
                (r'vaccine.*caus.*autism', 'Extensive scientific studies have conclusively shown no link between vaccines and autism'),
                (r'drink.*bleach.*cure', 'Drinking bleach is extremely dangerous and has no medical benefits')
            ],
            'TECH': [
                (r'5g.*(spread|cause).*virus', 'Radio waves cannot transmit biological viruses. This is scientifically impossible'),
                (r'5g.*(radiation|dangerous)', '5G operates within safe radiation limits set by international standards')
            ],
            'SCIENCE': [
                (r'earth.*flat', 'Multiple independent observations and measurements confirm Earth is spherical'),
                (r'moon landing.*fake', 'Extensive documentation, physical evidence, and independent verification confirm moon landings')
            ],
            'ENVIRONMENT': [
                (r'climate.*(hoax|fake)', 'Climate change is supported by overwhelming scientific evidence from multiple independent sources'),
                (r'global warming.*not real', 'Temperature records and multiple scientific indicators confirm global warming')
            ]
        }
        
        # Check for false claims first
        if category in known_false_patterns:
            for pattern, evidence in known_false_patterns[category]:
                if re.search(pattern, claim_lower):
                    return {
                        'matched': True,
                        'evidence': evidence,
                        'sources': ['who.int', 'science.org', 'nasa.gov'],
                        'confidence': 0.95,
                        'contradicted': True
                    }
        
        # Check knowledge base for verified claims
        if category in self.knowledge_base:
            knowledge = self.knowledge_base[category]
            
            # Encode claim
            claim_embedding = self.semantic_model.encode([claim])[0]
            
            matches = []
            for topic, entries in knowledge.items():
                for entry in entries:
                    entry_embedding = self.semantic_model.encode([entry['claim']])[0]
                    similarity = np.dot(claim_embedding, entry_embedding)
                    
                    if similarity > 0.7:
                        matches.append({
                            'similarity': similarity,
                            'entry': entry
                        })
            
            # Sort by similarity
            matches.sort(key=lambda x: x['similarity'], reverse=True)
            
            if matches:
                best_match = matches[0]['entry']
                contradicting = any(m['entry']['contradicts'] for m in matches if 'contradicts' in m['entry'])
                
                return {
                    'matched': True,
                    'evidence': best_match['evidence'],
                    'sources': best_match['sources'],
                    'confidence': best_match['confidence'] * matches[0]['similarity'],
                    'contradicted': contradicting
                }
        
        # No strong match found
        return {
            'matched': False,
            'evidence': None,
            'sources': [],
            'confidence': 0.5,
            'contradicted': False
        }

    def _detect_patterns(self, claim: str) -> Dict[str, Any]:
        """Detect misinformation patterns"""
        claim_upper = claim.upper()
        patterns_found = {
            'sensational': 0,
            'conspiracy': 0,
            'false_authority': 0
        }
        
        for category, patterns in self.misinfo_patterns.items():
            for pattern in patterns:
                if re.search(pattern, claim_upper):
                    patterns_found[category] += 1
        
        total_patterns = sum(patterns_found.values())
        risk_score = min(100, total_patterns * 20)
        
        return {
            'patterns': patterns_found,
            'total': total_patterns,
            'risk_score': risk_score
        }

    def _calculate_scores(self, claim_data: Dict, verification: Dict, patterns: Dict) -> Dict[str, Any]:
        """Calculate structured scores"""
        # Base credibility starts at 50 (neutral)
        credibility = 50
        
        # Adjust based on verification confidence and evidence
        if verification['matched']:
            # Strong positive verification
            if verification['confidence'] >= 0.8 and not verification['contradicted']:
                credibility += 40 * verification['confidence']
            # Strong negative verification
            elif verification['confidence'] >= 0.8 and verification['contradicted']:
                credibility -= 40 * verification['confidence']
            # Weak or unclear verification
            else:
                credibility += 20 * verification['confidence']
        
        # Penalize for misinformation patterns
        pattern_penalty = 0
        if patterns['patterns']['sensational'] > 0:
            pattern_penalty += 15 * patterns['patterns']['sensational']
        if patterns['patterns']['conspiracy'] > 0:
            pattern_penalty += 20 * patterns['patterns']['conspiracy']
        if patterns['patterns']['false_authority'] > 0:
            pattern_penalty += 10 * patterns['patterns']['false_authority']
            
        credibility = max(0, credibility - pattern_penalty)
        
        # Source trust score
        if verification['sources']:
            # Calculate weighted source trust
            source_scores = []
            for source in verification['sources']:
                base_score = self.source_credibility.get(source, 40)
                # Boost score if from highly trusted domain
                if any(domain in source for domain in ['.gov', '.edu', '.org']):
                    base_score = min(100, base_score + 10)
                source_scores.append(base_score)
            source_trust = sum(source_scores) / len(source_scores)
        else:
            source_trust = 40  # Default trust score
        
        # Count corroborating and contradicting sources
        if verification['matched']:
            corroboration = len([s for s in verification['sources'] 
                               if self.source_credibility.get(s, 0) >= 70])
            contradiction = len([s for s in verification['sources'] 
                              if verification['contradicted'] and self.source_credibility.get(s, 0) >= 70])
        else:
            corroboration = 0
            contradiction = 0
        
        # Language safety score (penalize sensational/misleading language)
        base_safety = 100
        for category, count in patterns['patterns'].items():
            if count > 0:
                if category == 'sensational':
                    base_safety -= 10 * count
                elif category == 'conspiracy':
                    base_safety -= 15 * count
                elif category == 'false_authority':
                    base_safety -= 5 * count
        
        language_safety = max(0, base_safety)
        
        return {
            'credibility': max(0, min(100, int(credibility))),
            'source_trust': int(source_trust),
            'corroboration': corroboration,
            'contradiction': contradiction,
            'language_safety': language_safety,
            'patterns': patterns['patterns']  # Include pattern details for verdict generation
        }

    def _generate_verdict(self, evidence_analysis: Dict[str, Any], scores: Any) -> Dict[str, Any]:
        """Generate final verdict and reasoning"""
        # Check if scores is a CredibilityFingerprint object
        if hasattr(scores, 'overall_credibility'):
            credibility = scores.overall_credibility
            corroboration_count = scores.corroboration_count
            contradiction_count = scores.contradiction_count
            source_trust = scores.source_trust
        # Otherwise, handle it as a dict
        elif isinstance(scores, dict):
            credibility = scores.get('credibility', 0) if 'credibility' in scores else scores.get('overall_credibility', 0)
            corroboration_count = scores.get('corroboration', 0)
            contradiction_count = scores.get('contradiction', 0)
            source_trust = scores.get('source_trust', 0)
            patterns = scores.get('patterns', {})
        else:
            # Default values if scores is neither object nor dict
            credibility = 0
            corroboration_count = 0
            contradiction_count = 0
            source_trust = 0
            patterns = {}
        
        # Extract verification data
        if isinstance(evidence_analysis, dict):
            matched = evidence_analysis.get('matched', False)
            confidence = evidence_analysis.get('confidence', 0)
            contradicted = evidence_analysis.get('contradicted', False)
            evidence_text = evidence_analysis.get('evidence', '')
            sources = evidence_analysis.get('sources', [])
            supporting = evidence_analysis.get('supporting', [])
            contradicting = evidence_analysis.get('contradicting', [])
        else:
            matched = False
            confidence = 0
            contradicted = False
            evidence_text = ''
            sources = []
            supporting = []
            contradicting = []
        
        # Determine verdict based on multiple factors
        if credibility >= 70 or (matched and confidence >= 0.8 and not contradicted) or len(supporting) > 2:
            verdict = VerificationStatus.TRUE
            reasoning = "Strong evidence confirms this claim."
            if evidence_text:
                reasoning += f" {evidence_text}"
            if sources or supporting:
                source_count = len(sources) if sources else len(supporting)
                reasoning += f" Supported by {source_count} reliable sources."
        
        # False if low credibility or contradicted by trusted sources
        elif credibility <= 40 or (matched and confidence >= 0.8 and contradicted) or len(contradicting) > 2:
            verdict = VerificationStatus.FALSE
            if evidence_text:
                reasoning = f"Evidence contradicts this claim. {evidence_text}"
            else:
                reasoning = "Claim lacks credible support or is contradicted by reliable sources."
        
        # Ambiguous if mixed evidence or insufficient data
        else:
            verdict = VerificationStatus.AMBIGUOUS
            if evidence_text:
                reasoning = f"Evidence is mixed or unclear. {evidence_text}"
            else:
                reasoning = "Additional verification needed for definitive assessment. Evidence is insufficient or contradictory."
        
        # Add more context to the reasoning
        reasoning += f"\n\nCredibility score: {credibility:.0f}%"
        if source_trust > 0:
            reasoning += f"\nSource trust: {source_trust:.0f}%"
        if corroboration_count > 0:
            reasoning += f"\nCorroborating sources: {corroboration_count}"
        if contradiction_count > 0:
            reasoning += f"\nContradicting sources: {contradiction_count}"
            
        # Ensure verdict is a VerificationStatus enum
        if not isinstance(verdict, VerificationStatus):
            verdict = VerificationStatus.AMBIGUOUS
            
        return {
            'verdict': verdict,
            'reasoning': reasoning
        }