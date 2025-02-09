from langchain.tools import StructuredTool
from typing import Dict, List, Any
from datetime import datetime
import numpy as np
from pydantic import BaseModel, Field

    # Entrada de Predicciones
class PredictionAnalysisInput(BaseModel):
    predicted_value: float = Field(..., description="Predicted sales value")
    confidence_interval: tuple[float, float] = Field(..., description="Confidence interval (lower, upper)")
    capacity: int = Field(..., description="Restaurant capacity")

class MetricsCalculationInput(BaseModel):
    predicted: List[float] = Field(..., description="List of predicted values")
    actual: List[float] = Field(..., description="List of actual values")

class PredictionTools:
    def analyze_prediction(self, data: PredictionAnalysisInput) -> Dict[str, Any]:
        predicted = data.predicted_value
        interval = data.confidence_interval
        capacity = data.capacity
        
        # Calculate metrics
        uncertainty_level = (interval[1] - interval[0]) / predicted
        utilization = (predicted / (capacity * 20)) * 100
        
        insights = []
        if uncertainty_level > 0.2:
            insights.append("Alta incertidumbre en la predicción")
        if utilization > 90:
            insights.append("Alta utilización - considerar aumentar capacidad")
        elif utilization < 40:
            insights.append("Baja utilización - optimizar recursos")
            
        return {
            "uncertainty_level": uncertainty_level,
            "capacity_utilization": utilization,
            "insights": insights,
            "timestamp": datetime.now().isoformat()
        }

    def calculate_metrics(self, data: MetricsCalculationInput) -> Dict[str, Any]:
        if not data.predicted or not data.actual:
            raise ValueError("Lists cannot be empty")
            
        pred = np.array(data.predicted)
        act = np.array(data.actual)
        
        mae = np.mean(np.abs(pred - act))
        mape = np.mean(np.abs((act - pred) / act)) * 100
        
        return {
            "mae": float(mae),
            "mape": float(mape),
            "accuracy": float(100 - mape),
            "sample_size": len(data.predicted)
        }

    def get_tools(self) -> List[StructuredTool]:
        return [
            StructuredTool.from_function(
                func=self.analyze_prediction,
                name="analyze_prediction",
                description="Analyze sales prediction data",
                args_schema=PredictionAnalysisInput
            ),
            StructuredTool.from_function(
                func=self.calculate_metrics,
                name="calculate_metrics",
                description="Calculate prediction metrics",
                args_schema=MetricsCalculationInput
            )
        ]