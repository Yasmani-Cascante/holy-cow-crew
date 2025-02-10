from typing import Dict, Any, List
import pandas as pd
import numpy as np
from datetime import datetime
from langchain.tools import StructuredTool
from ..models.inventory_models import (
    InventoryItem,
    InventoryPrediction
)

class PredictionTools:
    def predict_demand(
        self,
        historical_data: pd.DataFrame,
        items: Dict[str, InventoryItem],
        target_date: datetime,
        location: str
    ) -> Dict[str, InventoryPrediction]:
        predictions = {}
        seasonal_factors = {
            1: 0.9, 2: 0.9, 3: 1.0, 4: 1.0, 5: 1.0, 6: 1.2,
            7: 1.2, 8: 1.2, 9: 1.0, 10: 1.0, 11: 1.0, 12: 1.1
        }
        
        for item_id, item in items.items():
            if not historical_data.empty:
                item_data = historical_data[historical_data['item_id'] == item_id]
                if not item_data.empty:
                    mean_sales = item_data['units_sold'].mean()
                    std_sales = item_data['units_sold'].std() or mean_sales * 0.1
                else:
                    mean_sales = 100  # valor por defecto
                    std_sales = 20
            else:
                mean_sales = 100
                std_sales = 20
            
            seasonal_factor = seasonal_factors.get(target_date.month, 1.0)
            predicted_demand = mean_sales * seasonal_factor
            
            predictions[item_id] = InventoryPrediction(
                predicted_demand=round(predicted_demand, 2),
                confidence_range=(
                    round(max(0, predicted_demand - 2 * std_sales), 2),
                    round(predicted_demand + 2 * std_sales, 2)
                ),
                trend_factor=1.0,
                seasonality_factor=seasonal_factor
            )
        
        return predictions

    def get_tools(self) -> List[StructuredTool]:
        return [
            StructuredTool.from_function(
                func=self.predict_demand,
                name="predict_demand",
                description="Predice demanda basada en datos históricos"
            )
        ]