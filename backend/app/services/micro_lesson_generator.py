import random
from typing import List
from ..models.claim import MicroLesson, Evidence, SuspiciousPhrase, VerificationStatus

class MicroLessonGenerator:
    def __init__(self):
        self.lessons = {
            "source_verification": [
                "Always check the original source before sharing claims online.",
                "Look for established news organizations and fact-checking sites.",
                "Be skeptical of claims that don't cite credible sources.",
                "Check if multiple independent sources report the same information.",
                "Verify the author's credentials and expertise on the topic."
            ],
            "language_analysis": [
                "Be wary of emotionally charged language designed to provoke reactions.",
                "Watch out for excessive capitalization and punctuation in headlines.",
                "Claims with absolute words like 'never' or 'always' need extra scrutiny.",
                "Sensational phrases like 'shocking' or 'they don't want you to know' are red flags.",
                "Objective reporting uses neutral, factual language without emotional appeals."
            ],
            "cross_referencing": [
                "Search for the claim on fact-checking websites like Snopes or PolitiFact.",
                "Use multiple search engines to find diverse perspectives on the topic.",
                "Check recent news from various sources to see if they report the same facts.",
                "Look for scientific studies or official reports that support or refute the claim.",
                "Compare information across different types of sources (news, academic, official)."
            ],
            "evidence_evaluation": [
                "Strong claims require strong evidence - look for data and studies.",
                "Check if evidence actually supports the conclusion being made.",
                "Be aware that correlation doesn't always mean causation.",
                "Look for peer-reviewed research rather than opinion pieces.",
                "Consider whether the evidence is recent and still relevant."
            ],
            "bias_awareness": [
                "Consider the political or financial motivations of the source.",
                "Look for balanced reporting that presents multiple viewpoints.",
                "Be aware of your own confirmation bias when evaluating information.",
                "Check if the source has a history of accurate reporting.",
                "Notice if important context or opposing views are being omitted."
            ],
            "misinformation_patterns": [
                "Misinformation often spreads faster than corrections, so verify before sharing.",
                "Be extra cautious with information that confirms your existing beliefs.",
                "Watch for claims that seem designed to make you angry or afraid.",
                "Old stories are sometimes recirculated as if they were current news.",
                "Manipulated images and videos are increasingly common - reverse image search helps."
            ]
        }
    
    def generate_lesson(
        self, 
        verification_status: VerificationStatus,
        credibility_score: float,
        evidence: List[Evidence],
        suspicious_phrases: List[SuspiciousPhrase],
        has_url_source: bool = False
    ) -> MicroLesson:
        """Generate a contextual micro-lesson based on the claim analysis"""
        
        # Determine primary lesson category based on analysis
        category = self._determine_lesson_category(
            verification_status, credibility_score, evidence, suspicious_phrases, has_url_source
        )
        
        # Select appropriate lesson
        lessons = self.lessons.get(category, self.lessons["source_verification"])
        tip = random.choice(lessons)
        
        # Customize tip based on specific findings
        tip = self._customize_tip(tip, verification_status, suspicious_phrases, evidence)
        
        return MicroLesson(tip=tip, category=category)
    
    def _determine_lesson_category(
        self,
        verification_status: VerificationStatus,
        credibility_score: float,
        evidence: List[Evidence],
        suspicious_phrases: List[SuspiciousPhrase],
        has_url_source: bool
    ) -> str:
        """Determine the most relevant lesson category"""
        
        # If suspicious language detected, prioritize language analysis
        if suspicious_phrases:
            return "language_analysis"
        
        # If claim is false or mixed, teach about evidence evaluation
        if verification_status in [VerificationStatus.FALSE, VerificationStatus.AMBIGUOUS]:
            return "evidence_evaluation"
        
        # If low credibility sources, teach source verification
        if credibility_score < 0.5:
            return "source_verification"
        
        # If little evidence available, teach cross-referencing
        if len(evidence) < 2:
            return "cross_referencing"
        
        # If conflicting evidence, teach bias awareness
        supporting = sum(1 for e in evidence if e.nli_label == "ENTAILMENT")
        contradicting = sum(1 for e in evidence if e.nli_label == "CONTRADICTION")
        if supporting > 0 and contradicting > 0:
            return "bias_awareness"
        
        # Default to misinformation patterns
        return "misinformation_patterns"
    
    def _customize_tip(
        self, 
        tip: str, 
        verification_status: VerificationStatus,
        suspicious_phrases: List[SuspiciousPhrase],
        evidence: List[Evidence]
    ) -> str:
        """Customize the tip based on specific analysis results"""
        
        # Add specific context for suspicious phrases
        if suspicious_phrases and "emotional" in tip.lower():
            suspicious_words = [p.phrase for p in suspicious_phrases[:2]]
            if suspicious_words:
                tip += f" (Notice words like '{', '.join(suspicious_words)}' in this text.)"
        
        # Add context for verification status
        if verification_status == VerificationStatus.FALSE and "evidence" in tip.lower():
            tip += " This claim appears to be contradicted by available evidence."
        elif verification_status == VerificationStatus.AMBIGUOUS and "balance" in tip.lower():
            tip += " This claim has both supporting and contradicting evidence."
        
        # Add context for evidence quality
        if evidence and "sources" in tip.lower():
            source_count = len(set(e.source for e in evidence))
            if source_count == 1:
                tip += " Try finding additional independent sources."
        
        return tip
    
    def get_lesson_by_category(self, category: str) -> MicroLesson:
        """Get a random lesson from a specific category"""
        if category not in self.lessons:
            category = "source_verification"
        
        tip = random.choice(self.lessons[category])
        return MicroLesson(tip=tip, category=category)
    
    def get_all_categories(self) -> List[str]:
        """Get all available lesson categories"""
        return list(self.lessons.keys())