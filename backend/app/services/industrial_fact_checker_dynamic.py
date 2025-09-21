    def _calculate_dynamic_verdict(self, evidence_comparison: Dict, content_markers: Dict, quality_multiplier: float, kb_match: Optional[Dict]) -> Dict[str, Any]:
        """Calculate verdict and credibility score using multiple metrics"""
        # Start with base credibility from evidence
        support_ratio = evidence_comparison.get('support_weight', 0) / max(1, evidence_comparison.get('total_weight', 1))
        base_credibility = support_ratio * 100
        
        # Adjust based on content quality
        quality_impact = (content_markers['scientific_indicators'].get('score', 0) - 
                         content_markers['manipulation_flags'].get('penalty', 0)) * 0.3
        
        # Factor in source credibility
        source_trust = content_markers.get('source_quality', 50)
        source_impact = (source_trust - 50) * 0.2
        
        # Calculate factual density impact
        fact_density = content_markers.get('factual_density', 0)
        fact_impact = min(10, fact_density * 2)
        
        # Knowledge base influence
        kb_impact = 0
        if kb_match:
            kb_similarity = kb_match.get('similarity', 0)
            if kb_similarity > 0.85:
                kb_impact = (20 if kb_match.get('truthfulness', True) else -20) * (kb_similarity - 0.85) * 5
        
        # Calculate final credibility score
        credibility_score = base_credibility + quality_impact + source_impact + fact_impact + kb_impact
        
        # Apply quality multiplier for final adjustment
        credibility_score *= quality_multiplier
        
        # Ensure score stays in valid range and add small variation
        content_hash = sum(ord(c) for c in str(content_markers)) % 11 - 5  # -5 to +5
        credibility_score = max(5, min(95, credibility_score + content_hash))
        
        # Determine verdict based on thresholds and confidence
        confidence = min(1.0, (abs(credibility_score - 50) / 30))  # Higher confidence further from 50%
        
        if credibility_score >= 70:
            verdict = 'TRUE'
        elif credibility_score <= 30:
            verdict = 'FALSE'
        else:
            verdict = 'AMBIGUOUS'
            
        return {
            'verdict': verdict,
            'credibility_score': credibility_score,
            'confidence': confidence
        }

    def _calculate_quality_multiplier(self, content_analysis: Dict, content_markers: Dict) -> float:
        """Calculate quality multiplier based on content analysis"""
        base_multiplier = 1.0
        
        # Adjust based on content quality score
        quality_score = content_analysis.get('quality_score', 50)
        if quality_score >= 80:
            base_multiplier *= 1.2
        elif quality_score <= 30:
            base_multiplier *= 0.8
            
        # Factor in scientific indicators
        scientific_score = content_markers['scientific_indicators'].get('score', 0)
        if scientific_score > 50:
            base_multiplier *= 1.1
            
        # Consider manipulation flags
        manipulation_penalty = content_markers['manipulation_flags'].get('penalty', 0)
        if manipulation_penalty > 50:
            base_multiplier *= 0.9
            
        return max(0.6, min(1.4, base_multiplier))  # Keep within reasonable bounds

    def _calculate_evidence_strength(self, evidence_comparison: Dict, kb_match: Optional[Dict]) -> float:
        """Calculate the strength of available evidence"""
        base_strength = evidence_comparison.get('support_weight', 0)
        
        # Add knowledge base contribution if available
        if kb_match and kb_match.get('similarity', 0) > 0.85:
            base_strength *= (1.0 + kb_match['similarity'] - 0.85)
            
        return base_strength

    def _analyze_credibility_signals(self, content: str) -> Dict[str, Any]:
        """Analyze various credibility signals in content"""
        signals = {
            'factual_language': len(re.findall(r'\b(study|research|evidence|data|analysis)\b', content.lower())),
            'qualified_claims': len(re.findall(r'\b(may|might|could|suggests?|indicates?)\b', content.lower())),
            'absolute_claims': len(re.findall(r'\b(always|never|everyone|no one|proves?|definitely)\b', content.lower())),
            'uncertainty_markers': len(re.findall(r'\b(possibly|perhaps|unclear|not certain|more research needed)\b', content.lower()))
        }
        
        score = min(100, sum([
            signals['factual_language'] * 5,
            signals['qualified_claims'] * 3,
            -signals['absolute_claims'] * 4,
            signals['uncertainty_markers'] * 2
        ]))
        
        return {'score': score, 'details': signals}

    def _calculate_factual_density(self, content: str) -> float:
        """Calculate the density of factual statements and data points"""
        total_words = len(content.split())
        if total_words == 0:
            return 0.0
            
        fact_patterns = [
            r'\b\d+(?:\.\d+)?%\b',  # Percentages
            r'\b(?:in|during|on)\s+\d{4}\b',  # Years
            r'\b\d+(?:\.\d+)?\s*(?:million|billion|trillion)\b',  # Large numbers
            r'\b(?:according to|cited by|reported by|study by)\b',  # Citations
            r'\b(?:increase(?:d|s)?|decrease(?:d|s)?|change(?:d|s)?)\s+by\s+\d+\b',  # Changes
            r'\b(?:approximately|estimated|averaged?|mean)\s+\d+\b'  # Statistical references
        ]
        
        fact_count = sum(len(re.findall(pattern, content.lower())) for pattern in fact_patterns)
        density = (fact_count * 100.0) / total_words
        
        return min(100.0, density * 10)