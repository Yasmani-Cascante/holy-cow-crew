from crewai import Agent
from ..tools.marketing_tools import MarketingTools
from typing import Dict, Any
from datetime import date, timedelta

class MarketingAgent:
    def __init__(self):
        self.tools = MarketingTools()
        self.agent = self.create_agent()
    
    def create_agent(self) -> Agent:
        return Agent(
            role='Marketing Strategy Specialist',
            goal='Develop effective marketing strategies based on local market analysis',
            backstory="""You are an expert marketing strategist with deep knowledge 
            of the Swiss market, particularly in the restaurant industry. You excel at 
            analyzing local trends, demographics, and events to create targeted 
            marketing campaigns that resonate with specific communities.""",
            tools=self.tools.get_tools(),
            verbose=True
        )
    
    def develop_strategy(self, location: str, timeframe: int = 30) -> Dict[str, Any]:
        """
        Develop a marketing strategy for a specific location
        
        Args:
            location: Target location (e.g., "Zurich")
            timeframe: Number of days to analyze for events
        """
        tools = self.tools
        start_date = date.today()
        end_date = start_date + timedelta(days=timeframe)
        
        # Analyze local events
        events = tools.analyze_local_events(
            location=location,
            start_date=start_date,
            end_date=end_date
        )
        
        # Analyze demographics
        demographics = tools.analyze_canton_demographics(location)
        
        # Generate recommendations
        recommendations = tools.generate_recommendations(
            events=events,
            demographics=demographics
        )
        
        return {
            "location": location,
            "timeframe": f"{start_date} to {end_date}",
            "events": [event.dict() for event in events],
            "demographics": demographics.dict(),
            "recommendations": recommendations.dict()
        }
    
    def get_agent(self) -> Agent:
        return self.agent