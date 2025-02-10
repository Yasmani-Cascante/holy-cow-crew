from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

class ItemCategory(BaseModel):
    name: str
    description: str

class StorageCondition(BaseModel):
    type: str
    temperature_range: Optional[tuple[float, float]] = None

class BatchInfo(BaseModel):
    batch_id: str
    quantity: float
    expiry_date: Optional[datetime] = None

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

class InventoryLevel(BaseModel):
    item_id: str
    current_quantity: float
    reserved_quantity: float = 0
    available_quantity: float
    last_updated: datetime
    batch_info: Optional[List[BatchInfo]] = None

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

class LocationRecommendation(BaseModel):
    new_orders: Dict[str, OrderRecommendation]
    transfers_in: Dict[str, TransferOption]
    transfers_out: Dict[str, TransferOption]

class InventoryPrediction(BaseModel):
    predicted_demand: float
    confidence_range: tuple[float, float]
    trend_factor: float
    seasonality_factor: float