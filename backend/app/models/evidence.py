from pydantic import BaseModel
from typing import Optional

class FactCheck(BaseModel):
    id: int
    claim: str
    verdict: str  # "TRUE", "FALSE", "MIXED", "UNVERIFIED"
    explanation: str
    source: str
    source_url: Optional[str] = None
    date_published: Optional[str] = None
    embedding: Optional[list] = None