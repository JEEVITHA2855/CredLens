"""
Ultra-Simple CredLens Backend
Uses only Gemini AI for fact-checking, no complex dependencies
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import List, Dict, Any, Optional

# Optional imports for URL extraction and HTTP calls
try:
    import requests  # type: ignore
except Exception:  # pragma: no cover
    requests = None
try:
    from bs4 import BeautifulSoup  # type: ignore
except Exception:  # pragma: no cover
    BeautifulSoup = None

# Optional imports for Vertex AI Gemini
try:
    from vertexai import init as vertex_init  # type: ignore
    try:
        # Prefer stable path if available
        from vertexai.generative_models import GenerativeModel as VertexGenerativeModel  # type: ignore
    except Exception:
        from vertexai.preview.generative_models import GenerativeModel as VertexGenerativeModel  # type: ignore
    VERTEX_AVAILABLE = True
except Exception:  # pragma: no cover
    VERTEX_AVAILABLE = False

# Load environment variables
load_dotenv()

app = FastAPI(
    title="CredLens API",
    description="AI-powered fact-checking with Gemini",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000", 
        "http://localhost:3001", 
        "http://127.0.0.1:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple models
class ClaimInput(BaseModel):
    text: str = None
    url: str = None

class HealthResponse(BaseModel):
    status: str
    message: str

class AnalysisResponse(BaseModel):
    claim_text: str
    status: str
    confidence_score: float
    explanation: str
    evidence: list
    metadata: dict
    # Added fields to enrich the UI
    suspicious_phrases: List[dict] = []
    micro_lesson: Optional[dict] = None
    credibility_fingerprint: Optional[Dict[str, float]] = None
    # New: concise detective-style reasons (max ~3)
    reasons: List[str] = []

@app.get("/", response_model=HealthResponse)
async def root():
    return HealthResponse(status="success", message="CredLens API is running!")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="success", message="API is healthy")

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_claim(claim_input: ClaimInput):
    """Analyze a claim using Gemini AI"""
    try:
        # Validate input
        if not claim_input.text and not claim_input.url:
            raise HTTPException(status_code=400, detail="Either text or URL must be provided")
        
        # If URL provided, try to fetch content (best-effort)
        text_to_analyze = claim_input.text
        page_meta: Dict[str, Any] = {}
        input_type = "text"
        if not text_to_analyze and claim_input.url:
            input_type = "url"
            text_to_analyze = claim_input.url
            fetched = _try_fetch_url_text(claim_input.url)
            if fetched and isinstance(fetched, dict):
                page_meta = fetched.get("meta", {})
                content = fetched.get("content") or ""
                text_to_analyze = f"URL: {claim_input.url}\n\nContent Summary:\n{content[:2000]}"
            elif isinstance(fetched, str):
                # backward compatibility if any
                text_to_analyze = f"URL: {claim_input.url}\n\nContent Summary:\n{fetched[:2000]}"
        else:
            input_type = "text"
        print(f"🔍 Analyzing: {text_to_analyze[:100]}...")
        
        # Pre-analysis: detect suspicious language for education
        suspicious = _detect_suspicious_language(text_to_analyze)
        micro_lesson = _micro_lesson_from_suspicion(suspicious)

    # Optional: query Google Fact Check Tools API for quick corroboration
        factcheck_evidence = _query_google_factcheck(text_to_analyze)

        # Use Gemini AI (Vertex AI when configured, otherwise google-generativeai)
        try:
            prompt = f"""You are a professional fact-checker. Analyze this claim: "{text_to_analyze}"

Provide analysis in JSON format:
{{
    "verdict": "TRUE" | "FALSE" | "UNCERTAIN",
    "confidence": <number between 0-100>,
    "explanation": "<detailed reasoning with evidence>",
    "sources": ["<reliable source 1>", "<reliable source 2>"],
    "key_evidence": ["<key fact 1>", "<key fact 2>"]
}}

Be thorough and cite reliable sources. Consider current information."""

            use_vertex_env = os.getenv('USE_VERTEX_AI', 'false').lower() in ['1', 'true', 'yes']
            response_text = None

            if use_vertex_env and VERTEX_AVAILABLE and os.getenv('GCP_PROJECT') and os.getenv('GCP_LOCATION'):
                # Vertex AI path
                try:
                    response_text = _generate_with_vertex(prompt)
                    provider = 'vertex'
                except Exception as ve:
                    print(f"⚠️ Vertex AI generation failed, falling back: {ve}")
                    response_text = None
            else:
                provider = 'generativeai'

            if response_text is None:
                # Fallback to google-generativeai
                response_text = _generate_with_generativeai(prompt)
                provider = 'generativeai'

            if not response_text:
                raise Exception('No response from Gemini provider')

            print(f"🔍 Raw Gemini response: {response_text[:200]}...")
            
            # Try to extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end != 0:
                json_text = response_text[json_start:json_end]
                try:
                    result = json.loads(json_text)
                    print(f"✅ Parsed JSON successfully: {result.get('verdict', 'Unknown')}")
                    
                    # Format response
                    status_map = {
                        'TRUE': 'VERIFIED',
                        'FALSE': 'DEBUNKED', 
                        'UNCERTAIN': 'UNCERTAIN'
                    }
                    
                    # Compose concise reasons
                    reasons = _compose_reasons(
                        status=status_map.get(result.get('verdict', 'UNCERTAIN'), 'UNCERTAIN'),
                        suspicious=suspicious,
                        factcheck=factcheck_evidence,
                        page_meta=page_meta,
                        claim_input=claim_input
                    )

                    formatted_result = AnalysisResponse(
                        claim_text=text_to_analyze,
                        status=status_map.get(result.get('verdict', 'UNCERTAIN'), 'UNCERTAIN'),
                        confidence_score=result.get('confidence', 50) / 100.0,
                        explanation=result.get('explanation', 'Analysis completed using Gemini AI'),
                        evidence=(factcheck_evidence or []) + result.get('sources', []) + result.get('key_evidence', []),
                        metadata={
                            "analysis_method": "gemini_ai",
                            "model": "gemini-1.5-flash",
                            "provider": provider,
                            "raw_verdict": result.get('verdict', 'UNCERTAIN'),
                            "timestamp": datetime.utcnow().isoformat() + "Z",
                            "input_type": input_type,
                            "source_domain": page_meta.get("domain"),
                            "has_author": page_meta.get("has_author"),
                            "has_date": page_meta.get("has_date"),
                            "published": page_meta.get("published"),
                            "author": page_meta.get("author"),
                        },
                        suspicious_phrases=suspicious,
                        micro_lesson=micro_lesson,
                        credibility_fingerprint=_build_fingerprint(result, suspicious, factcheck_evidence),
                        reasons=reasons
                    )
                    
                    print(f"✅ Analysis complete: {formatted_result.status} ({formatted_result.confidence_score:.1%})")
                    return formatted_result
                    
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON parse failed: {e}")
                    print(f"⚠️ Attempted to parse: {json_text}")
                    # Fallback to text-based parsing
            
            # Fallback: Simple text-based analysis
            print("🔄 Using fallback text analysis...")
            if "false" in response_text.lower() or "incorrect" in response_text.lower() or "not true" in response_text.lower():
                status = "DEBUNKED"
                confidence = 0.7
            elif "true" in response_text.lower() or "correct" in response_text.lower() or "accurate" in response_text.lower():
                status = "VERIFIED"
                confidence = 0.7
            else:
                status = "UNCERTAIN"
                confidence = 0.5
            
            # Compose concise reasons for fallback
            reasons = _compose_reasons(
                status=status,
                suspicious=suspicious,
                factcheck=factcheck_evidence,
                page_meta=page_meta,
                claim_input=claim_input
            )

            fallback_result = AnalysisResponse(
                claim_text=text_to_analyze,
                status=status,
                confidence_score=confidence,
                explanation=response_text[:500] + "..." if len(response_text) > 500 else response_text,
                evidence=(factcheck_evidence or []) + ["Based on AI analysis"],
                metadata={
                    "analysis_method": "gemini_ai_fallback",
                    "model": "gemini-1.5-flash",
                    "provider": provider,
                    "note": "JSON parsing failed, used text analysis",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "input_type": input_type,
                    "source_domain": page_meta.get("domain"),
                    "has_author": page_meta.get("has_author"),
                    "has_date": page_meta.get("has_date"),
                    "published": page_meta.get("published"),
                    "author": page_meta.get("author"),
                },
                suspicious_phrases=suspicious,
                micro_lesson=micro_lesson,
                credibility_fingerprint=_build_fingerprint({}, suspicious, factcheck_evidence, confidence),
                reasons=reasons
            )
            
            print(f"✅ Fallback analysis: {status} ({confidence:.1%})")
            return fallback_result
                
        except Exception as e:
            print(f"⚠️ Gemini API error: {e}")
            # Ultimate fallback
            reasons = _compose_reasons(
                status="UNCERTAIN",
                suspicious=suspicious,
                factcheck=factcheck_evidence,
                page_meta=page_meta,
                claim_input=claim_input
            )

            fallback_result = AnalysisResponse(
                claim_text=text_to_analyze,
                status="UNCERTAIN",
                confidence_score=0.3,
                explanation=f"Unable to analyze claim due to API error: {str(e)[:200]}",
                evidence=(factcheck_evidence or []) + ["API error occurred"],
                metadata={
                    "analysis_method": "error_fallback",
                    "error": str(e)[:100],
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "input_type": input_type,
                    "source_domain": page_meta.get("domain"),
                    "has_author": page_meta.get("has_author"),
                    "has_date": page_meta.get("has_date"),
                    "published": page_meta.get("published"),
                    "author": page_meta.get("author"),
                },
                suspicious_phrases=suspicious,
                micro_lesson=micro_lesson,
                credibility_fingerprint=_build_fingerprint({}, suspicious, factcheck_evidence, 0.3),
                reasons=reasons
            )
            return fallback_result
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def stats():
    """Basic service stats for the frontend dashboard"""
    use_vertex_env = os.getenv('USE_VERTEX_AI', 'false').lower() in ['1', 'true', 'yes']
    project = os.getenv('GCP_PROJECT')
    location = os.getenv('GCP_LOCATION')
    vertex_ready = bool(use_vertex_env and VERTEX_AVAILABLE and project and location)
    return {
        "service": "ultra-simple",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "gemini": True,
        "google_factcheck": bool(os.getenv("GOOGLE_FACTCHECK_API_KEY")),
        "vertex_ai": vertex_ready,
        "gemini_provider": "vertex" if vertex_ready else "generativeai",
        "project": project if vertex_ready else None,
        "location": location if vertex_ready else None,
    }


# ------------------------- Utilities -------------------------

SUSPICIOUS_TERMS = [
    # Sensational/misleading
    "shocking", "secret", "you won't believe", "exposed", "guaranteed", "miracle",
    # Urgency/pressure
    "urgent", "act now", "limited time", "last chance", "immediately",
    # Scams common in India
    "kyc update", "lottery", "prize", "otp", "bank verification", "pan update", "aadhaar"
]

def _detect_suspicious_language(text: str) -> List[dict]:
    found: List[dict] = []
    tl = text.lower()
    for term in SUSPICIOUS_TERMS:
        pos = tl.find(term)
        if pos != -1:
            found.append({
                "phrase": term,
                "start_pos": pos,
                "end_pos": pos + len(term),
                "reason": _reason_for_term(term)
            })
    return found

def _reason_for_term(term: str) -> str:
    if term in ["shocking", "secret", "you won't believe", "exposed", "guaranteed", "miracle"]:
        return "Sensational language can be used to manipulate emotions and bypass critical thinking"
    if term in ["urgent", "act now", "limited time", "last chance", "immediately"]:
        return "Urgency pressure is a common tactic to reduce scrutiny—verify before acting"
    return "Common term in online scams—verify the sender and use official channels"

def _micro_lesson_from_suspicion(suspicious: List[dict]) -> dict:
    if not suspicious:
        return {"tip": "Cross-check with at least two reputable sources (e.g., PIB, WHO, or official .gov.in sites)", "category": "cross_referencing"}
    if any("kyc" in s["phrase"] or "otp" in s["phrase"] for s in suspicious):
        return {"tip": "Banks never ask for OTP or KYC via links in messages. Use the official website/app.", "category": "bias_awareness"}
    if any(s["phrase"] in ["urgent", "act now", "limited time", "last chance", "immediately"] for s in suspicious):
        return {"tip": "Beware of urgency. Pause and verify on official sources before sharing or clicking.", "category": "language_analysis"}
    return {"tip": "Be cautious of sensational keywords. Look for neutral, fact-based reporting.", "category": "language_analysis"}

def _try_fetch_url_text(url: str) -> Optional[dict]:
    if not requests:
        return None
    try:
        headers = {"User-Agent": "Mozilla/5.0 (CredLens)"}
        resp = requests.get(url, headers=headers, timeout=8)
        if resp.status_code != 200:
            return None
        html = resp.text
        meta: Dict[str, Any] = {"domain": _extract_domain(url)}
        if BeautifulSoup:
            soup = BeautifulSoup(html, 'html.parser')
            # Remove script/style
            for tag in soup(["script", "style", "noscript"]):
                tag.extract()
            # Title + meta description + first paragraphs
            parts = []
            if soup.title and soup.title.string:
                parts.append(soup.title.string.strip())
            desc = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
            if desc and desc.get("content"):
                parts.append(desc.get("content").strip())
            paras = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
            if paras:
                parts.extend(paras[:10])
            content = "\n\n".join([p for p in parts if p])
            # Extract simple metadata: author and publication date
            author = None
            author_meta = soup.find("meta", attrs={"name": "author"}) or soup.find("meta", attrs={"property": "article:author"})
            if author_meta and author_meta.get("content"):
                author = author_meta.get("content").strip()
            if not author:
                byline = soup.find(attrs={"class": lambda x: x and ("author" in x or "byline" in x)})
                if byline:
                    author = byline.get_text(" ", strip=True)[:120]

            published = None
            time_tag = soup.find("time")
            if time_tag:
                published = time_tag.get("datetime") or time_tag.get_text(" ", strip=True)
            if not published:
                pub_meta = soup.find("meta", attrs={"property": "article:published_time"}) or soup.find("meta", attrs={"name": "date"})
                if pub_meta and pub_meta.get("content"):
                    published = pub_meta.get("content").strip()

            meta.update({
                "has_author": bool(author),
                "author": author,
                "has_date": bool(published),
                "published": published,
            })
            return {"content": content, "meta": meta}
        # Fallback: crude text
        return {"content": html[:2000], "meta": meta}
    except Exception:
        return None

def _query_google_factcheck(query: str) -> Optional[List[str]]:
    api_key = os.getenv("GOOGLE_FACTCHECK_API_KEY")
    if not api_key or not requests:
        return None
    try:
        params = {
            "key": api_key,
            "query": query[:512],
            "languageCode": "en-IN"
        }
        url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
        r = requests.get(url, params=params, timeout=6)
        if r.status_code != 200:
            return None
        data = r.json()
        out: List[str] = []
        for c in data.get("claims", [])[:5]:
            for review in c.get("claimReview", [])[:1]:
                site = review.get("publisher", {}).get("name", "Fact Check")
                link = review.get("url")
                rating = review.get("textualRating")
                if link:
                    label = f"{site}: {rating or 'Reviewed'}"
                    out.append(link)
                    out.append(label)
        return out or None
    except Exception:
        return None

def _build_fingerprint(result_json: Dict[str, Any], suspicious: List[dict], factcheck: Optional[List[str]], fallback_conf: Optional[float] = None) -> Dict[str, float]:
    # Confidence from result_json if present (0..100) else fallback_conf (0..1)
    if "confidence" in result_json:
        overall = max(0.0, min(1.0, float(result_json.get("confidence", 50)) / 100.0))
    else:
        overall = float(fallback_conf) if isinstance(fallback_conf, (int, float)) else 0.5
        overall = max(0.0, min(1.0, overall))
    corroboration_count = 0
    if factcheck:
        # Roughly half of the list may be labels; count urls
        corroboration_count = sum(1 for x in factcheck if isinstance(x, str) and x.startswith("http"))
    language_risk = max(0.0, min(1.0, 0.2 + 0.15 * len(suspicious)))
    source_cred = min(1.0, 0.5 + 0.1 * corroboration_count)
    return {
        "overall_score": overall,
        "source_credibility": source_cred,
        "language_risk": language_risk,
        "corroboration_count": float(corroboration_count),
    }


def _extract_domain(url: str) -> Optional[str]:
    try:
        from urllib.parse import urlparse
        return urlparse(url).hostname
    except Exception:
        return None


def _compose_reasons(status: str, suspicious: List[dict], factcheck: Optional[List[str]], page_meta: Dict[str, Any], claim_input: ClaimInput) -> List[str]:
    """Compose up to 3 short reasons tailored to the verdict.
    Prioritize missing author/date, language issues, and presence/absence of corroboration.
    """
    reasons: List[str] = []

    # 1) Source hygiene
    if page_meta:
        if not page_meta.get("has_author"):
            reasons.append("This source has no clear author attribution.")
        if not page_meta.get("has_date"):
            reasons.append("No publication date is visible.")
        if page_meta.get("domain"):
            dom = page_meta.get("domain")
            if dom.endswith(".gov") or "who.int" in dom or "un.org" in dom:
                reasons.append("Cited from an official or authoritative domain.")

    # 2) Language cues
    if suspicious:
        phrases = ", ".join([s.get("phrase", "") for s in suspicious[:2] if s.get("phrase")])
        reasons.append(f"Language uses emotional or clickbait terms ({phrases}).")

    # 3) Corroboration
    if factcheck and any(isinstance(x, str) and x.startswith("http") for x in factcheck):
        reasons.append("Independent fact-checks and sources are available.")
    else:
        reasons.append("Limited corroboration found; verify with additional sources.")

    # Trim to top 3 and ensure uniqueness
    out = []
    for r in reasons:
        if r and r not in out:
            out.append(r)
        if len(out) >= 3:
            break
    return out


# ------------------------- Providers -------------------------

def _generate_with_vertex(prompt: str) -> str:
    project = os.getenv('GCP_PROJECT')
    location = os.getenv('GCP_LOCATION', 'us-central1')
    if not (project and location):
        raise RuntimeError('Missing GCP_PROJECT or GCP_LOCATION for Vertex AI')
    vertex_init(project=project, location=location)
    model_name = os.getenv('VERTEX_GEMINI_MODEL', 'gemini-1.5-flash')
    model = VertexGenerativeModel(model_name)
    resp = model.generate_content(prompt)
    try:
        text = getattr(resp, 'text', None)
        if text:
            return text
        # Fallback extraction
        if hasattr(resp, 'candidates') and resp.candidates:
            parts = getattr(resp.candidates[0], 'content', None)
            if parts and hasattr(parts, 'parts'):
                return "\n".join([getattr(p, 'text', '') for p in parts.parts if getattr(p, 'text', '')])
    except Exception:
        pass
    raise RuntimeError('Vertex AI returned no text')


def _generate_with_generativeai(prompt: str) -> str:
    import google.generativeai as genai  # type: ignore
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise RuntimeError('GEMINI_API_KEY not found in environment')
    genai.configure(api_key=api_key)
    model_name = os.getenv('GENAI_GEMINI_MODEL', 'gemini-1.5-flash')
    model = genai.GenerativeModel(model_name)
    resp = model.generate_content(prompt)
    text = getattr(resp, 'text', None)
    if not text:
        raise RuntimeError('Generative AI returned no text')
    return text

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting CredLens Ultra-Simple Backend...")
    print("🔑 Using Gemini AI for fact-checking")
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, log_level="info")
    except KeyboardInterrupt:
        print("👋 Server shutting down...")
    except Exception as e:
        print(f"❌ Server error: {e}")