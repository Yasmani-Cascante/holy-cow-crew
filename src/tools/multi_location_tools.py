from typing import Dict, List
from datetime import datetime
from langchain.tools import StructuredTool
from ..models.inventory_models import (
    InventoryItem,
    TransferOption,
    LocationRecommendation,
    OrderRecommendation,
    InventoryPrediction
)

class MultiLocationTools:
    def __init__(self):
        self.transfer_costs = {
            ('Zurich', 'Geneva'): 120,
            ('Zurich', 'Basel'): 100,
            ('Geneva', 'Basel'): 150,
        }
        self.min_transfer_value = 500

    def optimize_orders(self,
        locations_inventory: Dict[str, Dict[str, float]],
        demand_predictions: Dict[str, Dict[str, InventoryPrediction]],
        items: Dict[str, InventoryItem]
    ) -> Dict[str, LocationRecommendation]:
        recommendations = {}
        
        for location, inventory in locations_inventory.items():
            new_orders = {}
            transfers_in = {}
            transfers_out = {}
            
            for item_id, current_stock in inventory.items():
                item = items[item_id]
                predicted_demand = demand_predictions[location][item_id].predicted_demand
                
                days_coverage = current_stock / (predicted_demand + 0.0001)
                needed_quantity = max(0,
                    item.reorder_point - current_stock +
                    predicted_demand * item.lead_time_days
                )
                
                if needed_quantity > 0:
                    transfer_options = self._find_transfer_options(
                        item_id, needed_quantity, location,
                        locations_inventory, demand_predictions, item
                    )
                    
                    if transfer_options:
                        best_transfer = min(
                            transfer_options,
                            key=lambda x: x.total_cost
                        )
                        
                        if best_transfer.total_cost < needed_quantity * item.cost_per_unit * 1.2:
                            transfers_in[item_id] = best_transfer
                            continue
                    
                    new_orders[item_id] = OrderRecommendation(
                        item_id=item_id,
                        quantity=needed_quantity,
                        priority='high' if days_coverage < item.lead_time_days else 'medium',
                        reason=f"Stock coverage: {days_coverage:.1f} days",
                        estimated_cost=needed_quantity * item.cost_per_unit,
                        suggested_order_date=datetime.now()
                    )
            
            recommendations[location] = LocationRecommendation(
                new_orders=new_orders,
                transfers_in=transfers_in,
                transfers_out=transfers_out
            )
        
        return recommendations

    def _find_transfer_options(self,
        item_id: str,
        quantity_needed: float,
        requesting_location: str,
        locations_inventory: Dict[str, Dict[str, float]],
        demand_predictions: Dict[str, Dict[str, InventoryPrediction]],
        item: InventoryItem
    ) -> List[TransferOption]:
        options = []
        
        for source_loc, inventory in locations_inventory.items():
            if source_loc == requesting_location:
                continue
                
            current_stock = inventory.get(item_id, 0)
            predicted_demand = demand_predictions[source_loc][item_id].predicted_demand
            
            excess_stock = current_stock - (
                item.min_level + predicted_demand * item.lead_time_days
            )
            
            if excess_stock > quantity_needed:
                transfer_cost = self._calculate_transfer_cost(
                    source_loc, requesting_location,
                    quantity_needed, item
                )
                
                options.append(TransferOption(
                    from_location=source_loc,
                    quantity=quantity_needed,
                    transport_cost=transfer_cost,
                    total_cost=transfer_cost + quantity_needed * item.cost_per_unit * 0.8,
                    available_immediately=True
                ))
        
        return options

    def _calculate_transfer_cost(self,
        from_loc: str,
        to_loc: str,
        quantity: float,
        item: InventoryItem
    ) -> float:
        base_cost = self.transfer_costs.get(
            (from_loc, to_loc),
            self.transfer_costs.get((to_loc, from_loc), 200)
        )
        
        if item.storage == 'FROZEN':
            base_cost *= 1.5
        elif item.storage == 'REFRIGERATED':
            base_cost *= 1.3
            
        return base_cost * (1 + quantity / 1000)

    def get_tools(self) -> List[StructuredTool]:
        return [
            StructuredTool.from_function(
                func=self.optimize_orders,
                name="optimize_multi_location_orders",
                description="Optimiza pedidos y transferencias entre locales"
            )
        ]