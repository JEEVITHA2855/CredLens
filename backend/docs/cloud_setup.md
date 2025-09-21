# Google Cloud Project Setup Guide

1. Create a new project:
   ```bash
   gcloud projects create credlens-ai --name="CredLens AI"
   gcloud config set project credlens-ai
   ```

2. Enable required APIs:
   ```bash
   gcloud services enable aiplatform.googleapis.com
   gcloud services enable language.googleapis.com
   gcloud services enable storage.googleapis.com
   ```

3. Create a service account:
   ```bash
   gcloud iam service-accounts create credlens-service \
       --description="CredLens ML Service Account" \
       --display-name="CredLens ML"
   ```

4. Generate and download service account key:
   ```bash
   gcloud iam service-accounts keys create credentials.json \
       --iam-account=credlens-service@credlens-ai.iam.gserviceaccount.com
   ```

5. Grant necessary permissions:
   ```bash
   gcloud projects add-iam-policy-binding credlens-ai \
       --member="serviceAccount:credlens-service@credlens-ai.iam.gserviceaccount.com" \
       --role="roles/aiplatform.user"
   
   gcloud projects add-iam-policy-binding credlens-ai \
       --member="serviceAccount:credlens-service@credlens-ai.iam.gserviceaccount.com" \
       --role="roles/storage.objectViewer"
   ```

6. Create Cloud Storage bucket:
   ```bash
   gcloud storage buckets create gs://credlens-ml-data \
       --location=us-central1 \
       --uniform-bucket-level-access
   ```