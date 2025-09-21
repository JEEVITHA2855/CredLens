"""
Process and prepare collected data for training the misinformation detection model.
"""
import os
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from datetime import datetime
from typing import Dict, List, Tuple
import re

class DataPreprocessor:
    def __init__(self, input_dir: str = "data", output_dir: str = "processed_data"):
        """Initialize data preprocessor."""
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        if not isinstance(text, str):
            return ""
            
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        
        # Remove special characters and extra whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()

    def encode_labels(self, df: pd.DataFrame) -> pd.DataFrame:
        """Encode categorical labels to numerical values."""
        label_map = {
            'TRUE': 1,
            'FALSE': 0,
            'UNCLEAR': 2
        }
        
        df['label'] = df['rating'].map(label_map)
        return df

    def balance_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        """Balance the dataset to handle class imbalance."""
        min_samples = df['label'].value_counts().min()
        
        balanced_data = []
        for label in df['label'].unique():
            samples = df[df['label'] == label].sample(n=min_samples, random_state=42)
            balanced_data.append(samples)
        
        return pd.concat(balanced_data, ignore_index=True)

    def extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extract additional features from the data."""
        # Add text length
        df['text_length'] = df['claim'].str.len()
        
        # Add word count
        df['word_count'] = df['claim'].str.split().str.len()
        
        # Add caps ratio
        df['caps_ratio'] = df['claim'].apply(lambda x: sum(1 for c in x if c.isupper()) / len(x) if len(x) > 0 else 0)
        
        # Add exclamation mark count
        df['exclamation_count'] = df['claim'].str.count('!')
        
        return df

    def prepare_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Prepare and split data for training."""
        # Load raw data
        with open(os.path.join(self.input_dir, "sample_claims.json"), 'r') as f:
            raw_data = json.load(f)
        df = pd.DataFrame(raw_data)
        
        # Clean text
        print("Cleaning text...")
        df['cleaned_claim'] = df['claim'].apply(self.clean_text)
        
        # Encode labels
        print("Encoding labels...")
        df = self.encode_labels(df)
        
        # Extract features
        print("Extracting features...")
        df = self.extract_features(df)
        
        # Balance dataset
        print("Balancing dataset...")
        df = self.balance_dataset(df)
        
        # Split into train/validation/test
        train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42)
        val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)
        
        # Save processed datasets
        train_df.to_csv(os.path.join(self.output_dir, "train.csv"), index=False)
        val_df.to_csv(os.path.join(self.output_dir, "validation.csv"), index=False)
        test_df.to_csv(os.path.join(self.output_dir, "test.csv"), index=False)
        
        # Save dataset statistics
        stats = {
            "total_samples": len(df),
            "train_samples": len(train_df),
            "validation_samples": len(val_df),
            "test_samples": len(test_df),
            "label_distribution": df['label'].value_counts().to_dict(),
            "feature_stats": df.describe().to_dict(),
            "timestamp": datetime.now().isoformat()
        }
        
        with open(os.path.join(self.output_dir, "dataset_stats.json"), "w") as f:
            json.dump(stats, f, indent=2)
        
        print("\nDataset Statistics:")
        print("-" * 50)
        print(f"Total samples: {len(df)}")
        print(f"Training samples: {len(train_df)}")
        print(f"Validation samples: {len(val_df)}")
        print(f"Test samples: {len(test_df)}")
        print("\nLabel distribution:")
        print(df['label'].value_counts())
        
        return train_df, val_df, test_df

if __name__ == "__main__":
    preprocessor = DataPreprocessor()
    train_df, val_df, test_df = preprocessor.prepare_data()