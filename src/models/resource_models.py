from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class ResourceOptimizationInput(BaseModel):
    """Datos de entrada para optimización de recursos"""
    predicted_sales: float = Field(..., description="Ventas predichas")
    current_staff: int = Field(..., description="Personal actual")
    inventory_levels: Dict[str, float] = Field(..., description="Niveles actuales de inventario")
    peak_hours: List[str] = Field(..., description="Horas pico")
    day_of_week: str = Field(..., description="Día de la semana")

class StaffRecommendation(BaseModel):
    """Recomendación de personal por turno"""
    shift: str = Field(..., description="Turno de trabajo")
    staff_count: int = Field(..., description="Número recomendado de personal")
    roles: Dict[str, int] = Field(..., description="Distribución por roles")

class InventoryOrder(BaseModel):
    """Orden de inventario recomendada"""
    item: str = Field(..., description="Ítem a ordenar")
    quantity: float = Field(..., description="Cantidad a ordenar")
    priority: str = Field(..., description="Prioridad de la orden (alta, media, baja)")

class OptimizationResult(BaseModel):
    """Resultado de la optimización de recursos"""
    recommended_staff: List[StaffRecommendation] = Field(..., description="Recomendaciones de personal")
    inventory_orders: List[InventoryOrder] = Field(..., description="Órdenes de inventario")
    efficiency_score: float = Field(..., ge=0, le=100, description="Puntuación de eficiencia")
    cost_savings: float = Field(..., description="Ahorro estimado en costos")
    alerts: List[str] = Field(default_factory=list, description="Alertas de optimización")