"""
Data collection script for building misinformation detection training dataset.
Uses official APIs and respects rate limits and terms of service.
"""
import os
import json
import time
import pandas as pd
import requests
from typing import List, Dict
from datetime import datetime, timedelta
from tqdm import tqdm

class DataCollector:
    def __init__(self, api_keys: Dict[str, str], output_dir: str = "data"):
        """Initialize data collector with API keys."""
        self.api_keys = api_keys
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize session with rate limiting
        self.session = requests.Session()
        self.last_request = {}
        
    def collect_from_factcheck_api(self, query: str = None, max_results: int = 100) -> List[Dict]:
        """
        Collect data from Google's Fact Check API.
        https://developers.google.com/fact-check/tools/api
        """
        endpoint = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
        results = []
        next_page_token = None
        
        while len(results) < max_results:
            params = {
                "key": self.api_keys["google"],
                "pageSize": min(50, max_results - len(results)),
                "pageToken": next_page_token,
                "query": query
            }
            
            response = self.session.get(endpoint, params=params)
            data = response.json()
            
            if "claims" not in data:
                break
                
            for claim in data["claims"]:
                results.append({
                    "claim": claim["text"],
                    "claimant": claim.get("claimant", ""),
                    "claimDate": claim.get("claimDate", ""),
                    "rating": claim.get("claimReview", [{}])[0].get("textualRating", ""),
                    "url": claim.get("claimReview", [{}])[0].get("url", ""),
                    "publisher": claim.get("claimReview", [{}])[0].get("publisher", {}).get("name", ""),
                    "reviewDate": claim.get("claimReview", [{}])[0].get("reviewDate", "")
                })
            
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break
                
            time.sleep(1)  # Rate limiting
            
        return results

    def collect_from_snopes(self) -> List[Dict]:
        """
        Collect fact-checks from Snopes using their API.
        Requires API key and follows usage guidelines.
        """
        endpoint = "https://www.snopes.com/api/facts/"
        results = []
        page = 1
        
        while True:
            params = {
                "key": self.api_keys["snopes"],
                "page": page,
                "per_page": 100
            }
            
            response = self.session.get(endpoint, params=params)
            data = response.json()
            
            if not data["facts"]:
                break
                
            for fact in data["facts"]:
                results.append({
                    "claim": fact["claim"],
                    "rating": fact["rating"],
                    "evidence": fact["explanation"],
                    "category": fact["category"],
                    "source": "snopes",
                    "url": fact["url"],
                    "date": fact["date_published"]
                })
            
            page += 1
            time.sleep(2)  # Rate limiting
            
        return results

    def collect_from_politifact(self) -> List[Dict]:
        """
        Collect fact-checks from PolitiFact using their API.
        Requires API key and follows usage guidelines.
        """
        endpoint = "https://api.politifact.com/v2/statements"
        results = []
        page = 1
        
        while True:
            params = {
                "key": self.api_keys["politifact"],
                "page": page,
                "per_page": 100
            }
            
            response = self.session.get(endpoint, params=params)
            data = response.json()
            
            if not data["statements"]:
                break
                
            for statement in data["statements"]:
                results.append({
                    "claim": statement["statement"],
                    "rating": statement["ruling"]["ruling"],
                    "evidence": statement["analysis"],
                    "category": statement["subject"],
                    "source": "politifact",
                    "url": statement["canonical_url"],
                    "date": statement["ruling_date"]
                })
            
            page += 1
            time.sleep(2)  # Rate limiting
            
        return results

    def standardize_ratings(self, data: List[Dict]) -> List[Dict]:
        """Standardize ratings across different sources to TRUE/FALSE/UNCLEAR."""
        rating_map = {
            # Snopes ratings
            "TRUE": "TRUE",
            "FALSE": "FALSE",
            "MIXTURE": "UNCLEAR",
            "UNPROVEN": "UNCLEAR",
            
            # PolitiFact ratings
            "True": "TRUE",
            "Mostly True": "TRUE",
            "False": "FALSE",
            "Mostly False": "FALSE",
            "Half True": "UNCLEAR",
            "Pants on Fire": "FALSE",
            
            # Other common ratings
            "Correct": "TRUE",
            "Incorrect": "FALSE",
            "Mixed": "UNCLEAR"
        }
        
        for item in data:
            original_rating = item["rating"]
            item["original_rating"] = original_rating
            item["rating"] = rating_map.get(original_rating, "UNCLEAR")
            
        return data

    def collect_and_save(self):
        """Collect data from all sources and save to files."""
        all_data = []
        
        # Collect from Google Fact Check API
        print("Collecting from Google Fact Check API...")
        factcheck_data = self.collect_from_factcheck_api(max_results=1000)
        all_data.extend(factcheck_data)
        
        # Collect from Snopes
        print("Collecting from Snopes...")
        snopes_data = self.collect_from_snopes()
        all_data.extend(snopes_data)
        
        # Collect from PolitiFact
        print("Collecting from PolitiFact...")
        politifact_data = self.collect_from_politifact()
        all_data.extend(politifact_data)
        
        # Standardize ratings
        all_data = self.standardize_ratings(all_data)
        
        # Save raw data
        with open(os.path.join(self.output_dir, "raw_data.json"), "w") as f:
            json.dump(all_data, f, indent=2)
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(all_data)
        
        # Save processed data
        df.to_csv(os.path.join(self.output_dir, "training_data.csv"), index=False)
        
        # Print statistics
        print("\nDataset Statistics:")
        print("-" * 50)
        print(f"Total examples: {len(df)}")
        print("\nLabel distribution:")
        print(df["rating"].value_counts())
        print("\nSource distribution:")
        print(df["source"].value_counts())
        
        return df

if __name__ == "__main__":
    # Load API keys from environment or config file
    api_keys = {
        "google": os.getenv("GOOGLE_FACTCHECK_API_KEY"),
        "snopes": os.getenv("SNOPES_API_KEY"),
        "politifact": os.getenv("POLITIFACT_API_KEY")
    }
    
    collector = DataCollector(api_keys)
    df = collector.collect_and_save()