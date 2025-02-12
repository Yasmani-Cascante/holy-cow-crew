from typing import Dict, Any, List
from datetime import datetime
import json
from pathlib import Path

class TestMetrics:
    def __init__(self):
        self.metrics = {
            "execution_time": {},
            "memory_usage": {},
            "agent_performance": {},
            "recommendations_quality": {},
            "errors": []
        }
        self.start_time = datetime.now()
    
    def start_test(self, location: str):
        """Registra el inicio de prueba para una ubicación"""
        self.metrics["execution_time"][location] = {
            "start": datetime.now().isoformat()
        }
    
    def end_test(self, location: str):
        """Registra el fin de prueba para una ubicación"""
        self.metrics["execution_time"][location]["end"] = datetime.now().isoformat()
        self.metrics["execution_time"][location]["duration"] = (
            datetime.fromisoformat(self.metrics["execution_time"][location]["end"]) -
            datetime.fromisoformat(self.metrics["execution_time"][location]["start"])
        ).total_seconds()
    
    def record_agent_performance(self, location: str, agent_name: str, metrics: Dict[str, Any]):
        """Registra métricas de rendimiento de un agente"""
        if location not in self.metrics["agent_performance"]:
            self.metrics["agent_performance"][location] = {}
        
        self.metrics["agent_performance"][location][agent_name] = metrics
    
    def evaluate_recommendations(self, location: str, recommendations: List[Dict[str, Any]]):
        """Evalúa la calidad de las recomendaciones"""
        quality_metrics = {
            "total_recommendations": len(recommendations),
            "actionable_recommendations": sum(1 for r in recommendations if self._is_actionable(r)),
            "high_impact_recommendations": sum(1 for r in recommendations if self._is_high_impact(r))
        }
        
        self.metrics["recommendations_quality"][location] = quality_metrics
    
    def record_error(self, location: str, error_type: str, error_message: str):
        """Registra un error ocurrido durante las pruebas"""
        self.metrics["errors"].append({
            "timestamp": datetime.now().isoformat(),
            "location": location,
            "type": error_type,
            "message": error_message
        })
    
    def _is_actionable(self, recommendation: Dict[str, Any]) -> bool:
        """Determina si una recomendación es accionable"""
        required_fields = ["action", "priority", "impact"]
        return all(field in recommendation for field in required_fields)
    
    def _is_high_impact(self, recommendation: Dict[str, Any]) -> bool:
        """Determina si una recomendación es de alto impacto"""
        return (
            recommendation.get("priority", "").lower() == "high" or
            recommendation.get("impact", 0) > 7
        )
    
    def save_metrics(self, output_dir: str = "data/results"):
        """Guarda las métricas en un archivo JSON"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = output_path / f"test_metrics_{timestamp}.json"
        
        # Calcular métricas globales
        self.metrics["total_duration"] = (datetime.now() - self.start_time).total_seconds()
        self.metrics["total_locations"] = len(self.metrics["execution_time"])
        self.metrics["total_errors"] = len(self.metrics["errors"])
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.metrics, f, indent=2)
        
        return file_path