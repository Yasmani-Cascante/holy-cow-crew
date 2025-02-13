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
        """
        Predice demanda basada en datos históricos
        Args:
            historical_data: DataFrame con historial de ventas
            items: Diccionario de items con configuración
            target_date: Fecha objetivo para predicción
            location: Ubicación para predicción
        """
        if historical_data is None or historical_data.empty:
            raise ValueError("Se requiere historical_data válido")
            
        predictions = {}
        seasonal_factors = {
            1: 0.9, 2: 0.9, 3: 1.0, 4: 1.0, 5: 1.0, 6: 1.2,
            7: 1.2, 8: 1.2, 9: 1.0, 10: 1.0, 11: 1.0, 12: 1.1
        }
        
        for item_id, item in items.items():
            df = historical_data[historical_data['item_id'] == item_id].copy()
            
            if df.empty:
                continue
                
            # Calcular métricas base
            mean_sales = df['units_sold'].mean()
            std_sales = df['units_sold'].std() or mean_sales * 0.1
            
            # Ajustar por estacionalidad
            seasonal_factor = seasonal_factors.get(target_date.month, 1.0)
            predicted_demand = mean_sales * seasonal_factor
            
            # Calcular tendencia
            if len(df) >= 2:
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date')
                sales_change = (df['units_sold'].iloc[-1] - df['units_sold'].iloc[0]) / df['units_sold'].iloc[0]
                trend_factor = 1 + (sales_change / len(df))
            else:
                trend_factor = 1.0
            
            predictions[item_id] = InventoryPrediction(
                predicted_demand=round(predicted_demand * trend_factor, 2),
                confidence_range=(
                    round(max(0, predicted_demand - 2 * std_sales), 2),
                    round(predicted_demand + 2 * std_sales, 2)
                ),
                trend_factor=round(trend_factor, 4),
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