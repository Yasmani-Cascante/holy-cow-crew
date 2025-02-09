from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class LocalEvent(BaseModel):
    name: str = Field(..., description="Event name")
    date: str = Field(..., description="Event date")
    location: str = Field(..., description="Event location")
    expected_attendance: int = Field(..., description="Expected attendance")
    category: str = Field(..., description="Event category (sports, cultural, etc.)")

class CantonInfo(BaseModel):
    name: str = Field(..., description="Canton name")
    language: str = Field(..., description="Primary language")
    population: int = Field(..., description="Population")
    key_demographics: Dict[str, float] = Field(..., description="Demographics breakdown")

class MarketingRecommendation(BaseModel):
    target_location: str = Field(..., description="Target location/canton")
    campaign_type: str = Field(..., description="Type of marketing campaign")
    timing: str = Field(..., description="Recommended timing")
    target_audience: str = Field(..., description="Target audience")
    expected_impact: Dict[str, float] = Field(..., description="Expected impact metrics")