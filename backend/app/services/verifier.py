from transformers import pipeline
from typing import List, Tuple
from ..models.evidence import FactCheck
from ..models.claim import Evidence
from ..config import NLI_MODEL

class NLIVerifier:
    def __init__(self):
        self.nli_pipeline = None
        self.load_model()
    
    def load_model(self):
        """Load the NLI model"""
        try:
            print("Loading NLI model...")
            self.nli_pipeline = pipeline(
                "zero-shot-classification",
                model=NLI_MODEL,
                device=-1  # Use CPU
            )
            print("NLI model loaded successfully")
        except Exception as e:
            print(f"Failed to load NLI model: {e}")
            # Fallback to a smaller model
            try:
                self.nli_pipeline = pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli",
                    device=-1
                )
                print("Loaded fallback NLI model")
            except Exception as e2:
                print(f"Failed to load fallback model: {e2}")
                self.nli_pipeline = None
    
    def verify_claim_against_evidence(
        self, 
        claim: str, 
        retrieved_fact_checks: List[Tuple[FactCheck, float]]
    ) -> List[Evidence]:
        """Verify claim against retrieved evidence using NLI"""
        if not self.nli_pipeline:
            # Fallback without NLI
            return self._fallback_verification(claim, retrieved_fact_checks)
        
        evidence_list = []
        
        for fact_check, similarity_score in retrieved_fact_checks:
            try:
                # Use NLI to determine relationship
                result = self.nli_pipeline(
                    claim,
                    [fact_check.claim, fact_check.explanation],
                    hypothesis_template="This claim is true: {}"
                )
                
                # Map labels
                label_mapping = {
                    "ENTAILMENT": "ENTAILMENT",
                    "CONTRADICTION": "CONTRADICTION", 
                    "NEUTRAL": "NEUTRAL"
                }
                
                primary_label = result['labels'][0]
                confidence = result['scores'][0]
                
                # Map to our labels
                nli_label = label_mapping.get(primary_label, "NEUTRAL")
                
                # Create evidence object
                evidence = Evidence(
                    text=fact_check.explanation,
                    source=fact_check.source,
                    url=fact_check.source_url,
                    nli_label=nli_label,
                    confidence=confidence,
                    similarity_score=similarity_score
                )
                
                evidence_list.append(evidence)
                
            except Exception as e:
                print(f"Error in NLI verification: {e}")
                # Fallback evidence
                evidence = Evidence(
                    text=fact_check.explanation,
                    source=fact_check.source,
                    url=fact_check.source_url,
                    nli_label="NEUTRAL",
                    confidence=0.5,
                    similarity_score=similarity_score
                )
                evidence_list.append(evidence)
        
        return evidence_list
    
    def _fallback_verification(
        self, 
        claim: str, 
        retrieved_fact_checks: List[Tuple[FactCheck, float]]
    ) -> List[Evidence]:
        """Fallback verification without NLI model"""
        evidence_list = []
        
        for fact_check, similarity_score in retrieved_fact_checks:
            # Simple heuristic based on fact check verdict and similarity
            nli_label = "NEUTRAL"
            confidence = similarity_score
            
            if fact_check.verdict.upper() == "TRUE":
                nli_label = "ENTAILMENT"
                confidence = min(0.8, similarity_score + 0.1)
            elif fact_check.verdict.upper() == "FALSE":
                nli_label = "CONTRADICTION"
                confidence = min(0.8, similarity_score + 0.1)
            
            evidence = Evidence(
                text=fact_check.explanation,
                source=fact_check.source,
                url=fact_check.source_url,
                nli_label=nli_label,
                confidence=confidence,
                similarity_score=similarity_score
            )
            
            evidence_list.append(evidence)
        
        return evidence_list
    
    def aggregate_evidence_verdict(self, evidence_list: List[Evidence]) -> Tuple[str, str]:
        """Aggregate evidence to determine overall verdict and explanation"""
        if not evidence_list:
            return "UNVERIFIED", "No evidence found to verify this claim."
        
        # Count evidence types weighted by confidence and similarity
        entailment_score = 0
        contradiction_score = 0
        neutral_score = 0
        
        for evidence in evidence_list:
            weight = (evidence.confidence + evidence.similarity_score) / 2
            
            if evidence.nli_label == "ENTAILMENT":
                entailment_score += weight
            elif evidence.nli_label == "CONTRADICTION":
                contradiction_score += weight
            else:
                neutral_score += weight
        
        total_score = entailment_score + contradiction_score + neutral_score
        
        if total_score == 0:
            return "UNVERIFIED", "Unable to determine claim veracity."
        
        # Normalize scores
        entailment_pct = entailment_score / total_score
        contradiction_pct = contradiction_score / total_score
        
        # Determine verdict
        if entailment_pct > 0.6:
            verdict = "LIKELY_TRUE"
            explanation = f"Evidence largely supports this claim ({entailment_pct:.1%} supporting evidence)."
        elif contradiction_pct > 0.6:
            verdict = "LIKELY_FALSE"
            explanation = f"Evidence largely contradicts this claim ({contradiction_pct:.1%} contradicting evidence)."
        elif abs(entailment_pct - contradiction_pct) < 0.2:
            verdict = "MIXED"
            explanation = f"Evidence is mixed: {entailment_pct:.1%} supporting, {contradiction_pct:.1%} contradicting."
        else:
            verdict = "UNVERIFIED"
            explanation = "Evidence is inconclusive or insufficient to verify this claim."
        
        return verdict, explanation