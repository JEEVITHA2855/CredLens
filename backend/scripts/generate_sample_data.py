"""
Mock data generator for testing the misinformation detection system.
"""
import random
import json
from datetime import datetime, timedelta
from typing import List, Dict

def generate_sample_claims(num_samples: int = 1000) -> List[Dict]:
    """Generate sample claims for testing."""
    
    # Sample true claims
    true_claims = [
        "Water boils at 100 degrees Celsius at sea level",
        "The Earth orbits around the Sun",
        "Humans need oxygen to breathe",
        "DNA contains genetic information",
        "Mount Everest is the highest peak on Earth",
        "The human body has 206 bones",
        "Light travels faster than sound",
        "Plants produce oxygen through photosynthesis",
        "The Moon orbits around the Earth",
        "Diamonds are made of carbon"
    ]
    
    # Sample false claims
    false_claims = [
        "The Earth is flat",
        "Vaccines cause autism",
        "5G networks spread viruses",
        "The Moon landing was faked",
        "Humans only use 10% of their brains",
        "Climate change is a hoax",
        "Evolution is just a theory without evidence",
        "COVID-19 is no worse than the common cold",
        "All GMO foods are dangerous",
        "The Great Wall of China is visible from space"
    ]
    
    # Sample unclear claims
    unclear_claims = [
        "Coffee might help prevent certain diseases",
        "Some studies suggest meditation can reduce stress",
        "Economic growth may improve next year",
        "Remote work could increase productivity",
        "Artificial intelligence might replace some jobs",
        "Certain diets may help with weight loss",
        "Some experts predict market volatility",
        "New technology could revolutionize transportation",
        "Alternative energy sources might become dominant",
        "Social media may affect mental health"
    ]
    
    # Generate random dates within the last year
    def random_date():
        days = random.randint(1, 365)
        return (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    # Generate random sources
    sources = ["FactCheck.org", "Reuters", "AP News", "Science Daily", "WHO", "CDC", "Nature", "Scientific American"]
    
    # Generate dataset
    dataset = []
    for _ in range(num_samples):
        claim_type = random.choices(["true", "false", "unclear"], weights=[0.4, 0.4, 0.2])[0]
        
        if claim_type == "true":
            claim = random.choice(true_claims)
            rating = "TRUE"
        elif claim_type == "false":
            claim = random.choice(false_claims)
            rating = "FALSE"
        else:
            claim = random.choice(unclear_claims)
            rating = "UNCLEAR"
            
        dataset.append({
            "claim": claim,
            "rating": rating,
            "source": random.choice(sources),
            "date": random_date(),
            "evidence": f"Multiple sources {random.choice(['confirm', 'dispute', 'discuss'])} this claim.",
            "category": random.choice(["Science", "Health", "Technology", "Politics", "Environment"]),
            "url": f"https://example.com/fact-check/{random.randint(1000, 9999)}"
        })
    
    return dataset

if __name__ == "__main__":
    # Generate sample dataset
    dataset = generate_sample_claims(1000)
    
    # Save to file
    with open("data/sample_claims.json", "w") as f:
        json.dump(dataset, f, indent=2)
    
    print(f"Generated {len(dataset)} sample claims")
    
    # Print some statistics
    ratings = [item["rating"] for item in dataset]
    print("\nRating distribution:")
    for rating in set(ratings):
        count = ratings.count(rating)
        print(f"{rating}: {count} ({count/len(ratings)*100:.1f}%)")