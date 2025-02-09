from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class SalesPrediction(BaseModel):
    """Base model for sales predictions"""
    timestamp: datetime = Field(..., description="Prediction timestamp")
    predicted_value: float = Field(..., description="Predicted sales value")
    confidence_interval: tuple[float, float] = Field(..., description="Confidence interval (lower, upper)")
    model_version: str = Field(..., description="Version of the prediction model")
    features_used: List[str] = Field(..., description="List of features used in prediction")

class PredictionMetrics(BaseModel):
    """Model for prediction accuracy metrics"""
    mae: float = Field(..., description="Mean Absolute Error")
    mape: float = Field(..., description="Mean Absolute Percentage Error")
    accuracy: float = Field(..., description="Model accuracy score")
    evaluation_period: str = Field(..., description="Period of evaluation")

class RestaurantContext(BaseModel):
    """Model for restaurant-specific context"""
    location_id: str = Field(..., description="Unique identifier for restaurant location")
    store_type: str = Field(..., description="Type of restaurant location")
    operating_hours: Dict[str, tuple[str, str]] = Field(..., description="Operating hours by day")
    capacity: int = Field(..., description="Restaurant seating capacity")
    local_events: Optional[List[Dict]] = Field(default=None, description="Upcoming local events")

class SalesAnalysis(BaseModel):
    """Complete sales analysis model"""
    prediction: SalesPrediction
    metrics: PredictionMetrics
    context: RestaurantContext
    recommendations: Optional[List[str]] = Field(default=None, description="System recommendations")
    alerts: Optional[List[Dict]] = Field(default=None, description="System alerts")