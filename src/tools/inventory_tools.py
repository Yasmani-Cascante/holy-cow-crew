from typing import Dict, List
from datetime import datetime
from langchain.tools import StructuredTool
from ..models.inventory_models import (
    InventoryItem,
    InventoryLevel,
    OrderRecommendation
)

class InventoryTools:
    def analyze_inventory_levels(
        self,
        current_levels: Dict[str, InventoryLevel],
        items: Dict[str, InventoryItem],
        historical_movements: List,
        predicted_sales: float
    ) -> Dict[str, OrderRecommendation]:
        recommendations = {}
        
        for item_id, level in current_levels.items():
            if item_id not in items:
                continue
                
            item = items[item_id]
            
            if level.available_quantity <= item.reorder_point:
                order_quantity = item.max_level - level.available_quantity
                
                recommendations[item_id] = OrderRecommendation(
                    item_id=item_id,
                    quantity=order_quantity,
                    priority="high" if level.available_quantity <= item.min_level else "medium",
                    reason=f"Stock bajo: {level.available_quantity} unidades disponibles",
                    estimated_cost=order_quantity * item.cost_per_unit,
                    suggested_order_date=datetime.now()
                )
        
        return recommendations

    def get_tools(self) -> List[StructuredTool]:
        return [
            StructuredTool.from_function(
                func=self.analyze_inventory_levels,
                name="analyze_inventory",
                description="Analiza niveles de inventario y genera recomendaciones"
            )
        ]