from typing import Dict, Any, List
from crewai import Agent
from ..tools.prediction_tools import PredictionTools
from ..models.inventory_models import (
    InventoryItem,
    InventoryPrediction,
    OrderRecommendation
)

class PerformanceAnalysisAgent:
    def __init__(self):
        self.tools = PredictionTools()
        self.agent = self.create_agent()

    def create_agent(self) -> Agent:
        return Agent(
            role='Performance Analysis Specialist',
            goal='Analizar y mejorar rendimiento de predicciones',
            backstory="""Experto en análisis de rendimiento para Holy Cow!""",
            tools=self.tools.get_tools(),
            verbose=True
        )

    def analyze_sales_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        historical_data = data.get('historical_data')
        items = data.get('inventory_items', {})
        location = data.get('location', 'Zurich')

        predictions = self.tools.predict_demand(
            historical_data=historical_data,
            items=items,
            target_date=data.get('target_date'),
            location=location
        )

        return {
            'predictions': {k: v.dict() for k, v in predictions.items()},
            'location': location,
            'resource_optimization': {
                'efficiency_score': self._calculate_efficiency(predictions),
                'recommendations': self._generate_recommendations(predictions)
            }
        }

    def _calculate_efficiency(self, predictions: Dict[str, InventoryPrediction]) -> float:
        efficiency_scores = []
        for pred in predictions.values():
            uncertainty = (pred.confidence_range[1] - pred.confidence_range[0]) / pred.predicted_demand
            efficiency_scores.append(max(0, 1 - uncertainty))
        return sum(efficiency_scores) / len(efficiency_scores) if efficiency_scores else 0

    def _generate_recommendations(self, predictions: Dict[str, InventoryPrediction]) -> List[str]:
        recommendations = []
        for item_id, pred in predictions.items():
            if pred.trend_factor > 1.2:
                recommendations.append(f"Tendencia creciente para {item_id}")
            elif pred.trend_factor < 0.8:
                recommendations.append(f"Tendencia decreciente para {item_id}")
        return recommendations

    def get_agent(self) -> Agent:
        return self.agent