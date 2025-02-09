from crewai import Agent, Task
from typing import Dict, List, Tuple, Any
from ..tools.market_tools import MarketTools

class MarketStrategyAgent:
    def __init__(self):
        self.tools = MarketTools()
        self.agent = self.create_agent()
    
    def create_agent(self) -> Agent:
        return Agent(
            role='Marketing Strategy Specialist',
            goal='Develop targeted marketing strategies',
            backstory="""Expert in Swiss regional marketing with deep understanding 
            of cultural nuances and local preferences.""",
            tools=self.tools.get_tools(),
            verbose=True
        )

    def create_strategy_task(self, location: str) -> Task:
        return Task(
            description=f"Develop marketing strategy for {location}",
            expected_output="Detailed marketing plan with audience targeting and campaign recommendations",
            agent=self.agent
        )

    def get_agent(self) -> Agent:
        return self.agent