from langchain.tools import StructuredTool
from typing import Dict, List, Any
from datetime import datetime
from ..models.resource_models import StaffRecommendation, InventoryOrder, OptimizationResult

class ResourceOptimizationTools:
    def __init__(self):
        self.staff_efficiency_threshold = 0.8
        self.inventory_threshold = 0.2
        
    def optimize_staffing(self, data: Dict[str, Any]) -> List[StaffRecommendation]:
        """Optimiza la programación del personal"""
        peak_hours = data.get('peak_hours', [])
        predicted_sales = data.get('predicted_sales', 0)
        
        recommendations = []
        for shift in ['morning', 'afternoon', 'evening']:
            is_peak = any(hour in peak_hours for hour in self._get_shift_hours(shift))
            base_staff = 3 if is_peak else 2
            
            recommendations.append(StaffRecommendation(
                shift=shift,
                staff_count=base_staff,
                roles={
                    'kitchen': base_staff - 1,
                    'service': base_staff - 1,
                    'manager': 1
                }
            ))
        
        return recommendations
    
    def optimize_inventory(self, data: Dict[str, Any]) -> List[InventoryOrder]:
        """Optimiza los niveles de inventario"""
        inventory_levels = data.get('inventory_levels', {})
        orders = []
        
        for item, level in inventory_levels.items():
            if level < 50:  # Nivel bajo
                orders.append(InventoryOrder(
                    item=item,
                    quantity=100 - level,
                    priority='alta' if level < 20 else 'media'
                ))
        
        return orders
    
    def calculate_efficiency(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Calcula métricas de eficiencia"""
        current_staff = data.get('current_staff', 0)
        predicted_sales = data.get('predicted_sales', 0)
        
        # Cálculos simplificados para el ejemplo
        staff_efficiency = min(predicted_sales / (current_staff * 200), 1) * 100
        inventory_efficiency = sum(data.get('inventory_levels', {}).values()) / len(data.get('inventory_levels', {}))
        
        return {
            'staff_efficiency': staff_efficiency,
            'inventory_efficiency': inventory_efficiency,
            'overall_efficiency': (staff_efficiency + inventory_efficiency) / 2
        }
    
    def _get_shift_hours(self, shift: str) -> List[str]:
        """Retorna las horas correspondientes a un turno"""
        shifts = {
            'morning': ['08:00-12:00'],
            'afternoon': ['12:00-16:00'],
            'evening': ['16:00-22:00']
        }
        return shifts.get(shift, [])