from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class ResourceOptimizationResult(BaseModel):
    """Modelo para resultados de optimización de recursos"""
    recommended_staff: List[Dict[str, Any]] = Field(..., description="Staff recommendations by shift")
    inventory_orders: List[Dict[str, Any]] = Field(..., description="Required inventory orders")
    efficiency_score: float = Field(..., ge=0, le=100, description="Overall efficiency score")
    cost_savings: float = Field(..., description="Estimated cost savings")
    alerts: List[str] = Field(default_factory=list, description="Resource-related alerts")

class IntegratedAnalysis(BaseModel):
    """Modelo para el análisis integrado de una ubicación"""
    location: str = Field(..., description="Restaurant location")
    timestamp: datetime = Field(default_factory=datetime.now)
    performance_metrics: Dict[str, Any] = Field(..., description="Performance analysis results")
    market_insights: Dict[str, Any] = Field(..., description="Market strategy insights")
    resource_optimization: Dict[str, Any] = Field(..., description="Resource optimization results")
    dashboard_data: Dict[str, Any] = Field(..., description="Dashboard configuration and data")
    
    def get_efficiency_metrics(self) -> Dict[str, float]:
        """Obtiene métricas combinadas de eficiencia"""
        return {
            'performance_score': self.performance_metrics.get('efficiency', 0),
            'resource_score': self.resource_optimization.get('efficiency_score', 0),
            'overall_efficiency': (
                self.performance_metrics.get('efficiency', 0) * 0.4 +
                self.resource_optimization.get('efficiency_score', 0) * 0.6
            )
        }
    
    def get_critical_alerts(self) -> List[str]:
        """Obtiene alertas críticas de todos los componentes"""
        alerts = []
        
        # Performance alerts
        if self.performance_metrics.get('alerts'):
            alerts.extend(self.performance_metrics['alerts'])
            
        # Resource alerts
        if self.resource_optimization.get('alerts'):
            alerts.extend(self.resource_optimization['alerts'])
            
        return [alert for alert in alerts if 'critical' in alert.lower()]

class SystemState(BaseModel):
    """Modelo para el estado del sistema integrado"""
    last_update: datetime = Field(default_factory=datetime.now)
    locations: List[str] = Field(..., description="Active locations")
    active_alerts: List[Dict[str, Any]] = Field(default_factory=list)
    system_health: Dict[str, bool] = Field(..., description="Components health status")
    
    def is_healthy(self) -> bool:
        """Verifica si todos los componentes están funcionando"""
        return all(self.system_health.values())
    
    def get_unhealthy_components(self) -> List[str]:
        """Retorna lista de componentes no saludables"""
        return [
            component 
            for component, status in self.system_health.items() 
            if not status
        ]