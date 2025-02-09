from crewai import Agent, Task
from typing import Dict, List, Any
from ..tools.resource_tools import ResourceTools, ResourceOptimizationInput, OptimizationResult

class ResourceOptimizationAgent:
    def __init__(self):
        self.tools = ResourceTools()
        self.agent = self.create_agent()

    def create_agent(self) -> Agent:
        return Agent(
            role='Resource Optimization Specialist',
            goal='Optimizar la asignación de recursos y personal',
            backstory="""Experto en optimización de recursos para restaurantes con 
            amplia experiencia en el mercado suizo. Especializado en:
            - Optimización de programación de personal
            - Gestión eficiente de inventario
            - Reducción de costos operativos
            - Mantenimiento de altos estándares de servicio""",
            tools=self.tools.get_tools(),
            verbose=True
        )

    def optimize_resources(self, data: Dict[str, Any]) -> OptimizationResult:
        input_data = ResourceOptimizationInput(
            predicted_sales=data['predicted_sales'],
            current_staff=data['current_staff'],
            inventory_levels=data['inventory_levels'],
            peak_hours=data.get('peak_hours', []),
            day_of_week=data.get('day_of_week', 'monday')
        )
        return self.tools.optimize_resources(input_data)

    def create_optimization_task(self, location: str) -> Task:
        return Task(
            description=f"Optimizar recursos para la ubicación {location}",
            expected_output="Recomendaciones detalladas de optimización incluyendo:\n"
                          "- Distribución óptima de personal\n"
                          "- Gestión de inventario\n"
                          "- Análisis de costos\n"
                          "- Alertas y recomendaciones",
            agent=self.agent
        )

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        return {
            'task_id': task_id,
            'status': 'completed',
            'progress': 100,
            'last_update': datetime.now().isoformat()
        }

    def get_agent(self) -> Agent:
        return self.agent