import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict
from langchain.tools import StructuredTool
from ..models.inventory_models import (
    InventoryItem,
    InventoryPrediction
)

class DemandPredictionTools:
    def __init__(self):
        self.seasonality_factors = {
            1: 0.9, 2: 0.9, 6: 1.2, 7: 1.2, 8: 1.2, 12: 1.1
        }
        self.day_factors = {4: 1.3, 5: 1.4, 6: 1.2}

    def predict_demand(self,
        historical_data: pd.DataFrame,
        items: Dict[str, InventoryItem],
        target_date: datetime,
        location: str
    ) -> Dict[str, InventoryPrediction]:
        predictions = {}
        
        for item_id in items.keys():
            item_data = historical_data[historical_data['item_id'] == item_id]
            if item_data.empty:
                continue
                
            avg_daily_sales = item_data['units_sold'].mean()
            month_factor = self.seasonality_factors.get(target_date.month, 1.0)
            day_factor = self.day_factors.get(target_date.weekday(), 1.0)
            trend = self._calculate_trend(item_data)
            
            predicted_demand = avg_daily_sales * month_factor * day_factor * trend
            std_dev = item_data['units_sold'].std()
            
            predictions[item_id] = InventoryPrediction(
                predicted_demand=round(predicted_demand, 2),
                confidence_range=(
                    round(max(0, predicted_demand - 2 * std_dev), 2),
                    round(predicted_demand + 2 * std_dev, 2)
                ),
                trend_factor=round(trend, 2),
                seasonality_factor=round(month_factor * day_factor, 2)
            )
        
        return predictions
    
    def _calculate_trend(self, data: pd.DataFrame) -> float:
        if len(data) < 2:
            return 1.0
            
        dates = pd.to_datetime(data['date'])
        sales = data['units_sold']
        days = [(d - dates.min()).days for d in dates]
        
        if not days or not any(days):
            return 1.0
            
        z = np.polyfit(days, sales, 1)
        slope = z[0]
        avg_sales = sales.mean()
        
        if avg_sales == 0:
            return 1.0
            
        trend = 1 + (slope * 30 / avg_sales)
        return max(0.5, min(trend, 1.5))

    def get_tools(self) -> list[StructuredTool]:
        return [
            StructuredTool.from_function(
                func=self.predict_demand,
                name="predict_demand",
                description="Predice demanda futura basada en datos históricos"
            )
        ]