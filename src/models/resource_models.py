from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

class StaffRecommendation(BaseModel):
    shift: str
    staff_count: int
    roles: Dict[str, int]

class InventoryOrder(BaseModel):
    item: str
    quantity: float
    priority: str

class ResourceOptimizationInput(BaseModel):
    predicted_sales: float = Field(..., description="Predicted sales value")
    current_staff: int = Field(..., description="Current staff count")
    inventory_levels: Dict[str, float] = Field(..., description="Current inventory levels")
    peak_hours: List[str] = Field(default_factory=list, description="Peak hours list")
    day_of_week: str = Field(..., description="Current day of week")

class OptimizationResult(BaseModel):
    recommended_staff: List[StaffRecommendation]
    inventory_orders: List[InventoryOrder]
    efficiency_score: float
    cost_savings: float
    alerts: List[str] = []