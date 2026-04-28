# CredLens

CredLens is an AI-powered system for detecting and analyzing potential misinformation in text or URLs. It combines semantic retrieval, transformer-based reasoning, and credibility scoring to provide explainable verification results along with educational insights.

---

## Overview

CredLens is designed to help users evaluate the reliability of information by breaking down claims, retrieving relevant evidence, and assessing credibility using multiple signals. The system emphasizes explainability by not only providing a verdict but also showing the reasoning behind it.

---

## Problem Statement

Misinformation spreads rapidly across digital platforms, often without verification. Users lack accessible tools that can:

* Identify factual claims within content
* Retrieve supporting or contradicting evidence
* Explain why a claim may be reliable or misleading

---

## Solution

CredLens provides an end-to-end verification pipeline where:

* Claims are extracted from raw text or URLs
* Relevant evidence is retrieved using semantic similarity
* Claims are evaluated using Natural Language Inference (NLI)
* Credibility is scored based on multiple factors
* Users receive explanations and guidance for verification

---

## Key Features

* Automated claim extraction from text or URLs
* Semantic retrieval using vector similarity search
* Evidence validation using transformer-based NLI models
* Multi-factor credibility scoring system
* Detection of sensational or high-risk language
* Explainable outputs with supporting evidence
* Educational micro-lessons for media literacy

---

## Tech Stack

### Backend

* FastAPI
* SQLite
* FAISS (vector search)
* Sentence Transformers (embeddings)
* HuggingFace Transformers (NLI models)

### Frontend

* React
* Tailwind CSS
* Axios

---

## System Architecture

```text
User Input (Text / URL)
        ↓
Claim Extraction
        ↓
Semantic Retrieval (FAISS)
        ↓
NLI Verification (Transformer Model)
        ↓
Credibility Scoring Engine
        ↓
Explainable Output + Micro-lessons
```

---

## Example Workflow

* User submits a claim or URL
* System extracts the primary factual claim
* Relevant evidence is retrieved using embeddings
* NLI model evaluates support or contradiction
* Credibility score is calculated
* User receives a verdict with explanation and guidance

---

## API Overview

### POST `/analyze`

Request:

```json
{
  "text": "Claim to analyze",
  "url": "Optional URL"
}
```

Response includes:

* Extracted claim
* Verification status (True / False / Mixed / Unverified)
* Credibility score
* Supporting and contradicting evidence
* Explanation and educational tip

---

## Setup Instructions

### Prerequisites

* Python 3.8+
* Node.js 16+

---

### Backend Setup

```bash
cd CredLens/backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

cd ..
python data/build_dataset.py

cd backend
python run.py
```

---

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

---

## Dataset

The system uses a curated dataset of fact-checked claims across multiple domains, including:

* Health
* Technology
* Climate
* Politics
* Science

This dataset supports demonstration of different verification outcomes such as true, false, mixed, and unverified claims.

---

## Engineering Highlights

* Designed a multi-stage NLP pipeline combining retrieval and reasoning
* Implemented semantic search using FAISS for efficient similarity matching
* Integrated transformer-based NLI models for evidence validation
* Built modular backend architecture using FastAPI
* Developed explainable scoring system combining multiple credibility factors

---

## Challenges

* Designing an explainable pipeline instead of a black-box classifier
* Handling semantic similarity across diverse claim types
* Integrating retrieval and inference models efficiently
* Managing model performance and response latency

---

## Future Improvements

* Real-time web data integration for live fact-checking
* Multilingual support
* Improved dataset scaling and diversity
* Model fine-tuning for domain-specific accuracy
* Deployment with scalable infrastructure

---

## Resume Impact

Built an AI-powered misinformation detection system using NLP, semantic retrieval (FAISS), and transformer-based NLI models, enabling explainable credibility scoring through a multi-stage verification pipeline.

---

## Notes

* The system emphasizes explainability over black-box predictions
* Outputs include reasoning and supporting evidence, not just labels
* Designed for educational use in improving digital literacy

---
