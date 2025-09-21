"""
Script to collect and prepare training data from fact-checking sources.
"""
import pandas as pd
import requests
from typing import List, Dict
from datetime import datetime
import json

def collect_snopes_data() -> List[Dict]:
    """Collect fact-checked claims from Snopes API."""
    # This is a placeholder - you'll need to use the actual Snopes API
    # or implement web scraping with their terms of service
    pass

def collect_politifact_data() -> List[Dict]:
    """Collect fact-checked claims from PolitiFact API."""
    # This is a placeholder - you'll need to use the actual PolitiFact API
    # or implement web scraping with their terms of service
    pass

def prepare_training_data(output_file: str = "training_data.json"):
    """Collect and prepare training data from multiple sources."""
    
    # Initialize empty dataset
    dataset = []
    
    # Collect data from various sources
    sources = [
        ("snopes", collect_snopes_data()),
        ("politifact", collect_politifact_data()),
        # Add more sources as needed
    ]
    
    for source_name, source_data in sources:
        if source_data:
            for item in source_data:
                dataset.append({
                    "claim": item["claim"],
                    "label": item["rating"],
                    "source": source_name,
                    "verification_date": item["date"],
                    "evidence": item.get("evidence", ""),
                    "category": item.get("category", ""),
                    "urls": item.get("urls", [])
                })
    
    # Save the dataset
    with open(output_file, 'w') as f:
        json.dump(dataset, f, indent=2)
    
    print(f"Collected {len(dataset)} training examples")
    
    return dataset

def analyze_dataset(dataset: List[Dict]):
    """Analyze the collected dataset for quality and distribution."""
    df = pd.DataFrame(dataset)
    
    print("\nDataset Statistics:")
    print("-" * 50)
    print(f"Total examples: {len(df)}")
    print("\nLabel distribution:")
    print(df['label'].value_counts())
    print("\nSource distribution:")
    print(df['source'].value_counts())
    print("\nCategory distribution:")
    print(df['category'].value_counts())
    
    # Check for potential issues
    print("\nPotential issues:")
    print(f"Missing claims: {df['claim'].isnull().sum()}")
    print(f"Missing labels: {df['label'].isnull().sum()}")
    print(f"Missing evidence: {df['evidence'].isnull().sum()}")
    
    return df

if __name__ == "__main__":
    # Collect and prepare the dataset
    dataset = prepare_training_data()
    
    # Analyze the dataset
    df = analyze_dataset(dataset)
    
    print("\nSample claims:")
    print("-" * 50)
    for _, row in df.sample(5).iterrows():
        print(f"\nClaim: {row['claim']}")
        print(f"Label: {row['label']}")
        print(f"Source: {row['source']}")
        print("-" * 30)