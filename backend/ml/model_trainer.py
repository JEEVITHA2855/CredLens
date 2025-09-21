import joblib
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from google.cloud import storage
import os

class MisinformationModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words='english'
        )
        self.classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            n_jobs=-1,
            random_state=42
        )
        
    def preprocess_text(self, texts):
        """Preprocess text data for model input."""
        # Convert to string and handle missing values
        texts = texts.astype(str).fillna('')
        # Convert to lowercase
        texts = texts.str.lower()
        return texts
        
    def train(self, X_train, y_train):
        """Train the model with the provided training data."""
        # Preprocess the text data
        X_train_processed = self.preprocess_text(X_train)
        
        # Transform text data to TF-IDF features
        X_train_tfidf = self.vectorizer.fit_transform(X_train_processed)
        
        # Train the classifier
        self.classifier.fit(X_train_tfidf, y_train)
        
    def predict(self, texts):
        """Make predictions on new text data."""
        # Preprocess the input texts
        processed_texts = self.preprocess_text(pd.Series(texts))
        
        # Transform texts using the fitted vectorizer
        X_tfidf = self.vectorizer.transform(processed_texts)
        
        # Make predictions
        predictions = self.classifier.predict(X_tfidf)
        probabilities = self.classifier.predict_proba(X_tfidf)
        
        return predictions, probabilities

    def evaluate(self, X_test, y_test):
        """Evaluate the model on test data."""
        # Preprocess and transform test data
        X_test_processed = self.preprocess_text(X_test)
        X_test_tfidf = self.vectorizer.transform(X_test_processed)
        
        # Make predictions
        predictions = self.classifier.predict(X_test_tfidf)
        
        # Generate and print classification report
        report = classification_report(y_test, predictions)
        print("Model Evaluation Report:")
        print(report)
        
        return report

    def save_model(self, bucket_name, model_path):
        """Save the model and vectorizer to Google Cloud Storage."""
        # Initialize storage client
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        
        # Save model and vectorizer locally first
        local_model_path = "temp_model.joblib"
        local_vectorizer_path = "temp_vectorizer.joblib"
        
        joblib.dump(self.classifier, local_model_path)
        joblib.dump(self.vectorizer, local_vectorizer_path)
        
        # Upload to GCS
        model_blob = bucket.blob(f"{model_path}/model.joblib")
        vectorizer_blob = bucket.blob(f"{model_path}/vectorizer.joblib")
        
        model_blob.upload_from_filename(local_model_path)
        vectorizer_blob.upload_from_filename(local_vectorizer_path)
        
        # Clean up local files
        os.remove(local_model_path)
        os.remove(local_vectorizer_path)
        
    @classmethod
    def load_model(cls, bucket_name, model_path):
        """Load a saved model from Google Cloud Storage."""
        model = cls()
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        
        # Download model and vectorizer
        model_blob = bucket.blob(f"{model_path}/model.joblib")
        vectorizer_blob = bucket.blob(f"{model_path}/vectorizer.joblib")
        
        local_model_path = "temp_model.joblib"
        local_vectorizer_path = "temp_vectorizer.joblib"
        
        model_blob.download_to_filename(local_model_path)
        vectorizer_blob.download_to_filename(local_vectorizer_path)
        
        # Load the model and vectorizer
        model.classifier = joblib.load(local_model_path)
        model.vectorizer = joblib.load(local_vectorizer_path)
        
        # Clean up local files
        os.remove(local_model_path)
        os.remove(local_vectorizer_path)
        
        return model

def train_and_evaluate_model(training_data_path):
    """Train and evaluate the model using the provided training data."""
    # Load and prepare the data
    data = pd.read_csv(training_data_path)
    X = data['text']  # Assuming 'text' is the column containing the article text
    y = data['label']  # Assuming 'label' is the column containing the labels
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Initialize and train the model
    model = MisinformationModel()
    model.train(X_train, y_train)
    
    # Evaluate the model
    evaluation_report = model.evaluate(X_test, y_test)
    
    return model, evaluation_report

if __name__ == "__main__":
    # Example usage
    training_data_path = "path/to/your/training_data.csv"
    bucket_name = "your-model-bucket"
    model_path = "models/misinformation_detector"
    
    # Train and evaluate the model
    model, evaluation_report = train_and_evaluate_model(training_data_path)
    
    # Save the model to Google Cloud Storage
    model.save_model(bucket_name, model_path)
    
    # Load the model (example)
    loaded_model = MisinformationModel.load_model(bucket_name, model_path)
    
    # Make predictions (example)
    sample_texts = ["Sample article text to classify"]
    predictions, probabilities = loaded_model.predict(sample_texts)
    print(f"Predictions: {predictions}")
    print(f"Probabilities: {probabilities}")