from typing import Dict, Any, List
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.report_types = {
            'inventory': self._generate_inventory_report,
            'performance': self._generate_performance_report,
            'optimization': self._generate_optimization_report
        }

    def generate_report(self, data: Dict[str, Any], report_type: str) -> Dict[str, Any]:
        if report_type not in self.report_types:
            raise ValueError(f"Report type {report_type} not supported")
        
        return self.report_types[report_type](data)

    def _generate_inventory_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'type': 'inventory',
            'timestamp': datetime.now().isoformat(),
            'content': data
        }

    def _generate_performance_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'type': 'performance',
            'timestamp': datetime.now().isoformat(),
            'content': data
        }

    def _generate_optimization_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'type': 'optimization',
            'timestamp': datetime.now().isoformat(),
            'content': data
        }