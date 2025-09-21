import numpy as np
import faiss
from typing import List, Tuple
import os
from ..models.evidence import FactCheck
from ..models.database import db
from ..config import EMBEDDING_MODEL, FAISS_INDEX_PATH, EMBEDDINGS_PATH
from transformers import AutoTokenizer, AutoModel
import torch

class SemanticRetriever:
    def __init__(self):
        try:
            # Try to import and use sentence-transformers
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(EMBEDDING_MODEL)
            self.use_basic_embedding = False
            print("Using SentenceTransformer for embeddings")
        except ImportError:
            # Fallback to basic embedding with transformers
            print("Using basic transformer model for embeddings")
            self.tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL)
            self.model = AutoModel.from_pretrained(EMBEDDING_MODEL)
            if torch.cuda.is_available():
                self.model = self.model.to('cuda')
            self.use_basic_embedding = True
        
        self.index = None
        self.fact_checks = []
        self.embeddings = None
        
    def _mean_pooling(self, model_output, attention_mask):
        """Mean pooling for basic embedding"""
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        
    def load_or_build_index(self):
        """Load existing FAISS index or build a new one"""
        if os.path.exists(FAISS_INDEX_PATH + ".index") and os.path.exists(EMBEDDINGS_PATH):
            self.load_index()
        else:
            self.build_index()
    
    def build_index(self):
        """Build FAISS index from fact checks in database"""
        print("Building FAISS index...")
        
        # Get all fact checks from database
        self.fact_checks = db.get_all_fact_checks()
        
        if not self.fact_checks:
            print("No fact checks found in database. Please run the dataset builder first.")
            return
        
        # Generate embeddings
        claims = [fc.claim for fc in self.fact_checks]
        self.embeddings = self.model.encode(claims, show_progress_bar=True)
        
        # Create FAISS index
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(self.embeddings)
        
        # Add embeddings to index
        self.index.add(self.embeddings.astype('float32'))
        
        # Save index and embeddings
        os.makedirs(os.path.dirname(FAISS_INDEX_PATH), exist_ok=True)
        faiss.write_index(self.index, FAISS_INDEX_PATH + ".index")
        np.save(EMBEDDINGS_PATH, self.embeddings)
        
        print(f"FAISS index built with {len(self.fact_checks)} fact checks")
    
    def load_index(self):
        """Load existing FAISS index"""
        print("Loading existing FAISS index...")
        
        self.index = faiss.read_index(FAISS_INDEX_PATH + ".index")
        self.embeddings = np.load(EMBEDDINGS_PATH)
        self.fact_checks = db.get_all_fact_checks()
        
        print(f"Loaded FAISS index with {len(self.fact_checks)} fact checks")
    
    def retrieve_similar_claims(self, query: str, top_k: int = 5) -> List[Tuple[FactCheck, float]]:
        """Retrieve similar claims using semantic search"""
        if self.index is None:
            self.load_or_build_index()
        
        if self.index is None or len(self.fact_checks) == 0:
            return []
        
        # Encode query
        query_embedding = self.get_embedding(query)
        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        # Return results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.fact_checks):  # Valid index
                fact_check = self.fact_checks[idx]
                results.append((fact_check, float(score)))
        
        return results
    
    def get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for a text"""
        if not self.use_basic_embedding:
            # Use sentence-transformers
            return self.model.encode([text])[0]
        else:
            # Use basic transformer model
            encoded_input = self.tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors='pt')
            with torch.no_grad():
                if torch.cuda.is_available():
                    encoded_input = {k: v.to('cuda') for k, v in encoded_input.items()}
                model_output = self.model(**encoded_input)
                embedding = self._mean_pooling(model_output, encoded_input['attention_mask'])
                return embedding.cpu().numpy()[0]