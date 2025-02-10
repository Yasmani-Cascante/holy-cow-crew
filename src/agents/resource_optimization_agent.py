from crewai import Agent, Task
from typing import Dict, List, Any
from datetime import datetime
import pandas as pd
from ..tools.resource_tools import ResourceTools
from ..tools.inventory_tools import InventoryTools
from ..tools.demand_prediction_tools import DemandPredictionTools
from ..tools.multi_location_tools import MultiLocationTools
from ..models.inventory_models import InventoryItem, InventoryLevel, LocationRecommendation

class ResourceOptimizationAgent:
    def __init__(self):
        self.resource_tools = ResourceTools()
        self.inventory_tools = InventoryTools()
        self.demand_tools = DemandPredictionTools()
        self.multi_location_tools = MultiLocationTools()
        self.agent = self.create_agent()

    def create_agent(self) -> Agent:
        return Agent(
            role='Resource Optimization Specialist',
            goal='Optimizar recursos y coordinar entre locales Holy Cow!',
            backstory="""Experto en optimización de recursos para Holy Cow! 
            especializado en análisis predictivo, gestión de inventario 
            y coordinación entre múltiples locales en Suiza.""",
            tools=[
                *self.resource_tools.get_tools(),
                *self.inventory_tools.get_tools(),
                *self.demand_tools.get_tools(),
                *self.multi_location_tools.get_tools()
            ],
            verbose=True
        )

    def optimize_resources(self, data: Dict[str, Any]) -> Dict[str, Any]:
        locations = data.get('locations', ['Zurich'])
        historical_data = pd.read_csv(data.get('historical_data_path', 
            'data/sample/inventory_data.csv'))
        inventory_items = data.get('inventory_items', {})
        
        location_predictions = {}
        location_inventory = {}
        
        for location in locations:
            location_data = historical_data[
                historical_data['location'] == location
            ]
            
            predictions = self.demand_tools.predict_demand(
                historical_data=location_data,
                items=inventory_items,
                target_date=datetime.now(),
                location=location
            )
            location_predictions[location] = predictions
            
            location_inventory[location] = {
                item_id: data.get('inventory_levels', {}).get(
                    f"{location}_{item_id}", {}
                ).get('current_quantity', 0)
                for item_id in inventory_items.keys()
            }
        
        multi_location_recommendations = self.multi_location_tools.optimize_orders(
            locations_inventory=location_inventory,
            demand_predictions=location_predictions,
            items=inventory_items
        )
        
        inventory_recommendations = {}
        for location in locations:
            inventory_recs = self.inventory_tools.analyze_inventory_levels(
                current_levels=data.get('inventory_levels', {}).get(location, {}),
                items=inventory_items,
                historical_movements=data.get('inventory_movements', []),
                predicted_sales=sum(
                    p.predicted_demand 
                    for p in location_predictions[location].values()
                )
            )
            inventory_recommendations[location] = inventory_recs
        
        return {
            'timestamp': datetime.now().isoformat(),
            'locations_analyzed': locations,
            'demand_predictions': location_predictions,
            'inventory_recommendations': inventory_recommendations,
            'multi_location_optimization': multi_location_recommendations,
            'metrics': {
                'total_transfer_value': self._calculate_transfer_value(
                    multi_location_recommendations
                ),
                'optimization_savings': self._calculate_optimization_savings(
                    multi_location_recommendations,
                    inventory_recommendations
                )
            }
        }

    def _calculate_transfer_value(self, recommendations: Dict[str, LocationRecommendation]) -> float:
        total_value = 0
        for location_data in recommendations.values():
            for transfer in location_data.transfers_in.values():
                total_value += transfer.total_cost
        return round(total_value, 2)

    def _calculate_optimization_savings(
        self,
        multi_location_recs: Dict[str, LocationRecommendation],
        inventory_recs: Dict
    ) -> float:
        traditional_cost = sum(
            sum(item.get('estimated_cost', 0) 
                for item in location.values())
            for location in inventory_recs.values()
        )
        
        optimized_cost = sum(
            sum(order.estimated_cost 
                for order in location.new_orders.values())
            for location in multi_location_recs.values()
        )
        
        return round(max(0, traditional_cost - optimized_cost), 2)

    def create_optimization_task(self, location: str) -> Task:
        return Task(
            description=f"Optimizar recursos para {location}",
            expected_output="Análisis completo incluyendo:\n"
                          "- Predicciones de demanda\n"
                          "- Recomendaciones de inventario\n"
                          "- Oportunidades de transferencia\n"
                          "- Métricas de optimización",
            agent=self.agent
        )

    def get_agent(self) -> Agent:
        return self.agent