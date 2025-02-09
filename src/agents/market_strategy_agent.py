from crewai import Agent
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from ..tools.market_tools import MarketTools

class MarketStrategyAgent:
    def __init__(self):
        self.tools = MarketTools()
        self.agent = self.create_agent()
        self._strategy_cache = {}
        self._default_date_range = self._get_default_date_range()

    def _get_default_date_range(self) -> Tuple[str, str]:
        today = datetime.now()
        end_date = today + timedelta(days=30)
        return (
            today.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )

    def create_agent(self) -> Agent:
        return Agent(
            role='Market Strategy Specialist',
            goal='Analyze market trends and develop effective strategies',
            backstory="""Expert in Swiss market analysis and strategy development.
            Specialized in identifying market opportunities and optimizing 
            pricing strategies for the restaurant industry.""",
            tools=self.tools.get_tools(),
            verbose=True
        )

    def develop_local_strategy(self, location: str, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        if not start_date or not end_date:
            start_date, end_date = self._default_date_range
            
        events = self.tools.analyze_local_events(location, [start_date, end_date])
        demographics = self.tools.analyze_canton_demographics(location)
        recommendations = self.tools.generate_recommendations(events, demographics)
        
        strategy = {
            'location': location,
            'date_range': [start_date, end_date],
            'events': events,
            'demographics': demographics,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }
        
        cache_key = f"{location}_{start_date}_{end_date}"
        self._strategy_cache[cache_key] = strategy
        return strategy

    def get_strategy_dict(self, location: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        if not start_date or not end_date:
            start_date, end_date = self._default_date_range
            
        cache_key = f"{location}_{start_date}_{end_date}"
        if cache_key not in self._strategy_cache:
            return self.develop_local_strategy(location, start_date, end_date)
        return self._strategy_cache[cache_key]

    def analyze_competitors(self, location: str) -> List[Dict[str, Any]]:
        return [
            {
                'name': 'Competitor A',
                'distance': 0.5,
                'price_range': 'medium',
                'strength': 'location'
            },
            {
                'name': 'Competitor B',
                'distance': 1.2,
                'price_range': 'high',
                'strength': 'quality'
            }
        ]

    def get_agent(self) -> Agent:
        return self.agent