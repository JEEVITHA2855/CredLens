# 🚀 CredLens — AI-Powered Misinformation Detection System

**Verify. Understand. Share Responsibly.**

CredLens is an end-to-end AI system that detects, analyzes, and explains misinformation in text or URLs using modern NLP techniques. It combines **semantic retrieval**, **transformer-based reasoning**, and **credibility scoring** to provide **interpretable, real-time fact-checking assistance**.

---

##  Why CredLens?

Misinformation spreads faster than verification. CredLens addresses this by:

* Automatically extracting factual claims
* Retrieving relevant evidence using semantic search
* Verifying claims using Natural Language Inference (NLI)
* Generating **explainable credibility scores**
* Educating users through contextual micro-lessons

---

## ⚙️ Tech Stack

### 🔹 Backend

* **FastAPI** — High-performance API framework
* **SQLite** — Lightweight storage
* **FAISS** — Vector similarity search
* **Sentence Transformers** — Text embeddings
* **HuggingFace Transformers** — NLI model

### 🔹 Frontend

* **React (Hooks)**
* **Tailwind CSS**
* **Axios**

---

## 🏗️ System Architecture

```
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

## ✨ Key Features

### 🔍 Core AI Pipeline

* Claim extraction from raw text/URLs
* Semantic similarity search using embeddings
* Evidence validation using NLI (entailment/contradiction)

### 📊 Credibility Fingerprint

* Source reliability scoring
* Corroboration across sources
* Detection of emotional/sensational language
* Final weighted credibility score

### 📚 Educational Layer

* Micro-lessons for media literacy
* Suspicious phrase highlighting
* Step-by-step verification guidance

### 💻 User Experience

* Clean, responsive UI
* Interactive explanations
* Accessible design

---

##  Example

### Input:

```
"5G towers spread COVID-19"
```

### Output:

* ❌ Likely False
* 📊 Low credibility score
* 📚 Explanation + supporting evidence
* ⚠️ Highlighted suspicious language

---

## 🚀 Getting Started

### 🔧 Prerequisites

* Python 3.8+
* Node.js 16+

---

### ▶️ Backend Setup

```bash
cd CredLens/backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt

cd ..
python data/build_dataset.py

cd backend
python run.py
```

Backend runs at:
👉 http://localhost:8000

---

### ▶️ Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs at:
👉 http://localhost:3000

---

## 📡 API Overview

### POST `/analyze`

```json
{
  "text": "Claim to analyze",
  "url": "Optional URL"
}
```

### Response Includes:

* Extracted claim
* Verification status
* Credibility score
* Supporting evidence
* Explanation + micro-lesson

---

## ⚡ Engineering Highlights

* Designed a **multi-stage NLP pipeline** combining retrieval + reasoning
* Integrated **FAISS for efficient vector search**
* Used **transformer-based NLI models** for explainable verification
* Built scalable backend using **FastAPI**
* Implemented modular architecture for extensibility

---

## 📊 Dataset

* 50+ curated fact-check cases
* Multi-domain coverage (health, tech, politics, etc.)
* Designed for demonstration of all verification outcomes

---

## Testing

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

---

## ⚠️ Limitations

* Not a replacement for professional fact-checking
* Performance depends on dataset quality
* Limited real-time web validation

---

## Future Improvements

* Real-time web scraping for live verification
* Multilingual support
* Improved dataset scaling
* Model fine-tuning for domain-specific accuracy
* Deployment with scalable cloud infrastructure

---

## 📌 Resume Impact

> Built an AI-powered misinformation detection system using NLP, semantic retrieval (FAISS), and transformer-based NLI models, enabling explainable credibility scoring through a multi-stage verification pipeline.

---





## 💡 Final Note

CredLens is not just a tool — it’s an attempt to improve **digital literacy** using AI.

---
