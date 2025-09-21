    def _initialize_knowledge_base(self) -> Dict[str, List[Dict]]:
        """Initialize knowledge base for common claims"""
        return {
            'health': {
                'vaccines': [
                    {
                        'claim': 'Vaccines cause autism',
                        'evidence': 'Multiple large studies have found no link between vaccines and autism. The original study that proposed this link has been retracted due to serious errors and ethical violations.',
                        'sources': ['cdc.gov', 'who.int', 'nejm.org'],
                        'truthfulness': False,
                        'confidence': 0.95
                    },
                    {
                        'claim': 'Vaccines are safe and effective',
                        'evidence': 'Extensive clinical trials and ongoing safety monitoring confirm that vaccines are safe and effective for the vast majority of people.',
                        'sources': ['cdc.gov', 'who.int', 'fda.gov'],
                        'truthfulness': True,
                        'confidence': 0.95
                    }
                ],
                'covid': [
                    {
                        'claim': 'COVID-19 is no more dangerous than the flu',
                        'evidence': 'COVID-19 has a higher mortality rate and complication rate than seasonal influenza, especially for elderly and immunocompromised individuals.',
                        'sources': ['cdc.gov', 'who.int', 'thelancet.com'],
                        'truthfulness': False,
                        'confidence': 0.90
                    }
                ]
            },
            'climate': {
                'global_warming': [
                    {
                        'claim': 'Climate change is not caused by humans',
                        'evidence': 'Scientific consensus based on multiple lines of evidence shows that current climate change is primarily driven by human activities, especially greenhouse gas emissions.',
                        'sources': ['nasa.gov', 'ipcc.ch', 'noaa.gov'],
                        'truthfulness': False,
                        'confidence': 0.95
                    },
                    {
                        'claim': 'Human activities are causing climate change',
                        'evidence': 'Scientific evidence conclusively shows that human activities, particularly burning fossil fuels, are the primary driver of current climate change.',
                        'sources': ['nasa.gov', 'ipcc.ch', 'noaa.gov'],
                        'truthfulness': True,
                        'confidence': 0.95
                    }
                ]
            },
            'technology': {
                '5g': [
                    {
                        'claim': '5G networks cause or spread coronavirus',
                        'evidence': 'Radio waves cannot transmit viruses. Viruses are biological entities that require biological transmission. This claim contradicts basic principles of physics and biology.',
                        'sources': ['who.int', 'fcc.gov', 'ieee.org'],
                        'truthfulness': False,
                        'confidence': 0.98
                    }
                ]
            }
        }
        
    def _semantic_search_knowledge_base(self, claim: str) -> Optional[Dict]:
        """Search knowledge base for semantically similar claims"""
        if not SENTENCE_TRANSFORMERS_AVAILABLE or not self.semantic_model:
            return None
            
        try:
            # Encode the input claim
            claim_embedding = self.semantic_model.encode(claim)
            
            best_match = None
            highest_similarity = 0.75  # Minimum similarity threshold
            
            # Search through knowledge base
            for domain, categories in self.knowledge_base.items():
                for category, entries in categories.items():
                    for entry in entries:
                        # Encode knowledge base claim
                        kb_embedding = self.semantic_model.encode(entry['claim'])
                        
                        # Calculate cosine similarity
                        similarity = np.dot(claim_embedding, kb_embedding) / (
                            np.linalg.norm(claim_embedding) * np.linalg.norm(kb_embedding)
                        )
                        
                        # Update best match if this is more similar
                        if similarity > highest_similarity:
                            highest_similarity = similarity
                            entry_with_metadata = entry.copy()
                            entry_with_metadata.update({
                                'domain': domain,
                                'category': category,
                                'similarity': float(similarity)
                            })
                            best_match = entry_with_metadata
            
            return best_match
        
        except Exception as e:
            print(f"Error in semantic search: {e}")
            return None