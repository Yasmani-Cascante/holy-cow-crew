from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime

class BatchInfo(BaseModel):
    batch_id: str
    quantity: float
    expiry_date: Optional[datetime] = None

class InventoryLevel(BaseModel):
    item_id: str
    current_quantity: float
    available_quantity: float
    reserved_quantity: float = Field(default=0)
    last_updated: datetime = Field(default_factory=datetime.now)
    batch_info: Optional[List[BatchInfo]] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class InventoryItem(BaseModel):
    id: str
    name: str
    category: str
    storage: str
    unit: str
    min_level: float
    max_level: float
    reorder_point: float
    lead_time_days: int
    shelf_life_days: Optional[int] = None
    cost_per_unit: float
    supplier_id: str
    last_order_date: Optional[datetime] = None
    average_daily_usage: Optional[float] = None

class OrderRecommendation(BaseModel):
    item_id: str
    quantity: float
    priority: str
    reason: str
    estimated_cost: float
    suggested_order_date: datetime

class TransferOption(BaseModel):
    from_location: str
    quantity: float
    transport_cost: float
    total_cost: float
    available_immediately: bool

class InventoryPrediction(BaseModel):
    predicted_demand: float
    confidence_range: tuple[float, float]
    trend_factor: float
    seasonality_factor: float

class LocationRecommendation(BaseModel):
    new_orders: Dict[str, OrderRecommendation]
    transfers_in: Dict[str, TransferOption]
    transfers_out: Dict[str, TransferOption]

class MultiLocationInput(BaseModel):
    locations_inventory: Dict[str, Dict[str, InventoryLevel]]
    demand_predictions: Dict[str, Dict[str, InventoryPrediction]]
    items: Dict[str, InventoryItem]