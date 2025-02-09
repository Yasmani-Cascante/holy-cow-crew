from crewai import Agent
from typing import List, Optional
from ..models.sales_prediction import SalesAnalysis

class HolyCowBaseAgent:
    """Base class for all Holy Cow agents"""
    
    @classmethod
    def create_agent(
        cls,
        name: str,
        role: str,
        goal: str,
        backstory: str,
        tools: Optional[List] = None,
        allow_delegation: bool = True
    ) -> Agent:
        """
        Creates a CrewAI agent with standard Holy Cow configuration
        
        Args:
            name: Agent's name
            role: Agent's role description
            goal: Agent's main goal
            backstory: Agent's backstory and context
            tools: List of tools available to the agent
            allow_delegation: Whether the agent can delegate tasks
            
        Returns:
            CrewAI Agent instance
        """
        return Agent(
            name=name,
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools or [],
            allow_delegation=allow_delegation,
            verbose=True
        )

    def process_sales_data(self, analysis: SalesAnalysis) -> dict:
        """
        Base method for processing sales analysis data
        
        Args:
            analysis: SalesAnalysis instance containing prediction and context
            
        Returns:
            Dictionary with processed results
        """
        raise NotImplementedError("Subclasses must implement process_sales_data")