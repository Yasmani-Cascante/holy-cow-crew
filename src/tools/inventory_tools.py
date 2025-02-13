from typing import Dict, List, Any
from datetime import datetime
from langchain.tools import StructuredTool
from ..models.inventory_models import (
    InventoryItem,
    InventoryLevel,
    InventoryPrediction
)

class InventoryTools:
    def analyze_inventory(
        self, 
        current_levels: Dict[str, InventoryLevel],
        items: Dict[str, InventoryItem],
        predicted_sales: float,
        historical_movements: List[Dict] = []
    ) -> Dict[str, Any]:
        """Analiza niveles de inventario y genera recomendaciones"""
        
        results = {
            'alerts': [],
            'recommendations': [],
            'status': {}
        }
        
        for item_id, level in current_levels.items():
            item_config = items.get(item_id)
            if not item_config:
                continue
                
            status = {
                'current_level': level.current_quantity,
                'available': level.available_quantity,
                'utilization': (level.current_quantity / item_config.max_level) * 100
            }
            
            if level.current_quantity <= item_config.reorder_point:
                results['alerts'].append(f"Reorder needed for {item_config.name}")
                results['recommendations'].append({
                    'item': item_id,
                    'action': 'reorder',
                    'quantity': item_config.max_level - level.current_quantity
                })
                
            results['status'][item_id] = status
        
        return results

    def get_tools(self) -> List[StructuredTool]:
        return [
            StructuredTool.from_function(
                func=self.analyze_inventory,
                name="analyze_inventory",
                description="Analiza niveles de inventario y genera recomendaciones"
            )
        ]