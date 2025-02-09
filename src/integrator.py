from typing import Dict, Any
from src.agents import (
    PerformanceAnalysisAgent,
    ReportingAgent
)

class HolyCowIntegrator:
    """Integrador principal para Holy Cow Crew"""
    
    def __init__(self):
        self.performance_agent = PerformanceAnalysisAgent()
        self.reporting_agent = ReportingAgent()
    
    def analyze_location(self, location: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza una ubicación específica"""
        try:
            # Generar reporte de rendimiento
            performance_results = self.performance_agent.process_sales_data(metrics)
            
            # Generar reporte visual
            report = self.reporting_agent.create_report(location, metrics)
            
            return {
                'performance_metrics': performance_results,
                'report': report,
                'location': location
            }
            
        except Exception as e:
            print(f"Error analizando ubicación {location}: {str(e)}")
            raise