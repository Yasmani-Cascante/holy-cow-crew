from crewai import Agent, Task
from typing import Dict, List, Any
from ..tools.prediction_tools import PredictionTools

class PerformanceAnalysisAgent:
    def __init__(self):
        self.tools = PredictionTools()
        self.agent = self.create_agent()
    
    def create_agent(self) -> Agent:
        return Agent(
            role='Performance Analysis Specialist',
            goal='Analyze sales predictions and performance metrics',
            backstory="""Expert in restaurant performance analysis 
            specializing in sales predictions and KPI tracking.""",
            tools=self.tools.get_tools(),
            verbose=True
        )
    
    def create_analysis_task(self) -> Task:
        return Task(
            description="Analyze sales performance and provide insights",
            expected_output="Detailed analysis report including prediction accuracy, error costs, and recommendations",
            agent=self.agent
        )

    def analyze_sales_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.tools.analyze_predictions(data)
    
    def get_agent(self) -> Agent:
        return self.agent