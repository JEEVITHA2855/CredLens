"""
Lesson Generator Service
Generates educational micro-lessons based on fact-checking analysis
"""
from typing import List, Dict, Any, Optional

class LessonGenerator:
    def __init__(self):
        self.lesson_templates = {
            'TRUE': [
                "This claim appears to be accurate. Here's why:",
                "Evidence supports this claim. Key points:",
                "This information checks out. Important details:"
            ],
            'FALSE': [
                "This claim appears to be false. Here's what you should know:",
                "Our analysis found issues with this claim. Key concerns:",
                "This information needs correction. Important facts:"
            ],
            'AMBIGUOUS': [
                "This claim needs more context. Consider these points:",
                "The truth is more nuanced. Here's what we found:",
                "More investigation is needed. Current findings:"
            ]
        }

    def generate_lesson(
        self,
        verification_status: Any,
        credibility_score: float,
        evidence_list: List[Dict[str, Any]],
        suspicious_phrases: List[Any],
        has_source_url: bool = False
    ) -> Dict[str, Any]:
        """
        Generate a micro-lesson based on fact-checking analysis
        """
        import random

        # Select template based on verification status
        template = random.choice(self.lesson_templates.get(verification_status, self.lesson_templates['AMBIGUOUS']))
        
        # Build lesson content
        lesson_points = []
        
        # Add credibility information
        if credibility_score >= 80:
            lesson_points.append("The source shows high credibility.")
        elif credibility_score <= 40:
            lesson_points.append("The source shows concerning credibility issues.")
        else:
            lesson_points.append("The source has mixed credibility indicators.")
            
        # Add evidence-based points
        for evidence in evidence_list[:3]:  # Limit to top 3 pieces of evidence
            if evidence.get('snippet'):
                lesson_points.append(evidence['snippet'])
                
        # Add warnings about suspicious language
        if suspicious_phrases:
            phrases_str = ", ".join(f'"{phrase}"' for phrase in suspicious_phrases[:3])
            lesson_points.append(f"Be cautious of potentially misleading phrases: {phrases_str}")
            
        # Source validation tip
        if has_source_url:
            lesson_points.append("Always verify information from multiple reliable sources.")
        
        # Determine lesson category based on analysis
        if suspicious_phrases:
            category = "language_analysis"
        elif has_source_url:
            category = "source_verification"
        else:
            category = "cross_referencing"
            
        # Combine points into a single tip
        tip = template + "\n" + "\n".join(f"- {point}" for point in lesson_points)
        if verification_status != 'TRUE':
            tip += "\n" + self._generate_recommendation(verification_status, credibility_score)
            
        return {
            'tip': tip,
            'category': category
        }
        
    def _generate_recommendation(self, verification_status: str, credibility_score: float) -> str:
        """Generate a specific recommendation based on analysis"""
        if verification_status == 'TRUE' and credibility_score >= 80:
            return "This information appears reliable and can be shared with confidence."
        elif verification_status == 'FALSE' or credibility_score <= 40:
            return "Exercise caution before sharing this information. Consider fact-checking with trusted sources."
        else:
            return "More research is recommended before drawing conclusions or sharing this information."