from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import Dict, List, Any
from datetime import datetime
from ..models.resource_models import (
    StaffRecommendation,
    InventoryOrder,
    ResourceOptimizationInput,
    OptimizationResult
)
from ..models.inventory_models import (
    InventoryLevel,
    InventoryItem,
    InventoryPrediction,
    MultiLocationInput
)

class ResourceTools:
    def __init__(self):
        self.STAFF_RATIOS = {
            'server': 1000,    # Ventas por servidor
            'cook': 2000,      # Ventas por cocinero
            'helper': 1500     # Ventas por ayudante
        }
        self.MIN_STAFF = {'server': 2, 'cook': 1, 'helper': 1}
        self.HOURLY_RATES = {
            'server': 25,  # CHF por hora
            'cook': 35,    # CHF por hora
            'helper': 22   # CHF por hora
        }

    def optimize_resources(self, data: ResourceOptimizationInput) -> OptimizationResult:
        """Optimiza recursos basado en predicciones y estado actual"""
        staff_recs = []
        for shift in ['morning', 'afternoon', 'evening']:
            is_peak = any(hour in data.peak_hours for hour in self._get_shift_hours(shift))
            shift_sales = data.predicted_sales * (0.4 if is_peak else 0.3)
            
            roles = {}
            for role, ratio in self.STAFF_RATIOS.items():
                staff_needed = max(
                    self.MIN_STAFF[role],
                    round(shift_sales / ratio)
                )
                roles[role] = staff_needed
            
            staff_recs.append(StaffRecommendation(
                shift=shift,
                staff_count=sum(roles.values()),
                roles=roles
            ))

        inventory_orders = []
        for item, level in data.inventory_levels.items():
            if level < 5:
                inventory_orders.append(InventoryOrder(
                    item=item,
                    quantity=10 - level,
                    priority='high' if level < 2 else 'medium'
                ))

        efficiency = self._calculate_efficiency(staff_recs, data.current_staff)
        savings = self._calculate_savings(staff_recs, data.current_staff)
        alerts = self._generate_alerts(staff_recs, inventory_orders)

        return OptimizationResult(
            recommended_staff=staff_recs,
            inventory_orders=inventory_orders,
            efficiency_score=efficiency,
            cost_savings=savings,
            alerts=alerts
        )

    def analyze_inventory(
        self,
        current_levels: Dict[str, InventoryLevel],
        items: Dict[str, InventoryItem],
        historical_movements: List[Dict] = [],
        predicted_sales: float = 0
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

    def optimize_multi_location_orders(self, data: MultiLocationInput) -> Dict[str, Any]:
        """Optimiza pedidos y transferencias entre locales"""
        recommendations = {}
        
        for location, inventory in data.locations_inventory.items():
            location_recs = {
                'orders': [],
                'transfers': []
            }
            
            predictions = data.demand_predictions.get(location, {})
            
            for item_id, level in inventory.items():
                item_config = data.items.get(item_id)
                if not item_config:
                    continue
                    
                prediction = predictions.get(item_id)
                if not prediction:
                    continue
                    
                # Análisis de necesidad de pedido
                if level.current_quantity < item_config.reorder_point:
                    order_quantity = item_config.max_level - level.current_quantity
                    location_recs['orders'].append({
                        'item_id': item_id,
                        'quantity': order_quantity,
                        'priority': 'high' if level.current_quantity < item_config.min_level else 'medium'
                    })
                    
            recommendations[location] = location_recs
            
        return recommendations

    def _get_shift_hours(self, shift: str) -> List[str]:
        shifts = {
            'morning': ['08:00', '09:00', '10:00', '11:00'],
            'afternoon': ['12:00', '13:00', '14:00', '15:00'],
            'evening': ['18:00', '19:00', '20:00', '21:00']
        }
        return shifts.get(shift, [])

    def _calculate_efficiency(self, recommendations: List[StaffRecommendation], current_staff: int) -> float:
        recommended_total = sum(rec.staff_count for rec in recommendations)
        ratio = min(current_staff, recommended_total) / max(current_staff, recommended_total)
        return ratio * 100

    def _calculate_savings(self, recommendations: List[StaffRecommendation], current_staff: int) -> float:
        HOURS_PER_SHIFT = 8
        DAYS_PER_MONTH = 30
        
        avg_rate = sum(self.HOURLY_RATES.values()) / len(self.HOURLY_RATES)
        current_daily_cost = current_staff * avg_rate * HOURS_PER_SHIFT
        
        optimized_daily_cost = 0
        for rec in recommendations:
            shift_cost = sum(
                count * self.HOURLY_RATES[role] * HOURS_PER_SHIFT
                for role, count in rec.roles.items()
            )
            optimized_daily_cost += shift_cost
        
        monthly_savings = (current_daily_cost - optimized_daily_cost) * DAYS_PER_MONTH
        return max(0, monthly_savings)

    def _generate_alerts(
        self,
        staff_recs: List[StaffRecommendation],
        inventory_orders: List[InventoryOrder]
    ) -> List[str]:
        alerts = []
        
        critical_items = [order.item for order in inventory_orders if order.priority == 'high']
        if critical_items:
            alerts.append(f"¡Niveles críticos de inventario en: {', '.join(critical_items)}!")
        
        total_staff = sum(rec.staff_count for rec in recommendations)
        if total_staff > 30:
            alerts.append("Alta demanda de personal - verificar disponibilidad")
        
        return alerts

    def get_tools(self) -> List[StructuredTool]:
        return [
            StructuredTool.from_function(
                func=self.optimize_resources,
                name="optimize_resources",
                description="Optimiza recursos basado en predicciones y estado actual",
            ),
            StructuredTool.from_function(
                func=self.analyze_inventory,
                name="analyze_inventory",
                description="Analiza niveles de inventario y genera recomendaciones"
            ),
            StructuredTool.from_function(
                func=self.optimize_multi_location_orders,
                name="optimize_multi_location_orders",
                description="Optimiza pedidos y transferencias entre locales"
            )
        ]