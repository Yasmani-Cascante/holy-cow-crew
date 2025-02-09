from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from langchain.tools import StructuredTool

class StaffRecommendation(BaseModel):
    shift: str
    staff_count: int
    roles: Dict[str, int]

class InventoryOrder(BaseModel):
    item: str
    quantity: float
    priority: str

class ResourceOptimizationInput(BaseModel):
    predicted_sales: float
    current_staff: int
    inventory_levels: Dict[str, float]
    peak_hours: List[str]
    day_of_week: str

class OptimizationResult(BaseModel):
    recommended_staff: List[StaffRecommendation]
    inventory_orders: List[InventoryOrder]
    efficiency_score: float
    cost_savings: float
    alerts: List[str] = []

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

    def optimize_resources(self, input_data: ResourceOptimizationInput) -> OptimizationResult:
        # Calcular personal recomendado
        staff_recs = []
        for shift in ['morning', 'afternoon', 'evening']:
            is_peak = any(hour in input_data.peak_hours for hour in self._get_shift_hours(shift))
            shift_sales = input_data.predicted_sales * (0.4 if is_peak else 0.3)
            
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

        # Calcular órdenes de inventario
        inventory_orders = []
        for item, level in input_data.inventory_levels.items():
            if level < 5:  # Umbral bajo
                inventory_orders.append(InventoryOrder(
                    item=item,
                    quantity=10 - level,
                    priority='high' if level < 2 else 'medium'
                ))

        # Calcular eficiencia y ahorro
        efficiency = self._calculate_efficiency(staff_recs, input_data.current_staff)
        savings = self._calculate_savings(staff_recs, input_data.current_staff)

        # Generar alertas
        alerts = self._generate_alerts(staff_recs, inventory_orders)

        return OptimizationResult(
            recommended_staff=staff_recs,
            inventory_orders=inventory_orders,
            efficiency_score=efficiency,
            cost_savings=savings,
            alerts=alerts
        )

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
        """Calcula ahorros potenciales basados en optimización de personal"""
        HOURS_PER_SHIFT = 8
        DAYS_PER_MONTH = 30
        
        # Calcular costo actual
        avg_rate = sum(self.HOURLY_RATES.values()) / len(self.HOURLY_RATES)
        current_daily_cost = current_staff * avg_rate * HOURS_PER_SHIFT
        
        # Calcular costo optimizado
        optimized_daily_cost = 0
        for rec in recommendations:
            shift_cost = sum(
                count * self.HOURLY_RATES[role] * HOURS_PER_SHIFT
                for role, count in rec.roles.items()
            )
            optimized_daily_cost += shift_cost
        
        # Calcular ahorro mensual
        monthly_savings = (current_daily_cost - optimized_daily_cost) * DAYS_PER_MONTH
        
        return max(0, monthly_savings)

    def _generate_alerts(self, staff_recs: List[StaffRecommendation], inventory_orders: List[InventoryOrder]) -> List[str]:
        alerts = []
        
        # Alertas de inventario
        critical_items = [order.item for order in inventory_orders if order.priority == 'high']
        if critical_items:
            alerts.append(f"¡Niveles críticos de inventario en: {', '.join(critical_items)}!")
        
        # Alertas de personal
        total_staff = sum(rec.staff_count for rec in staff_recs)
        if total_staff > 30:
            alerts.append("Alta demanda de personal - verificar disponibilidad")
        
        return alerts

    def get_tools(self) -> List[StructuredTool]:
        return [
            StructuredTool.from_function(
                func=self.optimize_resources,
                name="optimize_resources",
                description="Optimiza recursos basado en predicciones y estado actual",
                args_schema=ResourceOptimizationInput
            )
        ]