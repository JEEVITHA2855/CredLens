# CredLens API Documentation

## Overview

The CredLens API provides AI-powered misinformation detection and educational insights. It analyzes text claims or article URLs to determine credibility and provide verification guidance.

## Base URL

```
http://localhost:8000
```

## Authentication

No authentication required for the current version.

## Endpoints

### Health Check

#### `GET /health`

Check if the API is operational.

**Response:**
```json
{
  "status": "success",
  "message": "API is healthy"
}
```

### System Statistics

#### `GET /stats`

Get information about the system's fact-check database and AI models.

**Response:**
```json
{
  "total_fact_checks": 50,
  "model_info": {
    "embedding_model": "all-MiniLM-L6-v2",
    "nli_model": "facebook/bart-large-mnli",
    "index_type": "FAISS"
  },
  "status": "operational"
}
```

### Analyze Claim

#### `POST /analyze`

Analyze a text claim or URL for misinformation and get educational insights.

**Request Body:**
```json
{
  "text": "string (optional)",
  "url": "string (optional)"
}
```

Either `text` or `url` must be provided, but not both.

**Examples:**

Text analysis:
```json
{
  "text": "Vaccines cause autism in children"
}
```

URL analysis:
```json
{
  "url": "https://example-news-site.com/article"
}
```

**Response:**
```json
{
  "original_input": "Full text that was analyzed",
  "extracted_claim": "Main factual claim extracted from input",
  "verification_status": "Likely True|Mixed|Likely False|Unverified",
  "credibility_fingerprint": {
    "source_credibility": 0.75,
    "corroboration_count": 3,
    "language_risk": 0.2,
    "overall_score": 0.8
  },
  "evidence": [
    {
      "text": "Evidence text from fact-check database",
      "source": "Source organization",
      "url": "https://source-url.com",
      "nli_label": "ENTAILMENT|NEUTRAL|CONTRADICTION",
      "confidence": 0.85,
      "similarity_score": 0.72
    }
  ],
  "suspicious_phrases": [
    {
      "phrase": "suspicious word",
      "start_pos": 10,
      "end_pos": 20,
      "reason": "Sensational/emotional language"
    }
  ],
  "micro_lesson": {
    "tip": "Always check the original source before sharing claims online.",
    "category": "source_verification"
  },
  "explanation": "Detailed explanation of the verification result"
}
```

### Rebuild Index (Admin)

#### `POST /rebuild-index`

Rebuild the FAISS search index from the current database.

**Response:**
```json
{
  "status": "success",
  "message": "Index rebuilt successfully"
}
```

## Data Models

### CredibilityFingerprint

| Field | Type | Description |
|-------|------|-------------|
| source_credibility | float (0-1) | Reliability of information sources |
| corroboration_count | integer | Number of corroborating sources |
| language_risk | float (0-1) | Risk score based on sensational language |
| overall_score | float (0-1) | Overall credibility score |

### Evidence

| Field | Type | Description |
|-------|------|-------------|
| text | string | Evidence text from fact-check |
| source | string | Source organization name |
| url | string | Optional source URL |
| nli_label | string | Relationship to claim (ENTAILMENT/NEUTRAL/CONTRADICTION) |
| confidence | float (0-1) | NLI model confidence |
| similarity_score | float (0-1) | Semantic similarity to claim |

### SuspiciousPhrase

| Field | Type | Description |
|-------|------|-------------|
| phrase | string | The suspicious text phrase |
| start_pos | integer | Starting character position |
| end_pos | integer | Ending character position |
| reason | string | Why this phrase is flagged |

### MicroLesson

| Field | Type | Description |
|-------|------|-------------|
| tip | string | Educational tip text |
| category | string | Lesson category (source_verification, language_analysis, etc.) |

## Verification Status

| Status | Description |
|--------|-------------|
| Likely True | Evidence largely supports the claim |
| Mixed | Evidence both supports and contradicts |
| Likely False | Evidence largely contradicts the claim |
| Unverified | Insufficient evidence to make determination |

## Error Handling

The API returns standard HTTP status codes:

- `200 OK` - Request successful
- `400 Bad Request` - Invalid input (missing text/URL, invalid URL format)
- `500 Internal Server Error` - Server error during processing

**Error Response Format:**
```json
{
  "detail": "Error description"
}
```

## Rate Limiting

Currently no rate limiting is enforced, but this may be added in production.

## Examples

### Analyzing a False Claim

**Request:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "5G networks spread coronavirus"}'
```

**Response:**
```json
{
  "verification_status": "Likely False",
  "credibility_fingerprint": {
    "overall_score": 0.15
  },
  "evidence": [
    {
      "nli_label": "CONTRADICTION",
      "confidence": 0.92,
      "text": "Viruses cannot spread through radio waves..."
    }
  ],
  "micro_lesson": {
    "tip": "Be skeptical of claims linking unrelated technologies to health issues",
    "category": "evidence_evaluation"
  }
}
```

### Analyzing a URL

**Request:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.cdc.gov/vaccines/facts/index.html"}'
```

The system will extract claims from the article and analyze them.

## Integration Guide

### Frontend Integration

```javascript
import axios from 'axios';

const analyzeClaimAPI = async (input) => {
  try {
    const response = await axios.post('http://localhost:8000/analyze', input);
    return response.data;
  } catch (error) {
    throw new Error(error.response.data.detail);
  }
};

// Usage
const result = await analyzeClaimAPI({ 
  text: "Climate change is not real" 
});
```

### Python Integration

```python
import requests

def analyze_claim(text=None, url=None):
    data = {}
    if text:
        data['text'] = text
    if url:
        data['url'] = url
    
    response = requests.post('http://localhost:8000/analyze', json=data)
    response.raise_for_status()
    return response.json()

# Usage
result = analyze_claim(text="Vaccines cause autism")
print(f"Status: {result['verification_status']}")
```

## Performance Notes

- Typical analysis time: 3-10 seconds
- First request may be slower due to model loading
- FAISS index provides fast similarity search
- Results are cached for identical inputs

## Development

### Running in Development Mode

```bash
cd backend
python run.py
```

The API will reload automatically when files change.

### API Documentation UI

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

### Testing

```bash
cd backend
python -m pytest tests/
```

## Changelog

### v1.0.0
- Initial release
- Basic claim analysis
- Credibility fingerprinting  
- Educational micro-lessons
- React frontend integration