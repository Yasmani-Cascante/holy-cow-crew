from typing import Dict, Any, List
from datetime import datetime
from .agents.performance_analysis_agent import PerformanceAnalysisAgent
from .agents.resource_optimization_agent import ResourceOptimizationAgent

class HolyCowIntegrator:
    def __init__(self):
        self.performance_agent = PerformanceAnalysisAgent()
        self.resource_agent = ResourceOptimizationAgent()
        self.system_state = {
            'last_update': None,
            'alerts': [],
            'health_status': 'operational'
        }

    def analyze_location(self, location_data: Dict[str, Any]) -> Dict[str, Any]:
        if not location_data.get('location'):
            raise ValueError("Location data must include 'location' field")

        performance_analysis = self.performance_agent.analyze_sales_data(location_data)
        resource_optimization = self.resource_agent.optimize_resources({
            'locations': [location_data['location']],
            **location_data
        })

        self._update_system_state(performance_analysis, resource_optimization)

        return {
            'timestamp': datetime.now().isoformat(),
            'location': location_data['location'],
            'performance_analysis': performance_analysis,
            'resource_optimization': resource_optimization,
            'system_status': self.get_system_state()
        }

    def get_system_state(self) -> Dict[str, Any]:
        return {
            'last_update': self.system_state['last_update'],
            'health_status': self.system_state['health_status'],
            'active_alerts': len(self.system_state['alerts'])
        }

    def get_active_alerts(self) -> List[Dict[str, Any]]:
        return self.system_state['alerts']

    def _update_system_state(self, performance_data: Dict, resource_data: Dict):
        self.system_state['last_update'] = datetime.now().isoformat()
        
        # Analizar alertas críticas
        critical_alerts = []
        
        if performance_data.get('resource_optimization', {}).get('efficiency_score', 1) < 0.7:
            critical_alerts.append({
                'type': 'efficiency',
                'level': 'critical',
                'message': 'Eficiencia del sistema por debajo del umbral'
            })

        for location, recs in resource_data.get('inventory_recommendations', {}).items():
            for item_id, rec in recs.items():
                if rec.get('priority') == 'high':
                    critical_alerts.append({
                        'type': 'inventory',
                        'level': 'high',
                        'message': f'Nivel crítico de inventario en {location}: {item_id}'
                    })

        self.system_state['alerts'] = critical_alerts
        self.system_state['health_status'] = 'degraded' if critical_alerts else 'operational'