from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import date

class LocalEvent(BaseModel):
    name: str
    date: date
    expected_attendance: int
    type: str
    location: str
    description: Optional[str] = None

class CantonDemographics(BaseModel):
    young_professionals: float
    families: float
    students: float
    tourists: float

class CantonInfo(BaseModel):
    name: str
    language: str
    population: int
    key_demographics: CantonDemographics

class MarketingRecommendationInput(BaseModel):
    events: List[LocalEvent]
    demographics: CantonInfo

class MarketingRecommendation(BaseModel):
    target_segments: List[str]
    channels: List[str]
    tactics: List[Dict[str, str]]
    budget_allocation: Dict[str, float]