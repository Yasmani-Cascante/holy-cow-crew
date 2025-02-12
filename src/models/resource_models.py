from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Optional, Any
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
    predicted_sales: float = 0.0
    current_staff: int = 0
    inventory_levels: Dict[str, float] = {}
    peak_hours: List[str] = []
    day_of_week: str = "Monday"

class OptimizationResult(BaseModel):
    recommended_staff: List[StaffRecommendation]
    inventory_orders: List[InventoryOrder]
    efficiency_score: float
    cost_savings: float
    alerts: List[str] = []

class InventoryPredictionInput(BaseModel):
    predicted_demand: float
    confidence_range: tuple[float, float]
    trend_factor: float
    seasonality_factor: float

class InventoryItemConfig(BaseModel):
    id: str
    name: str
    category: str
    storage_type: str
    unit: str
    min_level: float
    max_level: float
    reorder_point: float
    lead_time_days: int
    cost_per_unit: float
    supplier_id: str

class MultiLocationInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    locations_inventory: Dict[str, Dict[str, float]]
    demand_predictions: Dict[str, Dict[str, InventoryPredictionInput]]
    items: Dict[str, InventoryItemConfig]